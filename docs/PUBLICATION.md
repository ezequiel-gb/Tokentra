# Public Windows release procedure

The owner explicitly authorises Tokentra 1.0.0 publication after final gates pass.
MIT is approved; Community 2022 entitlement, scoped Microsoft recipient acceptance,
LGPL notices and dynamic replacement arrangements are documented in COMPLIANCE.md.

## Canonical history

Use the clean `publication-preparation` lineage beginning at
`152773ce89f497b8ce44dd4d81295d05181ce109`, followed by
`c4fea80e688d806f98460cc359c8937f5a79b01b` and the final version-promotion commit.
The unrelated private historical `main` branch must remain local. Push only the
reviewed publication branch to remote `main`; never push `--all` or rewrite remote history.

Build from the clean committed source. Record that commit in the build manifest;
tag `v1.0.0` at that exact commit after tests, package audit and desktop upgrade pass.
Later evidence-only documentation commits may advance main without changing the tag.
Source archives must come from `git archive` of the build commit, not the unfiltered workspace.

## Assets and verification

The primary binary is `Tokentra-1.0.0-windows-x64-setup.exe`. Do not publish a
portable binary without an equivalent Microsoft recipient-acceptance arrangement.
Publish the two complete QtBase/PySide 6.12.0 source archives identified in
QT_REPLACEMENT.md beside the binary, with equivalent access, not just upstream links.
Include source revision, checksums, third-party notices and release notes.

Review current files and all clean-branch history for private paths/secrets before
creating or updating `ezequiel-gb/Tokentra`. Never upload raw private desktop logs.
After publication verify default branch, MIT, tag commit and anonymous access to
every required asset; compare downloaded bytes with recorded SHA-256 checksums.
Do not describe macOS/Linux packages as released or clean-machine testing as completed.
