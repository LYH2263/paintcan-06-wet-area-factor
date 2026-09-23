# 16-paintcan（刷墙涂料）

Paintcan — 墙面积 − 门窗开洞；按涂布率与遍数换升数

## 启动

```bash
docker compose up --build
```

| 入口 | 地址 |
| --- | --- |
| 前端 | http://localhost:4500 |
| API | http://localhost:9500 |

## 主链

房间墙面减门窗 → 涂料升数 → 用量清单

## 潮湿区系数

房间可标记为潮湿区（房间详情页开关）。潮湿区的墙面净面积先乘潮湿系数（设置页维护，缺省 1）再按涂布率换升数；系数 ≤ 0 时估漆整单拒绝且不写记录。持久化的估算记录钉选当次的潮湿标记、系数、折算净面积与升数，`GET /api/history/{id}` 原样取回，改默认系数不影响旧记录。

## 技术栈

Python 3.12 + FastAPI + SQLite；Vue 3 + Vite + Nginx。
