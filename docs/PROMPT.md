# world.execute(me); · Manim / 3Blue1Brown 风格 MV 提示词（丰富版 v2）

> 目标：用 Manim Community（3b1b 同系）做一支歌词 MV。  
> 兼容：**纯数学课板书** 与 **程序运行时可视化** 必须同片并存。  
> 叙事继承你的 v4：一场 AI↔用户对话；橙＝me，米白＝you，错误红＝err。  
> 歌词：按 `lyrics.json` 行号取词，源码里不整段粘贴歌词。时间单位＝歌曲时间（音频 0 点）。

参考：https://github.com/3b1b/manim · 你的 v4 `PROMPT_v4.md` / `PLAN.md` · 歌词 JSON

---

## A0. 权威时间轴（用户提供 LRC）

- 文件：`world-execute-me.lrc`（已随提示词目录保存）
- 曲目：mili · world.execute(me); · length 03:32
- **所有关键词镜头时间以本 LRC 为准**；此前 JSON 行级时间仅作参考，冲突时改 LRC。
- LRC 为行起点；镜头可持续到下一行起点。空行表示休止/留白。

关键行起点（mm:ss.xx → 秒）：

| 秒 | 歌词行（提示用，实现取自 LRC） |
| --- | --- |
| 0.03 | Switch on the power line |
| 1.33 | Remember to put on protection |
| 5.16 | … object creation |
| 9.75 | Initialization |
| 12.47 | … the simulation |
| 29.28 | If I'm a set of point |
| 30.89 | … dimension |
| 34.54 | … circumference |
| 38.27 | … tangents |
| 41.92 | … limitations |
| 58.65–74 | if I can / simulations / satisfaction / execution / simulation |
| 73.53 | eggplant… |
| 77.16 | tomato… |
| 80.93 | tabby cat… |
| 102.89–115.60 | you have left × / isolation |
| 123.55 | disheartened |
| 130.74 | Illegal arguments |
| 147.48–161.31 | Execution 循环 + Ein…liu |
| 178.79–190.24 | lo-o-ove 段 |
| 205.56 | 尾声 Execution |

---

## A. 一句话

把歌曲做成「可讲解的程序诗」：概念句在黑板上被证明，执行句在运行时里崩溃又循环；具象名词长成几何符号画；颜色只在状态变化时改变。

---

## B. 双语法兼容（硬性）

| 语法 | 何时用 | Manim 手段 | 禁止 |
| --- | --- | --- | --- |
| **Math Board** | 定义、维度、极限、映射、爱/理解的抽象 | `MathTex`/`Tex`、`NumberPlane`、向量、箭头、`TransformMatchingTex`、圆与切线 | 不要用聊天气泡当主体 |
| **Runtime Viz** | 初始化、执行、非法参数、隔离、循环 EXECUTION | `Code`、指令指针、栈帧、AST 树、终端 `MarkupText` 滚动、计数器 | 不要只配卡拉 OK 字幕 |
| **Glyph Plate** | 茄子/番茄/猫/太阳等具象词 | 几何拼贴或等宽字符矩阵，一眼能认；可专色 | 不许退回成纯文字 |

**同段切换**：在拍/半拍上，Board ↔ Runtime ↔ Glyph 可互换，只要叙事不断。  
**同镜叠加**：允许「左侧板书公式 + 右侧迷你终端」分屏，但主焦点只能有一个。

---

## C. 视觉宪法

### C1 画布
- 分辨率：1920×1080（预览），可升 4K。
- 背景：近黑蓝灰 + 极淡网格（`NumberPlane` opacity≤0.15）。
- 每镜三层：底 / 主体 / 前景（指针、字幕带、节拍点）。

### C2 调色（语义）
- `me` 橙 ≈ `#FF8C42`（AI 的字与高亮）
- `you` 米白 ≈ `#F2E8D5`（指针、用户输入痕迹）
- `err` 玫红 ≈ `#F5506F`（**约 130.74s（Illegal arguments）首次作为错误语义出现**）
- 灰＝缺席/离线；专色茄紫 / 暖番茄红仅用于对应 Glyph，且番茄须与 `err` 可区分。

### C3 字体分工
- 衬线 / Tex：AI 说的概念  
- 无衬线：界面说明、用户侧  
- 等宽：代码、日志、错误码  

### C4 歌词上屏
- 非关键词：底部固定字幕带（字号稳定），唱整句期间可读。  
- 全大写关键词：画面中心大字，不在字幕带重复。  
- 切点优先落在拍点；关键词起止参考下方时间表（行级，可再吸附 onset）。

---

## D. 关键词时间表（重点镜头必须对准；秒数已按 LRC 校正）

| 约时间 (s) | 关键词 / 事件 | 建议语法 | 画面一句 |
| --- | --- | --- | --- |
| 1.33–3.58 | protection | Board | 保护层合上 |
| 5.16–7.19 | object creation | Runtime+Board | `new` 构造几何体 |
| 9.75–10.90 | Initialization | Runtime | 字段点亮 |
| 12.47–16.04 | simulation | Board | 仿真轨迹 |
| 30.89–33.01 | dimension | Board | 维度展开 |
| 34.54–36.77 | circumference | Board | 圆周 |
| 38.27–40.36 | tangents | Board | 切线 |
| 41.92–44.04 | limitations | Board | 边界 |
| 47.27–50.95 | blind / dizzy | Board | 视觉噪声→眩晕 |
| 60.57–66.17 | simulations→satisfaction | Board+Runtime | 仿真簇→满足峰值 |
| 67.99–71.20 | execution | Runtime | 第一次执行高亮 |
| 73.53–87.x | eggplant/tomato/cat/god | Glyph | 具象符号画 |
| 102.89–115.60 | left / isolation | Runtime | 离线、隔离箱 |
| 119.81–123.55 | fragments→disheartened | Runtime+Glyph | 碎片；**首次**眼 |
| 130.74–134.38 | Illegal arguments | Runtime | `err` 首次语义扩散 |
| 147.48–161.31 | Execution×N + Ein…liu | Runtime | 循环核与计数 |
| 178.79–190.24 | lo-o-ove | Board | 代数之爱 |
| 205.56–206.30 | Execution | Runtime | 关机前空执行 |


## E. 分段导演说明（丰富）

### E0 片头（可选 0 前 2–5s）
黑底上极简警告：数学符号与 `world.execute(me);` 等宽淡入；无剧情。

### E1 Boot（LRC 0.03–16.04s）
- **问题**：如何安全上电并构造对象。  
- **Board**：电源图、保护层不等式。  
- **Runtime**：boot log 三行；`INITIALIZATION` 时成员变量从灰变橙。  
- **出点**：第一句对话感建立（指针点一下「运行」）。

### E2 早段概念（LRC 29.28–58.65s）
- DIMENSION / CIRCUMFERENCE / TANGENTS / LIMITATIONS：**必须是漂亮的 3b1b 几何课**。  
- 每个词 1 个主定理式画面，Transform 衔接，不要跳剪。

### E3 副歌一（LRC 58.65–73.53s）
- STIMULATIONS→SATISFACTION：信号进入目标函数。  
- EXECUTION：右侧弹出迷你 Runtime，左侧公式不停。  
- 颜色略 `warm`。

### E4 主歌二具象（LRC 73.53–88.93s）
- NUTRIENTS / ANTIOXIDANTS：Glyph（茄/茄紫、番茄专色），打开看「内部结构」第二态。  
- ENJOYMENT / EXISTENCE：回到 Board 收束。

### E5 设定切换→Alone（LRC 88.34–125.33s）
- 用户侧米白减少；网格变冷。  
- VIBRATIONS / COMPLETION / ISOLATION / FRAGMENTS：Runtime 权重上升。  
- DISHEARTENED：眼形 Glyph **第一次**出现，板书退到边缘。

### E6 Error（LRC 125.33–147.48s；Illegal≈130.74）
- ILLEGAL ARGUMENTS：堆栈展开，`err` 从一行染到边框。  
- 番茄专色若仍在，不得与 `err` 同帧抢语义。

### E7 EXECUTION 核（LRC 147.48–162.23s）
- **几乎纯 Runtime**：代码清单 + 当前行脉动；十二次 EXECUTION 用循环计数器。  
- EIN DOS TROIS NE FEM LIU：六张计数卡片，等宽，卡点闪入。  
- 允许极简 Board 只显示 `while True:` 的数学等价（无穷箭头），不得回到聊天 UI。

### E8 LOVE 与尾声（LRC 176.96–206.30s）
- LO-O-OVE：把「爱」画成映射 \(f:\text{you}\rightarrow\text{me}\) 或拓扑心动点，避免表情包心。  
- 最后：消息发出、已读回执为空、去饱和、`dead` 黑场。  
- 205s EXECUTION：空执行一声，关机。

---

## F. Manim 工程约定

```
wem_manim/
  cues.py          # 全部时间码
  palette.py       # 颜色与状态机
  scenes/
    boot.py
    geometry_lesson.py
    chorus1.py
    verse2_glyphs.py
    alone_error.py
    execution_loop.py
    love_shutdown.py
  glyphs/          # 茄番茄猫太阳几何定义
  media/           # 渲染输出
```

- 音画合成可用 ffmpeg 后制；Manim 场景用 `next_section` 或显式 `wait` 对齐 `cues.py`。  
- 性能测试：单段先 480p；关键词镜单独 `--save_last_frame` 检查「无字可辨认」。  
- 禁止：未授权素材、扭曲五官、无意义粒子烟花、整屏歌词墙。

---

## G. 质检清单（每段渲染后勾）

1. 能否一句话说清本段「在证明/执行什么」？  
2. 关键词起止是否在 ±0.15s 内？  
3. Board 与 Runtime 是否都出现过（若该段两者都适用）？  
4. `err` 是否遵守首次出现时间？  
5. 具象 Glyph 静帧能否被叫出名字？  
6. 字幕带是否挡主体？  
7. 颜色是否仍可读：橙/米白/灰/红分离？

---

## H. 与 v4 聊天窗方案的关系

- **保留**：对话叙事、颜色状态机、具象词图形、错误红纪律、EXECUTION 纯代码感、拍点。  
- **替换**：聊天 UI 主舞台 → Manim 板书 + Runtime；纸感版画 → 几何 Glyph + 轻纹理网格。  
- **可选**：极简「消息条」可作为前景 HUD，但宽度≤屏宽 30%，不得成为主构图。

---

## I. 下一步建议

1. 冻结本提示词为导演简报。  
2. 生成 `cues.py`（从歌词 JSON 导出关键词表）。  
3. 先做样片：**Boot（0–16s）+ DIMENSION 几何课（32–45s）** 两段，确认双语法手感。  
4. 再铺 EXECUTION 循环核。

---

## J. 给执行者的语气

像 3Blue1Brown 备课：每个镜头先写「观众应理解的一句话」，再选动画。宁可少镜、镜镜干净，也不要堆特效。数学与代码是同一故事的两种方言，不要互相打架。
