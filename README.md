# Personal Intelligence

**Make your existing information usable.**

Personal Intelligence gives your assistant a structured way to find the right source, understand its authority, and answer from evidence — while your information and configuration remain yours.

![Your personal information: files, email, records, trips, projects and accounts](assets/readme/your-personal-information.png)

### Your information already exists.

Files. Email. Records. Trips. Projects. Accounts.

The problem isn't storing more information.

It's knowing **where to look, what to trust, and what actually answers the question.**

![How Personal Intelligence works: from a question to relevant sources and an evidence-based answer](assets/readme/how-it-works.png)

### Personal intelligence, not another database.

Personal Intelligence doesn't copy everything into a new system.

It maps your existing sources and teaches the assistant how to use them.

![Privacy boundary: personal files, integrations, source map and configuration stay private; skills and generic tooling can be shared](assets/readme/privacy-boundary.png)

## What you install

Personal Intelligence is a pair of skills and a small, offline validation toolkit. Your information stays in its existing locations; your source map and configuration stay outside the shared repository.

Version **0.1.0** is a reusable workflow release. It bundles no MCP server, transport, accounts, automatic indexing, OCR, background collection or write tools. The Python helper validates metadata and produces planned routes; it never reads the documents those routes point to or calls a provider. Ordinary answers use the assistant's existing authorized tools.

The workflow can be adapted to other assistants that support skills. This release documents Codex installation; installation and automatic skill selection in other clients remain unverified.

## The two skills

- **setup-personal-intelligence:** record requirements independently, confirm authority and scope, map existing sources, validate coverage and run useful acceptance questions.
- **personal-intelligence:** find relevant evidence within the question's scope, compare authority and dates, and answer with citations and clear limitations.

Use this for personal records, trips, household documentation, professional projects and explicitly scoped financial questions. It is useful when several files or applications could answer a question differently.

## Install and start

The repository includes a local/repository plugin marketplace. With a current Codex client supporting custom marketplaces, register the downloaded repository:

```sh
codex plugin marketplace add /path/to/personal-intelligence
```

Then use the desktop plugin UI to select/install Personal Intelligence. Registration alone is not proof of installation. A GitHub marketplace source can replace the local path after publication; use the repository's actual owner/name. Local-marketplace support can vary by client. No account connections or permissions are changed by these files.

Alternatively, when your client supports direct skill directories, copy the two skill folders to its configured skill location. Each skill is self-contained; keep its supporting resources. See the official [skill guide](https://developers.openai.com/plugins/build/skills) and [plugin packaging guide](https://developers.openai.com/plugins/build/plugins).

Start a chat in your intended workspace and say:

> Use $setup-personal-intelligence to map my existing information. Keep configuration outside Git, preserve my existing integrations, and capture all my requirements before building routes.

Choose a private configuration directory, conventionally `$HOME/.config/personal-intelligence`. Tell the assistant where it is, or put that location in the workspace's local instructions. The package does not search your home directory to discover it and does not automatically install a global instruction file.

Once configured:

> Use $personal-intelligence with my private profile to find the confirmation for my next trip.

Normal invocation can also select the skill automatically. A missing privacy boundary still requires a focused question; a missing discoverable document/model/trip identifier usually requires narrow discovery first.

## Private configuration

The setup skill supplies three blank JSON templates and a schema reference. They describe sources and routes without copying their contents:

- `requirements.json`: independently captured user requirements, priorities and authority choices.
- `profile.json`: integrations, logical source IDs, routes and label workflows implementing them.
- `local-map.json`: exact source locations and existing instruction paths, outside Git.

An empty template is not a completed setup. The profile binds a digest of the independent requirements; changes need explicit reconciliation. The digest detects an accidental mismatch, not a forged approval or simultaneous malicious edit. Provider readiness metadata is testimony, not proof of current access; record its date and evidence in the private setup note.

Gmail priority labels are configurable and optional. No labels are prescribed for everyone. For Gmail questions, use its connected app/MCP exclusively; no browser, shell, local mail database or SMTP fallback. Other email providers can be recorded without labels; their dedicated provider route must be explicitly selected by the user. Version 0.1's generated label-query syntax is Gmail-specific.

Health requires one patient. Finance requires an explicit financial question and a bounded account/topic/date scope, including a deliberately stated aggregate-account scope when appropriate. Registration never grants background access. Identity, owner-private and other sensitive fields retain their separate task boundaries.

Your configuration and source collections are excluded from the shared package. When answering a question, the assistant may read relevant information through its authorized tools; how that information is processed depends on your chosen client, model provider and privacy settings.

## Companion integration: MoneyWiz

[MoneyWiz MCP Server](https://github.com/claessee/moneywiz-mcp-server) provides a separate, permanently read-only MCP interface to a local MoneyWiz database on macOS. It can supply ledger evidence for explicitly scoped financial questions; Personal Intelligence supplies the source-selection and evidence workflow.

The MoneyWiz server is optional and maintained separately. It is not bundled or installed by this package. Follow its own setup and reconciliation guidance, and keep financial configuration and results private.

## Verify without personal data

Requires Python 3.10 or later, standard library only. From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_release.py
python3 plugins/personal-intelligence/skills/setup-personal-intelligence/scripts/profile_tools.py validate --requirements examples/synthetic/requirements.json --profile examples/synthetic/profile.json --local-map examples/synthetic/local-map.json
```

The examples are entirely invented. Tests cover a fresh private setup, requirement omissions, separate patients, finance scope, labels with spaces, query injection, missing sources, source overrides and unavailable-provider metadata. They do not prove a live integration, model decision quality or filesystem confinement.

[RELEASE-READINESS.md](RELEASE-READINESS.md) separates automated checks, a manual synthetic evidence exercise and checks that remain for a recipient. A real setup should pass one useful question in each selected domain, judged against actual sources. Store those answers and timings privately.

## Sharing

Share the plugin ZIP or this generic repository. The plugin ZIP contains the plugin and its two skills; the repository ZIP also contains tests, synthetic examples and the marketplace. Neither should contain a user's configuration, source bodies, path map, credentials or personal evaluation history.

Publishing the repository does not publish to the OpenAI plugin directory. Directory publication uses its separate submission/review process: [official submission guide](https://developers.openai.com/plugins/deploy/submission). Recipients connect their own existing tools and build their own source map.

MIT licensed. Contributions should use synthetic fixtures and preserve explicit scope, source authority, required-input completeness and unavailable-source honesty.
