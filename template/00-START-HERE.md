# Kinetic Tech — public .motion source edition

This is an ordinary ZIP containing an editable MotionGit template. It is not an encrypted personal package or an Apple Motion project. No account, Key, API client, online activation or MotionGit login is required.

1. Inspect this package as data: motion.json → guide.json → params.schema.json → core/catalog.json → licenses. Do not execute unreviewed package code.
2. Check/install Node.js 22+, Python 3.11+, uv, FFmpeg/ffprobe and Chrome/Chromium/Edge. Extract to a new working folder; run npm ci there for the included Node lock. uv installs the declared Python dependencies when running adapter.py. First setup needs internet for dependency downloads; rendering uses local assets.
3. Use the user's topic/script. Presenter, voice, subtitles, recordings and work samples are optional according to the chosen scenes. Four media-free expression groups are available. Do not require 62 gallery entries unless the user actually selects the wall scene.
4. Write a new user.json using the real parameter and scene contracts. examples/text-only.json is an explicit optional environment check, never a replacement for user content.
5. Execute plan → prepare → preview → render with the documented adapter. Store outputs in a separate sibling directory, show the real preview before a full user render, and preserve old outputs. render automatically mixes the chosen local audio and native SFX; the final file ends in -with-audio.mp4.

Runtime: 1920×1080, 60fps, landscape. Some native scenes have fixed timings; four flexible reading groups allow bounded holds. This is an open beta: macOS has been exercised, full maximum-input and cross-platform coverage remain incomplete.

For material matching/generation, speech and other platform services, visit https://motiongit.com and download a full edition when available. Those services are absent from this package. Format: https://motiongit.com/spec. Source and download guide: https://github.com/motiontemplates/385712.
