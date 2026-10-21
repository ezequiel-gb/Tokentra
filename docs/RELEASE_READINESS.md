# Tokentra 1.0.0 Windows release evidence

21 October 2026. This build-source checkpoint promotes the verified RC3 baseline
to 1.0.0 through version metadata and release documentation only. Application
counting, workers, planning, geometry and styling remain unchanged. Stable installer
AppId, per-user directory, recipient licence acceptance and uninstall rules remain intact.

## Exact final-build gates

The build-source commit is recorded by the release build manifest and matching
`v1.0.0` tag. At this source checkpoint, final tests/build/desktop checks have not
yet been executed. Post-build evidence is supplied with the release manifest and
an evidence-only main-branch documentation update; the release tag remains at
the exact build commit. Never infer a final-build pass from RC3 results alone.

Required final checks: full pytest suite; payload and licence audit; empty-cache
packaged diagnostics for all three encodings, import and planning; final native
window checks; visible RC3 upgrade including Microsoft terms; one Windows Settings
entry showing 1.0.0; Start menu launch; matching installed payload and uninstaller.
Publish installer and complete Qt/PySide sources only after these pass.

## Reused evidence and limits

RC3 completed 121 tests, four Qt scale factors (1, 1.25, 1.5, 2), cache-independent
packaged counting and actual desktop installation/upgrade/uninstall/reinstall checks.
The command-runner registry context was insufficient; actual Settings is authoritative
for desktop registration. See INSTALLATION_DISCREPANCY.md.

Prior mixed-text million-token benchmarks remain relevant because performance-sensitive
code and native dependencies are unchanged. See release-audit/benchmark.json.
These measurements are machine/input-specific, not universal performance guarantees.

No clean Windows VM, physical network-disconnection test, packet capture, actual
OS scaling-change/multi-monitor exercise or macOS/Linux package validation is claimed.
Empty-cache Python socket denial and native endpoint sampling have narrower scopes.
The final installer is unsigned. Native dependency refresh and improved supplier
provenance remain documented recommendations, not concealed completed work.

## Licensing and delivery

MIT: Copyright (c) 2026 Ezequiel Gomez. See COMPLIANCE.md for the resolved
Community entitlement, scoped Microsoft acceptance page, retained native/Rust notices,
LGPL external-library replacement and exact QtBase/PySide source identities.
Both full corresponding-source archives must accompany the public binary with equivalent
access. No portable binary is approved by the setup-only recipient arrangement.
The assessment is engineering evidence, not formal legal certification.
