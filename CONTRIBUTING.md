# Contributing to SigTrack

Thanks for taking the time to improve SigTrack. This guide covers the development environment, the conventions the codebase actually follows, and the manual checks expected before a pull request.

SigTrack is a desktop PySide2 application, not a web service. Most changes touch Qt widgets, QML, FFmpeg subprocesses, or hardware-dependent paths, so a compile check is not enough — please run the relevant manual scenarios.

---

## 1. Set up a development environment

### Prerequisites

- Python **3.9** (the PySide2 5.15 wheels used here are the constraint; newer Pythons may not have wheels).
- Qt 5.15 runtime, installed by PySide2.
- FFmpeg and FFprobe binaries.
- A Keygen license key if you need to launch the full app.
- Optional: a Meshtastic radio for the mesh workspace.

### Install

```bash
git clone https://github.com/Serkhani/SigTrack.git
cd SigTrack
```

Windows:

```bat
py -3.9 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`requirements.txt` is UTF-16 encoded. If pip rejects it, re-save it as UTF-8 or install the pinned packages manually:

```bash
python -m pip install exif==1.6.0 qt-material==2.14 py-machineid==0.2.1 requests==2.28.0 meshtastic==2.3.8 pub==0.0.4 fpdf2==2.7.8 PySide2==5.15.2.1
```

> The repository also pins PySide6. Do not import it in application code — the runtime is PySide2/Qt 5.

### Runtime files

Create these beside `main_window.py` (`license.key`, `loraChat2.db`, and build output are git-ignored; `settings.json` is not):

```text
ffmpeg/ffmpeg.exe
ffmpeg/ffprobe.exe
license.key
settings.json          # optional, for the theme picker
```

### Run

```bash
python main_window.py
```

Run from the repository root so relative FFmpeg, license, and database paths resolve.

---

## 2. Project conventions

### Layout

| Layer | Location | Rule |
|-------|----------|------|
| Views | `sigtrack/views/` | Qt widgets, `.ui`-generated `Ui_*` classes, QML |
| Models | `sigtrack/models/` | Qt item models or plain state objects; no widget imports |
| Controllers | `sigtrack/controllers/` | Glue between a view and its model |
| Parsing | `sigtrack/klv_data/` | MISB/KLV only; keep Qt out of it |
| Utilities | `sigtrack/utils/` | Small, side-effect-light helpers |
| Resources | `sigtrack/resources/` | `.qrc` sources and compiled `*_rc.py` |

New features should follow the existing split: a widget in `views`, state in `models`, wiring in `controllers` when the wiring is non-trivial.

### Code style

- PEP 8 baseline, 4-space indentation, UTF-8 source.
- Match the surrounding file. The codebase mixes `camelCase` and `snake_case`; consistency within a module matters more than one global rule.
- Keep Qt imports explicit (`from PySide2.QtWidgets import ...`) rather than wildcard imports in new code.
- Guard optional hardware and network calls; the app must still start without a radio or internet.
- Do not add blocking work to a slot. If you need a subprocess or network call, use a worker thread and report back through a signal.

### Imports and entry points

`main_window.py` is the only entry point. `sigtrack/__init__.py` is intentionally empty. Avoid adding import-time side effects — importing `sigtrack.utils.activate_license` must not perform a network call until invoked.

### UI files

`form.ui` is the main-window source. Regenerate with:

```bash
pyside2-uic form.ui -o sigtrack/views/ui_form.py
```

The dock UI modules (`ui_videoview.py`, `ui_markerpopup.py`, `ui_report_window_view.py`) were generated from `.ui` files that are not checked in. If you need to change them, either add the `.ui` source to the repository or edit the generated module carefully and note it in the pull request. Never hand-edit `form.ui`-generated code without regenerating.

### Resources

Compile `.qrc` files with `pyside2-rcc`:

```bash
pyside2-rcc sigtrack/resources/icons/editing_icons.qrc -o sigtrack/resources/compiled/editing_icons_rc.py
pyside2-rcc sigtrack/resources/icons/map.qrc          -o sigtrack/resources/compiled/map_rc.py
pyside2-rcc sigtrack/resources/icons/vid_icons.qrc    -o sigtrack/resources/compiled/vid_icons_rc.py
```

New icons must be added to the `.qrc`, compiled, and referenced by alias. `.gitignore` excludes `*_rc.py`; the tracked compiled files are force-added. If you regenerate them, commit the result so other checkouts do not break.

### Adding a MISB field

1. Add the tag class in `sigtrack/klv_data/misb0601.py` with the correct 1-byte key and element parser.
2. Confirm it is registered under the ST 0601 local set.
3. Surface it in `VideoViewModel.extract_metadata` / `updateDurationInfo` if it should reach the map.
4. Extend `MapWidget.updateDronePosition` and the QML model roles only if the field changes geometry.

Test against a real ST 0601 clip, not a synthetic byte string, and include the `ffprobe` stream summary in the PR.

### Licensing headers

The KLV modules under `sigtrack/klv_data/` retain the MIT copyright notice from Matthew Pare's `klvdata`. Do not remove or rewrite those headers. New files should not claim an open-source license the project does not have.

---

## 3. Branching and commits

The history uses short, scoped branches and imperative subjects:

```text
feat/licensing
feature/chat
fix/video-marker
merge/joining_sigtrack
```

Recommended:

- Branch from `master`.
- Use `feat/`, `fix/`, `docs/`, or `chore/` prefixes.
- Keep the subject under ~72 characters: `fix: resolve watermark oversize bug`.
- Keep refactors separate from behavior changes.
- Reference the issue number in the body when one exists.

Avoid committing generated virtualenvs, `dist/`, `build/`, `license.key`, `loraChat2.db`, or `settings.json`.

---

## 4. Manual test checklist

There is no automated test suite yet. Before opening a pull request, run the scenarios your change touches:

| Area | Check |
|------|-------|
| Startup | App exits cleanly without `license.key`; starts with a valid key |
| Video | Open `.ts`, `.mp4`, `.mov`; play, pause, seek, stop, volume |
| FMV | Open map first, press **FMV**, play; icon, trail, footprint and frame line move |
| Video marker | Toggle the panel, **Add Marker**, drag the pin, confirm the tooltip updates |
| Mux | Mux a clip and log to `output.ts`; reopen and press **FMV** |
| Map | Switch all six map types; pan/zoom; click an image pin |
| Images | Import one file and a folder; verify pins; import a JPG without GPS and see the warning |
| Editor | Draw each shape; undo/redo; add text; add/scale/rotate watermark; save the view |
| Report | Generate a PDF with a PNG snapshot; open it and check header/footer/page number |
| Mesh | Open **View → Chat** with a radio connected and disconnected; send broadcast and direct messages |
| Panels | Peers table, symbols tabs, weather refresh, dock toggle |
| Theme | Change and reset a theme; restart and confirm persistence |
| Packaging | `pyinstaller SigTrack.spec`; launch `dist/SigTrack.exe` on a clean machine if possible |

If a scenario cannot be run because you lack hardware (radio, license, Windows), say so in the pull request rather than claiming it passed.

---

## 5. Pull request checklist

- [ ] The change is scoped to one concern.
- [ ] `python -m compileall sigtrack main_window.py` passes.
- [ ] `python main_window.py` starts (or the reason it cannot is explained).
- [ ] New code imports **PySide2**, not PySide6.
- [ ] No absolute local paths or secrets are added.
- [ ] `.ui`/`.qrc` sources and generated modules are consistent.
- [ ] New runtime dependencies are added to `requirements.txt` and documented.
- [ ] Affected docs (`README.md`, `USAGE.md`, `ARCHITECTURE.md`) are updated.
- [ ] Screenshots are included for visible UI changes.
- [ ] The manual scenarios touched by the change are listed as run.

---

## 6. Reporting bugs

Open an issue at [github.com/Serkhani/SigTrack/issues](https://github.com/Serkhani/SigTrack/issues) and include:

1. **What happened** and what you expected.
2. **Steps to reproduce**, including the exact menu path.
3. **Console output** — SigTrack logs at DEBUG and prints FFmpeg/KLV errors.
4. **Media details** for video issues:

   ```bash
   ffprobe -hide_banner -show_streams -show_format clip.ts
   ```

5. **Environment** — OS, Python, PySide2/Qt version, and whether a Meshtastic radio was attached.

For crashes, include the Python traceback. For rendering issues, a screenshot of the dock layout helps.

---

## 7. Security and privacy

- Do not commit `license.key`, `loraChat2.db`, or `settings.json`.
- The OpenWeatherMap key and Keygen account ID are embedded in the source for the current build. Do not add more embedded secrets; propose a configuration mechanism instead.
- Mesh node data may contain callsigns and locations. Scrub screenshots and logs before posting them publicly.
- Report suspected license-bypass or credential issues privately to the maintainers rather than in a public issue.

---

## 8. Questions

Start a discussion in an issue if you are unsure where a change belongs. For architecture context, read [ARCHITECTURE.md](ARCHITECTURE.md) first; for user-facing behavior, see [USAGE.md](USAGE.md).
