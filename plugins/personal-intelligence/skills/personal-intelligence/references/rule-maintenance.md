# Maintain shared rules without sharing private context

Private instructions and corrections belong to the recipient. Shared skills contain reusable behavior, blank templates and invented examples. There is **no automatic anonymizer or synchronization from personal AGENTS.md files**. Neither setup nor the helper reads a personal instruction file and publishes its contents.

## From a correction to a shared improvement

1. Understand the demonstrated failure within its authorized private task. Separate actual tool/source evidence from an assumption or an unperformed check. Keep the original records and evaluation trace private.
2. Extract the smallest reusable behavior. For example, a failed appointment task can yield “verify the saved identity and intended fields before reporting success.” Remove personal names, source paths, labels, account details, dates, appointments and surrounding conversation. Write a new invented case rather than copying and editing a real transcript.
3. Update the appropriate shared skill or reference. Put ordinary evidence/action behavior in `personal-intelligence`; put onboarding and requirement reconciliation in `setup-personal-intelligence`. Keep recipient-specific routing and authority choices in private instructions/profile files. Do not broaden permissions or bypass patient, finance, identity or subject gates.
4. Preserve `<stem>_prev.<ext>` before replacing a maintained file; for suffixless files use `<name>_prev`. Retain an older backup under a distinct dated name before refreshing the required backup. Backups stay outside Git and archives. Add each intentional generic package file to `release-files.json`.
5. Run proportional offline checks and inspect the exact diff and staged inventory. Review every changed document and any graphic visually. Where behavior needs a live operation, record that check separately as not run until a real scoped trace exists; offline tests cannot pass it.
6. Build both archives from the reviewed allowlist, inspect their member lists/content and checksums, then commit and push only the reviewed generic changes when authorized. Verify the remote commit, repository visibility and hosted validation result. A push is not a GitHub release, tag or directory submission. Publish a version only when separately authorized and appropriate.

## Release allowlist and checks

The repository's `release-files.json` enumerates the generic release inventory. `scripts/check_release.py` requires the working inventory to match it, with deliberate exclusions for Git metadata, backups and caches. It checks local links, JSON, plugin identity/version, two skill entrypoints, file types/sizes and the three exact README PNG paths with structural checks. Its heuristic scan looks for user-specific absolute home paths, private-key markers and selected credential-like token patterns, including embedded PNG bytes.

These checks are not an anonymizer, a comprehensive secret scanner or OCR. They do not reliably detect names, account values, sensitive prose or text visible in images. An allowlisted file can still contain private information. Manual review of the exact content and diff is mandatory; `.gitignore` alone does not exclude already tracked files. Keep private maps, populated configuration, source bodies, runtime databases and real evaluation transcripts out of the inventory and index.

From an authorized repository checkout:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_release.py
git diff --cached --check
git diff --cached
git ls-files
```

Compare the complete staged tree with the allowlist, not just changed filenames. Preserve existing archives and checksum files with the same backup convention before rebuilding:

```sh
python3 scripts/build_release.py --destination /path/outside/repository
```

The builder refuses existing output files and writes only allowlisted files. The repository ZIP includes tests, invented fixtures, guides and the marketplace. The plugin ZIP includes both complete skills, their guides/resources, manifest and license. Archives exclude backups; checksums are generated outside the repository. Review ZIP members against their expected subsets. Keep versions consistent in the manifest, builder, documentation and archive names; 0.1.0 remains the initial pre-release version for this preparation.

## Recipients obtain updates explicitly

Read the published change description and new requirements before updating. For a supported Git-backed Codex marketplace, refresh the selected marketplace with `codex plugin marketplace upgrade personal-intelligence-local`, then confirm the plugin's updated installed files through the client's supported update/install flow. For a local downloaded marketplace, first replace its generic package with the reviewed new version, refresh/reinstall it and restart if needed. Marketplace refresh alone is not proof that a cached installed skill changed. See the [official marketplace guidance](https://developers.openai.com/plugins/build/plugins).

For direct skill installation, preserve the previous installed skill outside its discovery directory, replace the two complete shared skill folders and confirm them in a fresh chat. Avoid duplicate names or partial resource copies. See the [official skill guidance](https://learn.chatgpt.com/docs/build-skills).

Keep the recipient's private configuration directory, maps, personal instructions, records, approvals, readiness evidence and integration settings in place. No automatic profile migration or map synchronization exists. If a later version changes a schema or prerequisite, inspect the documented change, back up the affected private metadata, reconcile it explicitly and rerun its offline validator. Recheck only affected live capabilities when authorized. Updating generic rules neither connects accounts nor grants new permissions.
