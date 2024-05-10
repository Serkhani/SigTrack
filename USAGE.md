# SigTrack — User guide

SigTrack is a desktop workspace for **full-motion video (FMV)**, map telemetry, imagery reports, and Meshtastic field comms. This guide covers the application as it ships in this repository: what to set up, how each workspace behaves, and what to do when something looks wrong.

> SigTrack is Windows-first. Paths in this guide use Windows separators; macOS and Linux work for development but need the path adjustments described in [Troubleshooting](#troubleshooting).

---

## Before you start

### 1. License

SigTrack checks a Keygen license at startup against a machine fingerprint.

1. Obtain a license key from the maintainers.
2. Save it as `license.key` in the directory you launch from — one line, no quotes, no trailing text.

```text
SigTrack/
├── main_window.py
├── license.key
└── ffmpeg/
```

If the file is missing, the app writes `No license key file found` to the log and exits. Validation and first-time machine activation both require network access.

### 2. FFmpeg

FFmpeg and FFprobe are used for:

- demultiplexing the KLV data stream when you press **FMV**,
- buffered telemetry reads,
- multiplexing video and telemetry into a `.ts`.

Create an `ffmpeg/` folder beside `main_window.py`:

```text
ffmpeg/
├── ffmpeg.exe
└── ffprobe.exe
```

The player calls `ffmpeg/ffmpeg.exe` and the multiplexer calls `ffmpeg/ffmpeg`, both **relative to the working directory**; the bundled KLV helpers also expect `ffprobe.exe` in the same folder. The buffered KLV reader in [`sigtrack/klv_data/constants.py`](sigtrack/klv_data/constants.py) also has an `ffmpegConf` setting; if your binaries live elsewhere, edit that value to the correct directory.

### 3. Supported media

| Input | Accepted | Notes |
|-------|----------|-------|
| Video | `.ts`, `.mp4`, `.mov` | The import dialog filters to these three |
| Telemetry log | `.log` | Used by the multiplexer |
| Images | `.jpg` | EXIF GPS is required for map placement |
| Radio | Meshtastic serial device | Auto-detected by the Meshtastic library |

### 4. Start the app

```bash
python main_window.py
```

The splash screen animates in, then the main window opens with the placeholder **Add a View**.

---

## The workspace

SigTrack uses dock widgets, not tabs. Each workspace you open is a dock you can move, float, tab, or close.

| Action | Opens |
|--------|-------|
| **View → Map** (`F1`) | OSM map dock |
| **View → Video** (`F3`) | Empty video dock with a **No Video** placeholder |
| **View → Image** (`F2`) | Empty image dock with a **No Image** placeholder |
| **View → Chat** | Meshtastic workspace |
| **View → Settings → App Theme** | Theme picker |

`File → Import → Video → File(s)` and `File → Import → Image → File(s)` open a dock **and** a map dock if one is not already open.

Docks are placed automatically: the first goes left, then top and bottom alternate as you add more. Closing the last dock restores the **Add a View** placeholder. The image editing panel is a separate floating dock on the left; it appears when an image view has focus.

> The **Edit → Undo / Redo / Zoom / Pan** menu entries are placeholders in this build. Use the buttons in the image editing panel instead.

---

## Video workspace

### Open a clip

1. **File → Import → Video → File(s)** (`Ctrl+Shift+F`).
2. Select one or more `.ts`, `.mp4`, or `.mov` files.
3. Each file gets its own video dock. A map dock opens automatically if needed.

The dock contains a transport row (play, stop, volume, **FMV**, **Marker**, **Mux**), a timecode label, and a seek slider.

### Transport

| Control | Shortcut | Behavior |
|---------|----------|----------|
| Play / Pause | `Space` | Starts or pauses playback; icon changes with state |
| Stop | `Esc` | Stops playback and returns the slider to zero |
| Volume | — | 0–100, applied directly to the media player |
| Seek | — | Scrubbing moves the player to that second |
| Timecode | — | `current / duration`, updated on position changes |

Playback itself is handled by Qt Multimedia's `QMediaPlayer`, so codec support depends on the Qt Media Service installed on your machine. If a clip opens but never renders, test the same file in another Qt-based player or convert it to H.264/AAC in an MP4 container.

### Load telemetry — the FMV button

**This is the step that links video to the map.**

1. Open the map dock first (**View → Map**, `F1`).
2. Open the video.
3. Press **FMV** (`Ctrl+F`).
4. Wait for the KLV stream to be demuxed and parsed.
5. Press play.

SigTrack runs FFmpeg with `-map 0:d` to extract data streams, then walks the KLV packets. On each position change it selects the packet whose **precision time stamp** has caught up with the playhead, and pushes these fields to the map:

| KLV field | Used for |
|-----------|----------|
| Sensor Latitude / Longitude | Platform icon and trail |
| Platform Heading Angle | Platform icon rotation |
| Frame Center Latitude / Longitude / Elevation | Footprint anchor and center line |
| Offset Corner Latitude/Longitude 1–4 | Footprint corners and sensor beams |

Notes:

- Indexing happens once per clip, sequentially. Long recordings take longer.
- The map only updates **after** indexing finishes; seeking far ahead stalls the UI while the parser catches up, and seeking backwards desynchronizes it.
- If the stream has no KLV, FFmpeg returns nothing and the map stays put. Check the clip with `ffprobe -show_streams <file>` and look for a data stream.
- The map that receives telemetry is the most recently opened map dock.

### Video markers

1. Press **Marker** (`Ctrl+I`) to show or hide the marker panel.
2. Click **Add Marker** in that panel.
3. Drag the purple pin over the object you want to annotate.
4. Keep playback running — the tooltip updates with an estimated latitude/longitude.

The estimate uses the current frame center plus the four corner offsets, scaled by the pin's position inside the video rectangle. Treat it as an approximation tied to the frame geometry, not a surveyed coordinate.

Press **Marker** again to hide the panel; the pin remains where you left it.

### Multiplexer

Use **Mux** (`Ctrl+M`) when you have a clean video and a separate telemetry log.

1. Click **Mux** in the video dock.
2. Select the **video** (`.mp4` / `.avi`).
3. Select the **log** (`.log`).
4. Select the **output directory**.
5. Click **Start**.

FFmpeg maps both inputs and writes `<output>/output.ts` using stream copy. The name is fixed, and the command has no `-y` flag: if `output.ts` already exists, FFmpeg prompts before overwriting. Remove the old file first if the run appears to hang. Reopen the result and press **FMV** to verify the telemetry survived.

If the mux fails, check that `ffmpeg/ffmpeg` resolves relative to the working directory and that the log is a valid KLV-bearing data file.

---

## Map workspace

**View → Map** (`F1`) opens a QML map backed by Qt Location's OpenStreetMap plugin.

### Symbology

| Element | Meaning |
|---------|---------|
| Drone icon | Sensor/platform position, rotated by heading |
| Blue trail | Every platform position received since playback started |
| Blue translucent polygon | Sensor footprint derived from the four corner offsets |
| Thin blue lines | Sensor beams from platform to each corner |
| Red line | Frame-center line |
| Pin markers | Imported geotagged images |

### Map types

Use the combo box on the map to switch between **Street, Cycle, Transit, Night Transit, Terrain, and Hiking** layers. Tiles are fetched from OpenStreetMap, so the first load needs connectivity. Qt may cache tiles on disk, but there is no packaged offline map.

### Image pins

Imported JPGs with EXIF GPS appear as pins. Hover for a tooltip; click to open that image in the annotation editor. Images without GPS are rejected with a warning dialog and are not pinned.

### Limits

- Every **View → Map** action adds another map dock; there is no single global map.
- Panning/zooming is handled by the QML map's own gestures and the on-screen `+` / `−` buttons.
- The map is loaded from compiled Qt resources (`qrc:///map`), not a local QML file.

---

## Imagery and reports

### Import images

| Action | Shortcut | Behavior |
|--------|----------|----------|
| **File → Import → Image → File(s)** | `Ctrl+Alt+F` | Multi-select JPGs |
| **File → Import → Image → Folder** | — | Reads every file in the chosen folder |

For each image SigTrack reads EXIF, converts DMS latitude/longitude to decimal degrees (respecting N/S/E/W), stores the image path, and adds a marker to the current map. A map dock is created if none exists.

Keep folders clean: the folder importer iterates every entry and expects images.

### Annotation editor

Clicking a map pin opens the image in a graphics view and reveals the **Editing Tools** panel.

#### View controls

| Button | Purpose |
|--------|---------|
| Extent | Fit the whole image |
| Zoom In / Zoom Out | 10% steps, clamped |
| Zoom Selection | Drag a rubber band to zoom that area |
| Pan | Hand-drag the image |
| Mouse wheel | Zoom under the cursor |

#### Drawing

| Tool | Behavior |
|------|----------|
| Rectangle | Drag to draw |
| Circle | Drag to draw an ellipse |
| Line | Drag from start to end |
| Freehand | Drag a stroked path |
| Text | Places an editable text item |
| Watermark | Load a PNG/JPG/BMP overlay |

Every committed item is pushed onto an undo stack. **Undo** (`Ctrl+Z`) and **Redo** (`Ctrl+Y`) work from the editing panel toolbar.

#### Stroke and fill

- **Stroke**: checkbox, width 1–10, palette or custom color.
- **Fill**: checkbox, palette or custom color, opacity 0–255.
- Style combo boxes exist but are hidden in this build.

#### Watermark

1. Click the watermark tool and choose an image.
2. Drag the body to move it.
3. Drag the **bottom-right** handle to scale.
4. Drag the **top-right** handle to rotate.

Watermark opacity follows the fill opacity slider.

#### Save the edited view

**File → Save** (`Ctrl+S`) grabs the current image view — including annotations and watermark — and asks where to write a PNG/JPG/XPM/BMP. This saves a flattened snapshot; the original file is untouched.

### PDF report

1. Open and annotate an image.
2. Click **Generate PDF Report** in the editing panel.
3. Click **Select Path** and choose the `.pdf` destination.
4. Fill in **Author**, **Report Title**, and **Report Content**.
5. Click **Save as PDF**.
6. When prompted, choose where to write the snapshot image (`.png`, `.bmp`, or `.xpm`). JPEG is rejected.
7. The PDF is written to the path from step 3.

The report includes the SigTrack logo, title, author, snapshot, body text, and page numbers. If you cancel the snapshot prompt, a text-only PDF is still produced.

> The snapshot prompt is a quirk of the current report writer: it requires an image file on disk before embedding it.

---

## Mesh workspace

The mesh workspace talks to a **Meshtastic** radio over USB serial and presents the network as a map, a chat, and a peer table.

### Requirements

- A Meshtastic radio connected by USB and visible to the OS.
- The radio's channel configured consistently across nodes.
- The `meshtastic` Python package (already pinned in `requirements.txt`).
- Network access if you want map tiles and weather.

### Open it

**View → Chat** opens the mesh window inside a dock. The Meshtastic serial interface connects immediately and reads the node database once. If no radio is present, node lists are empty and the map has no pins.

The window has a vertical toolbar:

| Button | Panel |
|--------|-------|
| Message | Chat |
| Symbols | NATO icon browser |
| Peers | Node table |
| Weather | Current conditions |
| Toggle | Show/hide the right-hand dock |

Clicking a panel button **sets** the dock's content; click **Toggle** to reveal or hide it.

### Map

Leaflet-based, with four base layers (Google satellite, terrain, hybrid, OSM), node pins labeled with short names, and Leaflet.draw tools for lines, polygons, rectangles, circles, and markers. No drawn feature is persisted.

### Chat

- Choose a node with the radio buttons, or tick **Broadcast** to address everyone.
- Type and press **Enter** or click **Send**.
- The list shows broadcasts, direct messages, and received packets.
- Received text is subscribed from `meshtastic.receive`.

The node list is built when the workspace opens. If a radio was connected later, reopen **View → Chat**.

### Peers

The peer table is intended to show name, hardware model, MAC address, last heard, SNR, and battery level, read from `interface.nodes`. The table declares six columns but writes seven values, so headers and data do not line up in the current build.

### NATO symbols

The symbol browser provides 16 tabs — friend, hostile, neutral, and unknown, each across air, land, equipment, and subsurface. Clicking an icon only records the selection; placement on the map is not implemented yet.

### Weather

The weather panel requests current conditions for a fixed city (**Accra**) using the demo API key embedded in the source. Replace the key and city in [`sigtrack/models/chat/modules/weather.py`](sigtrack/models/chat/modules/weather.py) before relying on it. Refresh with the button at the bottom; a failed request is printed to stdout and leaves the labels unchanged.

### Chat data

Opening the workspace creates or opens `loraChat2.db` in the working directory and defines `nodes`, `sent_messages`, and `received_messages` tables. Several insert helpers still reference an unset connection, so history may not persist reliably.

---

## Themes

**View → Settings → App Theme** opens the `qt-material` theme picker. Themes are applied immediately and written to `settings.json`.

The picker expects this file to already exist in the working directory:

```json
{
  "preferences": {
    "theme": "Light Blue"
  }
}
```

If `settings.json` is missing, create it with the content above before opening the picker. **Reset** returns the app to the default stylesheet.

---

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `F1` | Open map dock |
| `F2` | Open image dock |
| `F3` | Open video dock |
| `Ctrl+Shift+F` | Import video file(s) |
| `Ctrl+Alt+F` | Import image file(s) |
| `Ctrl+S` | Save the focused image view |
| `Ctrl+Z` / `Ctrl+Y` | Undo / redo in the image editor |
| `Space` | Play / pause video |
| `Esc` | Stop video; in the image view it exits fullscreen or closes the window |
| `Ctrl+F` | Load FMV telemetry |
| `Ctrl+I` | Show/hide video marker panel |
| `Ctrl+M` | Open multiplexer |
| `F11` | Toggle fullscreen from the image view |

The main-window **Edit → Zoom** shortcuts (`+`, `-`, `Shift+P`) are wired to placeholder handlers; use the editing panel.

---

## Files and paths

| File / folder | Written by | Purpose |
|---------------|------------|---------|
| `license.key` | You | Keygen license key |
| `settings.json` | Theme picker | Saved theme |
| `loraChat2.db` | Chat model | SQLite message/node tables |
| `ffmpeg/` | You | `ffmpeg.exe` and `ffprobe.exe` |
| `output.ts` | Multiplexer | Muxed video + telemetry |
| `*.pdf` | Report writer | Generated reports |
| `sigtrack/resources/compiled/` | Qt resource compiler | Compiled icons/QML |

All relative paths resolve from the **working directory**, not from the script location. Launch SigTrack from the folder that contains `license.key` and `ffmpeg/`.

---

## Troubleshooting

| Symptom | Likely cause | What to try |
|---------|--------------|-------------|
| App exits immediately | Missing `license.key` | Add the key file; check the console for `license validation failed` |
| `license validation failed` | Key expired, wrong account, or machine already bound | Reissue the key; activation is machine-bound |
| Video dock opens but stays black | Qt media backend cannot decode the codec | Convert to H.264/AAC MP4; install the platform media service |
| **FMV** does nothing | No data stream in the file | `ffprobe -show_streams clip.ts`; the file must carry KLV |
| Map does not move | Map dock opened after playback started, or indexing incomplete | Open **View → Map**, press **FMV**, then play from the start |
| `Error interpreting klv data` | Unrecognized KLV key | Confirm ST 0601 (or ST 0102 / EG 0104) metadata |
| Map is blank | No network / OSM plugin issue | Check connectivity; restart the map dock |
| Image import shows no pin | No EXIF GPS | Geotag the image; only JPGs with GPS become pins |
| PDF save fails | Snapshot path used `.jpg` | Choose `.png`, `.bmp`, or `.xpm` |
| Mux fails | Wrong FFmpeg path or invalid log | Verify `ffmpeg/ffmpeg`; test the log separately |
| Chat has no nodes | Radio not connected or node DB empty | Reconnect USB, reopen **View → Chat**, check serial permissions |
| Theme picker crashes | Missing `settings.json` | Create the JSON file shown above |
| Map type combo empty | OSM plugin did not initialize | Check Qt Location plugin installation; restart |

### Logs

SigTrack configures stdlib logging at `DEBUG` in `main_window.py` and prints FFmpeg/KLV diagnostics to the console. Run from a terminal so you can see them:

```bash
python main_window.py
```

---

## Getting help

Open an issue at [github.com/Serkhani/SigTrack/issues](https://github.com/Serkhani/SigTrack/issues) with:

- what you were doing and what you expected,
- the exact error text from the console,
- `ffprobe` stream summary for video/KLV problems,
- OS, Python version, and Qt/PySide2 version.

For architecture and code-level details, see [ARCHITECTURE.md](ARCHITECTURE.md). For development setup, see [CONTRIBUTING.md](CONTRIBUTING.md).
