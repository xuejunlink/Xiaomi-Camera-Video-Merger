# 小米、米家监控视频自动合并工具 (Xiaomi-Camera-Video-Merger)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-green.svg)

小米/米家监控录制的视频通常是每分钟一个片段。本工具旨在将这些细碎的片段**全自动合并**为一个完整的视频长片，并支持**音量增强**功能。

---

## ✨ 核心功能

* **一键全自动合并**：递归扫描选定目录及其子目录下的所有 MP4 片段，按时间顺序合而为一。
* **自定义音量增强**：支持 0-20dB 的音频增益调节，解决监控视频声音太小的问题。
* **无损高速合成**：视频流采用 `copy` 模式，不重新编码，合成速度极快且画质零损失。
* **智能化命名**：输出文件自动命名为 `[video]_当前时间.mp4`，避免文件名冲突。
* **全静默后台**：调用 FFmpeg 渲染时后台完全静默，不会弹出任何黑色控制台窗口。
* **专业版 UI**：基于 `customtkinter` 打造，橙色暖调 UI 界面，操作更直观。

---

## 🚀 快速上手

### 1. 环境准备
确保电脑已安装 Python 3.8 或更高版本。

### 2. 安装依赖库
在终端运行：
```bash
pip install customtkinter imageio-ffmpeg
```

### 3. 获取 FFmpeg
建议将 `ffmpeg.exe` 放在本程序根目录下，以确保最佳兼容性。

### 4. 运行程序
```bash
python XiaomiTool.py
```

---

## 🎨 界面预览

![软件截图](https://github.com/你的用户名/你的仓库名/raw/main/screenshot.png)

---

## 📜 开源协议

本项目基于 **MIT License** 开源。
