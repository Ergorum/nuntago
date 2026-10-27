# Nuntago

**Partner discovery, qualification, and human-reviewed outreach.**

Nuntago helps an AI engineer find consultancies and agencies that may need overflow or white-label engineering capacity. It combines Serper discovery, website research, deterministic fit scoring, optional AI-assisted copy, a persistent lead workflow, and a React operator console.

This repository is the partner-outreach application. It does not implement the separate Google Business Profile/reporting product.

## Workflow

1. Discover and rank potential partners.
2. Suppress already-handled domains and qualify commercial fit.
3. Research bounded same-domain pages, including contact pages.
4. Select relevant proof and draft concise outreach.
5. Review the lead and contact provenance.
6. Approve eligible leads for Gmail draft creation.
7. Review and send manually in Gmail, then record sent status and follow-ups.

There is no automatic email sending. Gmail integration creates unsent drafts only after the required approval.

## Start with Docker

```bash
git clone https://github.com/Ergorum/nuntago.git
cd nuntago
git switch main
cp .env.example .env
mkdir -p data secrets
# Configure only the integrations you intend to use.
docker compose build
docker compose run --rm nuntago-cli init-db
docker compose up -d nuntago-web
```

The web runtime binds to [http://127.0.0.1:8080](http://127.0.0.1:8080). Its health endpoint is `/api/health`. Keep the origin private behind the configured authentication/proxy layer.

On Linux, set `LOCAL_UID` and `LOCAL_GID` in `.env` to your host IDs if they differ from 1000. Data and OAuth files are persisted under `data/` and `secrets/`; keep both out of Git.

## Configuration

Use [.env.example](.env.example) as the full reference.

| Setting                                   | Purpose                                                          |
| ----------------------------------------- | ---------------------------------------------------------------- |
| `SERPER_API_KEY`                          | Required for live discovery                                      |
| `OPENAI_API_KEY`                          | Optional analysis/copy generation; deterministic fallbacks exist |
| `PORTFOLIO_URL`                           | Portfolio link used in outreach                                  |
| `MIN_SCORE`, `DISCOVERY_LIMIT`            | Qualification and batch controls                                 |
| `DB_PATH`                                 | SQLite persistence                                               |
| `NUNTAGO_DEMO_MODE`                       | Fictional, read-only local demonstration                         |
| `LOG_LEVEL`, `LOG_FILE`                   | Console and optional rotating-file logs                          |
| `GMAIL_CLIENT_SECRET`, `GMAIL_TOKEN_FILE` | OAuth client and persisted token paths                           |

Public demonstration and private operation are separate surfaces: `nuntago-demo.ergorum.com` uses the isolated read-only `/api/public/*` API; the operator workspace at `nuntago.ergorum.com` uses validated Cloudflare Access identity, with a configured bearer-token fallback for tools.

Demo mode blocks pipeline execution, lead mutations, Gmail draft creation, and sent-state changes.

## CLI

```bash
./nuntago --help
./nuntago status
./nuntago doctor --strict

# Read-only discovery:
./nuntago discover --limit 20

# Live research, qualification, and draft generation:
./nuntago run --limit 10

# Review and explicit actions:
./nuntago list --status drafted --min-score 70
./nuntago show 12
./nuntago approve 12
./nuntago reject 13
./nuntago do-not-contact 14
./nuntago gmail-drafts --limit 10
./nuntago mark-sent 12
./nuntago due-followups
```

Inside Docker, replace `./nuntago` with `docker compose run --rm nuntago-cli`.

Live discovery/research may use external APIs and paid providers. Use `status` and `doctor` for configuration inspection before starting a live run.

## Gmail setup

Create a Google OAuth Desktop application and enable Gmail API. Place its client JSON at `secrets/client_secret.json`. The draft command requests the `gmail.compose` scope and stores its token in `secrets/token.json`.

The CLI container uses host networking for the temporary localhost callback. Complete OAuth in your own browser when required. Approvals do not send messages: review and send each draft manually.

## Develop and test

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m pytest -q
uvicorn app.api:app --host 127.0.0.1 --port 8080 --reload
```

In another terminal:

```bash
cd frontend
npm ci
npm run dev
npm run build
```

Vite uses port 5173 and proxies `/api` to port 8080.

For the Docker test environment:

```bash
docker compose run --rm --entrypoint pytest nuntago-cli -q
```

CI validates Compose/deployment scripts, builds CLI and web images, runs the full Python suite, and checks the read-only demo boundary.

## Structure and operations

- `app/`: discovery, crawling, contact provenance, scoring, copy, persistence, API, and CLI.
- `frontend/`: React operator console.
- `tests/`: pipeline and API regression coverage.
- `infra/`: release deployment and migration scripts.
- [Hetzner deployment and rollback](docs/hetzner-cicd.md)
- [Repository consolidation record](docs/maintenance/2026-10-27-branch-consolidation.md)

Current contact discovery already supersedes the older unmerged contact-hardening alternative: it handles mailto provenance separately and ranks contact/research pages deterministically. That historical branch is archived without replacing the current implementation.

## Collaboration and release branches

Use `main` for integration and target new feature/fix/docs PRs there. Report the final behavior and checks before merging, then delete the short-lived branch.

`master` remains the repository's existing default/release branch. It is synchronized during this consolidation and retained because changing GitHub's default-branch setting is not exposed by the connector. Existing automatic deployment from normal master pushes remains in place. Repository-cleanup commits are explicitly excluded from deployment.

No production deployment, discovery run, Gmail action, or prospect-data change is performed by this consolidation.
