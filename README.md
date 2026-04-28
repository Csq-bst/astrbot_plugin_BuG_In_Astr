<div align="center">

# BuG_In_Astr

_✨ AstrBot 布吉岛（BugLand）Minecraft 服务器数据查询插件 ✨_

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

[![GitHub](https://img.shields.io/badge/作者-醋酸铅糖不是糖-blue)](https://github.com/Csq-bst)

</div>

## 🤝 介绍

通过 AstrBot 查询你在 Minecraft 服务器 **布吉岛**（BugLand）中的游戏数据，包括玩家信息、公会、排行榜、比赛详情等。

## 📦 安装

在 AstrBot 插件市场搜索 `astrbot_plugin_BuG_In_Astr` 安装即可。或克隆到插件目录：

```bash
cd /AstrBot/data/plugins
git clone https://github.com/Csq-bst/astrbot_plugin_BuG_In_Astr
```

## ⌨️ 配置

前往插件配置面板，填写 `auth_key`（API 鉴权 Key，从布吉岛官网获取）。

## 🐔 使用说明

### 一、基础说明

- 使用 `/register <游戏ID>` 绑定你的游戏账号
- 之后可通过 `/bjd` 指令组查询各类数据
- LLM 工具会在对话中被自动调用，无需手动输入指令

### 二、命令一览表

| 命令 | 别名 | 权限 | 参数 | 功能说明 |
|------|------|------|------|----------|
| /register | 绑定 | ALL | `<游戏ID>` | 绑定 QQ 到游戏 ID |
| /unbind | 解绑 | ALL | - | 解除绑定 |
| /update_auth_key | - | ADMIN | `<key>` | 更新 API 鉴权密钥 |
| /bjd player | - | ALL | - | 查询玩家基本信息 |
| /bjd guild | - | ALL | - | 查询公会信息 |
| /bjd leaderboard | - | ALL | - | 查询排行榜数据 |
| /bjd stats | - | ALL | `<游戏类型>` | 查询游戏统计数据（bedwars, skywars 等） |
| /bjd log | - | ALL | `[页码]` | 查询对局记录 |
| /bjd match | - | ALL | `<日期>` | 查询比赛详情（yyyy-MM-dd HH:mm:ss） |
| /bjd 2025 | - | ALL | - | 查询 2025 年度总结 |
| /bjd list | - | ADMIN | - | 查看所有绑定记录 |
| /bjdhelp | - | ALL | - | 查看帮助 |

### 三、使用示例

```text
/register Steve
/绑定 Steve
/bjd player
/bjd guild
/bjd stats bedwars
/bjd match 2025-01-01 12:00:00
/bjd log
/bjd list
```

## 💡 TODO

- [x] QQ 绑定游戏 ID
- [x] 玩家基本信息查询
- [x] 公会信息查询
- [x] 排行榜查询
- [x] 游戏数据查询
- [x] 对局记录查询
- [x] 比赛详情查询
- [x] 2025 年度总结
- [x] LLM 工具调用

## 👥 贡献指南

- 🌟 Star 这个项目！
- 🐛 提交 Issue 报告问题
- 🔧 提交 Pull Request 改进代码

## 📌 注意事项

- 请先在插件面板配置 `auth_key`
- 使用前请先通过 `/register` 绑定游戏 ID