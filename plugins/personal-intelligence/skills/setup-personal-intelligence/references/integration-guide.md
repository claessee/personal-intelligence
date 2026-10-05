# Choose and verify integrations

Personal Intelligence installs skills and offline metadata tooling. It does not install integrations, start services, connect accounts or grant permissions. Pick capabilities first, preserve working routes, and connect only missing dependencies the recipient chooses. These instructions are for a separately authorized recipient setup; preparing the package performs none of these actions.

## Recommended macOS starting point: iMCP

[iMCP](https://imcp.app) is the recommended starting integration for macOS recipients who want basic Calendar, Reminders, Contacts, Maps and Weather. File-only use needs none of these services. An existing working integration remains the selected route unless the user chooses a change.

Documentation and public tool definitions were checked on 2026-10-05 at upstream commit `8d2328197b173029dffa195d849b297605bb70db`. This is upstream evidence, not a test of the recipient's installed build. See the [upstream setup and client guide](https://github.com/mattt/iMCP/blob/8d2328197b173029dffa195d849b297605bb70db/README.md). Tool names and client support can change; inspect the connected tool catalog before relying on an operation.

### Install and choose permissions

1. Use a Mac running macOS 15.3 or later. Download the app from [iMCP's website](https://imcp.app), install it and open its menu-bar interface. If Homebrew is already available, upstream also documents `brew install --cask mattt/tap/iMCP`.
2. Select only the services the user wants. Calendar and Reminders require their respective full-access macOS grants; Contacts requires Contacts access. OS grants can be broader than a single task, so tool requests must still stay within the selected subject and scope.
3. Maps activation in the inspected implementation depends on Location access, even when the request supplies an address. Explain that dependency before the user decides to enable Maps. Weather tools accept explicit coordinates without a current-location lookup. Location permission and a `location_current` call are distinct choices; do not infer permission to read the user's location from a weather question about a named place.
4. Review denied permissions in macOS Privacy & Security only if the user chooses to remedy them. Leave a declined or missing capability unavailable. Connect the selected client and approve its iMCP connection deliberately; persistent client trust is optional.

iMCP's app and bundled `imcp-server` communicate through local Bonjour discovery; clients connect to the executable over STDIO. The app must remain available. A running toggle or saved configuration does not establish usable access. Local data returned to an assistant can be processed off device by its client/model provider; review that client's privacy settings.

Messages, Phone and Shortcuts are outside this starting recommendation. Leave unselected services off. Do not replace an existing Messages route, invoke an identity tool during onboarding, or grant broad file access merely to verify these five capabilities. Calendar, Reminders and Contacts expose writes as well as reads; service activation alone is not read-only confinement. Where supported, select a client tool allowlist for the requested operations.

### Connect a supported client

| Client | Connection route and evidence |
| --- | --- |
| Claude Desktop | Upstream documents the app's Claude Desktop configuration action, or copying the server command into its MCP configuration. Preserve existing server entries, restart the client and review the connection prompt. |
| Claude Code | Upstream provides a STDIO registration recipe and an import-from-Claude-Desktop option. Use only the chosen route and avoid importing unrelated integrations. |
| Cursor | Upstream supplies an installation link. Review it and the resulting server configuration rather than assuming a click proves access. |
| Amp | Upstream supplies a STDIO registration recipe for the bundled executable. |
| Codex local clients | Codex documents STDIO MCP support. Using iMCP's executable with that support is a compatibility inference; this package has not tested a fresh Codex connection. |

For a chosen local Codex setup, copy the actual server command from iMCP. A conventional installation uses:

```sh
codex mcp add iMCP -- /Applications/iMCP.app/Contents/MacOS/imcp-server
```

Use the copied path if the app is elsewhere. A client with an MCP settings form can use the same executable and STDIO transport. Registration changes that client's configuration and requires the user's setup authorization. `codex mcp list` reports configuration; a scoped successful tool call establishes access. Codex also supports per-server `enabled_tools` and `disabled_tools`: select actual discovered names rather than copying a universal list. See the [official MCP guide](https://learn.chatgpt.com/docs/extend/mcp?surface=cli). A hosted web chat does not acquire local iMCP access from these instructions.

### Operations, limits and small checks

The following reflects inspected upstream service implementations. Run only a check selected and scoped by the recipient; never run the whole table automatically. Use deterministic dates and explicit time zones where material. Keep results and timings in private setup notes.

| Capability | Inspected operations | Limit and smallest useful read check |
| --- | --- | --- |
| Calendar | `calendars_list`, `events_fetch`, `events_create`, `events_delete` | No event-update tool. Fetch by one chosen calendar, title clue and short date window; inspect returned identity, times and calendar. Empty calendar filters search all calendars. Calendar/list creation targets are name-based; duplicate names and fallback to defaults require care. [Calendar definition](https://github.com/mattt/iMCP/blob/8d2328197b173029dffa195d849b297605bb70db/App/Services/Calendar.swift). |
| Reminders | `reminders_lists`, `reminders_fetch`, `reminders_create` | No edit, completion or deletion tool in this definition. Fetch one selected list with a title clue and completion filter. Date filters apply to due dates for incomplete items and completion dates for completed items. Empty list filters search all lists; unmatched creation list names can fall back to the default. [Reminders definition](https://github.com/mattt/iMCP/blob/8d2328197b173029dffa195d849b297605bb70db/App/Services/Reminders.swift). |
| Contacts | `contacts_search`, `contacts_list`, `contacts_me`, `contacts_create`, `contacts_update` | Search one chosen third-party contact with a known clue. Broad listing returns all contacts by default; do not use it as a setup test. The self-contact tool is sensitive identity access, requires a task-specific need, and does not supersede designated canonical personal facts. [Contacts definition](https://github.com/mattt/iMCP/blob/8d2328197b173029dffa195d849b297605bb70db/App/Services/Contacts.swift). |
| Maps | `maps_search`, `maps_directions`, `maps_explore`, `maps_eta`, `maps_generate` | Requires the Location activation dependency and network services. Search one public place with an explicit region; confirm the result's location. Estimates do not guarantee actual travel time. [Maps definition](https://github.com/mattt/iMCP/blob/8d2328197b173029dffa195d849b297605bb70db/App/Services/Maps.swift). |
| Weather | `weather_current`, `weather_daily`, `weather_hourly`, `weather_minute` | Query explicit public coordinates, inspect location and forecast/observation time. Daily forecast requests allow up to 10 days; requested hours/minutes and available coverage differ. Minute forecasts can be unavailable. Network or service failures remain unavailable. [Weather definition](https://github.com/mattt/iMCP/blob/8d2328197b173029dffa195d849b297605bb70db/App/Services/Weather.swift). |

The README advertises recurrence, but the inspected event-creation schema has no recurrence-rule input or rule construction. Do not promise creation of a recurring series from a general capability description. Deleting a recurring event requires its occurrence start and an explicit occurrence/future-series choice. Do not substitute delete-and-create for an unsupported update without separate authorization for those operations.

Read checks do not prove writes. A write check requires an explicitly authorized disposable item, chosen destination and fields, actual execution and verification; cleanup also needs authorization. Follow the [authorized-action rule](../../personal-intelligence/references/authorized-actions.md). A missing returned field or ambiguous destination prevents a verified-success claim.

## Optional advanced alternatives

**cal-cli for Calendar:** its [repository and installation guide](https://github.com/claessee/cal-cli#install) were verified public on 2026-10-05 after the maintainer's availability update. Retain it where already working, or choose it for dedicated availability checks, event updates and revision-aware writes. Upstream requires the Codex app on macOS 13+, Python 3.9+ and Xcode Command Line Tools. Add `claessee/cal-cli` as a plugin marketplace in Codex, select Cal CLI and follow its onboarding; installing the local helper and granting Calendar access are separate recipient setup actions. Preserve existing availability-calendar selections and use either the plugin or direct MCP route to avoid duplicates. Calendar access is required; Reminders and Full Disk Access are not. Inspect connection status and one scoped event read before claiming access. Its recurring-event edits support one occurrence or future occurrences, and automatic creation conflict checks cover only the first occurrence. Follow upstream for complete limits. No new-recipient live check was run here and this preparation changed no repository visibility.

**RemCTL for Reminders:** its [public repository](https://github.com/viticci/remctl) and [v2.3.1 release](https://github.com/viticci/remctl/releases/tag/v2.3.1) with an Apple-silicon download were verified on 2026-10-05. Upstream requires macOS 14+ and iCloud Reminders; Intel uses its source-build route. It provides editing, completion, deletion and advanced Reminders features beyond the inspected iMCP tools. Its signed Capability Host owns Reminders, Automation and Full Disk Access permissions. Some advanced features use private Apple APIs and can change with macOS updates. Review those dependencies before choosing it. Follow [upstream installation](https://github.com/viticci/remctl/blob/main/docs/installation.md) and [client/MCP guidance](https://github.com/viticci/remctl/blob/main/docs/mcp.md), connect only the chosen client, and avoid duplicate MCP/plugin routes. Check the host's effective-access result, then one scoped reminder read; configuration alone is not a pass. See the [upstream README](https://github.com/viticci/remctl/blob/main/README.md).

## Separate optional email and finance integrations

**Gmail:** choose a connected Gmail app/MCP separately for email. Personal Intelligence neither authenticates an account nor supplies email transport. Use Gmail tools exclusively for Gmail content; no shell, browser, raw mail database or SMTP fallback. Missing Gmail access makes the requested email operation unavailable. Labels are optional private choices. Sending requires an explicit send instruction.

**MoneyWiz:** the separate [MoneyWiz MCP Server](https://github.com/claessee/moneywiz-mcp-server) repository and README were verified public on 2026-10-05. Its [installation guide](https://github.com/claessee/moneywiz-mcp-server#install) requires macOS with MoneyWiz or a compatible database, Python 3.10+ and a STDIO MCP client; `uv` is recommended. It provides a permanently read-only interface and requires the recipient to select their actual database privately. Personal Intelligence neither installs it nor connects that database. Public documentation establishes the described capabilities, not live access to a recipient's store. Follow its [reconciliation guidance](https://github.com/claessee/moneywiz-mcp-server#validation) when separately authorized; preserve explicit currencies, completeness and unsupported-balance limitations. Use the existing ledger integration only for an explicit financial question with bounded account/topic/date scope. No financial records were accessed or live MoneyWiz checks performed during package preparation. No background financial verification or raw-database fallback follows from onboarding.

## File-based use and readiness

Existing authorized file/PDF/JSON readers can use a narrowly selected mapped folder or document. Another MCP is not required. Read the applicable local instructions first, resolve only the relevant private-map entry, and report an actual reader failure rather than assuming that an absent MCP makes files inaccessible. Do not index, OCR a collection or enumerate unrelated roots as setup.

Record each desired capability, selected route, dependency, permission status, observed tool names, dated evidence and remaining check in private notes. Keep `readiness: unverified` in the profile until evidence supports a stronger observation. The schema's `user_confirmed` or `verified` value records testimony or a dated observation, not a current access grant. A listed tool is not successful execution; a read pass is not a write pass. Preserve missing dependencies as unavailable/unverified and ask only about choices that affect scope, authority or setup authorization.
