# Tokentra v1.0 release preparation (unreleased)

The application feature/UI baseline remains 1.0.0-rc.3. No final v1.0 artefact or tag
is approved. MIT was authorised with Copyright (c) 2026 Ezequiel Gomez.

This audit adds dependency/source evidence, GPL/LGPL and upstream component notices,
a licence-aware clean source preparation, and corrects build-host PATH contamination
of packaged OpenSSL/UCRT DLLs. Counting, workers, geometry, planning and UI are unchanged.

Publication remains on hold. Owner reports accepting Community 2022 terms; Microsoft
runtime terms during setup are approved. Native/Rust notices and Qt source/replacement
guidance are prepared. Updated-installer validation and separate publication authorisation
remain required; recommended provenance/rebuild checks are distinguished from legal duties.
See COMPLIANCE.md and RELEASE_READINESS.md. Retain existing RC3 installers for rollback.

After these gates close, set the final version consistently, commit the reviewed source,
build from that exact revision, repeat applicable offline/installer tests, create a matching
v1.0.0 tag, and generate checksums. The intended installer name is
Tokentra-1.0.0-windows-x64-setup.exe. Publish only after the package and source are cleared.
