# TOKENTRA
### Precision Token Counter
**Product Specification & Development Blueprint | Version 1.0**

**Product identity:** Tokentra  
**Category:** Standalone desktop utility  
**Platforms:** Windows, macOS and Linux  
**Visual identity:** Refined Blue Glass Finish  
**Operating model:** 100% offline, local processing  
**Core technology:** Python, PySide6 and OpenAI tiktoken  
**Development status:** Specification approved in principle, implementation pending

---

## 1. Product Overview

**Tokentra** is a modern, standalone desktop application designed to calculate text token counts accurately using GPT-compatible tokenisation.

The application allows users to paste, type or import text and immediately determine how many tokens it contains under a selected OpenAI tokeniser.

Tokentra prioritises five principles:

1. **Accuracy:** Exact token counting under supported OpenAI encodings.
2. **Privacy:** All text remains on the user's device.
3. **Performance:** Efficient handling of ordinary and exceptionally large text.
4. **Simplicity:** A focused interface without unnecessary complexity.
5. **Independence:** No AI models, API connections, accounts, subscriptions or usage fees.

The application will run locally on Windows, macOS and Linux through platform-specific packages built from a shared codebase.

Tokentra is not an AI assistant. It does not generate, interpret or transmit text. Its purpose is to measure tokens reliably and efficiently.

---

## 2. Visual Identity

### Design Direction: Refined Blue Glass Finish

Tokentra will feature a sophisticated desktop interface combining metallic midnight-blue surfaces, subtle translucency, frosted glass panels and restrained lighting effects.

The design should communicate precision, quality and technological sophistication without appearing excessively decorative.

### 2.1 Colour Palette

| Element | Colour | HEX |
|---|---|---|
| Primary background | Midnight Navy | `#081626` |
| Secondary surface | Metallic Blue | `#153A63` |
| Interactive accents | Cobalt Blue | `#3178C6` |
| Glass overlays | Steel Blue | `#487FA8` |
| Highlight colour | Ice Blue | `#A8DFFF` |
| Primary text | Silver White | `#E7F1F9` |

Additional gradients may transition between midnight navy, dark cobalt and metallic blue.

### 2.2 Glass and Metallic Effects

The interface will incorporate:

- Semi-transparent, frosted-glass panels.
- Subtle metallic gradients.
- Fine silver-blue borders.
- Gentle depth and shadow effects.
- Restrained luminous accents.
- Soft hover effects and transitions.
- Clear contrast between foreground text and background surfaces.

Transparency will be concentrated around decorative panels and the application shell.

The text-editing area will remain predominantly opaque to ensure readability when processing large documents.

Native background-blur effects may vary across operating systems. Tokentra will provide consistent visual fallbacks where blur or transparency is unavailable.

### 2.3 Geometry

| Component | Design |
|---|---|
| Main application window | 18 px rounded corners |
| Internal glass panels | 12–16 px rounded corners |
| Buttons | 10–12 px rounded corners |
| Input fields | 10–12 px rounded corners |
| Borders | Approximately 1 px |
| Window shadow | Soft, diffuse dark blue |
| Spacing | Consistent, spacious layout |

All dimensions are proposed defaults and may be refined during implementation.

### 2.4 Typography and Icons

Tokentra will use a modern system sans-serif font with a clear visual hierarchy.

Large numerical token counts will receive prominent emphasis, while secondary metrics will use smaller, understated typography.

Icons will follow a consistent minimal outlined style.

Animations should feel smooth and responsive without introducing unnecessary visual distractions.

---

## 3. Desktop Window Behaviour

Tokentra will support conventional desktop window operations.

### 3.1 Windowed Mode

When operating in a normal desktop window:

- Rounded outer corners are visible.
- A subtle exterior shadow creates depth.
- Glass and metallic effects frame the interface.
- The window can be moved and resized.
- Standard minimise, maximise and close functions remain available.

### 3.2 Maximised Mode

When maximised:

- Outer corners become square.
- The window occupies the available desktop work area.
- Decorative exterior margins disappear.
- The workspace expands proportionally.
- Internal panels retain their rounded corners.

### 3.3 Full-Screen Mode

In full-screen mode:

- Tokentra fills the display edge to edge.
- Window decorations are hidden.
- The editor expands to utilise available space.
- The application remains fully interactive.

### 3.4 Window Persistence

Tokentra should remember non-sensitive preferences, including:

- Last window dimensions.
- Last normal window position, where valid.
- Last selected tokeniser.
- Relevant display preferences.

The application must handle different screen sizes and high-DPI displays.

Custom window effects will be implemented with platform-specific compatibility checks, particularly for macOS and Linux desktop environments.

---

## 4. Application Interface

Tokentra will use a clean, single-window design built around a spacious text workspace.

### 4.1 Main Interface Structure

The application will contain four primary areas:

**A. Application Header**

Displays:

- Tokentra branding and application icon.
- Selected tokeniser information.
- Window management controls.
- Optional settings access.

**B. Tokeniser Selection**

A compact selector allows users to choose the desired GPT-compatible encoding.

The default will be `o200k_base`.

**C. Text Workspace**

The central workspace occupies the largest portion of the application.

It supports:

- Text entry.
- Pasting from the clipboard.
- Standard text selection.
- Keyboard shortcuts.
- Scrolling through large documents.
- Plain-text file import.
- Copying and clearing content.

**D. Results Dashboard**

A persistent metrics panel displays:

- Total tokens.
- Total words.
- Total characters.
- Selected encoding.
- Processing status, where relevant.

The token count will be the most visually prominent metric.

### 4.2 Responsive Layout

Tokentra's interface will adapt to window resizing.

When additional screen space is available, the text editor expands.

At smaller window sizes, controls and metrics reorganise to avoid clipping or unnecessary horizontal scrolling.

The user should not need to scroll away from the text editor to see the token count.

---

## 5. Tokenisation Engine

### 5.1 Core Technology

Tokentra will use OpenAI's open-source `tiktoken` library.

The library will be integrated directly into the packaged application, allowing supported token counts to be calculated locally without accessing an external service.

All required tokenisation assets will be bundled during packaging.

### 5.2 Supported Encodings

The initial implementation will target:

| Encoding | Purpose |
|---|---|
| `o200k_base` | Modern GPT-family tokenisation |
| `cl100k_base` | Earlier GPT-family tokenisation |
| `p50k_base` | Optional legacy compatibility |

The application will display the active encoding to avoid ambiguity.

Additional supported OpenAI encodings may be introduced through future updates.

Model compatibility mappings will be checked against the version of `tiktoken` included in each release.

### 5.3 Accuracy Standard

Tokentra will provide exact raw-text token counts under supported encodings.

Special-token handling will be explicitly defined and tested.

Importantly, these results are not guaranteed to equal every token reported by ChatGPT or an API request.

Additional tokens may arise from message formatting, system instructions, tools, multimodal inputs and other model-specific processing.

Tokentra will therefore describe its results as **text token counts**, not universal API billing totals.

### 5.4 Calculation Behaviour

The counting system will operate as follows:

1. The user types, pastes or imports text.
2. Tokentra identifies the selected encoding.
3. The local tokeniser processes the input.
4. The resulting count is returned.
5. The interface updates the displayed metrics.

For ordinary text, recalculation will occur automatically following edits.

A short configurable internal delay may be used to prevent excessive processing during continuous typing.

For large inputs, calculation will take place on background workers.

The application will never display outdated results as though they represent the latest input.

### 5.5 Supported Content

Tokentra will count text containing:

- Ordinary prose.
- Source code.
- Numbers and punctuation.
- Spaces and line breaks.
- Unicode characters.
- Emoji.
- Multilingual text.
- Markdown and other text-based formatting syntax.

The input will be measured as text, without interpretation by an AI model.

---

## 6. Large-Text Performance

Large-document support is a fundamental requirement.

Tokentra will be designed without an arbitrary predefined input limit.

Practical capacity will depend on available RAM, processing resources, input characteristics and tokeniser performance.

### 6.1 Performance Targets

| Input size | Expected design behaviour |
|---|---|
| Small text | Rapid automatic updates |
| Medium documents | Responsive interactive counting |
| 100,000 tokens | Background processing without freezing |
| 1,000,000 tokens | Initial large-input benchmark target |
| Larger inputs | Best-effort processing within hardware limits |

These are engineering targets rather than guaranteed benchmark results.

### 6.2 Performance Architecture

Tokentra will use several techniques to maintain responsiveness.

**Background processing**

Counting operations will execute outside the main GUI thread.

**Debounced updates**

Repeated edits will not trigger unnecessarily expensive simultaneous calculations.

**Outdated-result protection**

Each calculation will be associated with its originating input state. Results for older versions of the text will be discarded.

**Memory management**

The application will minimise unnecessary copying of text, particularly when processing large files.

**File-based processing**

Where appropriate, large imported files may use a processing route separate from the interactive editor.

**Accuracy-preserving processing**

Tokentra will not assume that separately tokenised chunks can always be added together to obtain an exact total. Any optimised processing technique must preserve tokenisation correctness.

### 6.3 Processing Feedback

For longer calculations, the interface will indicate that processing is taking place.

The user must be able to continue interacting with the application without the entire window freezing.

Memory exhaustion and other processing failures will produce clear errors rather than misleading counts.

---

## 7. Core Features

### 7.1 Version 1.0

The initial release will include:

1. Large plain-text editing workspace.
2. Paste and type functionality.
3. Accurate local GPT token counting.
4. Selectable supported OpenAI encodings.
5. Word counting.
6. Character counting.
7. Automatic recalculation.
8. Plain-text file import.
9. Copy text.
10. Copy token count.
11. Clear text.
12. Processing status indication.
13. Responsive application layout.
14. Standard keyboard shortcuts.
15. Persistent non-sensitive preferences.
16. Refined Blue Glass visual theme.
17. Rounded windowed mode.
18. Maximised and full-screen support.
19. Offline operation.
20. Windows, macOS and Linux packaging.

### 7.2 Potential Future Features

The following are deliberately excluded from the initial scope:

- Token-by-token colour highlighting.
- Multiple-document tabs.
- Side-by-side tokeniser comparisons.
- Exportable statistical reports.
- User-defined token-limit indicators.
- Additional non-OpenAI tokenisers.
- Historical counting sessions.
- Advanced text statistics.

These additions should only be considered after the core application has been validated.

---

## 8. Technical Architecture

### 8.1 Recommended Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Desktop framework | PySide6 / Qt 6 |
| Tokenisation engine | OpenAI tiktoken |
| Parallel processing | Qt background workers |
| Local preferences | Qt settings facilities |
| Application packaging | PyInstaller |
| Automated testing | pytest |
| Source control | Git |

This stack is recommended for its maturity, cross-platform support and relatively straightforward development process.

### 8.2 Architectural Separation

Tokentra will separate interface presentation from tokenisation and application logic.

**Presentation layer**

Responsible for the metallic-blue interface, text editor, metrics, controls and window behaviour.

**Application controller**

Coordinates user actions, selected encodings, file operations and interface updates.

**Processing layer**

Manages counting tasks, result delivery and outdated-result protection.

**Tokenisation layer**

Provides a reusable interface to the locally installed and bundled `tiktoken` engine.

**Persistence layer**

Stores permitted application settings without automatically storing pasted documents.

This structure allows the counting engine to be tested independently of the GUI.

### 8.3 Proposed Project Structure

```text
tokentra/
│
├── app/
│   ├── main.py
│   │
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── title_bar.py
│   │   ├── editor.py
│   │   ├── metrics.py
│   │   └── theme.py
│   │
│   ├── core/
│   │   ├── tokenizer.py
│   │   ├── counter.py
│   │   └── workers.py
│   │
│   ├── services/
│   │   ├── file_handler.py
│   │   └── settings.py
│   │
│   └── assets/
│       ├── icons/
│       └── tokenizers/
│
├── tests/
├── packaging/
├── requirements.txt
└── README.md
```

The project structure may be adjusted during implementation if a simpler architecture meets the same requirements.

---

## 9. Platform Compatibility and Distribution

Tokentra will use one shared source codebase and separate native packages for its supported operating systems.

### 9.1 Windows

Target distribution:

- Standalone executable.
- Optional installer.
- No separate Python installation.
- Standard Windows window controls and shortcuts.

Unsigned builds may trigger operating-system security warnings.

### 9.2 macOS

Target distribution:

- Native `.app` bundle.
- Optional `.dmg` distribution.
- Apple Silicon compatibility.
- Intel compatibility where validated.
- macOS-appropriate keyboard shortcuts and window behaviour.

Code signing and notarisation may be required for frictionless public distribution and could introduce external costs.

### 9.3 Linux

Target distribution:

- Portable application package, preferably AppImage if validation supports it.
- Compatibility testing across representative distributions.
- Support for common desktop display environments, including X11 and Wayland where feasible.

Window transparency and decorative effects will use fallbacks when unsupported.

### 9.4 Build Process

PyInstaller packages will be built using operating-system-specific build environments.

Cross-platform source compatibility does not mean that one executable can run unchanged on every operating system.

The initial objective is functional parity and a consistent visual experience, with practical allowances for platform conventions.

---

## 10. Privacy, Offline Operation and Security

Tokentra will be designed as a local-only utility.

### Mandatory Requirements

- No AI model execution.
- No OpenAI API requests.
- No internet dependency.
- No mandatory accounts or authentication.
- No subscriptions or usage charges.
- No analytics or telemetry.
- No automatic upload of text.
- No cloud storage.
- No automatic saving of pasted content.
- No mandatory external update service.

The application will bundle all assets required for offline counting, including tokeniser data.

Offline functionality will be validated by launching and using the packaged application with network access disabled.

### Local Data Handling

By default, Tokentra will store only non-sensitive preferences such as window dimensions and the selected encoding.

Pasted and imported content will remain in application memory during the session unless the user explicitly uses a future save or export function.

Tokentra will handle unsupported files, decoding errors and resource limitations without exposing input text to remote services.

---

## 11. Development Approach

The recommended implementation sequence consists of five phases.

### Phase 1: Core Tokenisation

- Establish the Python environment.
- Integrate `tiktoken`.
- Implement encoding selection.
- Bundle tokeniser assets.
- Validate exact reference counts.
- Test offline initialisation.

**Outcome:** A verified local token-counting engine.

### Phase 2: Functional Desktop Interface

- Build the main application window.
- Implement the text editor.
- Connect counting results to the interface.
- Add copy, clear and file import actions.
- Implement settings persistence.

**Outcome:** A functional desktop token calculator.

### Phase 3: Refined Blue Glass Design

- Apply the metallic midnight-blue palette.
- Create frosted-glass panels.
- Introduce rounded window geometry.
- Implement maximise, restore and full-screen transitions.
- Refine typography, spacing and interactions.

**Outcome:** The intended Tokentra visual experience.

### Phase 4: Performance and Reliability

- Introduce background counting workers.
- Benchmark large inputs.
- Validate memory usage.
- Test Unicode and unusual input content.
- Test concurrent edit and calculation behaviour.
- Ensure errors are handled appropriately.

**Outcome:** A stable and responsive application.

### Phase 5: Packaging and Validation

- Generate Windows builds.
- Generate macOS builds.
- Generate Linux builds.
- Test installation and launch behaviour.
- Validate offline execution.
- Resolve platform-specific visual and functional issues.

**Outcome:** Version 1.0 release candidates for all three operating systems.

---

## 12. Testing and Acceptance Criteria

Tokentra will be considered ready for version 1.0 when the following criteria are met.

### Functional Accuracy

- Supported encodings produce correct counts against verified reference cases.
- Empty text produces zero tokens.
- Unicode, punctuation, code and line breaks are counted correctly.
- Changing encodings produces the appropriate recalculation.
- Outdated results cannot overwrite current results.

### Interface Quality

- Text remains readable under the blue-glass theme.
- Window resizing does not break the layout.
- Rounded corners are displayed where supported.
- Maximised mode removes the rounded exterior framing.
- Keyboard navigation and standard shortcuts operate correctly.
- High-DPI rendering remains clear.

### Performance

- Ordinary inputs are counted responsively.
- Large counting tasks do not block the main GUI thread.
- The 1-million-token benchmark is evaluated on representative hardware.
- Memory use is measured and documented.
- Resource failures are reported clearly.

### Distribution

- Each supported platform has a working package.
- No separate Python installation is required.
- Tokenisation works without an internet connection.
- Tokeniser assets are included.
- Platform-specific limitations are documented.

---

## 13. Cost and Licensing

Tokentra is intended to operate without recurring service costs.

The proposed software stack uses publicly available development tools and libraries.

No AI API charges or token-processing fees will apply.

However, zero operating fees should not be confused with an unconditional guarantee of zero development or distribution costs.

Potential costs could include optional Apple developer registration, code-signing services or other public-distribution infrastructure.

Software licences and redistribution requirements must be checked before releasing packaged binaries.

---

## 14. Current Decisions and Remaining Assumptions

### Established Decisions

- Product name: **Tokentra**.
- Product descriptor: Precision Token Counter.
- Scope: GPT/OpenAI tokenisation.
- Operation: Fully offline.
- Target platforms: Windows, macOS and Linux.
- No AI models or API dependency.
- No recurring usage fees.
- Large-text capability.
- Refined Blue Glass Finish.
- Rounded corners in windowed mode.
- Square external corners when maximised or full-screen.

### Proposed Implementation Defaults

- Python and PySide6.
- OpenAI `tiktoken`.
- Default encoding: `o200k_base`.
- Initial large-text benchmark: 1 million tokens.
- Main-window corner radius: 18 px.
- Automatic recalculation with debouncing.
- Initial file-import support: `.txt`.
- Plain-text workspace with no automatic content persistence.
- PyInstaller-based platform packaging.

These defaults can be refined without changing the underlying product objective.

### Outstanding Verification

Before the first public release, the project must verify:

- Current tokeniser compatibility and mappings.
- Offline packaging of all required data.
- Large-text performance on representative hardware.
- Native window effects across operating systems.
- Component licences and redistribution obligations.
- Availability of the Tokentra name for the intended distribution.

The name has been selected for the project, but trademark and existing-product availability have not been established.

---

## 15. Final Product Definition

**Tokentra | Precision Token Counter**

Tokentra is a modern, privacy-focused desktop application that accurately counts text tokens using locally installed OpenAI-compatible tokenisers.

Its interface combines a spacious text-editing workspace with a refined metallic-blue glass appearance, subtle translucent panels, elegant rounded corners and immediately accessible counting results.

The application is designed for Windows, macOS and Linux, using a shared codebase and separate platform-specific distribution packages.

Tokentra does not require AI models, API credentials, internet connectivity, subscriptions or ongoing processing fees.

Its core objective is to deliver **accurate, fast, private and effortless GPT token counting**, even when working with large volumes of text.

**Development recommendation:** Proceed with a verified offline tokenisation engine and functional desktop prototype before finalising advanced visual effects and cross-platform packaging.

The specification is sufficiently defined to begin implementation, with remaining technical decisions addressed through testing rather than further broad conceptual redesign.


## Implemented interface refinements — RC3

The authorised RC3 refinement replaces the permanent technical footer with keyboard-accessible contextual
information beside Text Tokens. Context Planning retains the shared editor and calculation logic, gives more
height to the dashboard in planning mode, and uses font-aware, equal-width responsive metric cards to keep
full numerical values readable. The established blue-glass styling and native window controls/geometry policy
are retained. Current implementation and verification status are recorded in `docs/RELEASE_READINESS.md`.
