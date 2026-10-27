"""One-time, lease-guarded cleanup of the audited Kairumen branch inventory."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def remote_refs() -> dict[str, str]:
    return {ref: sha for sha, ref in (line.split() for line in git("ls-remote", "--heads", "--tags", "origin").splitlines())}


def is_ancestor(sha: str) -> bool:
    result = subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", sha, "origin/main"])
    if result.returncode not in (0, 1):
        raise RuntimeError(f"Cannot verify ancestry for {sha}")
    return result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Create archive tags and delete the verified branches")
    args = parser.parse_args()
    inventory = json.loads((ROOT / "docs/maintenance/2026-10-27-branches.json").read_text())
    if args.apply:
        if os.environ.get("GITHUB_REPOSITORY") != inventory["repository"] or os.environ.get("GITHUB_REF") != "refs/heads/main":
            raise SystemExit("Apply is restricted to the audited repository's main workflow")
    git("fetch", "--prune", "--tags", "origin")
    if not is_ancestor(inventory["baseline"]):
        raise SystemExit("Application baseline is not merged into main; no cleanup performed")
    refs = remote_refs()
    archived = {item["branch"]: item for item in inventory["archives"]}
    keep = set(inventory.get("keep_branches", ["main"]))
    work_branch = inventory.get("consolidation_branch", "maintenance/consolidate-main")
    candidates = [item for item in inventory["branches"] if item["name"] not in keep and item["name"] != work_branch]
    # Include only this consolidation PR branch, and only when already merged.
    temp_ref = "refs/heads/" + work_branch
    if temp_ref in refs:
        if not is_ancestor(refs[temp_ref]):
            raise SystemExit("Consolidation branch is not merged; no cleanup performed")
        candidates.append({"name": work_branch, "sha": refs[temp_ref]})
    for item in candidates:
        ref = "refs/heads/" + item["name"]
        if ref in refs and refs[ref] != item["sha"]:
            raise SystemExit(f"Branch moved since audit: {item['name']}; no cleanup performed")
        if not is_ancestor(item["sha"]) and item["name"] not in archived:
            raise SystemExit(f"Branch is neither merged nor archived: {item['name']}")
    new_tags = []
    for item in inventory["archives"]:
        tag_ref = "refs/tags/" + item["tag"]
        if tag_ref in refs:
            if refs.get(tag_ref + "^{}", refs[tag_ref]) != item["sha"]:
                raise SystemExit(f"Archive tag has unexpected target: {item['tag']}")
        else:
            new_tags.append(tag_ref)
    if not args.apply:
        print(json.dumps({"dry_run": True, "new_archive_tags": new_tags, "branches": [x["name"] for x in candidates if "refs/heads/" + x["name"] in refs]}, indent=2))
        return
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    for item in inventory["archives"]:
        tag_ref = "refs/tags/" + item["tag"]
        if tag_ref in new_tags:
            git("tag", "-a", item["tag"], item["sha"], "-m", "Preserve original branch before 2026-10-27 consolidation: " + item["branch"])
    if new_tags:
        git("push", "--atomic", "origin", *new_tags)
    refs = remote_refs()
    for item in inventory["archives"]:
        tag_ref = "refs/tags/" + item["tag"]
        if refs.get(tag_ref + "^{}", refs.get(tag_ref)) != item["sha"]:
            raise SystemExit(f"Remote archive verification failed: {item['tag']}")
    deletions = [x for x in candidates if "refs/heads/" + x["name"] in refs]
    if deletions:
        leases = ["--force-with-lease=refs/heads/" + x["name"] + ":" + x["sha"] for x in deletions]
        git("push", "--atomic", *leases, "origin", *[":refs/heads/" + x["name"] for x in deletions])
    remaining = remote_refs()
    leftovers = [x["name"] for x in candidates if "refs/heads/" + x["name"] in remaining]
    if leftovers:
        raise SystemExit("Cleanup incomplete: " + ", ".join(leftovers))
    print(json.dumps({"archived_tags": len(inventory["archives"]), "deleted_branches": len(deletions), "remaining_branches": [x.removeprefix("refs/heads/") for x in remaining if x.startswith("refs/heads/")]}, indent=2))


if __name__ == "__main__":
    main()
