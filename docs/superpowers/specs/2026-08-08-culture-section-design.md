# 「国家风情」模块沉浸式改版 · 设计文档

> 日期：2026-08-08 · 状态：已获用户批准（"ok"）· 范围：`index.html` 的 `#culture` 区块 + `tools/check_page.py` 断言同步

## 背景与目标

现状：`#culture` 区块为 5 张扁平小卡（国旗 emoji + 标题 + 一段描述 + 2 个标签行），内容与视觉均过于简单。

用户选定方向：**沉浸视觉型 + 全宽横幅式 + 视觉内容双升级**。

目标：
1. 每国一张全宽大图横幅，与 hero 首屏风格呼应，视觉冲击力强
2. 内容从 2 个标签扩充为 5 项结构化信息（关键数字 / 描述 / 必吃 / 必体验 / 冷知识 / 实用语）
3. 保持纯静态 HTML/CSS、零新依赖、保留 `#culture` 锚点与 reveal 动效体系

## 结构设计

每个国家一个 `<article class="c-banner">`，上下排列：

```
<section id="culture">
  <div class="section-head reveal">（kicker/h2/描述，微调）</div>
  <div class="container c-banner-stack">
    <article class="c-banner reveal" style="--acc:#0a84ff">
      <div class="cb-media"><img class="cb-img" src="…?width=1600" alt="法国" loading="lazy" onerror="…"></div>
      <div class="cb-body">
        <div class="cb-head"><span class="cb-flag">🇫🇷</span><h3>法国 · 艺术与咖啡</h3></div>
        <div class="cb-facts">首都 巴黎 · 语言 法语 · 货币 欧元</div>
        <p class="cb-desc">露天咖啡座是法国人的客厅……</p>
        <div class="cb-tags">
          <span>🍽 必吃：焗蜗牛 · 油封鸭腿 · 可丽饼 · 马卡龙</span>
          <span>✨ 必体验：铁塔晨光 · 塞纳河游船 · 蒙马特日落</span>
          <span>💡 冷知识：牛角包源自奥地利，19 世纪才传入法国</span>
          <span>🗣 实用语：Bonjour · Merci · L'addition, s'il vous plaît</span>
        </div>
      </div>
    </article>
    <!-- × 5 -->
  </div>
</section>
```

## 视觉设计

| 项 | 规格 |
|---|---|
| 横幅高度 | `min-height:300px`（移动端自适应撑高） |
| 圆角 / 阴影 | 24px / 现有 `--shadow` 体系 |
| 背景图 | `object-fit:cover`，`.cb-img` 绝对定位铺满 |
| 渐变遮罩 | `linear-gradient(100deg, rgba(13,13,18,.85) 0%, rgba(13,13,18,.45) 45%, rgba(13,13,18,0) 78%)`，覆盖全幅，文字叠于左侧 |
| 文字 | 白色系（与 hero 一致）：标题 22-26px bold；facts 13px 半透明白；描述 14.5px；标签为半透明白底胶囊（`rgba(255,255,255,.14)` + 白字） |
| 顶部色条 | 横幅左侧 4px `--acc` 竖条（保留现有国家色系：法国蓝 / 比利时红 / 荷兰橙 / 德国紫 / 卢森堡青） |
| hover | 图片 `scale(1.05)` 缓慢放大（`.6s cubic-bezier(.2,.8,.2,1)`）+ 横幅阴影加深 |
| 进入动效 | 复用 `.reveal` + 新增交错延迟（5 个横幅依次 0.08s） |
| 响应式 | ≤768px：facts/描述正常换行，标签纵向排列 |

## 各国内容与配图

配图全部使用已验证可达的 Wikimedia Commons 文件（`Special:FilePath/<编码名>?width=1600`）：

| 国家 | 色条 | 图片 | 标题 |
|---|---|---|---|
| 法国 | `#0a84ff` | `Arc de Triomphe Paris.jpg` | 法国 · 艺术与咖啡 |
| 比利时 | `#ff3b30` | `Grand Place, Brussels.jpg` | 比利时 · 巧克力与漫画 |
| 荷兰 | `#ff9f0a` | `Zaanse Schans windmills.jpg` | 荷兰 · 风车与自行车 |
| 德国 | `#bf5af2` | `Kölner Dom nachts 2013.jpg` | 德国 · 哥特与啤酒 |
| 卢森堡 | `#64d2ff` | `Luxembourg, Vieille ville 04-2021.jpg` | 卢森堡 · 袖珍公国 |

**法国**
- 描述：露天咖啡座是法国人的客厅——花神咖啡馆里萨特写下存在主义，清晨的牛角包配浓缩咖啡是每天的仪式。
- 数字：首都 巴黎 · 语言 法语 · 货币 欧元
- 必吃：焗蜗牛 · 油封鸭腿 · 可丽饼 · 马卡龙
- 必体验：铁塔晨光 · 塞纳河游船 · 蒙马特日落
- 冷知识：牛角包源自奥地利，19 世纪才传入法国
- 实用语：Bonjour · Merci · L'addition, s'il vous plaît

**比利时**
- 描述：布鲁塞尔大广场被誉为欧洲最美客厅，撒尿小童的传说流传四百年——薯条与华夫饼在这里才是正统。
- 数字：首都 布鲁塞尔 · 语言 法语/荷语 · 货币 欧元
- 必吃：薯条配美乃滋 · 列日华夫 · 青口 · 巧克力
- 必体验：大广场夜景 · 圣于贝尔拱廊街 · 漫画墙
- 冷知识："法式薯条"其实是比利时人的发明——一战美军在比利时吃到后误以为来自法国
- 实用语：Bonjour · Goedendag · Merci / Dank je wel

**荷兰**
- 描述：比海平面低 7 米的国度里，风车与运河是千年智慧的雕塑——骑行和游船，是打开阿姆斯特丹的正确方式。
- 数字：首都 阿姆斯特丹 · 语言 荷兰语 · 货币 欧元
- 必吃：Stroopwafel · 生鲱鱼 · 高达奶酪
- 必体验：运河日落游船 · 风车村 · 骑行
- 冷知识：荷兰自行车约 2,300 万辆，比人口（约 1,780 万）还多；约 1/4 国土低于海平面
- 实用语：Goedemorgen · Dank je wel · De rekening, alstublieft

**德国**
- 描述：科隆大教堂建了 632 年——哥特式巅峰之下，一小杯 Kölsch 配一根香肠，就是科隆人的下午茶。
- 数字：首都 柏林 · 语言 德语 · 货币 欧元
- 必吃：科隆香肠 · 酸菜 · Kölsch 啤酒
- 必体验：大教堂登塔 · 爱情锁桥 · 莱茵河畔
- 冷知识：科隆大教堂建造历时 632 年（1248-1880）；正宗 Kölsch 只能在科隆酿造
- 实用语：Guten Tag · Danke · Die Rechnung, bitte

**卢森堡**
- 描述：欧盟最小的首都之一，却有欧洲最深的峡谷——站在 Calvarieberg 俯瞰老城，仿佛中世纪画卷铺展脚下。
- 数字：首都 卢森堡市 · 语言 卢森堡语/法语/德语 · 货币 欧元
- 必吃：烟熏猪肉配蚕豆 · 李子挞 Quetschentaart
- 必体验：Bock 地道 · Grund 峡谷 · 老城全景
- 冷知识：卢森堡 2020 年起全国公共交通免费（世界首例）；人均 GDP 常年全球前列
- 实用语：Moien · Merci · Salut

## 技术要点

- 纯静态 HTML/CSS：新增 `.c-banner` 系列样式（约 30 行 CSS），删除 `.country` 旧样式（或保留无害——删除更干净）
- 图片懒加载 `loading="lazy"` + `onerror` 文字兜底（沿用现有 `.photo-fallback` 模式，横幅内嵌 fallback 层）
- 保留 `id="culture"` 与导航锚点；`section-head` 副标题文案微调
- 动效：`.reveal` 已有；5 个横幅的 stagger 延迟用 nth-child 规则（与 spot-grid 模式一致）

## 验证

- `tools/check_page.py`：`country` 卡数量断言（5 张 `.country`）需改为新结构断言（5 张 `.c-banner` + 5 张图片可达）
- 浏览器目检：桌面/375px 移动端横幅渲染、图片加载、hover 放大、reveal 交错生效
- 零残留：`class="country"`、`c-list` 旧类无残留

## 范围外（不包含）

- 不动其他区块；不新增图片资源（全部复用已验证图）；不做点击切换等复杂交互
