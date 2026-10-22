# Public source edition / 公开源码版 · 0.2.30-open-beta

This is the no-Key ordinary source package, synchronized from official release **626 / 722**. Run the extracted source directly with `python3 -B kinetic_bootstrap.py`; this archive does not include `assistant/motion.mjs`, personal identity, API credentials or signed personal updates. First read PUBLIC-SOURCE.md, motion.json, guide.json (English: guide.en.json), and STARTUP.md. Runtime code, native media, fonts, dependencies and timing contracts match the released author source; only public documentation, guide entry and integrity metadata are adapted.

本包是免登录、无 Key 的普通公开源码包，同步官网 **626 / 722** 的修复。解压到新目录后使用 `python3 -B kinetic_bootstrap.py` 正常制作；不需要个人包。官网个人下载与 API/增量更新请使用 https://motiongit.com/@adunext/385712，本包不包含这些身份。先读 PUBLIC-SOURCE.md 与实际参数合同，不把旧版本说明或演示当作本期内容。保留原包、工程与原始字幕时间。

## Start / 开始

Use the existing environment. Run from the extracted package root with real absolute input/output paths:

```sh
python3 -B kinetic_bootstrap.py doctor
python3 -B kinetic_bootstrap.py capabilities
python3 -B kinetic_bootstrap.py check-params --input /absolute/work/user.json
python3 -B kinetic_bootstrap.py plan --input /absolute/work/user.json --out /absolute/work/plan.json
python3 -B kinetic_bootstrap.py prepare --input /absolute/work/user.json --out /absolute/work/project
python3 -B kinetic_bootstrap.py preview --instance /absolute/work/project --time 2 --out /absolute/work/preview.png
python3 -B kinetic_bootstrap.py render --instance /absolute/work/project --out /absolute/work/silent.mp4
```

If doctor reports missing declared dependencies, run `python3 -B kinetic_bootstrap.py setup` once and rerun doctor. It uses the external isolated dependency cache and Python 3.13; it does not install packages into system Python. Existing compatible Chrome, Node and FFmpeg are reused. Setup may download the declared runtime dependencies or an automation browser, never creative media. The final sound result is `silent-with-audio.mp4`; the plain `silent.mp4` is not the final audio delivery. Use fresh output paths.

`capabilities.inputSchemaContent` is the complete schema; `inputSchema` is a relative path. Its inherited `next.readSchemaCommand` / `next.readBasicCommand` arrays describe the official personal reader, which is not included in this public archive; read the named root files directly instead. 公共源码不要执行这些 personal helper 阅读示例，直接读对应根文件。 Read params.schema.json, BASIC.md and MEDIA.md directly from the extracted root. New narration with checked captions should use the declared `compose` route in NARRATED-STORY.md before plan. Preserve complete speech and actual whole-cue timings; sentence SRT does not authorize invented word timings. The examples are environment tests, not a substitute for a user's content.

先检查现有环境，只补 doctor 明确缺少的依赖。依赖进入系统外部缓存，不在模板或系统 Python 安装。用户已有内容时直接承接；纯文字可用 B1–B4，无指定人物或配音时保持 none。本版默认竖屏口播把原先右下的人物移到画面中部（1080×1920 画布的中心坐标 540,1040），保留原生尺寸与裁切，字幕向上移动。

Default portrait narration moves the bottom-right presenter to the middle (centre 540,1040), preserving its native size and crop while lifting the captions.

显式 captionPosition 和人物位置优先；过长字幕应按实际容量提示，不截断内容或伪造时轴。

## Languages and layouts / 语言与画幅

- Chinese: declared landscape 1920×1080 and portrait 1080×1920, 60fps, native units and B1–B4.
- English: declared landscape native units and B1–B4; portrait supports B1–B4 only.
- 中文默认说明：guide.json；English guide: guide.en.json. Both archives contain the same bilingual runtime.
- Full extraction coverage and Windows native visual acceptance are not claimed. Actual source-specific limitations remain in motion.json and the guides.

## Official personal edition / 官网个人版

For connected asset/API services and verified personal updates, obtain your own personal package from https://motiongit.com/@adunext/385712 and follow its bundled verified assistant. This public source package has no Key, does not authenticate as a personal package, and is not a signed incremental update. Never copy credentials between packages or commit a personal package. Older named GitHub downloads remain available as history; the unversioned aliases point to this release.

Upstream author archive SHA256: `c502364502cc8560fef05683d1c69c919db3f90771962946ecca9bb1c2aa3d25`.
The public ZIP has a separate checksum because public entry documentation and integrity metadata are adapted. Executable source, assets, fonts, dependency locks, parameters and timing/layout behavior are unchanged from that upstream author archive. MIT and third-party notices are retained byte-for-byte in licenses/.
