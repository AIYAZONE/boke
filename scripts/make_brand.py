# -*- coding: utf-8 -*-
"""生成 boke · 播客收录 品牌套件：矢量 logo、favicon、节目封面、规范文档、预览页。

设计原则：站点品牌固定（boke · 播客收录），单个节目用「编号 + 主色」区分，
后续收录多个播客时只需换 No. 与主色，版式不动。
"""
import os
import base64
import cairosvg

# 输出到仓库根目录下的 brand/，不依赖沙箱绝对路径
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "brand")
os.makedirs(OUT, exist_ok=True)

FONT = "'Noto Sans CJK SC','PingFang SC','Microsoft YaHei',sans-serif"
INK = "#22201e"
ACCENT = "#e2602c"
PAPER = "#fffdfa"
CREAM = "#f7f5f1"


def icon_svg(bg=INK, fg=PAPER, bars=None, size=512):
    """方形主标：深色圆角底 + 声波柱 + 播放点。"""
    bars = bars or [("#e2602c", 1.0), ("#f0a273", .85), ("#e2602c", 1.0),
                    ("#f0a273", .85), ("#e2602c", 1.0)]
    # 5 根声波柱，高度对称起伏
    heights = [96, 168, 232, 168, 96]
    xs = [132, 208, 284, 360, 436]
    rects = []
    for (color, op), h, x in zip(bars, heights, xs):
        y = 256 - h / 2
        rects.append(
            f'<rect x="{x}" y="{y:.0f}" width="52" height="{h}" rx="26" '
            f'fill="{color}" fill-opacity="{op}"/>')
    bar_html = "\n  ".join(rects)
    # 播放三角（右侧圆点内）
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512" role="img" aria-label="boke 播客收录 logo">
  <rect width="512" height="512" rx="112" fill="{bg}"/>
  <rect x="16" y="16" width="480" height="480" rx="96" fill="none" stroke="{fg}" stroke-opacity=".10" stroke-width="2"/>
  <g>
  {bar_html}
  </g>
  <circle cx="256" cy="256" r="0" fill="none"/>
</svg>'''


def icon_mark_svg(fg=ACCENT, size=512):
    """纯声波标记（无底），用于浅色背景 / 页面内嵌。"""
    heights = [96, 168, 232, 168, 96]
    xs = [132, 208, 284, 360, 436]
    rects = []
    for h, x, c in zip(heights, xs, [ACCENT, "#f0a273", ACCENT, "#f0a273", ACCENT]):
        y = 256 - h / 2
        rects.append(f'<rect x="{x}" y="{y:.0f}" width="52" height="{h}" rx="26" fill="{c}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512" role="img" aria-label="boke 声波标记">
  {''.join(rects)}
</svg>'''


def wordmark_svg(dark_bg=True, width=1000, height=280):
    """横版字标：声波标记 + boke + 中文副标。"""
    fg = PAPER if dark_bg else INK
    sub = "#c9bdb1" if dark_bg else "#77716a"
    mark = icon_mark_svg(ACCENT, 1)  # 不用其尺寸，取内部图形
    # 直接内嵌缩放后的声波图形
    heights = [96, 168, 232, 168, 96]
    xs = [132, 208, 284, 360, 436]
    rects = []
    for h, x, c in zip(heights, xs, [ACCENT, "#f0a273", ACCENT, "#f0a273", ACCENT]):
        y = 256 - h / 2
        rects.append(f'<rect x="{x}" y="{y:.0f}" width="52" height="{h}" rx="26" fill="{c}"/>')
    mark_inner = "".join(rects)
    bg = f'<rect width="{width}" height="{height}" rx="28" fill="{INK}"/>' if dark_bg else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="boke 播客收录">
  {bg}
  <g transform="translate(48,28) scale(0.42)">{mark_inner}</g>
  <text x="292" y="140" font-family={'"' + FONT + '"'} font-size="86" font-weight="800" fill="{fg}" letter-spacing="-2">boke</text>
  <text x="296" y="196" font-family={'"' + FONT + '"'} font-size="34" font-weight="600" fill="{sub}" letter-spacing="6">播 客 收 录</text>
  <text x="296" y="236" font-family={'"' + FONT + '"'} font-size="19" fill="{sub}" letter-spacing="2" opacity=".8">听点值得留下来的 · boke.aiyazone.com</text>
</svg>'''


def cover_svg(no="01", title="二十讲", subtitle="YC 斯坦福创业课 · 精华与播客",
              accent=ACCENT, bg1="#262320", bg2="#5a3a25", tag="YC CS183B · 2014",
              meta="20 讲 · 6 集播客 · 约 30 分钟"):
    """1:1 节目封面：站点品牌 + 节目编号 + 主色。后续节目只改这几个参数。"""
    heights = [70, 122, 168, 122, 70]
    xs = [1060, 1120, 1180, 1240, 1300]
    wm = []
    for h, x in zip(heights, xs):
        y = 300 - h / 2
        wm.append(f'<rect x="{x}" y="{y:.0f}" width="34" height="{h}" rx="17" fill="{accent}" opacity=".16"/>')
    wm_html = "".join(wm)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1400" viewBox="0 0 1400 1400" role="img" aria-label="{title} 播客封面">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/>
    </linearGradient>
  </defs>
  <rect width="1400" height="1400" fill="url(#bg)"/>
  <rect x="56" y="56" width="1288" height="1288" rx="40" fill="none" stroke="{PAPER}" stroke-opacity=".12" stroke-width="2"/>
  <!-- 站点品牌行 -->
  <g transform="translate(112,120) scale(0.16)">
    {' '.join(f'<rect x="{x}" y="{256-h/2:.0f}" width="52" height="{h}" rx="26" fill="{accent}"/>' for x,h in zip([132,208,284,360,436],[96,168,232,168,96]))}
  </g>
  <text x="208" y="163" font-family={'"' + FONT + '"'} font-size="30" font-weight="700" fill="{PAPER}" letter-spacing="1">boke</text>
  <text x="208" y="199" font-family={'"' + FONT + '"'} font-size="19" fill="#d9d1c7" letter-spacing="4">播 客 收 录</text>
  <rect x="1090" y="120" width="200" height="62" rx="31" fill="{accent}"/>
  <text x="1190" y="161" font-family={'"' + FONT + '"'} font-size="26" font-weight="700" fill="{PAPER}" text-anchor="middle">No.{no}</text>
  <!-- 主标题 -->
  <text x="112" y="590" font-family={'"' + FONT + '"'} font-size="34" font-weight="600" fill="{accent}" letter-spacing="4">{tag}</text>
  <text x="104" y="800" font-family={'"' + FONT + '"'} font-size="230" font-weight="800" fill="{PAPER}" letter-spacing="-8">{title}</text>
  <rect x="112" y="858" width="120" height="8" rx="4" fill="{accent}"/>
  <text x="112" y="948" font-family={'"' + FONT + '"'} font-size="44" font-weight="500" fill="#e7ddd2">{subtitle}</text>
  <!-- 右下声波水印 -->
  <g transform="translate(0,940)">{wm_html}</g>
  <!-- 底部信息 -->
  <line x1="112" y1="1230" x2="1288" y2="1230" stroke="{PAPER}" stroke-opacity=".18" stroke-width="2"/>
  <text x="112" y="1290" font-family={'"' + FONT + '"'} font-size="27" fill="#c9bdb1" letter-spacing="2">{meta}</text>
  <text x="1288" y="1290" font-family={'"' + FONT + '"'} font-size="27" fill="#c9bdb1" text-anchor="end" letter-spacing="2">boke.aiyazone.com</text>
</svg>'''


def png(svg_str, name, w, h):
    cairosvg.svg2png(bytestring=svg_str.encode("utf-8"),
                     write_to=os.path.join(OUT, name), output_width=w, output_height=h)


def save(svg_str, name):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg_str)


# --- 主标 ---
save(icon_svg(), "boke-icon.svg")
save(icon_svg(bg=PAPER, fg=INK, bars=[(ACCENT, 1), ("#e2602c", .6)] * 2 + [(ACCENT, 1)]),
     "boke-icon-light.svg")
save(icon_mark_svg(), "boke-mark.svg")
save(wordmark_svg(True), "boke-wordmark-dark.svg")
save(wordmark_svg(False), "boke-wordmark-light.svg")

png(icon_svg(), "boke-icon-512.png", 512, 512)
png(icon_svg(), "boke-icon-1024.png", 1024, 1024)
png(wordmark_svg(True), "boke-wordmark-dark.png", 1000, 280)
png(wordmark_svg(False), "boke-wordmark-light.png", 1000, 280)

# --- favicon（含透明底简版）---
fav_svg = icon_svg(size=64)
save(fav_svg, "favicon.svg")
png(fav_svg, "favicon-64.png", 64, 64)
png(fav_svg, "favicon-32.png", 32, 32)
png(fav_svg, "apple-touch-icon.png", 180, 180)
# data URI 供页面内嵌（避免中文路径/跨域问题）
fav_b64 = base64.b64encode(fav_svg.encode("utf-8")).decode()
with open(os.path.join(OUT, "_favicon_datauri.txt"), "w") as f:
    f.write("data:image/svg+xml;base64," + fav_b64)

# --- 节目封面 No.01《二十讲》---
c1 = cover_svg()
save(c1, "cover-01-二十讲.svg")
png(c1, "cover-01-二十讲.png", 1400, 1400)
# 后续节目示例：换编号与主色（蓝绿），证明可延展
c2 = cover_svg(no="02", title="示例节目", subtitle="换编号与主色即可 · 版式不变",
               accent="#4b9d8a", bg1="#1f2b2a", bg2="#2f4a45", tag="PODCAST · 2026",
               meta="第 2 档 · 版式沿用")
save(c2, "cover-02-示例.svg")
png(c2, "cover-02-示例.png", 1400, 1400)

# --- 品牌规范 ---
guide = """# boke · 播客收录 ｜ 品牌与延展规范

> 站点：`boke.aiyazone.com`。目前只收录《二十讲》一档，后续会做成多播客归集站。
> 所以 logo 分两层：**站点品牌固定不动**，**每档节目用「编号 + 主色」区分**。

## 一、两层结构

| 层 | 内容 | 是否常变 |
|---|---|---|
| 站点品牌 | 声波标记 + `boke` + 「播客收录」 | 不变 |
| 节目标识 | `No.01`、节目名、节目主色 | 每新增一档改一次 |

声波标记的含义：五根高低起伏的柱子，既是音频波形，也像一排书脊——
对应「把多个播客收在一处」。不做耳机、麦克风，是为了避免绑死某一种节目类型。

## 二、配色

| 用途 | 色值 |
|---|---|
| 主色 / 强调 | `#e2602c` 橙 |
| 主色辅助 | `#f0a273` 浅橙 |
| 深色底 | `#22201e`，渐变到 `#5a3a25` |
| 纸白 | `#fffdfa` |
| 米色底 | `#f7f5f1` |
| 次级文字 | `#77716a` |

节目主色只用于封面编号胶囊、标题上的小标签、进度条，**不要改动站点主色**。
No.02 示例用了 `#4b9d8a`，可见换色后仍属同一套版式。

## 三、文件清单

| 文件 | 用途 |
|---|---|
| `boke-icon.svg` / `.png` | 方形主标，头像、App 图标、分享缩略图 |
| `boke-icon-light.svg` | 浅底版（浅色背景上用） |
| `boke-mark.svg` | 纯声波标记，无底，可叠在任意背景 |
| `boke-wordmark-dark.svg` / `.png` | 横版字标（深色底） |
| `boke-wordmark-light.svg` / `.png` | 横版字标（浅色底） |
| `favicon.svg` / `favicon-32.png` / `apple-touch-icon.png` | 站点图标 |
| `cover-01-二十讲.svg` / `.png` | 当前节目封面，1400×1400（播客平台通用） |
| `cover-02-示例.svg` / `.png` | 换色换号示例 |

全部为矢量 SVG，放大不糊；PNG 只是导出副本。改字、改色直接编辑 SVG 即可。

## 四、新增一档节目怎么做

1. 复制 `cover-01-二十讲.svg`，改四个参数：`no`、`title`、`subtitle`、`accent`（外加 `tag`、`meta` 两行小字）。
2. 编号按顺序递增，主色挑一个与已用色区分度够的。
3. 封面导出 1400×1400 PNG，命名 `cover-XX-节目名.png`。
4. 站点首页用同一张卡片版式：封面缩略图 + 节目名 + 编号 + 一句话简介 + 集数。

生成脚本：`make_brand.py`（在仓库 `scripts/` 或本地工作区），改参数后重跑即可批量出图。

## 五、尺寸与留白

- 方形主标内边距约 10%，不要贴边；最小使用尺寸 24px，再小只保留三根柱。
- 横版字标最小宽度 180px。
- 封面安全边距 56px（见 SVG 里的描边内框），文字不要越过。
- 深色底上用 `boke-wordmark-dark`，浅色底用 `boke-wordmark-light`，不要反着用。

## 六、页面内怎么用

`index.html` 的 `<head>` 已内嵌 favicon（data URI，不依赖外部文件），
页头用 `boke-mark.svg` 作前缀。若部署到静态托管，把整个 `brand/` 目录一起传上去即可。
"""
with open(os.path.join(OUT, "品牌与延展规范.md"), "w") as f:
    f.write(guide)

# --- 预览页 ---
cards = "".join(
    f'<div class="c"><img src="{n}" alt="{t}"><div class="lb">{t}<br><span>{n}</span></div></div>'
    for n, t in [
        ("boke-icon-512.png", "方形主标"),
        ("boke-icon-light.svg", "浅底主标"),
        ("boke-wordmark-dark.png", "横版字标 · 深底"),
        ("boke-wordmark-light.png", "横版字标 · 浅底"),
        ("cover-01-二十讲.png", "节目封面 No.01"),
        ("cover-02-示例.png", "节目封面 No.02 · 换色示例"),
    ])
preview = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>boke · 播客收录 ｜ 品牌套件</title>
<style>
body{{margin:0;background:#f7f5f1;color:#22201e;font-family:{FONT};padding:48px 24px 80px}}
.wrap{{max-width:1080px;margin:0 auto}}
h1{{font-size:38px;margin:0 0 8px}} .sub{{color:#77716a;font-size:15px;margin-bottom:36px}}
.g{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}}
.c{{background:#fffdfa;border:1px solid #e8e2d9;border-radius:16px;overflow:hidden}}
.c img{{display:block;width:100%;height:260px;object-fit:contain;background:#efeae2;padding:18px;box-sizing:border-box}}
.lb{{padding:14px 18px;font-size:14px;font-weight:600;border-top:1px solid #eee7dd}}
.lb span{{font-weight:400;color:#77716a;font-size:12px}}
.note{{margin-top:32px;background:#fdf0e9;border-left:4px solid #e2602c;border-radius:10px;padding:16px 20px;font-size:14px;line-height:1.8}}
</style></head><body><div class="wrap">
<h1>boke · 播客收录</h1>
<div class="sub">站点品牌固定，节目用「编号 + 主色」区分。下面是全套素材预览。</div>
<div class="g">{cards}</div>
<div class="note"><b>延展方式</b>：新增一档播客时复制 <code>cover-01-二十讲.svg</code>，
改 <code>no / title / subtitle / accent</code> 四个参数即可，版式不动。详见《品牌与延展规范.md》。</div>
</div></body></html>'''
with open(os.path.join(OUT, "预览.html"), "w") as f:
    f.write(preview)

print("brand files:")
for n in sorted(os.listdir(OUT)):
    print(" ", n, os.path.getsize(os.path.join(OUT, n)), "bytes")
