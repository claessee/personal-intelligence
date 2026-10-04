# Synthetic demonstration

Use only the release repository's `examples/synthetic/` when an offline demonstration is requested. Every profile subject, label, date and record is invented. Copy the three JSON metadata files to an isolated temporary directory outside Git; set restrictive file modes where supported, then run validation. The map's `synthetic://` locations do not resolve production files.

For an evidence exercise, the expressly supplied synthetic documents are the only content scope. Ask:

1. What travel dates and breakfast terms does the supplier confirmation establish? Check `documents/journey-confirmation.md`, whose old issue date differs from its later stay dates. The plan cannot establish breakfast terms.
2. Does the property decision index establish assembly approval? Compare `documents/decision-index.md` with `documents/committee-minutes.md` and preserve the approving body.
3. Does the newer patient report replace all baseline context? Compare `documents/patient-baseline.md` and `documents/patient-report.md`, matching the selected patient and affected fact only.
4. Can the provisional ledger fixture establish a definitive current balance? Inspect `documents/ledger-result.json`; distinguish diagnostic calculation from a verified recorded balance.

Record the observed answer, source/locator, role/date and exact limit. These are manual reasoning exercises, separate from the automated route/digest/completeness tests. Do not call their provider-style fixtures live evidence or claim they exercise a real connector.
