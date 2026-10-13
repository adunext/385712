# Local setup and first export

Follow README steps 1 and 2 first. Inspect the downloaded .motion, verify its SHA256 against downloads/SHA256SUMS, and extract it to a new folder. .motion is a standard ZIP; on Windows you may copy it with a .zip extension and use Extract All. Keep the original download.

Run these commands **inside the extracted template folder**:

```sh
npm ci
uv run adapter.py plan --input examples/text-only.json --out ../kinetic-run/first-plan.json
uv run adapter.py prepare --input examples/text-only.json --out ../kinetic-run/first-instance
uv run adapter.py preview --instance ../kinetic-run/first-instance --out ../kinetic-run/first-preview.png --time 2
```

Inspect ../kinetic-run/first-preview.png, then:

```sh
uv run adapter.py render --instance ../kinetic-run/first-instance --out ../kinetic-run/first-silent.mp4
```

The final video is **../kinetic-run/first-silent-with-audio.mp4** (8 seconds; native SFX, no presenter/narration/music). This is an optional, explicitly chosen environment check. For actual production, replace the example with your own new user.json according to guide.json, params.schema.json and core/catalog.json. Use a new output name/directory for each revision.

Node is locked to playwright-core@1.64.0 via package-lock.json. Python 3.11+ needs numpy, scipy, soundfile, pyloudnorm and jsonschema; uv reads these declarations from adapter.py. Python versions are not pinned. Chrome/Chromium/Edge and FFmpeg/ffprobe must be available locally. Set CHROME to an existing browser executable if automatic discovery fails; alternatively, after npm ci, explicitly install Chromium with `npx playwright-core install chromium`.

Text-only groups: B1 keyword/explanation (8s), B2 1–5 neutral points (10s), B3 two perspectives/conclusion (10s), B4 summary/action (8s). Each supports a bounded 0–12s reading hold. Choose scenes from meaning, then bind required text/media; no original demo fallback exists. Supply full-duration local narration/music tracks or explicitly choose none. Real measured subtitle units are needed for word highlighting.

The package has no API client or Key. Platform services require a full edition from https://motiongit.com when available. macOS is tested; Linux/Windows native execution and portrait are pending. Public Chinese font is Noto Sans SC under OFL; preview your actual text before a full render.
