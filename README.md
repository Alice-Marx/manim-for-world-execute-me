# manim for world-execute-me

> **English (short):** A 3Blue1Brown-style lyric music video built with [Manim Community](https://www.manim.community/) Edition for mili’s *world.execute(me);*. Dual visual grammar — chalkboard math + runtime/terminal visualization — timed to an LRC lyric track. **Song audio is not included**; you must supply your own licensed copy to mux.

用 [Manim CE](https://www.manim.community/) 做的 *world.execute(me);*（mili / Project Moon）歌词 MV：一条线是数学板书，一条线是程序运行可视化，按 LRC 逐句对齐。仓库只含代码与时间轴，**不含商业音源**。

| | |
|---|---|
| 仓库名 | `Alice-Marx/manim-for-world-execute-me` |
| 引擎 | Manim Community **0.22** |
| 分辨率默认 | 1080p60（`-qh`） |
| 歌曲时长（LRC） | 约 3:32（`DURATION = 212`） |
| 成片时长（参考 mp3） | 约 3:37（含约 5.16s 前置静音） |
| 代码许可 | MIT（见 `LICENSE`） |
| 音频 | **不收录、不传播** — 请自备合法授权音轨 |

---

## 这是什么

本工程把整首歌做成**一条连续 Scene**（`WorldExecuteMe`），视频时间 = `AUDIO_OFFSET + 歌曲时间（LRC）`。每一拍用 `self.at(song_seconds)` 对齐真实帧时钟，底部字幕按 LRC 精确换行。

**双语法（Dual grammar）**

1. **Board（数学板书）** — 点集维数、圆周长 \(C=2\pi r\)、切线、极限与约束、代数心形曲线 \((x^2+y^2-1)^3-x^2y^3=0\) 等，风格接近 3Blue1Brown。
2. **Runtime（运行时 / 终端）** — 初始化、栈与日志、`while True` 循环计数、`Illegal arguments` 红色报错扩散、`execute() → None` 关机收尾。

配色见 `palette.py`：`ME` 橙 = 我 / AI，`YOU` 米色 = 你，**错误红 `ERR` 只从「Illegal arguments」起才语义启用**。

---

## 环境要求

- **Python** 3.10+（开发时用过 3.13）
- **Manim Community 0.22**（见 `requirements.txt`）
- **ffmpeg**（混音与成片封装）
- 系统依赖（随发行版略有不同）：
  - Cairo / Pango（Manim 文字与矢量）
  - **可选 LaTeX**（`latex` + `dvisvgm`）：有则用 `MathTex`，没有则自动退回 Unicode 衬线字

Debian / Ubuntu 示例：

```bash
sudo apt update
sudo apt install -y python3 python3-venv ffmpeg \
  libcairo2-dev libpango1.0-dev pkg-config \
  texlive-latex-base texlive-latex-extra dvisvgm   # 可选，板书更清晰
```

---

## 安装

```bash
git clone https://github.com/Alice-Marx/manim-for-world-execute-me.git
cd manim-for-world-execute-me

python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -r requirements.txt
```

---

## 音频（必须自备）

本仓库**故意不包含**歌曲 mp3。音源为商业作品（mili），请勿把未授权音频提交进本仓库或二次分发。

1. 取得合法授权副本后，放到：

   ```text
   audio/world-execute-me.mp3
   ```

   或渲染时指定：

   ```bash
   AUDIO=/绝对或相对路径/song.mp3 ./build.sh
   ```

2. **时间对齐（重要）**  
   参考轨开头有约 **5.19s 数字静音**，第一声人声大致落在静音结束后。LRC 第一句在 `0.03s`，因此代码里：

   ```python
   AUDIO_OFFSET = 5.16   # cues.py
   ```

   含义：**歌曲时间 0 ≈ 音频时间 5.16s**。成片前 5.16s 是标题卡，之后才进入歌词。若你的音轨没有这段前置静音，需要改 `AUDIO_OFFSET`（通常改为 `0`）并重新渲染。

3. 无音频时，`build.sh` 仍会输出静音成片到 `out/`。

---

## 构建

```bash
# 默认 1080p60，输出到 ./out/
./build.sh

# 预览质量（快）
./build.sh -ql    # 480p15
./build.sh -qm    # 720p30
./build.sh -qh    # 1080p60（默认）
./build.sh -qk    # 2160p60

# 自备音轨混音
AUDIO=./audio/world-execute-me.mp3 ./build.sh -qh
```

等价的直接调用：

```bash
.venv/bin/manim -qh --disable_caching --media_dir media \
  scenes/world_execute_me.py WorldExecuteMe
```

产物：

| 文件 | 说明 |
|------|------|
| `out/world-execute-me-manim-silent.mp4` | 仅画面 |
| `out/world-execute-me-manim.mp4` | 有音轨则混音；否则与 silent 相同 |
| `media/` | Manim 缓存（已 gitignore，可删） |

完整 1080p60 渲染通常需要较长时间与足够磁盘；可先用 `-ql` 验证时间轴。

---

## 工程结构

```text
.
├── README.md                 # 本说明
├── LICENSE                   # MIT（代码）
├── requirements.txt          # manim==0.22.0
├── build.sh                  # 渲染 + 可选混音 → ./out/
├── world-execute-me.lrc      # 歌词时间权威（勿与 JSON 冲突时以 LRC 为准）
├── cues.py                   # 解析后的 LINES / KEYS / AUDIO_OFFSET
├── palette.py                # 颜色与字体常量
├── scenes/
│   └── world_execute_me.py   # 唯一 Scene：WorldExecuteMe
├── glyphs/                   # 可选静态素材（默认用几何图元）
├── audio/                    # 本地音轨目录（*.mp3 已忽略）
├── docs/
│   └── PROMPT.md             # 设计提示词备份
├── out/                      # 成片输出（gitignore）
└── media/                    # Manim 渲染缓存（gitignore）
```

**文件职责简述**

- `cues.py` — 96 条 LRC 起点、关键事件字典 `KEYS`、`AUDIO_OFFSET` / `AUDIO_DURATION`。
- `palette.py` — `BG / ME / YOU / ERR / GREY / …` 与字体名。
- `scenes/world_execute_me.py` — 字幕带 `Subtitles`、`at` / `p` 节拍工具，以及按段落拆开的方法（`intro` → `shutdown`）。
- `build.sh` — 质量档位、拷贝静音片、ffmpeg 混音；路径相对仓库根目录，克隆后即可用。

---

## 段落与时间线（歌曲时间，秒）

| 段落 | 方法 | 大致区间 | 画面要点 |
|------|------|----------|----------|
| 前置静音 / 标题 | `intro` | 音频 0–5.16（歌曲前） | 标题卡 `world.execute(me);` |
| Boot | `boot` | 0.03–~16 | 上电、保护、对象创建、初始化、开仿真 |
| 几何课 | `geometry` | 29.28–~44 | 点集维数、圆周、正弦切线、∞ 与 limitations |
| 电流 / 眩晕 | `current` | 44–~58 | AC/DC、dizzy、AD/BC |
| 副歌 1 | `chorus1` | 58.65–~73 | simulations → satisfaction → 第一次 execution 终端 |
| 物件 | `glyphs`（+ eggplant/tomato/cat） | 73.53–~88 | 茄子 / 番茄 / 虎斑猫 / God·existence（几何简化） |
| 切换 | `switches` | 88.34–~103 | F/M、AM→PM、S/M、trance 螺旋 |
| 振动 / 离开 | `alone` | 102.93–~130 | vibrations、completion、「you have left」日志、isolation、fragments、disheartened |
| 报错 | `error` | 130.74–~147 | **Illegal arguments** — 首次启用错误红并扩散 |
| 处决循环 | `execution_loop` | 147.48–~162 | `while True` ×12、Ein…Liu 卡片 |
| 副歌 2 | `chorus2` | 162.23–~177 | execution / trapped |
| 爱 | `love` | 176.96–~193 | \(f:\mathrm{you}\to\mathrm{me}\)、心形曲线、lo-o-ove |
| 收尾 | `shutdown` | 193.46–end | are you still there? → `shutdown` → `execute() → None` → 黑屏 |

关键时间戳也集中在 `cues.KEYS`（如 `ILLEGAL_ARGUMENTS = 130.74`、`FINAL_EXECUTION = 205.56`）。

---

## 配色约定

| 符号 | 色值 | 用途 |
|------|------|------|
| `ME` | `#FF8C42` | 我 / AI / 关键词强调 |
| `YOU` | `#F2E8D5` | 你 / 正文 / 板书默认 |
| `ERR` | `#F5506F` | **仅自 Illegal arguments（130.74s）起**作错误语义 |
| `GREY` | `#5A6270` | 离线、缺席、关机 |
| `BG` | `#0E1116` | 背景 |

番茄等物件用独立暖色（`TOMATO`），刻意与 `ERR` 区分，避免「还没报错就一片红」。

---

## 许可与版权声明

- **本仓库源代码与文档**：MIT License（`LICENSE`）。
- **歌曲 *world.execute(me);***：版权归 mili / 相关权利方（与 Project Moon 作品关联）。**本仓库不提供、不托管、不分发音频文件。** 个人学习渲染可以，公开发布成片请自行解决音源授权。
- 画面灵感来自 [3Blue1Brown](https://www.3blue1brown.com/) 与 [Manim Community](https://www.manim.community/)；Manim CE 本身亦为 MIT。

---

## 致谢

- **mili** — *world.execute(me);*
- **Project Moon** — 相关世界观语境
- **Grant Sanderson / 3Blue1Brown** — 数学可视化语言
- **Manim Community Developers** — Manim CE 0.22

---

## 常见问题

**Q: 克隆后 `./build.sh` 报找不到 manim？**  
先按「安装」一节建好 `.venv` 并 `pip install -r requirements.txt`。

**Q: 画面和歌声错位？**  
检查你的 mp3 是否有约 5s 前置静音；没有则把 `cues.py` 里 `AUDIO_OFFSET` 改为 `0` 后重渲。

**Q: 没有 LaTeX 能渲吗？**  
可以。场景会检测 `latex`/`dvisvgm`，缺失时用 Unicode 衬线字代替 `MathTex`。

**Q: 为什么仓库里没有 mp4？**  
成片体积大且依赖音源；请本地渲染。`media/` 与 `out/` 均已忽略。

**Q: `glyphs/` 是空的？**  
当前版本用 Manim 几何图元画物件；该目录留给可选 SVG 等素材。

---

## 设计提示词

更细的镜头与语法说明见 [`docs/PROMPT.md`](docs/PROMPT.md)（从制作时的提示词整理，时间轴以本仓库 LRC / `cues.py` 为准）。
