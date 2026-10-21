# Windows geometry and desktop verification

## Automated evidence

The code uses native OS decorations, not a frameless/custom title bar. The earlier guard accepted any screen intersection
and ran before final frame sizing; it did not establish that the title bar or whole frame was accessible. A 1120 × 820
client default could also exceed the logical desktop after scaling. The new policy uses Qt logical coordinates,
`QScreen.availableGeometry()`, actual client/frame differences and pre-show plus queued post-show validation.

Native Windows event tracing established an additional restore race: `WindowStateChange` can already say normal while
the rectangle still describes the maximised window. The policy now captures the normal client rectangle before expansion,
restores it before containment and ignores startup restoration events until initialisation is complete.
It does not clamp every interactive resize/move or alter native maximise work-area management.

Geometry unit/widget regressions cover full frame containment, partial overlap, top/left reserved desktop strips,
negative-origin monitors, oversized defaults, reduced work areas, corrupt preferences, valid geometry roundtrips,
screen-change repair, maximised-state persistence and normal restoration. Small logical desktops temporarily relax
the usual 680 × 540 minimum rather than push window controls outside the available area.

Native `windows` Qt platform smoke tests passed at **Qt scale factors 1, 1.25, 1.5 and 2**. Evidence:
`release-audit/frozen-windows-scale-1.json`, `frozen-windows-scale-1.25.json`, `frozen-windows-scale-1.5.json`, `frozen-windows-scale-2.json`.
The final frozen executable also passed all four scales from an external temporary directory with developer search paths
removed; see `release-audit/frozen-windows-scale-*.json`.
These use isolated INI settings and cover first launch, valid/invalid/oversized/corrupt saved geometry, programmatic
maximise/restore, minimise/reopen, full-screen exit and resize. The saved normal rectangle survives maximise/restore.
Qt/DWM may report invisible maximised resize borders outside the work area; normal frames and maximised client areas
are recorded. For maximised Windows windows, DWM visible physical bounds are compared directly with the monitor work area,
because Qt's separately rounded logical client position and height can differ by one logical pixel at fractional scaling.
At scale 1.5 the measured visible bounds and work area both equal `[0,32,1280,800]`. There is no arbitrary pixel tolerance.
Normal Qt outer frames remain strictly contained, and there are no hard-coded taskbar dimensions.

**Qt scale factors are not a substitute for changing Windows display scaling or physical monitor topology.**
The original reported machine/display configuration has not been reproduced directly.

## Repeat native smoke tests

```powershell
foreach ($scale in @('1','1.25','1.5','2')) {
    $env:QT_SCALE_FACTOR=$scale
    python -m app.main --window-check --report "window-scale-$scale.json"
}
Remove-Item Env:\QT_SCALE_FACTOR
```

Use the packaged executable with the same `--window-check` and `--report` arguments to test the frozen build.
The diagnostics open their own short-lived test windows, never read normal user preferences and never write text content.

## Physical acceptance checklist, still required

Use a separate Windows account or back up the Tokentra preferences before intentionally changing them. Standard Windows
preferences are under `HKEY_CURRENT_USER\Software\Tokentra\Tokentra`; the application stores window geometry, selected encoding, mode, context capacity and additional allowance; never document text.

| Check | Procedure | Expected result | Status |
|---|---|---|---|
| Fresh account / no preferences | Launch the extracted candidate | Whole normal frame and native title bar inside work area | Native synthetic-account equivalent passed; real fresh account pending |
| Valid saved window | Move/resize, close, reopen | Position and dimensions preserved | Automated roundtrip passed; manual confirmation pending |
| Invalid coordinates | Use native diagnostic invalid-saved case | Controls accessible without dragging from off-screen | Passed |
| Reduced resolution | Lower actual display resolution, relaunch | Window resized/repositioned into work area | Simulated logical bounds passed; physical test pending |
| Windows scaling | Set OS display scale to 100%, 125%, 150%, 200%; sign out if required | No clipped controls or inaccessible title bar | Qt scale-factor tests passed; OS settings test pending |
| Single monitor | Launch on primary display | Work-area containment | Passed on available Windows desktop |
| Multiple monitors | Move to second display, close, reopen | Valid secondary position preserved | Simulated negative-origin selection passed; physical test pending |
| Disconnect external display | Disconnect while running and while closed | Return to remaining work area | Signal-path regression passed; physical test pending |
| Maximise/restore | Use native buttons and double-click title bar | Square maximised shell; valid rounded normal restore | Programmatic native transitions passed; manual controls pending |
| Minimise/reopen | Use taskbar and native button | Window accessible, state retained | Programmatic native transition passed; taskbar interaction pending |
| Drag/resize/snap | Drag native title bar, all edges, Windows snap | No fight with geometry policy or layout damage | Pending manual test |
| Full-screen | F11, Escape, from normal and maximised | Correct edge-to-edge entry and valid restoration | Automated coverage; manual keyboard test pending |
| Input/focus/accessibility | Tab controls; type/paste scripts; screen reader | Clear focus and readable controls | Widget functionality checked; assistive-tech sign-off pending |

Also verify actual 100k/1m multilingual/code files, clipboard operations, decoding errors, processing feedback and low-memory
behaviour. Extremely small logical work areas can leave little room for the editor even though window controls remain accessible.
Do not change physical system display settings automatically in a release test on a user's working desktop.


## RC2 Context Planning and installer checks

Repeat both modes at each physical scaling/resolution/monitor configuration above. Import a synthetic
Unicode transcript, change encoding, then switch modes and confirm the text/count stay consistent. Tab to
capacity and allowance, enter invalid/zero/large/over-capacity scenarios and verify immediate validation,
negative remaining capacity and explicit excess. At 680×540, scroll the dashboard to both inputs and the
interpretation/limitations; confirm focus stays visible and the editor is usable. Clear during a pending count
and confirm stale values do not return. Check copy, import failure, F11/Escape and maximise/restore in both modes.

On a clean Windows 11 machine without Python/development tools: disconnect networking, run the unsigned setup,
check branding and optional desktop task, find Tokentra in Start/search and Installed Apps, launch from both
shortcuts, and exercise all three encodings and import/planning. Inspect native network activity if available.
Close the app before upgrading/uninstalling; while open, setup/uninstall should refuse without discarding text.
Verify a newer candidate replaces the prior one with a single entry. Uninstall through Settings, confirm tracked
files and shortcuts disappear while unrelated documents/preferences remain, then reinstall and launch again.
Record actual OS settings and results; QT_SCALE_FACTOR diagnostics do not replace these physical checks.


## RC3 refinement checks

The persistent technical footer should be absent in both modes. In Token Counter, hover or Tab to the outlined
information control beside Text Tokens; read all of the wrapped explanation. Move focus, move the pointer away,
press Escape or change mode and confirm dismissal. Move the window near each screen edge and verify the tooltip
stays readable. Confirm selecting/copying the number and Ctrl+Shift+C still work.

In Context Planning, enter capacities 1,000 / 8,000 / 128,000 / 1,000,000 / 10,000,000. Confirm the card and input
show the same full capacity and every metric has sufficient width. Test negative unallocated capacity, exact fit,
invalid inputs, and very long totals without abbreviation. Resize slowly around card reflow thresholds. At a
comfortable desktop size, cards, inputs, allocation bar and interpretation should fit without needless scrolling;
at compact/high-DPI sizes scroll within the dashboard and Tab to offscreen inputs. Switch modes repeatedly while
editing; the editor content must survive and pending results must not be presented as current.

Current native Qt scale-factor evidence is under `release-audit/ui-clean`; actual OS scaling changes, monitor hot-plug and
assistive technology checks remain physical validation work. The automation records actual client sizes because
Windows may constrain a requested logical size on the test monitor.

At the smallest available high-DPI work area, also verify the entire dashboard frame stays within the client
boundary and at least one complete editor text line remains readable. Below 500 logical pixels the secondary
branding caption is hidden and spacing tightens; below 400 it tightens further. Tab through the planning cards
to both scenario inputs and confirm each focused control scrolls fully into view. Wider/taller windows restore
the normal branding and spacing. RC3 native diagnostics explicitly check startup containment before any resize.
