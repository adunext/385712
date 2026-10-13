<p align="center"><img src="assets/hero.svg" alt="MotionGit · Kinetic Tech" width="100%"></p>

# Kinetic Tech

Silver metal typography, amber light, sparks and mechanical motion for talking videos, tutorials and technical stories. **Open source · no account · no login.** [中文](README.zh-CN.md) · [Format](https://motiongit.com/spec)

**Install dependencies → download the `.motion` → make your video.**

## 1 · Prepare your tools

Ask your assistant to check existing tools first. Install only what is missing; environment setup is reusable.

| Tool | Used for |
| --- | --- |
| [Node.js 22+](https://nodejs.org/en/download) | Locked browser-rendering dependency |
| [Python 3.11+](https://www.python.org/downloads/) + [uv](https://docs.astral.sh/uv/getting-started/installation/) | Planning, input validation and audio mixing |
| [FFmpeg + ffprobe](https://ffmpeg.org/download.html) | Media preparation and MP4 export |
| [Chrome](https://www.google.com/chrome/) / Chromium / Edge | Local HTML/Canvas rendering |

Check `node --version`, `python3 --version`, `uv --version`, `ffmpeg -version` and `ffprobe -version`. On Windows, your Python command may be `python`. First-time dependency downloads need internet; video production uses local files.

## 2 · Download the template

### [↓ Download English .motion](https://github.com/motiontemplates/385712/raw/refs/heads/main/downloads/kinetic-tech-0.2.4-open-beta-en.motion)

[Chinese .motion](downloads/kinetic-tech-0.2.4-open-beta-zh.motion) · [SHA256 checksums](downloads/SHA256SUMS) · [Editable source](template/)

Save the file, then give it (or its local path) to your assistant. It is a self-contained ZIP; extract it into a **new** folder and read `00-START-HERE.md`. No additional production skill or MotionGit activation is needed. In that extracted folder, run `npm ci` to install the locked Node dependency. The included Python entry declares its dependencies for uv.

## 3 · Make your video

Start with your **topic or script**. Add a presenter photo/video, recorded narration, SRT subtitles, screen recording, work samples or licensed music if your story needs them. Text-only animation is supported. Your assistant selects suitable scenes and explains only the materials those scenes need.

It prepares your own input → shows a plan → generates a preview → exports MP4. Native sound effects are included; narration and music use your local files or an explicit “none” choice.

> Send this to Codex, Doubao or another assistant:
>
> https://github.com/motiontemplates/385712
>
> Guide me to make a video with this template. First check/install dependencies, then help me download the .motion directly from GitHub. Read its real guide, use my topic and materials, and show a plan and preview before export. I do not need to register or log in to MotionGit.

[Assistant instructions](ASSISTANT.md) · [Local commands and environment check](QUICKSTART.md)

## See the style

[![Chinese showcase highlights](assets/preview.gif)](assets/demo.mp4)

[▶ Watch the Chinese demo highlights](https://motiontemplates.github.io/385712/#demo) · [Download MP4](assets/demo.mp4?raw=true). The showcase contains example presenter and audio; those are not bundled as user inputs.

![Typography, composition and mechanical details](assets/compositions.jpg)

## What is a .motion?

A MotionGit `.motion` joins the template's editable code, guide, parameter contract, dependencies and permitted assets in one package. This public source edition is an ordinary ZIP. It supports **1920 × 1080 · 60fps · landscape**, 23 native units and four flexible expression groups. [Read the format specification](https://motiongit.com/spec).

## Want the full MotionGit workflow?

This open-source edition contains **no Key, personal identity or API capability**. For asset matching, generation, voiceover and other platform services, [visit MotionGit](https://motiongit.com) and download the full edition when available. Check its live availability and service terms there.

Open beta: macOS tested; portrait and Windows/Linux execution are pending. Noto Sans SC replaces the internal Chinese font in this public edition, so Chinese lettering can differ from the showcase. Code: [MIT](LICENSE); fonts and brand assets: [separate notices](template/licenses/THIRD-PARTY-NOTICES.md).
