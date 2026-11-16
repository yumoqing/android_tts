---
name: android-tts-repo
version: 1.0.0
description: android_tts
trigger_conditions:
  - 需要理解、修改或排障 android_tts 的代码
  - 在 android_tts 里定位入口、数据表、对外契约或构建方式
---

# android_tts 仓库技能

> 由仓库实际内容生成的骨架（README/目录/模型定义/契约/构建脚本逐项取证）。新增判断与坑位请直接在下面对应小节补充。

## 定位

**android_tts**

Use android native tts engine to pack as a pyttsx3 driver for android device

- 远端：`https://github.com/yumoqing/android_tts.git`
- 默认分支：`main`（共 12 个提交）
- 最近提交：2022-09-21 `412612f` bugfix
- 规模：5 个文件；Python 3

## 目录结构

- `android_tts/` — Python 包源码（模块本体）（2 个文件）
- 根文件：`README.md`、`requirements.txt`、`setup.py`

## 代码入口（顶层 Python）

- `setup.py`
- `android_tts/version.py`

## 构建与运行

- `setup.py`：`android_tts` v?，依赖 0 项
- `requirements.txt`：1 项（pyjnius）
- Python 包 `android_tts/`：`__init__.py`、`version.py`

## 建议阅读顺序

1. `README.md`

