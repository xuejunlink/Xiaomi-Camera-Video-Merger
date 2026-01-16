# 小米、米家监控视频自动合并工具 (Xiaomi Video Merger Pro)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)
![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-green.svg)

小米/米家监控录制的视频通常是每分钟一个片段，存储结构细碎。本工具旨在将这些细碎的片段**无损、快速**地合并为一个完整的视频长片，并支持**音量增强**功能，解决监控录音偏小的问题。

---

## ✨ 核心功能

* **一键深度合并**：自动递归扫描选定目录及其所有子目录下的所有 MP4 片段。
* **按序无损合成**：按文件名（时间顺序）自动排列片段，采用视频流 `copy` 模式，合成极快且不损画质。
* **自定义音量增强**：支持 0-20dB 的音频增益调节，大幅提升监控录音的清晰度。
* **智能化命名**：输出文件自动命名为 `[video]_当前时间.mp4`，方便检索与管理。
* **全静默运行**：调用 FFmpeg 渲染时后台完全静默，不弹出任何黑色控制台窗口。
* **专业版 UI**：基于 `customtkinter` 打造的深色模式橙色主题界面，视觉体验更佳。

---

## 🚀 快速上手

### 1. 克隆/下载本项目
下载 `mivideo.py` 源代码到本地。

### 2. 安装必要环境
确保你已安装 Python 3.8+，然后在终端运行：
```bash
pip install customtkinter imageio-ffmpeg

### 3. 配置 FFmpeg

本工具依赖 FFmpeg 进行处理：

    开发环境：程序会自动尝试通过 imageio-ffmpeg 获取。

    生产环境：建议将 ffmpeg.exe 放在程序根目录下。
