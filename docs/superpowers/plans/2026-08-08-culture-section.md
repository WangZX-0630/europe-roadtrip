# 「国家风情」沉浸式改版 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `index.html` 的 `#culture` 区块从 5 张扁平小卡改造为 5 张全宽大图横幅（沉浸视觉 + 内容双升级）。

**Architecture:** 纯静态 HTML/CSS 改造。新增 `.c-banner` 系列样式（约 45 行 CSS），替换旧 `.country-grid/.country` 体系；5 个横幅复用已验证的 Wikimedia 图片与现有 `.reveal` 动效；`tools/check_page.py` 的 culture 断言同步更新。

**Tech Stack:** 原生 HTML/CSS · 校验脚本 `tools/check_page.py` · Playwright 目检（node）

## Global Constraints

- 只修改 `index.html`、`tools/check_page.py`；其他文件一律不动
- 保留 `<section id="culture">` 与导航锚点 `#culture`
- 图片全部使用 Wikimedia `Special:FilePath/<编码文件名>?width=1600`，5 张图均已验证可达：
  - `Arc%20de%20Triomphe%20Paris.jpg`（法国）
  - `Grand%20Place%2C%20Brussels.jpg`（比利时）
  - `Zaanse%20Schans%20windmills.jpg`（荷兰）
  - `K%C3%B6lner%20Dom%20nachts%202013.jpg`（德国）
  - `Luxembourg%2C%20Vieille%20ville%2004-2021.jpg`（卢森堡）
- 文案逐字采用 `docs/superpowers/specs/2026-08-08-culture-section-design.md` 的「各国内容与配图」表
- 颜色变量沿用现有 `--acc` 内联样式（法国 `#0a84ff` / 比利时 `#ff3b30` / 荷兰 `#ff9f0a` / 德国 `#bf5af2` / 卢森堡 `#64d2ff`）
- 完成后 `python tools/check_page.py` 必须全 PASS；grep `class="country"|c-list|country-grid` 零残留

---

### Task 1: 横幅 CSS 样式 + 删除旧国家卡样式

**Files:**
- Modify: `index.html`（`<style>` 内：`/* Task 8 国家风情板块 */` 注释块整块替换）

**Interfaces:**
- Consumes: 现有变量 `--shadow`/`--shadow-lg`/`--line`/`--acc`；现有 `.reveal` 机制
- Produces: `.c-banner` / `.cb-media` / `.cb-img` / `.cb-shade` / `.cb-body` / `.cb-acc` / `.cb-head` / `.cb-flag` / `.cb-facts` / `.cb-desc` / `.cb-tags` / `.cb-fallback` 类——Task 2 的 HTML 依赖这些类名

- [ ] **Step 1: 替换旧样式块为横幅样式**

定位 `/* Task 8 国家风情板块 */` 注释到其 `@media(max-width:768px){.country-grid{grid-template-columns:1fr}}` 结束的整块（含 `.country-grid`、`.country`、`.c-flag`、`.country h3`、`.c-desc`、`.c-list`、`.c-list span` 共 7 条规则 + 1 条媒体查询），整块替换为：

```css
/* Task 8 国家风情横幅 */
.c-banner-stack{display:flex;flex-direction:column;gap:20px;padding-top:40px}
.c-banner{position:relative;min-height:300px;border-radius:24px;overflow:hidden;border:1px solid var(--line);box-shadow:var(--shadow);background:#1d1d1f;transition:box-shadow .35s}
.c-banner:hover{box-shadow:var(--shadow-lg)}
.cb-media{position:absolute;inset:0}
.cb-img{width:100%;height:100%;object-fit:cover;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.c-banner:hover .cb-img{transform:scale(1.05)}
.cb-fallback{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#e8e8ed,#f5f5f7);color:#3b3b40;font-weight:600;opacity:0}
.cb-media .cb-img[data-failed] + .cb-fallback{opacity:1}
.cb-shade{position:absolute;inset:0;background:linear-gradient(100deg,rgba(13,13,18,.85) 0%,rgba(13,13,18,.45) 45%,rgba(13,13,18,0) 78%)}
.cb-body{position:relative;padding:34px 40px;max-width:820px;color:#fff}
.cb-acc{position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--acc,#0071e3)}
.cb-head{display:flex;align-items:center;gap:12px}
.cb-flag{font-size:30px;line-height:1}
.cb-body h3{font-size:clamp(21px,3vw,27px);font-weight:700;letter-spacing:-.015em;color:#fff}
.cb-facts{font-size:13px;color:rgba(255,255,255,.72);margin-top:6px}
.cb-desc{font-size:14.5px;color:rgba(255,255,255,.92);margin-top:10px;line-height:1.7}
.cb-tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.cb-tags span{font-size:12.5px;color:#fff;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:5px 12px;backdrop-filter:blur(6px)}
/* 横幅交错渐显 */
.js .c-banner-stack>.reveal:nth-child(2){transition-delay:.08s}
.js .c-banner-stack>.reveal:nth-child(3){transition-delay:.16s}
.js .c-banner-stack>.reveal:nth-child(4){transition-delay:.24s}
.js .c-banner-stack>.reveal:nth-child(5){transition-delay:.32s}
@media(max-width:768px){
  .cb-body{padding:24px 20px}
  .cb-desc{font-size:13.5px}
  .c-banner{min-height:260px}
}
```

- [ ] **Step 2: 快速校验**

Run: `grep -c "c-banner" index.html` 应 ≥ 3（CSS 引用）；`grep -c "country-grid" index.html` 应为 0

- [ ] **Step 3: 提交**

```bash
git add index.html
git commit -m "style: 国家风情横幅样式（替换旧国家卡样式）"
```

---

### Task 2: 替换 #culture 区块 HTML（5 国横幅全量文案）

**Files:**
- Modify: `index.html`（`<section id="culture">…</section>` 整块）

**Interfaces:**
- Consumes: Task 1 的 `.c-banner` 等类名；spec 文案表
- Produces: 5 个 `<article class="c-banner reveal" style="--acc:…">` 结构——Task 3 的断言与目检依赖

- [ ] **Step 1: 替换整块 HTML**

定位 `<section id="culture">` 到对应 `</section>`（含 section-head 与 container country-grid 全部内容），替换为（文案逐字取自 spec）：

```html
  <section id="culture">
    <div class="section-head reveal">
      <div class="kicker">Local Flavor</div>
      <h2>国家风情</h2>
      <p>五国四味——把路上的风土人情装进心里，也装进胃里</p>
    </div>
    <div class="container c-banner-stack">
      <article class="c-banner reveal" style="--acc:#0a84ff">
        <div class="cb-media">
          <img class="cb-img" src="https://commons.wikimedia.org/wiki/Special:FilePath/Arc%20de%20Triomphe%20Paris.jpg?width=1600" alt="法国 · 凯旋门" loading="lazy" onerror="this.setAttribute('data-failed','')">
          <div class="cb-fallback">法国 · 凯旋门</div>
        </div>
        <div class="cb-shade"></div>
        <span class="cb-acc"></span>
        <div class="cb-body">
          <div class="cb-head"><span class="cb-flag">🇫🇷</span><h3>法国 · 艺术与咖啡</h3></div>
          <div class="cb-facts">首都 巴黎 · 语言 法语 · 货币 欧元</div>
          <p class="cb-desc">露天咖啡座是法国人的客厅——花神咖啡馆里萨特写下存在主义，清晨的牛角包配浓缩咖啡是每天的仪式。</p>
          <div class="cb-tags">
            <span>🍽 必吃：焗蜗牛 · 油封鸭腿 · 可丽饼 · 马卡龙</span>
            <span>✨ 必体验：铁塔晨光 · 塞纳河游船 · 蒙马特日落</span>
            <span>💡 冷知识：牛角包源自奥地利，19 世纪才传入法国</span>
            <span>🗣 实用语：Bonjour · Merci · L'addition, s'il vous plaît</span>
          </div>
        </div>
      </article>
      <article class="c-banner reveal" style="--acc:#ff3b30">
        <div class="cb-media">
          <img class="cb-img" src="https://commons.wikimedia.org/wiki/Special:FilePath/Grand%20Place%2C%20Brussels.jpg?width=1600" alt="比利时 · 布鲁塞尔大广场" loading="lazy" onerror="this.setAttribute('data-failed','')">
          <div class="cb-fallback">比利时 · 布鲁塞尔大广场</div>
        </div>
        <div class="cb-shade"></div>
        <span class="cb-acc"></span>
        <div class="cb-body">
          <div class="cb-head"><span class="cb-flag">🇧🇪</span><h3>比利时 · 巧克力与漫画</h3></div>
          <div class="cb-facts">首都 布鲁塞尔 · 语言 法语 / 荷语 · 货币 欧元</div>
          <p class="cb-desc">布鲁塞尔大广场被誉为欧洲最美客厅，撒尿小童的传说流传四百年——薯条与华夫饼在这里才是正统。</p>
          <div class="cb-tags">
            <span>🍽 必吃：薯条配美乃滋 · 列日华夫 · 青口 · 巧克力</span>
            <span>✨ 必体验：大广场夜景 · 圣于贝尔拱廊街 · 漫画墙</span>
            <span>💡 冷知识："法式薯条"其实是比利时人的发明——一战美军在比利时吃到后误以为来自法国</span>
            <span>🗣 实用语：Bonjour · Goedendag · Merci / Dank je wel</span>
          </div>
        </div>
      </article>
      <article class="c-banner reveal" style="--acc:#ff9f0a">
        <div class="cb-media">
          <img class="cb-img" src="https://commons.wikimedia.org/wiki/Special:FilePath/Zaanse%20Schans%20windmills.jpg?width=1600" alt="荷兰 · 风车村" loading="lazy" onerror="this.setAttribute('data-failed','')">
          <div class="cb-fallback">荷兰 · 风车村</div>
        </div>
        <div class="cb-shade"></div>
        <span class="cb-acc"></span>
        <div class="cb-body">
          <div class="cb-head"><span class="cb-flag">🇳🇱</span><h3>荷兰 · 风车与自行车</h3></div>
          <div class="cb-facts">首都 阿姆斯特丹 · 语言 荷兰语 · 货币 欧元</div>
          <p class="cb-desc">比海平面低 7 米的国度里，风车与运河是千年智慧的雕塑——骑行和游船，是打开阿姆斯特丹的正确方式。</p>
          <div class="cb-tags">
            <span>🍽 必吃：Stroopwafel · 生鲱鱼 · 高达奶酪</span>
            <span>✨ 必体验：运河日落游船 · 风车村 · 骑行</span>
            <span>💡 冷知识：荷兰自行车约 2,300 万辆，比人口（约 1,780 万）还多；约 1/4 国土低于海平面</span>
            <span>🗣 实用语：Goedemorgen · Dank je wel · De rekening, alstublieft</span>
          </div>
        </div>
      </article>
      <article class="c-banner reveal" style="--acc:#bf5af2">
        <div class="cb-media">
          <img class="cb-img" src="https://commons.wikimedia.org/wiki/Special:FilePath/K%C3%B6lner%20Dom%20nachts%202013.jpg?width=1600" alt="德国 · 科隆大教堂" loading="lazy" onerror="this.setAttribute('data-failed','')">
          <div class="cb-fallback">德国 · 科隆大教堂</div>
        </div>
        <div class="cb-shade"></div>
        <span class="cb-acc"></span>
        <div class="cb-body">
          <div class="cb-head"><span class="cb-flag">🇩🇪</span><h3>德国 · 哥特与啤酒</h3></div>
          <div class="cb-facts">首都 柏林 · 语言 德语 · 货币 欧元</div>
          <p class="cb-desc">科隆大教堂建了 632 年——哥特式巅峰之下，一小杯 Kölsch 配一根香肠，就是科隆人的下午茶。</p>
          <div class="cb-tags">
            <span>🍽 必吃：科隆香肠 · 酸菜 · Kölsch 啤酒</span>
            <span>✨ 必体验：大教堂登塔 · 爱情锁桥 · 莱茵河畔</span>
            <span>💡 冷知识：科隆大教堂建造历时 632 年（1248-1880）；正宗 Kölsch 只能在科隆酿造</span>
            <span>🗣 实用语：Guten Tag · Danke · Die Rechnung, bitte</span>
          </div>
        </div>
      </article>
      <article class="c-banner reveal" style="--acc:#64d2ff">
        <div class="cb-media">
          <img class="cb-img" src="https://commons.wikimedia.org/wiki/Special:FilePath/Luxembourg%2C%20Vieille%20ville%2004-2021.jpg?width=1600" alt="卢森堡 · 老城" loading="lazy" onerror="this.setAttribute('data-failed','')">
          <div class="cb-fallback">卢森堡 · 老城</div>
        </div>
        <div class="cb-shade"></div>
        <span class="cb-acc"></span>
        <div class="cb-body">
          <div class="cb-head"><span class="cb-flag">🇱🇺</span><h3>卢森堡 · 袖珍公国</h3></div>
          <div class="cb-facts">首都 卢森堡市 · 语言 卢森堡语 / 法语 / 德语 · 货币 欧元</div>
          <p class="cb-desc">欧盟最小的首都之一，却有欧洲最深的峡谷——站在 Calvarieberg 俯瞰老城，仿佛中世纪画卷铺展脚下。</p>
          <div class="cb-tags">
            <span>🍽 必吃：烟熏猪肉配蚕豆 · 李子挞 Quetschentaart</span>
            <span>✨ 必体验：Bock 地道 · Grund 峡谷 · 老城全景</span>
            <span>💡 冷知识：卢森堡 2020 年起全国公共交通免费（世界首例）；人均 GDP 常年全球前列</span>
            <span>🗣 实用语：Moien · Merci · Salut</span>
          </div>
        </div>
      </article>
    </div>
  </section>
```

- [ ] **Step 2: 零残留检查**

Run: `grep -c 'class="country' index.html` 应输出 0；`grep -c 'c-banner' index.html` 应 ≥ 30（样式+5 横幅×结构）

- [ ] **Step 3: 提交**

```bash
git add index.html
git commit -m "feat: 国家风情模块沉浸式横幅（5 国全量内容）"
```

---

### Task 3: 校验脚本断言同步 + 全量验证 + 目检

**Files:**
- Modify: `tools/check_page.py`（如有 culture 相关断言）
- Verify: `index.html`（check_page + Playwright）

**Interfaces:**
- Consumes: Task 2 的 `c-banner` 结构；现有 check_page 的图片可达性检查（自动覆盖新 5 图）

- [ ] **Step 1: 检查并更新 culture 断言**

Run: `grep -n "country\|c-list" tools/check_page.py`
- 若有 `class="country"` / `country-grid` / `c-list` 计数断言：改为 `must('5 个国家横幅', html.count('class="c-banner') == 5)`（注意 `c-banner-stack` 也含 `c-banner` 子串——用 `class="c-banner ` 带空格前缀精确匹配，或 `html.count('article class="c-banner')`）
- 若原断言为 `id="culture"` 存在性：无需改
- 若无相关断言：跳过本步，记下结论

- [ ] **Step 2: 运行校验**

Run: `python tools/check_page.py`
Expected: 全 PASS（含 5 张新横幅图片可达性 200）；若有 FAIL 按输出修复后重跑

- [ ] **Step 3: 浏览器目检（桌面 + 移动端）**

Run（node + playwright，`tools/qa-screenshots/` 输出截图）：
- 桌面 1280px：滚动到 `#culture`，断言 `.c-banner` 数量 = 5、`.cb-img` 全部 `naturalWidth > 0`、无 JS 报错；截图 `culture-banners-desktop.png`
- 移动 375px：断言文字不溢出（`document.body.scrollWidth <= 375`）；截图 `culture-banners-mobile.png`
- 悬停第一张横幅：断言 `.cb-img` 的 transform 变为 `scale(1.05)`（可选）

- [ ] **Step 4: 提交**

```bash
git add tools/check_page.py index.html
git commit -m "test: 国家风情横幅断言与目检"
```

---

## Self-Review 结论（写入计划时已核）

- **Spec 覆盖**：§结构→Task 2 ✓；§视觉（高度/遮罩/色条/hover/响应式）→Task 1 ✓；§各国内容与配图（5 国文案逐字）→Task 2 ✓；§技术要点（lazy 加载、reveal、零依赖）→Task 1/2 ✓；§验证（check_page 断言 + 目检 + 零残留）→Task 3 ✓
- **占位符**：无 TBD/TODO；全部 CSS 与 HTML 完整给出
- **一致性**：类名 `.c-banner/.cb-media/.cb-img/.cb-shade/.cb-body/.cb-acc/.cb-head/.cb-flag/.cb-facts/.cb-desc/.cb-tags/.cb-fallback` 在 Task 1 定义、Task 2 使用一致；图片 URL 与 spec 表一致（含 URL 编码）；`--acc` 五色与 spec 一致
