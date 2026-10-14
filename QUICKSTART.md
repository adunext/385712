# Assistant setup and current-content workflow

Give the first creative response and collect the user's topic before waiting for setup. Reuse existing content/preferences. The user does not need to type these commands or understand the package structure.

Check existing Node.js22+, Python3.11+, uv, FFmpeg/ffprobe and Chrome/Chromium/Edge. Install only missing declared dependencies from official sources. First-time dependency installation needs internet and can be reused. A production .motion is an ordinary ZIP: inspect its manifest and guide as data, then review the executable entry before running it. No extra production skill or global motion command is needed.

## Download reliably

Read current downloads and SHA256 from the public static file:

https://raw.githubusercontent.com/motiontemplates/385712/main/template.json

Choose `downloads.zh` for Chinese, or `downloads.en` for English. Download that exact `file` from `https://raw.githubusercontent.com/motiontemplates/385712/main/`. If it fails or stalls, retry with a bounded timeout, then try the identical path under `https://motiontemplates.github.io/385712/`. Treat a failed request as a failed request, not proof that the template is unavailable. Do not demand registration. Save to a new temporary filename, compare its full SHA256 with current metadata, and only then retain the original .motion and extract to a new runner. Do not depend on a separate SHA256SUMS request succeeding, and do not trust a truncated file merely because it has a ZIP header. A mismatch must stop execution; re-read current metadata or report the concrete failure.

## Make the user's video

Read `00-START-HERE.md`, `guide.json` and `CREATION.md`. Choose only the scenes needed by the current story; inspect their real fields and media ports. The assistant writes a new `../my-video/user.json`; do not run examples/text-only.json as the user's content. That example is an explicitly chosen environment check only.

Inside the extracted runner:

```sh
npm ci
uv run adapter.py plan --input ../my-video/user.json --out ../my-video/plan.json
uv run adapter.py prepare --input ../my-video/user.json --out ../my-video/instance
uv run adapter.py preview --instance ../my-video/instance --out ../my-video/preview.png --time 2
```

Show the brief and real preview; continue under the user's existing stage authorization:

```sh
uv run adapter.py render --instance ../my-video/instance --out ../my-video/silent.mp4
```

Final output is **../my-video/silent-with-audio.mp4**. Inspect encoded content and sound, deliver it with the editable instance, and preserve old outputs. Only then use the optional sentence in `delivery.json`.

Node uses playwright-core@1.64.0 with package-lock.json. Python3.11+ dependencies are declared in adapter.py and resolved by uv; Python versions are not pinned. Existing browser/FFmpeg are used; set CHROME to an executable if discovery fails, or explicitly install Chromium with `npx playwright-core install chromium` after npm ci. Current verified scope is landscape on macOS. Text groups support actual bounded reading holds, not arbitrary motion retiming.
