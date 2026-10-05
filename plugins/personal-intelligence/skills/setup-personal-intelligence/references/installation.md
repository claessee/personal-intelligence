# Install and onboard — 0.1.0

The initial release, v0.1.0, was published on 2026-10-05. The repository is public. Use a repository checkout or GitHub's source archive from the published release.

## Install the skills

Use a current local Codex client with custom marketplace support. For an authorized repository checkout or extracted repository ZIP, register the repository root:

```sh
codex plugin marketplace add /path/to/personal-intelligence
```

Select Personal Intelligence in the client's plugin UI and install it. Registration only makes the catalog available; confirm installation separately. Restart the client if needed, then use a fresh chat to confirm both skills are visible. A supported Git-backed marketplace can use a repository source when the recipient has access; no visibility change is implied. The portable plugin manifest declares version 0.1.0 and bundles no MCP configuration. See the [official packaging guide](https://developers.openai.com/plugins/build/plugins).

The plugin ZIP contains the plugin, both skills and their resources plus the license; it does not contain the repository marketplace or tests. For a local marketplace install, use the repository ZIP. If a client supports direct skills, copy both complete directories from `skills/` in the extracted plugin, or `plugins/personal-intelligence/skills/` in the repository, into its configured skill location. Codex documents `$HOME/.agents/skills` for user skills. Preserve supporting files and avoid installing a second copy with the same name. Other clients' skill installation and selection remain unverified here. See the [official skills guide](https://learn.chatgpt.com/docs/build-skills).

This does not connect accounts, install integration dependencies, start a server or grant file access. File-based use works with the client's existing authorized readers. Python 3.10+ is needed only for the bundled offline helper/tests, which use the standard library.

## Onboard from desired capabilities

Start in the intended workspace and invoke:

> Use $setup-personal-intelligence to map my existing information. Keep my configuration outside Git, preserve working integrations, identify the capabilities I want and explain any missing dependencies before proposing setup changes.

1. Read existing local instructions and record what the recipient actually wants: file questions, appointments, reminders, contact lookup, maps, weather, optional email or explicitly scoped finance. Do not treat the example list as a request for every capability.
2. Keep working routes. For missing basic macOS capabilities, recommend iMCP first; use the [integration guide](integration-guide.md) for permissions, client connection, operations and limits. cal-cli and RemCTL are optional advanced alternatives. Shared recommendations do not override private routing instructions.
3. Select a private configuration directory, conventionally `$HOME/.config/personal-intelligence`, and tell the assistant its location. Readiness notes, maps, records and evaluation transcripts stay outside Git and release archives. No automatic home-directory search or global instruction installation occurs.
4. Capture independent requirements, then populate the three blank metadata templates. Resolve patient, owner, identity and financial boundaries before content reads. Finance setup can record a desired route without querying records. Use the [profile schema](profile-schema.md) and preserve required `_prev` backups before replacing private files.
5. Validate metadata with the helper. A valid route or requirement digest proves structural consistency only. Record unverified dependencies honestly; do not turn metadata into a claimed connection or permission.
6. With explicit scope, test one useful question for each chosen capability. Inspect actual source/tool evidence and record date, relevant fields, limitation and elapsed time privately. Verify reads and writes separately. A write test is optional and needs its own authorization; no live pass follows from an offline fixture.

Normal use can invoke:

> Use $personal-intelligence with my private profile to find the supplier confirmation for my selected trip.

Resolve discoverable item clues through narrow prescribed-source discovery. Ask only when a real ambiguity or privacy choice remains. Missing tools remain unavailable until the recipient chooses and verifies a setup; preserve existing permission boundaries.

For later changes, follow the [rule-maintenance guide](../../personal-intelligence/references/rule-maintenance.md). Updating shared skills retains private configuration; it does not automatically update source maps or integrations.
