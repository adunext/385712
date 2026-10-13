<p align="center"><img src="assets/hero.svg" alt="MotionGit · 酷炫科技风" width="100%"></p>

# 酷炫科技风

银色金属字、琥珀光、焊花和机械动效，适合口播、教程、技术观点与作品讲解。**开源版 · 免注册 · 免登录。** [English](README.md) · [格式说明](https://motiongit.com/spec)

**安装依赖 → 下载 `.motion` → 开始制作。**

## 1 · 准备制作工具

让助手先检查已有环境，只安装缺少的工具；首次配置完成后可以复用。

| 工具 | 用途 |
| --- | --- |
| [Node.js 22+](https://nodejs.org/en/download) | 浏览器渲染依赖 |
| [Python 3.11+](https://www.python.org/downloads/) 与 [uv](https://docs.astral.sh/uv/getting-started/installation/) | 内容规划、校验、音频混合 |
| [FFmpeg 与 ffprobe](https://ffmpeg.org/download.html) | 素材处理、MP4 导出 |
| [Chrome](https://www.google.com/chrome/) / Chromium / Edge | 本地 HTML/Canvas 渲染 |

检查 `node --version`、`python3 --version`、`uv --version`、`ffmpeg -version`、`ffprobe -version`。Windows 的 Python 命令可能是 `python`。首次安装依赖需要联网；视频制作使用本地文件。

## 2 · 直接下载模板

### [↓ 下载中文 .motion](https://github.com/motiontemplates/385712/raw/refs/heads/main/downloads/kinetic-tech-0.2.4-open-beta-zh.motion)

[英文 .motion](downloads/kinetic-tech-0.2.4-open-beta-en.motion) · [SHA256 校验](downloads/SHA256SUMS) · [可编辑源码](template/)

把下载的文件或本地路径交给助手。在新目录解压这个 ZIP，读取 `00-START-HERE.md`；无需另装制作 Skill，也不需要 MotionGit 登录或激活。在解压后的目录运行 `npm ci` 安装已锁定的 Node 依赖；包内 Python 入口声明了 uv 所需依赖。

## 3 · 用你的内容制作

先提供**主题或口播文案**。人物照片/视频、旁白、SRT 字幕、录屏、作品素材与授权配乐按需要提供，也可以选择纯文字动效。助手会根据内容选择镜头，只列出这些镜头真正需要的素材。

流程是：整理你的输入 → 审阅计划 → 查看预览 → 导出 MP4。内置原生动作音效；配音与配乐使用你的本地文件，或明确选择不使用。

> 把这段话发给 Codex、豆包等助手：
>
> https://github.com/motiontemplates/385712
>
> 引导我用这个模板制作视频。先检查并安装缺少的依赖，再帮我直接从 GitHub 下载 .motion，读取包内真实指南，用我的主题和素材制作，先给我看计划和预览再导出。我不需要注册或登录 MotionGit。

[给助手的指引](ASSISTANT.zh-CN.md) · [本地命令与环境验证](QUICKSTART.md)

## 看看风格

[![中文 Demo 精选片段](assets/preview.gif)](assets/demo.mp4)

[▶ 播放中文 Demo 精选片段](https://motiontemplates.github.io/385712/zh.html#demo) · [下载 MP4](assets/demo.mp4?raw=true)。演示人物与声音是效果示例，不作为用户素材打入模板包。

![金属字、构图和机械细节](assets/compositions.jpg)

## .motion 是什么？

一个文件包含可编辑代码、制作指南、参数合同、依赖声明和可分发资产。本开源版是普通 ZIP，支持 **1920 × 1080 · 60fps · 横屏**，含 23 个原生单元与四组灵活表达。[阅读 .motion 格式协议](https://motiongit.com/spec)。

## 需要 MotionGit 完整配套功能？

本开源版**没有 Key、个人标识，也没有 API 调用能力**。需要素材匹配、素材生成、配音等平台服务时，请到 [MotionGit](https://motiongit.com) 下载开放后的完整版；开放状态与服务条款以官网为准。

当前为公开测试版：已实测 macOS；竖屏及 Windows/Linux 实机仍待验证。公开包的中文字体改用 Noto Sans SC，字形和排版可能与展示视频略有差别。代码采用 [MIT](LICENSE)，字体和品牌资产见[独立许可](template/licenses/THIRD-PARTY-NOTICES.md)。
