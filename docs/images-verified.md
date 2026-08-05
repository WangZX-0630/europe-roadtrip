# 已验证图片 URL（2026-08-05，全部 HEAD 200）

> 全部通过 `curl -sIL https://commons.wikimedia.org/wiki/Special:FilePath/<文件名>?width=<w>` 验证，
> 最终 HTTP 状态 200（302/301 跳转到 upload.wikimedia.org 后 200 视为有效）。
> 后续任务中所有图片一律使用本清单 URL。

| 用途 | URL |
|---|---|
| Hero 巴黎天际线 | https://commons.wikimedia.org/wiki/Special:FilePath/Eiffel%20Tower%20from%20Champ%20de%20Mars.jpg?width=1600 |
| 埃菲尔铁塔 | https://commons.wikimedia.org/wiki/Special:FilePath/Eiffel%20Tower%20from%20Champ%20de%20Mars.jpg?width=1200 |
| 罗浮宫 | https://commons.wikimedia.org/wiki/Special:FilePath/Louvre%20Museum%20Wikimedia%20Commons.jpg?width=1200 |
| 凯旋门 | https://commons.wikimedia.org/wiki/Special:FilePath/Arc%20de%20Triomphe%20Paris.jpg?width=1200 |
| 蒙马特 | https://commons.wikimedia.org/wiki/Special:FilePath/Sacre-coeur-montmartre.jpg?width=1200 |
| 奥赛 | https://commons.wikimedia.org/wiki/Special:FilePath/Musee%20d%27Orsay%20and%20Pont%20Royal%2C%20North-West%20view%20140402%201.jpg?width=1200 |
| 圣母院 | https://commons.wikimedia.org/wiki/Special:FilePath/NotreDameDeParis.jpg?width=1200 |
| 圣礼拜堂 | https://commons.wikimedia.org/wiki/Special:FilePath/Sainte%20Chapelle%20Interior%20Stained%20Glass.jpg?width=1200 |
| 布鲁塞尔大广场 | https://commons.wikimedia.org/wiki/Special:FilePath/Grand%20Place%2C%20Brussels.jpg?width=1200 |
| 撒尿小童 | https://commons.wikimedia.org/wiki/Special:FilePath/Bruxelles%20Manneken%20Pis.jpg?width=1200 |
| 风车村 | https://commons.wikimedia.org/wiki/Special:FilePath/Zaanse%20Schans%20windmills.jpg?width=1200 |
| 阿姆运河 | https://commons.wikimedia.org/wiki/Special:FilePath/Amsterdam%20Canals%20-%20July%202006.jpg?width=1200 |
| 水坝广场 | https://commons.wikimedia.org/wiki/Special:FilePath/Dam%20Amsterdam%207308.jpg?width=1200 |
| 国家博物馆 | https://commons.wikimedia.org/wiki/Special:FilePath/Rijksmuseum%20Amsterdam.jpg?width=1200 |
| 安妮之家 | https://commons.wikimedia.org/wiki/Special:FilePath/AnneFrankHouseAmsterdamtheNetherlands.jpg?width=1200 |
| 科隆大教堂 | https://commons.wikimedia.org/wiki/Special:FilePath/K%C3%B6lner%20Dom%20nachts%202013.jpg?width=1200 |
| 霍亨索伦桥 | https://commons.wikimedia.org/wiki/Special:FilePath/Hohenzollernbr%C3%BCcke%20K%C3%B6ln.jpg?width=1200 |
| 卢森堡峡谷 | https://commons.wikimedia.org/wiki/Special:FilePath/Bock%20casemates%2C%20Luxembourg%20-%20panoramio%20%282%29.jpg?width=1200 |
| 凡尔赛宫 | https://commons.wikimedia.org/wiki/Special:FilePath/Palace%20of%20Versailles%20Gardens%20France.jpg?width=1200 |
| 塞纳河 | https://commons.wikimedia.org/wiki/Special:FilePath/Seine%20River%20and%20the%20Eiffel%20Tower%2C%2027%20October%202012%20-%20panoramio.jpg?width=1200 |
| 杜乐丽 | https://commons.wikimedia.org/wiki/Special:FilePath/Paris%20Jardin%20des%20Tuileries%20printemps%202014.jpg?width=1200 |

## 换名记录（原候选 404，已换为真实文件名）

| 用途 | 原候选（404） | 替换为 |
|---|---|---|
| 奥赛 | Musée d'Orsay, North-West view, Paris 2017.jpg | Musee d'Orsay and Pont Royal, North-West view 140402 1.jpg |
| 圣母院 | Notre-Dame de Paris 2013-07-01.jpg | NotreDameDeParis.jpg |
| 圣礼拜堂 | Sainte-Chapelle Upper Chapel.jpg | Sainte Chapelle Interior Stained Glass.jpg |
| 撒尿小童 | Manneken pis Brussels.jpg | Bruxelles Manneken Pis.jpg |
| 水坝广场 | Dam Square Amsterdam.jpg | Dam Amsterdam 7308.jpg |
| 安妮之家 | Anne Frank House Amsterdam.jpg | AnneFrankHouseAmsterdamtheNetherlands.jpg |
| 科隆大教堂 | Kölner Dom bei Nacht.jpg | Kölner Dom nachts 2013.jpg |
| 霍亨索伦桥 | Hohenzollern Bridge and Cologne Cathedral.jpg | Hohenzollernbrücke Köln.jpg |
| 卢森堡峡谷 | Bock Casemates Luxembourg.jpg | Bock casemates, Luxembourg - panoramio (2).jpg |
| 凡尔赛宫 | Palace of Versailles from Gardens.jpg | Palace of Versailles Gardens France.jpg |
| 塞纳河 | Seine River and Eiffel Tower at dusk.jpg | Seine River and the Eiffel Tower, 27 October 2012 - panoramio.jpg |
| 杜乐丽 | Jardin des Tuileries, Paris.jpg | Paris Jardin des Tuileries printemps 2014.jpg |

> 注：真实文件名通过 Wikimedia Commons API（`action=query&list=search&srnamespace=6`）检索得到，
> 每个替换名均经 curl 终验 200。
