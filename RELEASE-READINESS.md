# Release readiness — 0.1.0

Preparation date: 2026-10-05. Planned first release: 2026-10-06. Version: 0.1.0. Status: pre-release drafts; no GitHub release or tag is published by this preparation. Scope: generic skills, private configuration templates, offline tooling and entirely invented examples. The source package was authored separately from any personal configuration or evaluation history.

## Verified locally

- At the original draft preparation on 2026-10-04, both skill entrypoints passed the bundled Skill Creator's metadata/scaffold checks. Current entrypoint structure is checked again by the release checker. PyYAML is absent in the available Python environments, so the checks were run through a temporary bridge to the existing Ruby safe YAML parser. The bridge is not installed or shipped; the release toolkit itself uses Python's standard library only.
- A fresh three-file synthetic profile was copied into an isolated private temporary directory and validated through the actual command-line helper. The map's intentionally nonexistent synthetic locations were not opened.
- Automated tests cover independent requirement drift, every priority-label omission, exact label names, missing/unconfirmed sources and capabilities, changed authority, patient separation, finance scopes, label injection, source/path overrides, mapping/instruction completeness, malformed JSON, secret-free error output and disabled general retrieval/fallback. Every negative case starts from a validated positive baseline.
- The CLI planner validates the independent requirement digest and mapping metadata before returning a logical plan. Provider-style sources remain explicitly unverified in the example; no content or live provider calls occur.
- Release files are an explicit allowlist. Structural/link checks and heuristic private-path/credential scans apply to that exact inventory. Backups, caches, Git metadata, populated profiles outside the invented example and source collections are excluded from archives. A heuristic scan is not a comprehensive secret detector; the intentionally small authored inventory is also reviewed for personal content.

- The three supplied README graphics were visually reviewed for generic content and included unchanged. Only those exact PNG asset paths are allowed; the checker verifies PNG structure, dimensions and chunk checksums, and scans embedded bytes for the same heuristic private-path/credential markers. This does not replace visual review or comprehensively detect information within images.
- The README preserves its framing, the three graphics and the separately maintained MoneyWiz reference. MoneyWiz remains optional and separate; private upstream content and live financial access were not inspected during this preparation.

## Manual synthetic evidence exercise

These original 2026-10-04 draft results were checked by the authoring assistant against the invented originals, not by an independent evaluator or live integration. Examples are not medical, financial or actual booking evidence.

| Question | Observed answer | Inspected synthetic evidence and limit |
| --- | --- | --- |
| What stay dates and breakfast terms are confirmed? | Check-in 2030-08-12, check-out 2030-08-15; breakfast is not included, parking covers one vehicle. | `examples/synthetic/documents/journey-confirmation.md`, issued 2029-11-03, original confirmation. Its older issue date does not exclude a future stay; current cancellation status remains unverified. The plan only hoped for breakfast. |
| Does the decision index establish assembly approval? | No. The Committee approved requesting quotes; assembly spending approval is not recorded. | `decision-index.md` is an index; `committee-minutes.md` is approved by the Committee on 2030-02-09 for its 2030-02-08 meeting. Neither can establish another body's approval. |
| Does the newer patient report replace all baseline context? | The 2030-02-02 examination supersedes ALPHA's 2029-09-10 observation for patient_a only. BETA remains baseline context because it was not examined; no medication change is inferred. | `patient-baseline.md` and `patient-report.md`, with matching patient and affected fact. The newer original changes only the established field. |
| Is the provisional ledger amount a definitive balance? | No. The calculated 123.45 DEMO is a diagnostic amount; recorded balance is unavailable. | `ledger-result.json`, explicitly a provider-style fixture with `provisional_unreconciled`, no recorded balance and no live retrieval date. |

## Recipient and publication checks still separate

Desktop/plugin installation, auto-selection behavior in a fresh client, live connector schemas/permissions, actual provider queries and real user-question acceptance are not proved by these offline checks. They depend on the recipient's environment and separately scoped tasks. No new server, index, OCR, transport, permission or global configuration is installed by preparing this package.

The repository includes a GitHub Actions validation workflow. Hosted validation must be checked for the exact pushed commit; local results do not establish its result. The release is suitable for an initial workflow release with these limits stated; it is not a production filesystem-enforcement system or a verified live service.

The author authorized initial publication to the private `claessee/personal-intelligence` repository under the included MIT license. Keep visibility private during the initial evaluation; the author will decide when to convert it to public. Use only the reviewed generic repository/archive, never a populated personal workspace. Public directory submission is a distinct later action.

## Initial package preparation checks

- Current public iMCP README and five service definitions inspected at commit `8d2328197b173029dffa195d849b297605bb70db` on 2026-10-05; platform, permissions, supported clients, tool operations and limitations documented in the [integration guide](plugins/personal-intelligence/skills/setup-personal-intelligence/references/integration-guide.md). Codex compatibility is inferred from documented STDIO support; no fresh-client or live iMCP check was run.
- cal-cli availability rechecked on 2026-10-05 after the maintainer's update: public. Its current public installation guidance is linked; no visibility change was made by this preparation. Public `viticci/remctl` repository and v2.3.1 Apple-silicon release verified; no integration installed or invoked.
- Reusable authorized-action behavior extracted from a read-only private instruction source. Only generic rules and invented cases were authored into [the action reference](plugins/personal-intelligence/skills/personal-intelligence/references/authorized-actions.md). No personal content, routing values, source maps or evaluation traces were copied. Every live action regression remains **not run** without an actual execution trace.
- [Rule maintenance](plugins/personal-intelligence/skills/personal-intelligence/references/rule-maintenance.md) documents manual extraction/review, the explicit allowlist, heuristic privacy limits and recipient updates. No automatic anonymizer, private-instruction synchronization or profile migration exists.
- Local validation, archive inventory/content verification and exact index review are recorded after execution below. GitHub commit/validation confirmation is reported separately after push, so this file does not claim an unperformed hosted run.

Local completion record on 2026-10-05: **35 tests passed** (28 profile/route cases, 4 release-inventory cases, 1 README-image case and 2 archive cases). The release checker passed **40 generic files**, two skill entrypoints and three README graphics. The synthetic CLI profile validator passed with zero mapped-content reads/provider calls. Archive tests compared every member with its source bytes, verified checksums and deterministic builds, and confirmed collision refusal before partial output. The exact staged inventory and generic diff were manually reviewed; private files and backups are absent. Both rebuilt drafts use version **0.1.0**, with 40 repository members and 15 plugin members including the license. Final archive/index identity is checked again before commit; no real action regression is marked passed. Real mapped-source reads and live provider calls by the helper: **0**.
