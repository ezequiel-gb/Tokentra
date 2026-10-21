# Tokentra v1.0.0 | Windows

Tokentra provides accurate local OpenAI text token counting, a dedicated desktop
workspace, three bundled encodings and interactive Context Planning.

- Token Counter uses tiktoken for exact raw-text counts, with Unicode code-point
  characters, words, plain-text import and background processing.
- Context Planning compares shared text and an additional allowance with a capacity
  you specify. It does not measure live ChatGPT context or predict hallucinations.
- No browser, API key or internet connection is required for application operation.
  No telemetry or automatic document saving is implemented.
- The conventional per-user Windows installer includes required notices and scoped
  Microsoft runtime terms. Upgrades from RC3 retain the stable installation identity.

## Install

Verify the setup SHA-256 against SHA256SUMS.txt, close Tokentra and open
`Tokentra-1.0.0-windows-x64-setup.exe` in File Explorer. Follow the wizard and
launch Tokentra from the Start menu. Uninstall from Windows Installed Apps.
The installer is unsigned and may produce Windows security/reputation warnings;
verify provenance without disabling security protections.

Windows 11 x64 is the tested target. macOS and Linux packages have not been
released or validated. Very large editor documents may pause layout; Count file
avoids editor layout overhead but still requires memory for the entire input.
Raw-text counts exclude conversation formatting, hidden instructions and service
overhead. No universal model compatibility or performance guarantee is implied.

QtBase and PySide/Shiboken corresponding-source archives accompany the installer
on the same release. See THIRD_PARTY_NOTICES.md, docs/QT_REPLACEMENT.md and
the build manifest for licences, checksums, verification scope and source revision.
