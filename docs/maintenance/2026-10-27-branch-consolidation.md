# nuntago branch consolidation — 27 October 2026

## Scope and decision

Master contains the latest accepted application. Its lone divergent contact-hardening branch is superseded by the current four-part clean_text/mailto-provenance contract and deterministic research-page prioritization. Keep the current runtime, archive that alternative, and provide main for integration. Retain master as the existing default/release branch; cleanup commits skip deployment.

Original default branch: `master`. Original application baseline: `47a35dc7740ba5826abfed4886c3939ad20713e9`.

This audit covers all **16 original branches** and the pull requests visible at the start of the task. GradeWise and Kairumen are excluded.

## Preservation and cleanup

- Preserve each divergent historical tip under its exact archive tag before deletion.
- Confirm the integrated baseline is reachable from main.
- Refuse cleanup if an audited branch has moved.
- Verify remote archive targets and use atomic, expected-tip branch deletion.
- Remove the temporary consolidation branch only after its final tip is an ancestor of main.
- Retain master because it is the current GitHub default; synchronize it to the final integrated tree. The connector does not expose the default-branch setting.
- Remove the one-time write-enabled workflow and script after successful cleanup verification.
- Do not run production deployment, provider jobs, outreach, publishing, or data migrations as part of this work.

## Original inventory

| Branch                                              | Original commit                            | Disposition                                                                                                                            |
| --------------------------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `feat/pactsignal-jwt-auth`                          | `edc9cdb941d956a7a16422dc6b47ea49e412f012` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `feat/public-showcase-cloudflare-console`           | `d9e206cd41fd0f2ca85ee4542afc1095c6d40be3` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `fix/demo-host-role-swap`                           | `94b9910a8334fe62ff9e5eb622126bd792997bda` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `fix/nuntago-demo-flat-host`                        | `29ade92270e9e667039a23feba146118e741f773` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `implementation/discovery-candidate-quality`        | `5219e7c439c0986e11932f21480ef900dafe7ce5` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `implementation/docker-runtime`                     | `7d773aade94d6440fb091aa2b3a944474bfd8e59` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `implementation/existing-lead-suppression`          | `70df327bb4acf844d87303e0d7203b4e5c9dc8e7` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `implementation/hetzner-cicd-deployment`            | `46640d22fa01ab313fc1f93d73186664cc0961ed` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `implementation/observability-and-runtime-logging`  | `798870f50f868ea2fbd3c4d027c21992656a8b74` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `implementation/operator-actions-contact-hardening` | `8bc0aae2fddc237cb92da10d0bf4f13f8ef8e17f` | Archive exact tip: [tag](https://github.com/Ergorum/nuntago/tree/archive/2026-10-27/implementation/operator-actions-contact-hardening) |
| `implementation/react-operator-ui`                  | `54141d23a18d054c1c5286606cdce1b013e4fcc8` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `implementation/search-query-quality`               | `802588b60637f46471bd97f52b3a1dae838e7729` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `improvement/outreach-copy-quality-v2`              | `2df14ee1a76c396d2ee4f5b59bd946962e019fe7` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `master`                                            | `47a35dc7740ba5826abfed4886c3939ad20713e9` | Retain existing default branch; synchronize to integrated source                                                                       |
| `ops/pactsignal-caddy-network`                      | `1c28ec9d326e44e9bb90ef87283a1d9f5c6f3313` | Integrate or preserve as an ancestor of the consolidated source                                                                        |
| `rebrand/nuntago`                                   | `8a9f7f99ff58e905cac77885fcb391d39f13bfa8` | Integrate or preserve as an ancestor of the consolidated source                                                                        |

## Validation

Checks and final cleanup results are recorded in the consolidation PR and its GitHub Actions runs. Compilation/tests verify the integrated source; they do not replace visual approval or a production release review.
