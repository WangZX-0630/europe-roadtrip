#!/usr/bin/env python3
"""校验 index.html 结构完整性与数据完整性。用法: python tools/check_page.py"""
import re, sys, time, urllib.request
# Windows GBK 控制台兼容：统一 UTF-8 输出
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

html = open('index.html', encoding='utf-8').read()
errors = []

def must(label, cond):
    print(('PASS  ' if cond else 'FAIL  ') + label)
    if not cond:
        errors.append(label)

# 1. 板块结构（#map 已于 2026-08-08 合并入 #route，改为断言地图容器）
for sid in ['hero', 'route', 'itinerary', 'culture', 'budget', 'bookings', 'tips']:
    must(f'<section id="{sid}">', f'<section id="{sid}">' in html)
must('<footer>', '<footer>' in html)
must('id="map-canvas"', 'id="map-canvas"' in html)
must('5 个国家横幅', html.count('article class="c-banner ') == 5)

# 2. 导航锚点可解析
for m in re.finditer(r'href="#([\w-]+)"', html):
    aid = m.group(1)
    if aid != 'hero':
        must(f'导航锚点 #{aid} 有目标', f'id="{aid}"' in html)

# 3. 行程数据完整性
must('7 个行程板块', len(re.findall(r'class="day( reveal)?" data-day="\d"', html)) == 7)
tl = re.findall(r'<li class="tl">', html)
must(f'69 条时刻表记录 (实际 {len(tl)})', len(tl) == 69)
spots = re.findall(r'<article class="spot( reveal)?"', html)
must(f'景点卡数量 ({len(spots)} 张)', len(spots) >= 28)
meals = re.findall(r'<article class="meal( reveal)?"', html)
must(f'美食卡数量 ({len(meals)} 张)', len(meals) >= 13)
drives = re.findall(r'<tr class="drive">', html)
must(f'9 段驾驶数据 (实际 {len(drives)})', len(drives) == 9)
# SVG 概览图已于 2026-08-08 移除（功能并入 Leaflet 地图），改为断言地图距离标注
must('地图距离标注存在', 'leg-dist' in html)
must('Leaflet 引入', 'unpkg.com/leaflet' in html)

# 4. 模板残留检查（JS 渲染或占位符泄漏）
for bad in ['{{', 'TODO', 'TBD', 'undefined']:
    if bad == 'undefined':
        # Task 5 离线降级代码中的合法 JS 判空（typeof L === 'undefined'）不计入残留
        filtered = '\n'.join(l for l in html.splitlines() if "typeof L === 'undefined'" not in l)
        must(f'无模板残留 "{bad}"', bad not in filtered)
    else:
        must(f'无模板残留 "{bad}"', bad not in html)

# 5. 图片 URL 有效性（离线时跳过，仅警告）
# Wikimedia Special:FilePath 对高频请求有限流（429/HTTPError），加退避重试与请求间隔
imgs = re.findall(r'src="(https://commons\.wikimedia\.org[^"]+)"', html)
if imgs:
    for url in imgs:
        ok = False
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) EuropeTourPlan-check/1.1'})
                code = urllib.request.urlopen(req, timeout=8).status
                ok = code == 200
                must(f'图片可达 ({code}) {url.split("/")[-1][:40]}', ok)
                break
            except Exception as e:
                if attempt < 2:
                    time.sleep(3 * (attempt + 1))
                    continue
                must(f'图片检查跳过/失败 {url.split("/")[-1][:40]} ({type(e).__name__})', False)
        time.sleep(0.6)

print()
if errors:
    print(f'共 {len(errors)} 项失败'); sys.exit(1)
print('全部通过 ✓')
