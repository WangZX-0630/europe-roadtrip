# 欧洲自驾游旅行网页 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `欧洲自驾游行程计划.xlsx` 的全部内容转化为一个苹果风、单文件、可离线打开的旅行展示网页 `index.html`。

**Architecture:** 单个自包含 HTML 文件，所有内容为静态语义化 HTML（无 JS 模板渲染，保证无 JS 也能看）；CSS 内联于 `<style>`；JS 仅做增强（导航、滚动动画、SVG 描线动画、Leaflet 地图）。内容直接转录自 Excel，脚本 `tools/check_page.py` 做结构化校验。

**Tech Stack:** 原生 HTML/CSS/JS（无构建步骤）· Leaflet 1.9.4（unpkg CDN）+ OpenStreetMap 瓦片 · 系统字体栈 · Wikimedia Commons 图片（`Special:FilePath`）。

## Global Constraints

- 交付物只有一个文件 `index.html`（项目根目录），外加校验脚本 `tools/check_page.py`
- 必须能通过 `file://` 协议直接双击打开；禁止 `fetch()` 本地文件、禁止需要服务器的功能
- 文案全中文；苹果风浅色：背景 `#f5f5f7`、文字 `#1d1d1f`、苹果蓝 `#0071e3`（hover `#0077ed`）
- 字体栈：`-apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif`，不引入网络字体
- 所有外部资源（图片、Leaflet、OSM 瓦片）失败时必须优雅降级：图片 `onerror` 换渐变占位、地图加载失败隐藏板块、SVG 路线图永不依赖网络
- 内容数据逐条转录自 `_excel_dump.txt`（项目根目录，UTF-8）：69 条时段记录、9 段驾驶、7 项预算、7 项预订、8 条贴士、5 国风情、7 天行程——零遗漏、零篡改（Excel 里没有的日期/价格不编造）
- 7 个行程板块须有 `data-day="1"…"7"` 属性；板块 id 清单（导航锚点）：`hero` `route` `map` `itinerary` `culture` `budget` `bookings` `tips`（footer 无 id）
- 时刻表用原生 `<details>`/`<summary>` 实现折叠，不用 JS
- 响应式：375px 无横向滚动；画廊网格在 `<768px` 单列
- 每完成一个任务：运行 `python tools/check_page.py`（必须全 PASS）+ 浏览器人工目检该任务板块

---

### Task 1: 项目初始化 — git 仓库、骨架、校验脚本

**Files:**
- Create: `index.html`（骨架：doctype、head、style 占位、9 个空板块容器 + 导航 + footer）
- Create: `tools/check_page.py`
- Create: `.gitignore`

**Interfaces:**
- Consumes: 无
- Produces: 以下 id/class 约定全项目通用——板块 id：`hero` `route` `map` `itinerary` `culture` `budget` `bookings` `tips`；行程卡：`<section class="day" data-day="N">`；景点卡：`<article class="spot">`；美食卡：`<article class="meal">`；时刻表行：`<li class="tl">`；导航链接 `class="nav-link"`；图片统一 `class="photo"`（带 `onerror` 降级）

- [ ] **Step 1: 初始化 git 仓库并写 .gitignore**

```bash
cd "C:\Users\wangz\project\EuropeTourPlan"
git init
```

`.gitignore` 内容：

```gitignore
_excel_dump.txt
__pycache__/
*.pyc
```

- [ ] **Step 2: 创建 `index.html` 骨架**

用 Write 创建 `index.html`，结构如下（占位部分后续任务填充，但导航、板块容器、footer 结构现在定死）：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>欧洲自驾 · 七日五国 — 2026.9.30-10.6</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="..." crossorigin="">
<style>
/* Task 2 填充完整设计系统 */
</style>
</head>
<body>
<nav id="topnav">…毛玻璃导航，锚点：路线 #route / 行程 #itinerary / 风情 #culture / 预算 #budget / 预订 #bookings / 贴士 #tips…</nav>
<main>
  <section id="hero"></section>
  <section id="route"></section>
  <section id="map"></section>
  <section id="itinerary"></section>
  <section id="culture"></section>
  <section id="budget"></section>
  <section id="bookings"></section>
  <section id="tips"></section>
</main>
<footer>…返程信息：10/6 22:00 CDG→北京 ✈️，时差 -7h，预计 10/7 中午抵达…</footer>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script>/* 后续任务填充增强脚本 */</script>
</body>
</html>
```

导航 HTML 具体结构（Task 2 里写完整样式）：

```html
<nav id="topnav">
  <div class="nav-inner">
    <a class="brand" href="#hero">欧洲自驾 · 七日五国</a>
    <div class="nav-links">
      <a class="nav-link" href="#route">路线</a>
      <a class="nav-link" href="#itinerary">行程</a>
      <a class="nav-link" href="#culture">风情</a>
      <a class="nav-link" href="#budget">预算</a>
      <a class="nav-link" href="#bookings">预订</a>
      <a class="nav-link" href="#tips">贴士</a>
    </div>
  </div>
</nav>
```

注意：Leaflet 的 CSS/JS 链接要带 `integrity` 与 `crossorigin` 属性和官方 SRI 值——具体值在 Task 5 用 `curl https://unpkg.com/leaflet@1.9.4/dist/leaflet.css | grep -o 'sha256-[^"]*'` 获取；**本任务先用不带 integrity 的裸链接占位，Task 5 时补上**。

- [ ] **Step 3: 创建校验脚本 `tools/check_page.py`**

```python
#!/usr/bin/env python3
"""校验 index.html 结构完整性与数据完整性。用法: python tools/check_page.py"""
import re, sys, urllib.request

html = open('index.html', encoding='utf-8').read()
errors = []

def must(label, cond):
    print(('PASS  ' if cond else 'FAIL  ') + label)
    if not cond:
        errors.append(label)

# 1. 板块结构
for sid in ['hero', 'route', 'map', 'itinerary', 'culture', 'budget', 'bookings', 'tips']:
    must(f'<section id="{sid}">', f'<section id="{sid}">' in html)
must('<footer>', '<footer>' in html)

# 2. 导航锚点可解析
for m in re.finditer(r'href="#([\w-]+)"', html):
    aid = m.group(1)
    if aid != 'hero':
        must(f'导航锚点 #{aid} 有目标', f'id="{aid}"' in html)

# 3. 行程数据完整性
must('7 个行程板块', len(re.findall(r'class="day" data-day="\d"', html)) == 7)
tl = re.findall(r'<li class="tl">', html)
must(f'69 条时刻表记录 (实际 {len(tl)})', len(tl) == 69)
spots = re.findall(r'<article class="spot">', html)
must(f'景点卡数量 ({len(spots)} 张)', len(spots) >= 28)
meals = re.findall(r'<article class="meal">', html)
must(f'美食卡数量 ({len(meals)} 张)', len(meals) >= 13)
drives = re.findall(r'<tr class="drive">', html)
must(f'9 段驾驶数据 (实际 {len(drives)})', len(drives) == 9)
must('SVG 路线图存在', '<svg' in html)
must('Leaflet 引入', 'unpkg.com/leaflet' in html)

# 4. 模板残留检查（JS 渲染或占位符泄漏）
for bad in ['{{', 'TODO', 'TBD', 'undefined']:
    must(f'无模板残留 "{bad}"', bad not in html)

# 5. 图片 URL 有效性（离线时跳过，仅警告）
imgs = re.findall(r'src="(https://commons\.wikimedia\.org[^"]+)"', html)
if imgs:
    for url in imgs:
        try:
            req = urllib.request.Request(url, method='HEAD')
            code = urllib.request.urlopen(req, timeout=8).status
            must(f'图片可达 ({code}) {url.split("/")[-1][:40]}', code == 200)
        except Exception as e:
            must(f'图片检查跳过/失败 {url.split("/")[-1][:40]} ({type(e).__name__})', False)

print()
if errors:
    print(f'共 {len(errors)} 项失败'); sys.exit(1)
print('全部通过 ✓')
```

注意：步骤 5 的图片检查在离线环境会全 FAIL——**这不是代码问题**；验收时若离线，以警告处理、人工确认图片 URL 格式正确即可。

- [ ] **Step 4: 运行校验脚本（此刻应只有部分 FAIL，因为板块还是空的）**

Run: `python tools/check_page.py`
Expected: 板块检查失败（空骨架属正常），无 Python 报错

- [ ] **Step 5: 提交**

```bash
git add .gitignore index.html tools/check_page.py
git commit -m "chore: 项目骨架 + 校验脚本"
```

---

### Task 2: 设计系统 CSS + 毛玻璃导航 + Hero 封面

**Files:**
- Modify: `index.html`（填充 `<style>` 完整样式 + 导航样式 + hero 内容）

**Interfaces:**
- Consumes: Task 1 的骨架与 id 清单
- Produces: 全站可复用的 CSS 类：`.container` `.section-head` `.badge` `.card` `.photo`（onerror 降级样式 `.photo[data-failed]`）`.chip` `.btn` `.reveal`（滚动渐入）`.day` `.spot` `.meal` `.tl` `.drive` 等，后续任务全部直接套用

- [ ] **Step 1: 写完整 CSS 设计系统（`<style>` 内）**

核心令牌与组件样式（完整代码，直接写入）：

```css
:root{
  --bg:#f5f5f7; --card:#fff; --ink:#1d1d1f; --ink2:#6e6e73; --blue:#0071e3; --blue2:#0077ed;
  --line:rgba(0,0,0,.06); --radius:24px; --radius-sm:16px;
  --shadow:0 8px 30px rgba(0,0,0,.06); --shadow-lg:0 20px 60px rgba(0,0,0,.12);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:72px}
body{background:var(--bg);color:var(--ink);font:400 16px/1.6 -apple-system,BlinkMacSystemFont,"SF Pro Display","PingFang SC","Microsoft YaHei",sans-serif;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:var(--blue);text-decoration:none}
.container{max-width:1100px;margin:0 auto;padding:0 24px}
/* 毛玻璃导航 */
#topnav{position:sticky;top:0;z-index:100;background:rgba(245,245,247,.8);backdrop-filter:blur(20px) saturate(180%);-webkit-backdrop-filter:blur(20px) saturate(180%);border-bottom:1px solid var(--line)}
.nav-inner{max-width:1100px;margin:0 auto;padding:12px 24px;display:flex;align-items:center;justify-content:space-between}
.brand{font-size:17px;font-weight:600;letter-spacing:-.01em;color:var(--ink)}
.nav-links{display:flex;gap:28px}
.nav-link{font-size:14px;color:var(--ink2);transition:color .2s}
.nav-link:hover{color:var(--ink)}
/* 板块头 */
.section-head{padding:72px 0 8px;text-align:center}
.section-head .kicker{font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--blue)}
.section-head h2{font-size:clamp(28px,5vw,44px);font-weight:700;letter-spacing:-.02em;margin:8px 0}
.section-head p{color:var(--ink2);font-size:17px;max-width:640px;margin:0 auto}
/* 卡片 */
.card{background:var(--card);border-radius:var(--radius);border:1px solid var(--line);padding:28px;box-shadow:var(--shadow);transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s}
/* 图片与降级 */
.photo-wrap{position:relative;border-radius:var(--radius-sm);overflow:hidden;background:linear-gradient(135deg,#e8e8ed,#f5f5f7)}
.photo{width:100%;aspect-ratio:16/10;object-fit:cover;transition:transform .6s}
.photo-wrap:hover .photo{transform:scale(1.04)}
.photo[data-failed]{opacity:0}
.photo-fallback{position:absolute;inset:0;display:flex;align-items:flex-end;padding:16px;background:linear-gradient(160deg,#dbe7ff 0%,#f5f5f7 60%);color:#3b3b40;font-weight:600;font-size:15px;opacity:0;transition:opacity .3s}
.photo-wrap .photo[data-failed] + .photo-fallback{opacity:1}
/* 徽标与碎块 */
.badge{display:inline-block;font-size:12px;font-weight:600;letter-spacing:.04em;padding:4px 12px;border-radius:999px;background:#e8f0fe;color:var(--blue)}
.chip{display:inline-block;font-size:12px;font-weight:500;padding:3px 10px;border-radius:999px;background:#f0f0f3;color:var(--ink2);margin:2px 3px 2px 0}
/* 滚动渐入 */
.reveal{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s cubic-bezier(.2,.8,.2,1)}
.reveal.in{opacity:1;transform:none}
/* 按钮 */
.btn{display:inline-block;background:var(--blue);color:#fff;font-size:15px;font-weight:500;padding:10px 22px;border-radius:980px;transition:background .2s}
.btn:hover{background:var(--blue2)}
/* 时刻表折叠 */
details.tl-box{border:1px solid var(--line);border-radius:var(--radius-sm);background:var(--card);overflow:hidden}
details.tl-box summary{list-style:none;cursor:pointer;padding:14px 20px;font-weight:600;font-size:15px;display:flex;justify-content:space-between;align-items:center;user-select:none}
details.tl-box summary::-webkit-details-marker{display:none}
details.tl-box summary::after{content:"+";font-size:20px;color:var(--ink2);transition:transform .3s}
details.tl-box[open] summary::after{transform:rotate(45deg)}
details.tl-box .tl-list{padding:0 20px 16px}
ul.tl{list-style:none}
li.tl{display:grid;grid-template-columns:86px 64px 1fr;gap:12px;padding:12px 0;border-top:1px solid var(--line);font-size:14px;align-items:start}
li.tl .t{font-variant-numeric:tabular-nums;font-weight:600;color:var(--ink)}
li.tl .ty{font-size:12px;color:var(--blue);font-weight:600;padding-top:2px}
li.tl .det b{display:block;font-size:14.5px;margin-bottom:2px}
li.tl .det span{color:var(--ink2);font-size:13px}
/* Hero */
#hero{position:relative;min-height:92vh;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden;background:#0d0d12}
#hero .hero-bg{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.62}
#hero .hero-bg[data-failed]{display:none}
#hero .hero-bg[data-failed]~.hero-inner{color:#fff}
.hero-inner{position:relative;z-index:2;padding:0 24px}
.hero-inner .kicker{font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:#a1a1a6;font-weight:600}
.hero-inner h1{font-size:clamp(40px,8vw,76px);font-weight:700;letter-spacing:-.03em;line-height:1.05;margin:18px 0 12px;color:#fff;text-shadow:0 2px 40px rgba(0,0,0,.4)}
.hero-inner .sub{font-size:clamp(17px,2.5vw,22px);color:#d2d2d7;max-width:640px;margin:0 auto}
.hero-stats{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:44px auto 0;max-width:760px}
.hero-stats .stat{flex:1 1 120px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.18);border-radius:20px;padding:18px 10px;backdrop-filter:blur(8px)}
.hero-stats .stat b{display:block;font-size:28px;font-weight:700;color:#fff;letter-spacing:-.01em}
.hero-stats .stat span{font-size:12.5px;color:#c7c7cc}
.hero-cta{margin-top:36px;display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
/* 响应式 */
@media(max-width:768px){
  .nav-links{gap:16px}
  .nav-link{font-size:13px}
  li.tl{grid-template-columns:72px 1fr;row-gap:4px}
  li.tl .ty{grid-column:2;padding-top:0}
  #topnav .brand{font-size:15px}
}
```

注意：图片降级结构约定——每个 `.photo-wrap` 内必须同时有 `<img class="photo" onerror="this.setAttribute('data-failed','')">` 和 `<div class="photo-fallback">景点名</div>` 两个元素（fallback 初始 `opacity:0`，图片失败时显示）。Hero 背景图失败则整层隐藏、文字变白。

- [ ] **Step 2: 写 Hero 内容（`<section id="hero">`）**

```html
<section id="hero">
  <div class="hero-bg" style="background-image:url('【Task 3 验证的巴黎天际线图URL】')" onerror="this.setAttribute('data-failed','')"></div>
  <div class="hero-inner">
    <div class="kicker">Sept 30 — Oct 6 · 2026</div>
    <h1>欧洲自驾 · 七日五国</h1>
    <p class="sub">从巴黎的晨光出发，途经布鲁塞尔、阿姆斯特丹、科隆与卢森堡，<br>驰骋 1,502 公里的欧洲公路，再回到铁塔之下，告别法国。</p>
    <div class="hero-stats">
      <div class="stat"><b>7</b><span>天 6 晚</span></div>
      <div class="stat"><b>5</b><span>个国家</span></div>
      <div class="stat"><b>1,502</b><span>公里驾驶</span></div>
      <div class="stat"><b>22</b><span>小时车程</span></div>
      <div class="stat"><b>6</b><span>座城市</span></div>
    </div>
    <div class="hero-cta">
      <a class="btn" href="#route">查看路线</a>
      <a class="btn" href="#itinerary" style="background:rgba(255,255,255,.18);backdrop-filter:blur(8px)">每日行程</a>
    </div>
  </div>
</section>
```

图片 URL 是占位——Task 3 验证后回填（hero 的 URL 用 Task 3 验证列表第 1 条）。

- [ ] **Step 3: 运行校验脚本 + 浏览器目检**

Run: `python tools/check_page.py` → 除图片检查外应全 PASS（hero/route/map 等板块已就位；itinerary 计数此刻为 0 会 FAIL，属预期，**Task 6 完成后必须全 PASS**）

目检：`start index.html`（Windows 下打开默认浏览器）——导航毛玻璃、吸顶、Hero 排版与数据条、滚动渐入（给 hero 内元素加 `.reveal` 类并在 Task 8 写 JS 前先无动画显示——**本任务先不加 `.reveal` 类，Task 8 统一加**）

- [ ] **Step 4: 提交**

```bash
git add index.html
git commit -m "feat: 设计系统 + 毛玻璃导航 + Hero 封面"
```

---

### Task 3: 图片素材验证（20 张 Wikimedia 图）

**Files:**
- Create: `docs/images-verified.md`（URL 清单，后续任务引用）
- Modify: `index.html` 的 hero 背景 URL（回填验证结果）

**Interfaces:**
- Consumes: 无
- Produces: `docs/images-verified.md` —— 每张图一行：`用途 | 最终URL`；所有任务中的图片一律使用该清单中的 URL

- [ ] **Step 1: 用 curl 验证候选 URL**

候选清单（Wikimedia Commons `Special:FilePath`，`?width=1200` 压缩）：

```
铁塔:      Eiffel Tower from Champ de Mars.jpg
罗浮宫:    Louvre Museum Wikimedia Commons.jpg
凯旋门:    Arc de Triomphe Paris.jpg
蒙马特:    Sacre-coeur-montmartre.jpg
奥赛:      Musée d'Orsay, North-West view, Paris 2017.jpg
圣母院:    Notre-Dame de Paris 2013-07-01.jpg
圣礼拜堂:  Sainte-Chapelle Upper Chapel.jpg
布鲁塞尔大广场: Grand Place, Brussels.jpg
撒尿小童:  Manneken pis Brussels.jpg
风车村:    Zaanse Schans windmills.jpg
阿姆运河:  Amsterdam Canals - July 2006.jpg
水坝广场:  Dam Square Amsterdam.jpg
国家博物馆: Rijksmuseum Amsterdam.jpg
安妮之家:  Anne Frank House Amsterdam.jpg
科隆大教堂: Kölner Dom bei Nacht.jpg
霍亨索伦桥: Hohenzollern Bridge and Cologne Cathedral.jpg
卢森堡峡谷: Bock Casemates Luxembourg.jpg
凡尔赛宫:  Palace of Versailles from Gardens.jpg
塞纳河:    Seine River and Eiffel Tower at dusk.jpg
杜乐丽:    Jardin des Tuileries, Paris.jpg
```

对每个文件名执行（把文件名 URL 编码后拼接）：

```bash
curl -sIL "https://commons.wikimedia.org/wiki/Special:FilePath/<URL编码后的文件名>?width=1200" | head -1
```

Expected: `HTTP/1.1 200` 或 `302`（302 是正常的，会重定向到 upload.wikimedia.org 实际文件，最终 200 即可）

**失败处理**：某文件名 404 时，用 WebSearch 搜该景点的真实 Wikimedia 文件名（如搜 `site:commons.wikimedia.org Eiffel Tower`），取最常用的那张，重新 curl 验证直到 200。

- [ ] **Step 2: 记录结果到 `docs/images-verified.md`**

格式（示例）：

```markdown
# 已验证图片 URL（2026-08-05，全部 HEAD 200）

| 用途 | URL |
|---|---|
| Hero 巴黎天际线 | https://commons.wikimedia.org/wiki/Special:FilePath/Eiffel%20Tower%20from%20Champ%20de%20Mars.jpg?width=1600 |
| 埃菲尔铁塔 | ... |
| ... | ... |
```

- [ ] **Step 3: 回填 hero 背景图**

把 Task 2 Step 2 的占位 URL 替换为清单第 1 条（宽 `width=1600`），并目检 hero 背景显示。

- [ ] **Step 4: 提交**

```bash
git add index.html docs/images-verified.md
git commit -m "docs: 图片 URL 验证清单 + hero 背景图"
```

---

### Task 4: SVG 路线总览图

**Files:**
- Modify: `index.html`（`<section id="route">` 内放入 SVG + 图例）

**Interfaces:**
- Consumes: Task 2 的 `.card` `.section-head` `.chip` 类
- Produces: SVG 内城市节点带 `data-city` 属性；点击节点 JS（Task 8 写）滚动到对应 `#day-N`。图例文字「● 城市 · —— 自驾路线」

- [ ] **Step 1: 写 SVG 路线图**

投影公式：区域 lat 47.0–53.8、lng -1.5–8.5，映射到 `viewBox="0 0 900 560"`：

```
x = (lng + 1.5) / 10 * 900
y = (53.8 - lat) / 6.8 * 560
```

已计算坐标（四舍五入到 1 位小数）：

| 城市 | lat, lng | x, y | 日 |
|---|---|---|---|
| 巴黎 | 48.8566, 2.3522 | 346.7, 407.1 | D1/D6 |
| 布鲁塞尔 | 50.8503, 4.3517 | 526.7, 242.9 | D2 |
| 阿姆斯特丹 | 52.3676, 4.9041 | 576.4, 118.0 | D3 |
| 风车村 | 52.4740, 4.8160 | 568.4, 109.2 | D3 |
| 科隆 | 50.9375, 6.9603 | 761.4, 235.8 | D4 |
| 卢森堡市 | 49.6116, 6.1319 | 686.9, 344.9 | D4晚/D5 |
| 凡尔赛 | 48.8049, 2.1204 | 325.8, 411.4 | D5 |

SVG 完整代码（描线动画用 `stroke-dasharray`/`stroke-dashoffset` + CSS 动画；节点用 `<a href="#day-N">` 包裹实现点击跳转）：

```html
<section id="route">
  <div class="section-head">
    <div class="kicker">The Route</div>
    <h2>整体路线</h2>
    <p>一次穿越五国的环形自驾——巴黎出发，逆时针驶过比利时、荷兰、德国与卢森堡，最后回到巴黎。</p>
  </div>
  <div class="container">
    <div class="card route-card">
      <svg viewBox="0 0 900 560" role="img" aria-label="欧洲自驾路线图">
        <defs>
          <linearGradient id="routeGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stop-color="#0071e3"/><stop offset="1" stop-color="#5ac8fa"/>
          </linearGradient>
          <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#0071e3"/>
          </marker>
        </defs>
        <!-- 分段路线（顺序：巴黎→布鲁塞尔→阿姆斯特丹→风车村(支线)→阿姆斯特丹→科隆→卢森堡→凡尔赛→巴黎） -->
        <path class="route-line" d="M346.7,407.1 Q440,300 526.7,242.9" />
        <path class="route-line" d="M526.7,242.9 Q560,160 576.4,118.0" />
        <path class="route-line" d="M576.4,118.0 L568.4,109.2" marker-end="url(#arrow)"/>
        <path class="route-line sub" d="M568.4,109.2 L576.4,118.0"/>
        <path class="route-line" d="M576.4,118.0 Q680,140 761.4,235.8" />
        <path class="route-line" d="M761.4,235.8 Q730,300 686.9,344.9" />
        <path class="route-line" d="M686.9,344.9 Q520,400 325.8,411.4" />
        <path class="route-line" d="M325.8,411.4 Q330,410 346.7,407.1" />
        <!-- 距离标注 -->
        <text class="dist" x="420" y="300">312km</text>
        <text class="dist" x="600" y="160">212km</text>
        <text class="dist" x="560" y="96">15km</text>
        <text class="dist" x="690" y="175">261km</text>
        <text class="dist" x="740" y="305">203km</text>
        <text class="dist" x="480" y="420">381km</text>
        <text class="dist" x="318" y="430">23km</text>
        <!-- 城市节点 -->
        <a href="#day-1" data-city="巴黎" class="city" transform="translate(346.7,407.1)"><circle r="9" class="city-dot"/><text class="city-name" y="-16">巴黎</text></a>
        <a href="#day-2" data-city="布鲁塞尔" class="city" transform="translate(526.7,242.9)"><circle r="9" class="city-dot"/><text class="city-name" y="-16">布鲁塞尔</text></a>
        <a href="#day-3" data-city="阿姆斯特丹" class="city" transform="translate(576.4,118.0)"><circle r="9" class="city-dot"/><text class="city-name" y="-16">阿姆斯特丹</text></a>
        <a href="#day-3" data-city="风车村" class="city sub" transform="translate(568.4,109.2)"><circle r="6" class="city-dot"/><text class="city-name" y="-14">风车村</text></a>
        <a href="#day-4" data-city="科隆" class="city" transform="translate(761.4,235.8)"><circle r="9" class="city-dot"/><text class="city-name" y="-16">科隆</text></a>
        <a href="#day-4" data-city="卢森堡" class="city" transform="translate(686.9,344.9)"><circle r="9" class="city-dot"/><text class="city-name" y="26">卢森堡</text></a>
        <a href="#day-5" data-city="凡尔赛" class="city" transform="translate(325.8,411.4)"><circle r="7" class="city-dot"/><text class="city-name" y="26">凡尔赛</text></a>
      </svg>
      <p class="route-note">▲ 数字为各段自驾里程 · 风车村为阿姆斯特丹当日往返支线 · 全程 1,502km</p>
    </div>
  </div>
</section>
```

配套 CSS（追加到 `<style>`）：

```css
.route-card{overflow:hidden}
.route-line{fill:none;stroke:url(#routeGrad);stroke-width:4;stroke-linecap:round;stroke-dasharray:1400;stroke-dashoffset:1400;animation:draw 2.4s cubic-bezier(.4,0,.2,1) forwards}
.route-line.sub{stroke-width:3;stroke-dasharray:600 14;animation-delay:.4s}
@keyframes draw{to{stroke-dashoffset:0}}
.dist{font-size:13px;font-weight:600;fill:#86868b;font-variant-numeric:tabular-nums}
.city{cursor:pointer}
.city-dot{fill:#0071e3;stroke:#fff;stroke-width:3;transition:r .2s, fill .2s}
.city:hover .city-dot{fill:#0077ed}
.city-name{font-size:15px;font-weight:600;fill:#1d1d1f;text-anchor:middle}
.city.sub .city-dot{fill:#ff9f0a}
.route-note{margin-top:16px;font-size:13px;color:var(--ink2);text-align:center}
```

注：`stroke-dasharray` 值 1400 需略大于全路径总长（目测总长约 1300）；若动画结束时虚线有残留，把两个 1400 加大到 1800。

- [ ] **Step 2: 目检**

`start index.html` → 检查：7 城市节点 + 风车村小节点、8 段路线动画依次描线（sub 支线延迟）、距离标注位置不压城市名、点击「科隆」跳转到 Day 4（此刻 `#day-4` 还不存在，点击无效属预期）。

- [ ] **Step 3: 提交**

```bash
git add index.html
git commit -m "feat: SVG 路线总览图（动画描线 + 城市节点）"
```

---

### Task 5: Leaflet 交互地图

**Files:**
- Modify: `index.html`（`<section id="map">` + 底部 `<script>` 中的地图初始化）

**Interfaces:**
- Consumes: Task 1 骨架、Task 2 样式
- Produces: `window.initMap` 不存在——直接 `DOMContentLoaded` 内执行；地图 marker 点击 → `location.hash = '#day-N'`；若 `typeof L === 'undefined'` 则隐藏 `#map` 板块

- [ ] **Step 1: 补上 Leaflet 的 SRI integrity**

```bash
curl -s https://unpkg.com/leaflet@1.9.4/dist/leaflet.css | grep -oE 'sha256-[A-Za-z0-9+/=]+'
curl -s https://unpkg.com/leaflet@1.9.4/dist/leaflet.js | grep -oE 'sha256-[A-Za-z0-9+/=]+'
```

把两个值分别填到 Task 1 占位的 `<link>` 与 `<script>` 标签：`integrity="sha256-<值>"` + `crossorigin=""`。

- [ ] **Step 2: 写地图板块 HTML**

```html
<section id="map">
  <div class="section-head">
    <div class="kicker">Interactive Map</div>
    <h2>交互地图</h2>
    <p>点击城市标记，直达对应行程日。</p>
  </div>
  <div class="container">
    <div class="card" style="padding:10px">
      <div id="map-canvas" style="height:520px;border-radius:16px;overflow:hidden"></div>
    </div>
  </div>
</section>
```

- [ ] **Step 3: 写地图初始化脚本（追加进底部 `<script>`）**

```html
<script>
(function(){
  var cityData = [
    {name:'巴黎',       lat:48.8566, lng:2.3522,  day:1},
    {name:'布鲁塞尔',   lat:50.8503, lng:4.3517,  day:2},
    {name:'阿姆斯特丹', lat:52.3676, lng:4.9041,  day:3},
    {name:'风车村',     lat:52.4740, lng:4.8160,  day:3, sub:true},
    {name:'科隆',       lat:50.9375, lng:6.9603,  day:4},
    {name:'卢森堡市',   lat:49.6116, lng:6.1319,  day:4},
    {name:'凡尔赛',     lat:48.8049, lng:2.1204,  day:5},
    {name:'巴黎(返程)', lat:48.8566, lng:2.3522,  day:6}
  ];
  function boot(){
    if (typeof L === 'undefined') {          // 离线降级：隐藏板块
      var sec = document.getElementById('map');
      if (sec) sec.style.display = 'none';
      return;
    }
    var map = L.map('map-canvas', {scrollWheelZoom:false}).setView([50.8, 4.5], 7);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    var line = cityData.filter(function(c){return !c.sub;}).map(function(c){return [c.lat, c.lng];});
    L.polyline(line, {color:'#0071e3', weight:4, opacity:.85, dashArray:'2 10'}).addTo(map);
    if (cityData[2] && cityData[3]) {
      L.polyline([[cityData[2].lat,cityData[2].lng],[cityData[3].lat,cityData[3].lng]],
        {color:'#ff9f0a', weight:3, dashArray:'4 6'}).addTo(map);
    }
    cityData.forEach(function(c){
      var marker = L.circleMarker([c.lat, c.lng], {
        radius: c.sub ? 6 : 9, color:'#fff', weight:2.5,
        fillColor: c.sub ? '#ff9f0a' : '#0071e3', fillOpacity:1
      });
      marker.bindTooltip(c.name, {direction:'top', offset:[0,-6]});
      marker.on('click', function(){ location.hash = '#day-' + c.day; });
      marker.addTo(map);
    });
    map.fitBounds(L.latLngBounds(line.concat([[cityData[3].lat,cityData[3].lng]])), {padding:[40,40]});
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
</script>
```

关键点：用 `L.circleMarker` 而非默认 marker——默认 marker 图标文件在 `file://` 下 404（Leaflet 已知问题），circleMarker 纯 CSS 渲染不受影响；`scrollWheelZoom:false` 避免滚动页面时误触缩放。

- [ ] **Step 4: 目检（需联网）**

`start index.html` → 检查：地图瓦片加载、蓝线主路线 + 橙色风车村支线、8 个圆形标记、hover 显示城市名、点击标记跳转对应 `#day-N`。**断网时** `#map` 板块应整体隐藏（可用浏览器 DevTools 的 Network: Offline 验证）。

- [ ] **Step 5: 提交**

```bash
git add index.html
git commit -m "feat: Leaflet 交互地图（路线 + 城市标记 + 离线降级）"
```

---

### Task 6: 行程板块 Day 1–3

**Files:**
- Modify: `index.html`（`<section id="itinerary">` 内写 Day 1–3 完整 HTML）

**Interfaces:**
- Consumes: Task 2 的 `.day .spot .meal .tl .photo-wrap .badge .chip` 类；Task 3 的图片 URL 清单
- Produces: `#day-1` `#day-2` `#day-3` 三个板块；每景点卡 `<article class="spot">` 内含 `.photo-wrap`（img+fallback）、名称、贴士；每餐卡 `<article class="meal">`；每时刻表 `<details class="tl-box">` 内含 `<ul class="tl">` 与 `<li class="tl">` 行

- [ ] **Step 1: 写板块容器 + Day 1**

板块容器：

```html
<section id="itinerary">
  <div class="section-head">
    <div class="kicker">Itinerary</div>
    <h2>每日行程</h2>
    <p>7 天 6 晚 · 每天 3 餐 + 核心景点 · 点击「展开时刻表」查看完整分时安排</p>
  </div>
  <div class="container day-stack">
    <!-- Day 1 -->
    <section class="day" id="day-1" data-day="1">
      <header class="day-head">
        <div class="day-no">Day 1</div>
        <div class="day-meta">
          <div class="day-date">9月30日 · 周三 · 抵达日</div>
          <h3>巴黎初印象 — 铁塔 · 罗浮宫 · 凯旋门 · 蒙马特</h3>
          <p class="day-tags"><span class="chip">🇫🇷 法国</span><span class="chip">市内约 20km</span><span class="chip">7 景点 + 3 餐</span></p>
        </div>
      </header>
      <div class="spot-grid">…景点卡…</div>
      <div class="meal-grid">…美食卡…</div>
      <details class="tl-box"><summary>展开完整时刻表（16 项）</summary><ul class="tl">…</ul></details>
    </section>
    …
  </div>
</section>
```

配套 CSS（追加）：

```css
.day-stack{display:flex;flex-direction:column;gap:40px;padding-top:40px}
.day{background:var(--card);border:1px solid var(--line);border-radius:28px;padding:32px;box-shadow:var(--shadow);scroll-margin-top:80px}
.day-head{display:flex;gap:20px;align-items:flex-start;margin-bottom:24px}
.day-no{flex:0 0 auto;font-size:13px;font-weight:700;letter-spacing:.06em;color:#fff;background:var(--blue);border-radius:12px;padding:8px 12px}
.day-date{font-size:13px;color:var(--ink2);font-weight:600}
.day h3{font-size:clamp(20px,3vw,26px);font-weight:700;letter-spacing:-.015em;margin:4px 0 8px}
.day-tags{margin-top:4px}
.spot-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin-bottom:20px}
.meal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-bottom:20px}
.spot{background:#fbfbfd;border:1px solid var(--line);border-radius:var(--radius-sm);overflow:hidden;transition:transform .3s, box-shadow .3s}
.spot:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg)}
.spot .s-body{padding:14px 16px 16px}
.spot h4{font-size:16px;font-weight:650;letter-spacing:-.01em}
.spot .s-tip{font-size:13px;color:var(--ink2);margin-top:6px}
.spot .s-price{display:inline-block;margin-top:8px;font-size:12px;font-weight:600;color:var(--blue);background:#e8f0fe;border-radius:999px;padding:3px 10px}
.meal{background:#fbfbfd;border:1px solid var(--line);border-radius:var(--radius-sm);padding:16px}
.meal h4{font-size:15.5px;font-weight:650}
.meal .m-meal{font-size:12.5px;color:var(--ink2);margin:4px 0}
.meal .m-dish{font-size:13px;color:#3b3b40;margin-top:8px}
.meal .m-price{display:inline-block;margin-top:8px;font-size:12px;font-weight:600;color:#d97706;background:#fef3c7;border-radius:999px;padding:3px 10px}
@media(max-width:768px){.spot-grid,.meal-grid{grid-template-columns:1fr}}
```

**Day 1 完整内容**（全部转录自 `_excel_dump.txt` 第 3–19 行；`img` 用 Task 3 清单对应 URL）：

- 4 张景点卡：
  1. 埃菲尔铁塔（img 铁塔图）——「清晨人最少，登二层 €18.80；战神广场免费，最佳拍照点在战神广场正对面与特罗卡德罗」→ `.s-price`：€18.80
  2. 罗浮宫（img 罗浮宫图）——「精华路线：Carrousel 入口→蒙娜丽莎→维纳斯→胜利女神→拿破仑三世公寓；€17 官网提前预约时段」→ €17
  3. 凯旋门（img 凯旋门图）——「登顶层 €13 俯瞰 12 条放射大道；外部拍照也极好」→ €13
  4. 蒙马特高地（img 蒙马特图）——「圣心大教堂免费，日落时分最美；小丘广场警惕旅游陷阱餐厅」→ 免费
- 3 张美食卡：
  1. 早餐 · 附近 Boulangerie——「牛角包 €2.5 + 咖啡 €3；或酒店早餐 €15-25」→ 人均 €5.5
  2. 午餐 · Le Foyot de Tuileries（1890 经典法餐厅）——「焗蜗牛 €14.5 / 油封鸭腿 €22 / 洋葱汤 €11.5」→ 人均 €45-60 · 需预订
  3. 晚餐 · Le Campanule（经典法餐厅）——「牛排 €22 / 法式炖蛋 €16」→ 人均 €40-55 · 需预订
- 时刻表 16 行（转录自 dump 第 4–19 行，每行 `<li class="tl">` 三列：`<div class="t">时段</div><div class="ty">类型</div><div class="det"><b>地点+详情</b><span>车程/贴士</span></div>`）。示例（首行）：

```html
<li class="tl"><div class="t">06:00</div><div class="ty">航班</div><div class="det"><b>抵达巴黎戴高乐机场 CDG T2</b><span>准备好申根签证、入境文件、海关申报</span></div></li>
<li class="tl"><div class="t">06:00-07:00</div><div class="ty">交通</div><div class="det"><b>入境手续 + 提取行李</b><span>机场内步行 · 法国海关现金 €10000+ 需申报</span></div></li>
<li class="tl"><div class="t">07:00-08:00</div><div class="ty">租车</div><div class="det"><b>租车柜台取车（Hertz / Sixt / Europcar）</b><span>选中型 SUV + 全险，检查车身拍照 · 推荐标致 3008 / 宝马 X1</span></div></li>
<li class="tl"><div class="t">08:00-09:00</div><div class="ty">驾车</div><div class="det"><b>CDG → 巴黎市区酒店</b><span>28km / 36min · A1 高速 €4.5 → Périphérique 环线</span></div></li>
<li class="tl"><div class="t">09:00-09:30</div><div class="ty">住宿</div><div class="det"><b>办理入住、寄存行李</b><span>推荐 1区/4区（市中心）或 15区（性价比）· 停车 €30-50/晚</span></div></li>
<li class="tl"><div class="t">09:30-10:00</div><div class="ty">餐饮</div><div class="det"><b>简单早餐：牛角包 + 咖啡</b><span>或酒店早餐 €15-25</span></div></li>
<li class="tl"><div class="t">10:00-11:30</div><div class="ty">景点</div><div class="det"><b>埃菲尔铁塔 + 战神广场</b><span>距酒店约 4km/12min · 清晨人最少，登二层 €18.80，最佳拍照点战神广场正对面 / 特罗卡德罗</span></div></li>
<li class="tl"><div class="t">11:30-12:00</div><div class="ty">驾车</div><div class="det"><b>铁塔 → 罗浮宫</b><span>4km / 12min · 停车 Parking Quai Branly €3.10/h</span></div></li>
<li class="tl"><div class="t">12:00-13:30</div><div class="ty">餐饮</div><div class="det"><b>午餐 Le Foyot de Tuileries（1890 经典法餐厅）</b><span>焗蜗牛 €14.5 / 油封鸭腿 €22 / 洋葱汤 €11.5 · 人均 €45-60 · 需预订</span></div></li>
<li class="tl"><div class="t">13:30-15:30</div><div class="ty">景点</div><div class="det"><b>罗浮宫精华游览</b><span>€17 官网提前预约时段 · 路线：Carrousel 入口→蒙娜丽莎→维纳斯→胜利女神→拿破仑三世公寓</span></div></li>
<li class="tl"><div class="t">15:30-16:00</div><div class="ty">驾车</div><div class="det"><b>罗浮宫 → 凯旋门</b><span>4km / 10min · 停车 Parking La Bourdonnais €3.10/h</span></div></li>
<li class="tl"><div class="t">16:00-17:00</div><div class="ty">景点</div><div class="det"><b>凯旋门 + 星形广场</b><span>登顶层 €13 俯瞰 12 条放射大道</span></div></li>
<li class="tl"><div class="t">17:00-17:30</div><div class="ty">驾车</div><div class="det"><b>凯旋门 → 蒙马特</b><span>5km / 12min · 蒙马特为行人区，停 Parking Garibaldi €2.5/h 步行上山 15min</span></div></li>
<li class="tl"><div class="t">17:30-19:00</div><div class="ty">景点</div><div class="det"><b>圣心大教堂 + 蒙马特艺术广场 + 小丘广场</b><span>步行上山 15min · 免费，日落时分最美</span></div></li>
<li class="tl"><div class="t">19:30-21:00</div><div class="ty">餐饮</div><div class="det"><b>晚餐 Le Campanule 经典法餐厅</b><span>牛排 €22 / 法式炖蛋 €16 · 人均 €40-55 · 需预订</span></div></li>
<li class="tl"><div class="t">21:00-22:00</div><div class="ty">驾车</div><div class="det"><b>蒙马特 → 酒店</b><span>5-8km / 20-30min · 晚上市区交通较好</span></div></li>
```

- [ ] **Step 2: 写 Day 2**（转录自 dump 第 20–27 行）

- 4 张景点卡：奥赛博物馆（img 奥赛图，€16，「莫奈《干草堆》、梵高《自画像》」）、西岱岛·巴黎圣母院外观+圣礼拜堂（img 圣母院图，€11，「圣母院 2024年12月重开，圣礼拜堂彩窗绝美」）、布鲁塞尔大广场（img 大广场图，€6，「UNESCO 世界遗产、欧洲最美广场，市政厅钟楼登顶」）、撒尿小童+圣于贝尔拱廊街（img 撒尿小童图，免费，「拱廊街买 Neuhaus 巧克力、Chimay 啤酒」）
- 3 张美食卡：午餐 Maison Dandoy 薯条 €8 + Neuve Garage 华夫饼 €6（人均 €14）；晚餐 Maison Antoine（1870 比利时餐厅，啤酒炖牛肉 €18 / 鸭胸 €24，人均 €45-55，需预订，Rue Antoine Dansaert 38）
- 时刻表 7 行（dump 第 21–27 行）：奥赛（08:30-10:00）→ 圣母院/圣礼拜堂（10:30-11:30）→ 驾车 312km/3h45（12:00-15:45，A1→A2/E19，法国段 €10-12，13:30 Laon 服务区休息）→ 午餐薯条华夫饼（16:30-17:30）→ 大广场（17:30-19:00）→ 撒尿小童+拱廊街（19:00-19:30）→ 晚餐 Maison Antoine（21:30-23:00）

- [ ] **Step 3: 写 Day 3**（转录自 dump 第 28–39 行）

- 4 张景点卡：风车村 Zaanse Schans（img 风车村图，免费入场，「17 座历史风车；木鞋制作工坊免费、奶酪工坊 €8、登塔 €4；风车+运河+蓝屋经典画面」）、阿姆斯特丹运河带日落游船（img 运河图，€15 含中文导览，「日落时分的运河 = 完美荷兰体验，码头 Centraal Station 附近」）、水坝广场 Dam Square（img 水坝广场图，免费，「王宫外观 + 国家纪念碑，傍晚灯光亮起后拍照效果好」）、九街 De Negen Straatjes 夜游（「最文艺街区：精品店、古董店、小酒馆，夜晚灯光下运河倒映」）
- 3 张美食卡：早餐比利时特色（华夫饼+巧克力+薯条）；午餐 Albert Cuyp Market（Stroopwafel €3 / 薯条 €5）；晚餐 De Eendracht（1919 最古老餐厅之一，荷兰炖牛肉 €18 / 鲱鱼三明治 €7 / 奶酪拼盘 €18，人均 €35-50，Egelantiersgracht 63，需预订）
- 时刻表 11 行（dump 第 29–39 行）：早餐（07:30-08:30）→ 驾车 212km（10:30-13:30，A1/E19→A2 经 Antwerp，荷兰高速免费，Antwerp 可看 Cathedral €4）→ 午餐市场（13:30-14:00）→ 入住（14:00-14:30，⚠停车 €5-7/h，选带停车场酒店 €40-60/晚）→ 驾车风车村 15km（14:30-15:00，N508/A7 北向，P1/P2 免费）→ 风车村 2.5h（15:00-17:30）→ 驾车返回（17:30-18:00，赶上日落运河）→ 运河游船（18:00-19:00）→ 水坝广场（19:00-19:30）→ 晚餐 De Pijp（19:30-21:00，骑车 10min）→ 九街夜游（21:00-22:30）

- [ ] **Step 4: 校验 + 目检**

Run: `python tools/check_page.py` — 此刻应 PASS 的项目：板块结构、`class="day"` 计数 3/7（仍会 FAIL，预期）、`<li class="tl">` 计数 16+7+11=34（≠69，预期 FAIL）、景点卡 12 张、美食卡 9 张、SVG、Leaflet。
目检：`start index.html` → Day 1–3 板块完整、图片正常显示（连网）、hover 上浮效果、`<details>` 展开时刻表、移动端单列（DevTools 375px 视口）。

- [ ] **Step 5: 提交**

```bash
git add index.html
git commit -m "feat: 行程板块 Day 1-3（景点画廊 + 美食 + 完整时刻表）"
```

---

### Task 7: 行程板块 Day 4–7

**Files:**
- Modify: `index.html`（Day 4–7 追加到 `#itinerary .day-stack` 内）

**Interfaces:**
- Consumes: Task 6 确立的 `.day` 卡结构；Task 3 图片 URL
- Produces: `#day-4` `#day-5` `#day-6` `#day-7`；SVG/地图的 `#day-N` 跳转全部有目标

- [ ] **Step 1: Day 4**（转录自 dump 第 40–51 行）—— 阿姆斯特丹 → 科隆 → 卢森堡（479km/6h）

- 6 张景点卡：Rijksmuseum（img 国家博物馆图，€20 提前预约，「必看：伦勃朗《夜巡》（世界最大画作 11×4m）、维米尔《代尔夫特风景》」）、博物馆广场+梵高博物馆外观（免费）、安妮之家（img 安妮之家图，€16 提前 2-3 个月预约，「《安妮日记》藏身地，非常感人」）、Bloemenmarkt 花市（免费，「全球唯一浮动花卉市场，郁金香球茎 €3-5 伴手礼」）、科隆大教堂（img 科隆大教堂图，€7 登塔 394 级台阶，「UNESCO 世界遗产、哥特式巅峰、世界第三大教堂」）、霍亨索伦桥（img 桥图，免费，「爱情锁桥，莱茵河畔散步看科隆全景」）
- 3 张美食卡：早午餐 Pancakes Amsterdam（€8-10，「荷兰煎饼比可丽饼厚，甜咸都有」）；午餐 Früh Kölsch Brewery（啤酒 €4/小杯、科隆香肠 €6、Reibekuchen 土豆饼 €5）；晚餐 Villa Le Rosey 米其林法餐厅（鹅肝 €35 / 松露 €45，人均 €80-120，需预订；预算有限选 Bons Vivants €35-45）
- 时刻表 11 行（dump 第 41–51 行）：国家博物馆（07:00-08:30）→ 博物馆广场（08:30-09:00）→ 安妮之家（09:00-10:30，驾车 6km/15min）→ 煎饼早午餐（10:30-11:00）→ 花市（11:00-11:30）→ 驾车 261km 3h15（11:30-14:45，A2 经 Utrecht→Düsseldorf→Cologne，德国高速免费不限速但安全驾驶，13:00 Düsseldorf 休息）→ 科隆大教堂（14:45-16:00，Parking Dom €2.50/h）→ 啤酒午餐（16:00-16:45）→ 霍亨索伦桥（16:45-17:15）→ 驾车 203km 2h30（17:15-19:45，A1/E41 经 Trier，沿途平原渐入山区，Trier 可看 Roman Amphitheatre €5）→ 晚餐 Villa Le Rosey（20:00-21:30）

- [ ] **Step 2: Day 5**（转录自 dump 第 52–60 行）—— 卢森堡 → 凡尔赛 → 巴黎（404km/4.9h）

- 3 张景点卡：佩特罗斯大峡谷 Bock Casemates + Grund（img 卢森堡峡谷图，€7 地道约 1h，「UNESCO 世界遗产，Grund 欧洲最美峡谷：彩色建筑 + Alzette 河」）、卢森堡老城（免费，「王宫 + 大剧院 + 亚当桥 + Calvarieberg 最佳全景俯瞰点」）、凡尔赛宫（img 凡尔赛宫图，€20 提前预约，「镜厅 73 米 17 面拱形镜、国王寝宫、法式花园」）
- 3 张美食卡：午餐 Judd mat Gaardebounen（€14，「卢森堡特色：烟熏猪肉配蚕豆」）；凡尔赛镇午餐 La Maison Rose（€18）/ Le Grand Véfour（€25-35）；晚餐 Bouillon Chartier 百年食堂（img 可用塞纳河图或省略——**无对应图时省略 img，只保留文字卡**；焗蜗牛 €8 / 油封鸭腿 €12 / 煎蛋卷 €9，人均 €20-30，复古金色装修，Rue du Faubourg Saint-Denis 18）
- 时刻表 8 行（dump 第 53–60 行）：大峡谷（08:30-10:00）→ 老城（10:00-11:00）→ 午餐蚕豆猪肉（11:00-11:30）→ 驾车 381km 4h30 最长一段（11:30-16:00，A31→A4 经 Metz→Reims，法国段 €15-18，13:00 Metz 休息 30min、14:30 Reims 服务区）→ 凡尔赛镇午餐（16:00-17:00，Parking Place d'Armes €2.50/h）→ 凡尔赛宫 2h（17:00-19:00）→ 驾车回巴黎 23km 36min（19:30-20:30，N104→A13 或 N186→Périphérique，€4-5）→ 晚餐 Bouillon Chartier（20:30-22:00）

- [ ] **Step 3: Day 6**（转录自 dump 第 61–69 行）—— 巴黎深度游最后一天

- 6 张景点卡：圣礼拜堂（img 圣礼拜堂图，€11，「15 扇 15 米高哥特彩窗，世界最美」）、玛莱区+孚日广场（免费，「巴黎最优雅广场（16 世纪），LVMH 基金会免费，精品店+古着店」）、塞纳河游船 Bateaux Mouches（img 塞纳河图，€15 含中文导览 1.5h，「途径圣母院→奥赛→铁塔→罗浮宫→大皇宫→亚历山大三世桥」）、老佛爷/春天百货（免费，「香水 Chanel/Dior、化妆品 L'Occitane、Ladurée 马卡龙」）、杜乐丽花园+亚历山大三世桥+荣军院（img 杜乐丽图，€11.5，「绿顶凉亭喷泉，巴黎最华丽的桥，金色圆顶拿破仑长眠地」）、特罗卡德罗铁塔日落夜景（img 铁塔图或省略，「日落约 19:00，整点闪烁 5 分钟，特罗卡德罗正对铁塔=最佳拍照点」）
- 3 张美食卡：午餐 L'As du Fallafel（法拉费 €7 排队名店）/ Breizh Café 顶级可丽饼（€25 布列塔尼风格）；告别晚餐 Les Ombres 屋顶餐厅（「俯瞰铁塔夜景」，海鲜拼盘 €35 / 鹅肝 €28，人均 €60-90，需预订）
- 时刻表 8 行（dump 第 62–69 行）：圣礼拜堂（09:00-09:45）→ 玛莱区（10:00-11:30）→ 午餐（11:30-12:30）→ 游船（13:00-15:00）→ 老佛爷（15:00-16:30）→ 杜乐丽+荣军院（16:30-17:30）→ 特罗卡德罗日落（18:30-19:30，Parking Trocadéro €3.10/h）→ Les Ombres 晚餐（19:30-22:00）

- [ ] **Step 4: Day 7**（转录自 dump 第 70–78 行）—— 巴黎 → CDG → 北京

- 2 张景点卡：奥斯曼大街漫步（免费，「花神咖啡馆 Café de Flore €5，萨特波伏娃据点」）、蓬皮杜艺术中心外观（免费，「彩色管道外露，内部 €14」）
- 1 张美食卡：最后一餐 Angelina 法式甜点（「热巧克力 €8 巴黎最浓稠、圣多诺黑 €10」）
- 时刻表 8 行（dump 第 71–78 行）：酒店早餐+退房（08:00-09:00，行李寄存前台）→ 奥斯曼大街（09:00-10:00）→ 蓬皮杜/购物（10:00-11:30）→ Angelina（11:30-12:30）→ 驾车回 CDG 27km 36min（13:00-14:30，A1 €4.5，⚠预留 1.5h 防堵车，22:00 航班建议 19:00 前到）→ 还车（14:30-15:00，满油还保留单据，T2/T3 间免费 CDG Val 穿梭巴士）→ 候机免税（15:00-21:00，T2 有 Dior/LVMH 免税店，21:00 左右登机 T2-E/T2-F）→ 22:00 起飞（✈️ 飞行约 11h，时差 -7h，预计 10/7 北京时间中午 11:00-12:00 抵达首都机场）

Day 7 的板块里加一个醒目的收尾卡（class 用 `.meal` 变体即可，文案：「✈️ 22:00 CDG → 北京 · 飞行约 11 小时 · 时差 -7h · 预计 10 月 7 日中午抵达」）。

- [ ] **Step 5: 校验 + 目检**

Run: `python tools/check_page.py` — **必须全 PASS**：7 个 day 板块、69 条 `.tl`、景点卡 ≥28（实际 4+4+4+6+3+6+2=29）、美食卡 ≥13（实际 3+2+3+3+3+2+1=17）、9 段驾驶还没写（Task 9 才补 `tr.drive`——此刻该行仍 FAIL 属预期）、SVG、Leaflet、图片可达。
目检：`start index.html` → 从 SVG 点「科隆」跳转 `#day-4` 正常；Day 4–7 内容齐全；移动端正常。

- [ ] **Step 6: 提交**

```bash
git add index.html
git commit -m "feat: 行程板块 Day 4-7 + SVG/地图跳转全部生效"
```

---

### Task 8: 国家风情板块

**Files:**
- Modify: `index.html`（`<section id="culture">`）

**Interfaces:**
- Consumes: Task 2 类、Task 3 图片（可选）
- Produces: `.country` 卡片 ×5，每张含国名、旗帜 emoji、标签行、三点（风情/美食/体验）

- [ ] **Step 1: 写板块 HTML**

```html
<section id="culture">
  <div class="section-head">
    <div class="kicker">Local Flavor</div>
    <h2>国家风情</h2>
    <p>五国四味——把路上的风土人情装进心里</p>
  </div>
  <div class="container country-grid">
    <article class="country" style="--acc:#0a84ff">
      <div class="c-flag">🇫🇷</div>
      <h3>法国 · 艺术与咖啡</h3>
      <p class="c-desc">露天咖啡座是法国人的客厅——花神咖啡馆里萨特写下存在主义，清晨的牛角包配浓缩咖啡是每天的仪式。</p>
      <div class="c-list"><span>🍽 焗蜗牛 · 油封鸭腿 · 可丽饼 · 马卡龙</span><span>📍 铁塔晨光 · 塞纳河游船 · 蒙马特日落</span></div>
    </article>
    <article class="country" style="--acc:#ff3b30">
      <div class="c-flag">🇧🇪</div>
      <h3>比利时 · 巧克力与漫画</h3>
      <p class="c-desc">布鲁塞尔大广场被誉为欧洲最美客厅，撒尿小童的传说流传四百年——薯条与华夫饼在这里才是正统。</p>
      <div class="c-list"><span>🍽 比利时薯条 · 华夫饼 · Neuhaus 巧克力</span><span>📍 大广场夜景 · 圣于贝尔拱廊街</span></div>
    </article>
    <article class="country" style="--acc:#ff9f0a">
      <div class="c-flag">🇳🇱</div>
      <h3>荷兰 · 风车与自行车</h3>
      <p class="c-desc">比海平面低 7 米的国度里，风车与运河是千年智慧的雕塑——骑行和游船，是打开阿姆斯特丹的正确方式。</p>
      <div class="c-list"><span>🍽 Stroopwafel · 奶酪 · 鲱鱼三明治</span><span>📍 风车村 · 运河日落游船 · 九街夜游</span></div>
    </article>
    <article class="country" style="--acc:#bf5af2">
      <div class="c-flag">🇩🇪</div>
      <h3>德国 · 哥特与啤酒</h3>
      <p class="c-desc">科隆大教堂建了 632 年——哥特式巅峰之下，一小杯 Kölsch 配一根香肠，就是科隆人的下午茶。</p>
      <div class="c-list"><span>🍽 科隆香肠 · Kölsch 啤酒 · 土豆饼</span><span>📍 大教堂登塔 · 爱情锁桥 · 莱茵河畔</span></div>
    </article>
    <article class="country" style="--acc:#64d2ff">
      <div class="c-flag">🇱🇺</div>
      <h3>卢森堡 · 袖珍公国</h3>
      <p class="c-desc">欧盟最小的首都之一，却有欧洲最深的峡谷——站在 Calvarieberg 俯瞰老城，仿佛中世纪画卷铺展脚下。</p>
      <div class="c-list"><span>🍽 烟熏猪肉配蚕豆</span><span>📍 Bock 地道 · Grund 峡谷 · 老城全景</span></div>
    </article>
  </div>
</section>
```

配套 CSS（追加）：

```css
.country-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px;padding-top:40px}
.country{background:var(--card);border:1px solid var(--line);border-radius:24px;padding:26px;box-shadow:var(--shadow);border-top:4px solid var(--acc,#0071e3);transition:transform .35s, box-shadow .35s}
.country:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg)}
.c-flag{font-size:34px;line-height:1}
.country h3{font-size:19px;font-weight:700;margin:12px 0 8px;letter-spacing:-.01em}
.c-desc{font-size:14px;color:var(--ink2);margin-bottom:14px}
.c-list{display:flex;flex-direction:column;gap:6px}
.c-list span{font-size:13px;color:#3b3b40;background:#f5f5f7;border-radius:10px;padding:7px 12px}
@media(max-width:768px){.country-grid{grid-template-columns:1fr}}
```

- [ ] **Step 2: 校验 + 目检**

Run: `python tools/check_page.py` → 板块检查 `#culture` PASS。
目检：五张卡、每张顶部 4px 品牌色条、hover 上浮。

- [ ] **Step 3: 提交**

```bash
git add index.html
git commit -m "feat: 国家风情板块（五国文化卡）"
```

---

### Task 9: 预算 + 预订 + 贴士 + 页脚

**Files:**
- Modify: `index.html`（`#budget` `#bookings` `#tips` 板块 + footer 补全 + 驾驶数据表 `#route` 下方）

**Interfaces:**
- Consumes: Task 2 类
- Produces: `.drive` 行 ×9（校验脚本计数）、`.budget-item` 卡、`.booking` 行、`.tip-card`、footer 返程信息

- [ ] **Step 1: 驾驶数据表（放进 `#route` 板块、SVG 卡片之后）**

完整 9 行（转录自 dump 第 89–97 行，合计行第 98 行作为最后一行 `<tfoot>`）：

```html
<div class="card" style="margin-top:20px">
  <table class="drive-table">
    <thead><tr><th>路段</th><th>距离</th><th>时间</th><th>高速 / 费用</th><th>途经</th></tr></thead>
    <tbody>
      <tr class="drive"><td>巴黎 CDG → 巴黎市区</td><td>28km</td><td>36min</td><td>A1 €4.5</td><td>—</td></tr>
      <tr class="drive"><td>巴黎 → 布鲁塞尔</td><td>312km</td><td>3h45min</td><td>A1→A2/E19 · 法国段 €10-12</td><td>Compiègne · Laon</td></tr>
      <tr class="drive"><td>布鲁塞尔 → 阿姆斯特丹</td><td>212km</td><td>2h45min</td><td>A1/E19→A2 · 荷兰免费</td><td>Antwerp</td></tr>
      <tr class="drive"><td>阿姆斯特丹市区 → 风车村</td><td>15km</td><td>20min</td><td>N508/A7 · 免费</td><td>单程</td></tr>
      <tr class="drive"><td>阿姆斯特丹 → 科隆</td><td>261km</td><td>3h15min</td><td>A2 · 德国免费</td><td>Utrecht · Düsseldorf</td></tr>
      <tr class="drive"><td>科隆 → 卢森堡市</td><td>203km</td><td>2h30min</td><td>A1/E41 · 免费</td><td>Trier</td></tr>
      <tr class="drive"><td>卢森堡市 → 凡尔赛</td><td>381km</td><td>4h30min</td><td>A31→A4 · 法国段 €15-18</td><td>Metz · Reims（最长！）</td></tr>
      <tr class="drive"><td>凡尔赛 → 巴黎市区</td><td>23km</td><td>36min</td><td>N104/A13 · €4-5</td><td>—</td></tr>
      <tr class="drive"><td>巴黎市区 → CDG</td><td>27km</td><td>36min</td><td>A1 · €4.5</td><td>预留 1.5h 防堵车</td></tr>
    </tbody>
    <tfoot><tr><td>合计</td><td>1,502km</td><td>约 22 小时</td><td>高速费 €40-50</td><td>较 V2 增加 36km（风车村往返）</td></tr></tfoot>
  </table>
</div>
```

配套 CSS：

```css
.drive-table{width:100%;border-collapse:collapse;font-size:14px}
.drive-table th{font-size:12px;color:var(--ink2);font-weight:600;text-align:left;padding:10px 12px;border-bottom:1px solid var(--line)}
.drive-table td{padding:11px 12px;border-bottom:1px solid var(--line);color:#3b3b40;font-variant-numeric:tabular-nums}
.drive-table tbody tr:hover td{background:#fbfbfd}
.drive-table tfoot td{font-weight:700;color:var(--ink);background:#f5f5f7}
@media(max-width:640px){.drive-table{font-size:12.5px}.drive-table td,.drive-table th{padding:8px 8px}}
```

- [ ] **Step 2: 预算板块**（转录自 dump 第 99–107 行）

```html
<section id="budget">
  <div class="section-head">
    <div class="kicker">Budget</div>
    <h2>预算参考</h2>
    <p>人均 €1,540–2,300（约 ¥12,000–18,500，不含国际机票）</p>
  </div>
  <div class="container budget-grid">
    <article class="budget-item"><div class="b-name">租车 · 7 天 SUV</div><div class="b-amt">€200–300<small>/人</small></div><div class="b-note">全险（CDW + THEP）· 推荐标致 3008 / 宝马 X1</div></article>
    <article class="budget-item"><div class="b-name">燃油 · 1,502km</div><div class="b-amt">€100–130<small>/人</small></div><div class="b-note">按 8L/100km × €1.8/L 估算</div></article>
    <article class="budget-item"><div class="b-name">过路费</div><div class="b-amt">€20–25<small>/人</small></div><div class="b-note">仅法国段收费，荷/德高速免费</div></article>
    <article class="budget-item"><div class="b-name">停车 · 6 天</div><div class="b-amt">€50–75<small>/人</small></div><div class="b-note">市区 €2.5–5/h · 风车村 P1/P2 免费</div></article>
    <article class="budget-item"><div class="b-name">酒店 · 6 晚四星</div><div class="b-amt">€600–900<small>/人</small></div><div class="b-note">€200–300/晚 · 阿姆斯特丹选带停车场</div></article>
    <article class="budget-item"><div class="b-name">餐饮 · 7 天</div><div class="b-amt">€400–550<small>/人</small></div><div class="b-note">法餐 + 当地小吃，含 2 顿米其林体验</div></article>
    <article class="budget-item"><div class="b-name">景点门票</div><div class="b-amt">€170–220<small>/人</small></div><div class="b-note">含罗浮宫、凡尔赛、博物馆等全部预约票</div></article>
    <article class="budget-item total"><div class="b-name">每人总计（不含机票）</div><div class="b-amt">€1,540–2,300<small>≈ ¥12,000–18,500</small></div><div class="b-note">7 天 6 晚 · 五国 · 含全部住宿与餐食</div></article>
  </div>
</section>
```

配套 CSS：

```css
.budget-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;padding-top:40px}
.budget-item{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:20px;box-shadow:var(--shadow)}
.b-name{font-size:14px;font-weight:600;color:var(--ink2)}
.b-amt{font-size:24px;font-weight:700;letter-spacing:-.02em;margin:8px 0 6px;font-variant-numeric:tabular-nums}
.b-amt small{font-size:12.5px;color:var(--ink2);font-weight:500;margin-left:4px}
.b-note{font-size:12.5px;color:var(--ink2)}
.budget-item.total{border:2px solid var(--blue);background:linear-gradient(160deg,#e8f0fe,#fff)}
.budget-item.total .b-amt{color:var(--blue)}
@media(max-width:768px){.budget-grid{grid-template-columns:1fr 1fr}}
@media(max-width:480px){.budget-grid{grid-template-columns:1fr}}
```

- [ ] **Step 3: 预订板块**（转录自 dump 第 108–115 行）

```html
<section id="bookings">
  <div class="section-head">
    <div class="kicker">Bookings</div>
    <h2>出发前 · 必预订清单</h2>
    <p>热门景点必须提前预约时段，7 项缺一不可</p>
  </div>
  <div class="container booking-list">
    <div class="booking"><span class="b-n">01</span><div><b>租车</b><p>提前 1 个月 · Hertz / Sixt · 中型 SUV + 全险</p></div></div>
    <div class="booking"><span class="b-n">02</span><div><b>梵高博物馆</b><p>提前 2-3 个月官网 · €20</p></div></div>
    <div class="booking"><span class="b-n">03</span><div><b>安妮之家</b><p>提前 2-3 个月官网 · €16</p></div></div>
    <div class="booking"><span class="b-n">04</span><div><b>罗浮宫</b><p>提前 2-4 周官网预约时段 · €17</p></div></div>
    <div class="booking"><span class="b-n">05</span><div><b>凡尔赛宫</b><p>提前 2-4 周官网 · €20</p></div></div>
    <div class="booking"><span class="b-n">06</span><div><b>Rijksmuseum</b><p>提前 1-2 周官网 · €20 · ⭐ 新增</p></div></div>
    <div class="booking"><span class="b-n">07</span><div><b>热门餐厅</b><p>Le Foyot / Les Ombres / Maison Antoine 提前 1-2 周</p></div></div>
  </div>
</section>
```

配套 CSS：

```css
.booking-list{display:flex;flex-direction:column;gap:10px;padding-top:40px}
.booking{display:flex;gap:16px;align-items:flex-start;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px 20px;box-shadow:var(--shadow)}
.b-n{flex:0 0 auto;width:36px;height:36px;border-radius:50%;background:var(--blue);color:#fff;font-weight:700;font-size:13px;display:flex;align-items:center;justify-content:center}
.booking b{font-size:15.5px}
.booking p{font-size:13px;color:var(--ink2);margin-top:2px}
```

- [ ] **Step 4: 贴士板块**（转录自 dump 第 120–128 行）

```html
<section id="tips">
  <div class="section-head">
    <div class="kicker">Practical Tips</div>
    <h2>实用贴士</h2>
  </div>
  <div class="container tips-grid">
    <div class="tip-card"><span class="t-icon">🛂</span><b>签证</b><p>护照有效期 6 个月以上 + 申根签证</p></div>
    <div class="tip-card"><span class="t-icon">🚗</span><b>限速</b><p>法国高速 130（雨 110）· 荷兰 100/130 · 德国不限速（建议 120-130）</p></div>
    <div class="tip-card"><span class="t-icon">🅿️</span><b>停车</b><p>市区 €2.5-7/h · P+R €5-10/天含公交 · 风车村 P1/P2 免费</p></div>
    <div class="tip-card"><span class="t-icon">⛽</span><b>加油</b><p>每到一个城市先加满再上高速</p></div>
    <div class="tip-card"><span class="t-icon">🌦</span><b>天气</b><p>10 月 12-18°C · 带外套 + 雨伞 + 舒适步行鞋</p></div>
    <div class="tip-card"><span class="t-icon">💶</span><b>货币</b><p>五国全部使用欧元 € · 备少量现金（海关申报线 €10,000）</p></div>
    <div class="tip-card"><span class="t-icon">📱</span><b>手机</b><p>欧洲漫游或 eSIM（Airalo / Holafly）</p></div>
    <div class="tip-card"><span class="t-icon">🛡</span><b>保险</b><p>欧洲旅行医疗保险 + 租车全险（CDW + THEP）</p></div>
  </div>
</section>
```

配套 CSS：

```css
.tips-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;padding-top:40px}
.tip-card{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:22px;box-shadow:var(--shadow)}
.t-icon{font-size:26px}
.tip-card b{display:block;font-size:15.5px;margin:10px 0 6px}
.tip-card p{font-size:13px;color:var(--ink2)}
```

- [ ] **Step 5: 页脚补全**（footer 内追加返程横幅）

```html
<footer>
  <div class="container">
    <div class="return-card">
      <div class="r-title">✈️ 10 月 6 日 22:00 · 巴黎 CDG → 北京</div>
      <p>飞行约 11 小时 · 时差 -7h · 预计 10 月 7 日北京时间 11:00-12:00 抵达首都机场</p>
    </div>
    <p class="foot-note">欧洲自驾 · 七日五国 · 2026.9.30 — 10.6 · 全程 1,502km · 用脚步和车轮丈量欧洲</p>
  </div>
</footer>
```

配套 CSS：

```css
footer{padding:72px 0 40px;background:linear-gradient(180deg,#f5f5f7,#e8e8ed)}
.return-card{background:#0d0d12;color:#fff;border-radius:28px;padding:36px;text-align:center;margin-bottom:32px}
.r-title{font-size:clamp(19px,3vw,26px);font-weight:700;letter-spacing:-.015em}
.return-card p{margin-top:10px;color:#d2d2d7;font-size:15px}
.foot-note{text-align:center;font-size:13px;color:var(--ink2)}
```

- [ ] **Step 6: 校验 + 目检**

Run: `python tools/check_page.py` → **必须全 PASS（含 9 行 `.drive`、图片可达）**。
目检：预算卡、预订清单、贴士网格、深色返程横幅、表格 hover。

- [ ] **Step 7: 提交**

```bash
git add index.html
git commit -m "feat: 驾驶数据表 + 预算 + 预订 + 贴士 + 返程页脚"
```

---

### Task 10: JS 增强 + QA 打磨

**Files:**
- Modify: `index.html`（底部 `<script>` 追加：滚动渐入、导航滚动态、svg 描线触发、地图已有；给内容块加 `.reveal` 类）

**Interfaces:**
- Consumes: 全部前序任务
- Produces: 成品 `index.html`——验收清单全过

- [ ] **Step 1: 追加增强脚本**

在底部 `<script>`（Task 5 的地图脚本之外）追加：

```html
<script>
(function(){
  // 滚动渐入
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, {threshold:.12});
    revealEls.forEach(function(el){ io.observe(el); });
  } else {
    revealEls.forEach(function(el){ el.classList.add('in'); });
  }
  // 导航：滚过 8px 后加阴影
  var nav = document.getElementById('topnav');
  function onScroll(){
    nav.classList.toggle('scrolled', window.scrollY > 8);
    var links = document.querySelectorAll('.nav-link');
    var cur = 'hero';
    document.querySelectorAll('section[id]').forEach(function(sec){
      if (window.scrollY >= sec.offsetTop - 160) cur = sec.id;
    });
    links.forEach(function(l){
      l.style.color = ('#' + l.getAttribute('href').slice(1)) === ('#' + cur) ? 'var(--ink)' : '';
      l.style.fontWeight = ('#' + l.getAttribute('href').slice(1)) === ('#' + cur) ? '600' : '';
    });
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();
})();
</script>
```

配套 CSS（追加到 `#topnav` 规则旁）：

```css
#topnav.scrolled{box-shadow:0 1px 12px rgba(0,0,0,.08)}
```

- [ ] **Step 2: 批量加 `.reveal` 类**

给以下元素加 `class="… reveal"`：每个 `.section-head`、每个 `.day` 卡、每张 `.country`、`.budget-item`、`.tip-card`、`.booking`、`.spot`、`.meal`。注意 `.reveal` 初始 `opacity:0`——若发现页面元素被 JS 失效遮挡（无 IntersectionObserver 时）已有 fallback（直接 `add('in')`）。**加完后打开页面确认没有元素永久透明**（若某元素没有触发，把 `threshold:.12` 调低为 `.05`）。

- [ ] **Step 3: 全面验收（按设计文档 §7 验收标准逐条）**

Run: `python tools/check_page.py` → 全 PASS
目检清单：
1. 双击 `index.html` 9 个板块全部正常显示
2. 苹果风：浅灰背景、大圆角、毛玻璃导航、滚动渐入、描线动画
3. SVG 路线：7 城 + 风车村 + 分段距离 + 动画
4. 每日行程 69 条时刻记录可展开查看
5. DevTools Network Offline 模式：页面仍完整（仅图片和地图降级）；断网刷新时 hero 渐变背景兜底、地图板块隐藏
6. DevTools 375px：无横向滚动、画廊单列、时刻表两列紧凑
7. 点击 SVG/地图城市 → 跳转对应行程日
8. 页面滚动时导航高亮当前板块

- [ ] **Step 4: 最终提交**

```bash
git add index.html
git commit -m "feat: JS 增强（滚动渐入/导航高亮）+ 全量验收"
```

---

## Self-Review 结论（写入计划时已核）

- **Spec 覆盖**：§2 设计语言→Task 2 ✓；§3 全部 9 板块→Task 2/4/5/6/7/8/9 ✓；§4 数据→Task 6/7/9 转录 ✓；§5 技术→Task 1/5 ✓；§6 降级→Task 2（图片）、Task 5（地图）、Task 10（验收）✓；§7 验收→Task 10 ✓；§8 范围外→无对应任务 ✓
- **占位符**：无 TBD/TODO；每个任务含完整代码与转写来源（`_excel_dump.txt` 行号）
- **类型一致性**：`class="day" data-day="N"`、`li.tl`、`tr.drive`、`article.spot/meal` 与 `tools/check_page.py` 的断言一致；`#day-N` 与 SVG/地图跳转一致
