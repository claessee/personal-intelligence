# Private profile schema v1

Templates in `../assets/` are deliberately incomplete. Configure only domains/subjects the user selects. Keep populated files outside the release repository and preserve backups before edits. Use JSON so the validator needs only Python's standard library. Actual personal values and body content do not belong in these metadata files.

## requirements.json: independent confirmed input

- `schema_version`: 1.
- `input_basis`: `kind` (`user_confirmation` or `synthetic`) and an ISO date/time `confirmed_at`. Historical recovery uncertainty belongs in a private setup note, not an invented confirmation.
- `source_requirements`: entries with unique `id`, exact logical `source_id`, `domain`, `subject` and `role` (`live`, `canonical`, `original`, `derived`, `archive`). Record every source choice independently of implementation.
- `capability_requirements`: unique `id`, `domain`, `intent`, `subject`, ordered `source_ids`, `required_qualifiers` and `freshness` (`live`, `dated`, `historical`). Describe desired source routing before building its implementation.
- `priority_labels`: unique `id`, exact `name`, email `source_id` and the implementing `route_id`. Capture the complete supplied label list. Labels are optional when no label workflow was requested.

At least one source and capability is needed for a usable setup. Capture missing or pending authority separately; don't mark it confirmed merely to pass validation.

## profile.json: implementation

- `requirements_sha256`: SHA-256 of the canonical JSON baseline. Use the `fingerprint` command; it sorts keys and omits whitespace. A digest is drift detection, not a signature or access grant.
- `general_retrieval_enabled`: false. Scoped questions can still use existing authorized tools.
- `policy`: `finance: explicit_question_only`, `identity: task_specific_need`, `email: designated_provider_only`, `automatic_fallback: false`.
- `integrations`: unique `id`, `kind` (`local_files` or `provider`), `provider` (user-selected name), `readiness` (`unverified`, `user_confirmed`, `verified`). No command, secret or connection configuration is stored here. Readiness does not mean currently accessible. Keep its observation date and evidence in the private setup note.
- `sources`: unique `id`, `domain`, `subjects`, `role`, `kind` (`file`, `email`, `ledger`, `service`), `integration_id`, `location_ref` (same logical ID for a local file; null for provider sources), and `instruction_refs` (logical names). Local clinical sources have one patient. Generic email can have several permitted subjects, but every route/request selects one.
- `routes`: unique `id`, `domain`, `intent`, one `subject`, ordered `source_ids`, `required_qualifiers`, `freshness`, and nullable `label_id`. Finance must include `account_ref`, `topic_ref`, `date_range`; an explicit aggregate-account qualifier is allowed. Owner-private includes `owner_ref`; identity includes `field_set`. Other qualifiers should reflect the user's needed scope, not a universal maximum checklist.
- `labels`: unique `id`, exact `name`, `source_id` and `route_id`, and `coverage` (`unknown` or `all_confirmations`). Generated Gmail queries quote the exact label; names containing controls, quotes or backslashes are rejected rather than interpolated. Do not assert full filing coverage without evidence. Version 0.1 label planning supports Gmail, not arbitrary provider query dialects.

Implement exactly the captured source/capability/label sets. Amend the independent baseline only with user-backed reconciliation when adding a real requirement. A digest catches accidental drift, not a coordinated change to both files.

## local-map.json: locations only

Each mapping has `source_id`, exact nonempty `location`, and `instructions`: an object resolving every source `instruction_ref` to its existing path. Include exactly the local-file source entries; no recursive grants, document bodies or credentials. The validator reads mapping metadata only, never locations it contains. Synthetic example locations use `synthetic://` URIs and are not production paths.

## Offline commands

Run the skill's `scripts/profile_tools.py` with `python3`:

```sh
python3 /path/to/profile_tools.py fingerprint --requirements /private/config/requirements.json
python3 /path/to/profile_tools.py validate --requirements /private/config/requirements.json --profile /private/config/profile.json --local-map /private/config/local-map.json
```

`plan --requirements <file> --profile <file> --local-map <file> --request <file>` first validates the independent baseline and map metadata, then checks a manually normalized request and prints only a logical plan/status. It reads private mapping metadata but never mapped source content. Requests use `domain`, `intent`, `subject`, `qualifiers`; financial/identity requests also require `explicit_financial_question`/`explicit_identity_need`. Missing qualifiers are normalization results: an assistant can discover them safely from prescribed evidence before asking the user. The helper cannot interpret free text, establish authorization or perform that discovery.

Pass `label_id` to request its configured Gmail query; the route's default label is otherwise used. A different route's label is rejected. No source/path overrides are accepted. An `unverified` integration produces an unavailable/unverified plan rather than claiming liveness.
