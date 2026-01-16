import os
import sys
import subprocess
import threading
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox
from imageio_ffmpeg import get_ffmpeg_exe

# --- 全局风格配置 ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")  # 使用蓝色底色，手动控制橙色按钮


class XiaomiFusionProfessional(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 设置正式的程序标题
        self.title("小米、米家监控视频合并工具")
        self.geometry("850x700")

        # 核心变量
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.volume_boost = ctk.IntVar(value=0)
        self.is_running = False

        # 橙色主题色配置
        self.theme_orange = "#e67e22"
        self.theme_orange_hover = "#d35400"

        # 获取 FFmpeg 路径
        self.ffmpeg_path = self._get_ffmpeg_path()

        self._build_ui()

    def _get_ffmpeg_path(self):
        if getattr(sys, 'frozen', False):
            bundle = os.path.join(sys._MEIPASS, "ffmpeg.exe")
            if os.path.exists(bundle): return bundle
        try:
            return get_ffmpeg_exe()
        except:
            return "ffmpeg.exe"

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # 1. 顶部标题区域 (双行标题)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=30, pady=(35, 15), sticky="w")

        ctk.CTkLabel(header_frame, text="小米、米家监控视频合并工具",
                     font=("微软雅黑", 22, "bold"), text_color=self.theme_orange).pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Xiaomi Camera Video Merger",
                     font=("Segoe UI", 14), text_color="#AAAAAA").pack(anchor="w", padx=2)

        # 2. 核心路径卡片
        path_card = ctk.CTkFrame(self, fg_color="#252525", corner_radius=12, border_width=1, border_color="#333333")
        path_card.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
        path_card.grid_columnconfigure(1, weight=1)

        # 来源目录
        ctk.CTkLabel(path_card, text="视频来源 (Source Directory)", font=("微软雅黑", 12, "bold")).grid(row=0, column=0,
                                                                                                        padx=20,
                                                                                                        pady=(20, 0),
                                                                                                        sticky="w")
        self.entry_in = ctk.CTkEntry(path_card, textvariable=self.input_path,
                                     placeholder_text="选择包含监控视频的文件夹...", height=38)
        self.entry_in.grid(row=1, column=0, columnspan=2, padx=20, pady=8, sticky="ew")
        ctk.CTkButton(path_card, text="浏览", width=90, height=38,
                      fg_color=self.theme_orange, hover_color=self.theme_orange_hover,
                      command=lambda: self.browse("in")).grid(row=1, column=2, padx=(0, 20))

        # 保存目录
        ctk.CTkLabel(path_card, text="输出保存 (Output Destination)", font=("微软雅黑", 12, "bold")).grid(row=2,
                                                                                                          column=0,
                                                                                                          padx=20,
                                                                                                          pady=(10, 0),
                                                                                                          sticky="w")
        self.entry_out = ctk.CTkEntry(path_card, textvariable=self.output_path,
                                      placeholder_text="合并后的成片保存位置...", height=38)
        self.entry_out.grid(row=3, column=0, columnspan=2, padx=20, pady=8, sticky="ew")
        ctk.CTkButton(path_card, text="浏览", width=90, height=38,
                      fg_color=self.theme_orange, hover_color=self.theme_orange_hover,
                      command=lambda: self.browse("out")).grid(row=3, column=2, padx=(0, 20), pady=(0, 20))

        # 3. 音量配置卡片
        vol_card = ctk.CTkFrame(self, fg_color="#252525", corner_radius=12, border_width=1, border_color="#333333")
        vol_card.grid(row=2, column=0, padx=30, pady=10, sticky="ew")
        vol_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(vol_card, text="音频增益调节 (Volume Boost)", font=("微软雅黑", 12, "bold")).grid(row=0, column=0,
                                                                                                       padx=20,
                                                                                                       pady=(15, 0),
                                                                                                       sticky="w")
        vol_inner = ctk.CTkFrame(vol_card, fg_color="transparent")
        vol_inner.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="ew")

        self.vol_label = ctk.CTkLabel(vol_inner, text="0 dB", font=("Consolas", 24, "bold"),
                                      text_color=self.theme_orange, width=90)
        self.vol_label.pack(side="left")
        self.vol_slider = ctk.CTkSlider(vol_inner, from_=0, to=20, number_of_steps=4,
                                        variable=self.volume_boost, command=self._update_vol,
                                        button_color=self.theme_orange, button_hover_color=self.theme_orange_hover)
        self.vol_slider.pack(side="left", fill="x", expand=True, padx=20)

        # 4. 日志控制台
        self.console = ctk.CTkTextbox(self, fg_color="#121212", border_width=1, border_color="#333333",
                                      font=("Consolas", 12))
        self.console.grid(row=3, column=0, padx=30, pady=10, sticky="nsew")
        self.rowconfigure(3, weight=1)

        # 5. 底部动作区
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=4, column=0, padx=30, pady=(5, 30), sticky="ew")

        self.progress = ctk.CTkProgressBar(action_frame, height=12, progress_color=self.theme_orange)
        self.progress.pack(fill="x", pady=(0, 15))
        self.progress.set(0)

        self.btn_run = ctk.CTkButton(action_frame, text="🚀 立即开始执行合并任务", height=60,
                                     font=("微软雅黑", 18, "bold"),
                                     fg_color=self.theme_orange, hover_color=self.theme_orange_hover,
                                     command=self.start_task)
        self.btn_run.pack(fill="x")

    def _update_vol(self, v):
        self.vol_label.configure(text=f"{int(v)} dB")

    def browse(self, m):
        p = filedialog.askdirectory()
        if p:
            if m == "in":
                self.input_path.set(p)
                if not self.output_path.get(): self.output_path.set(p)
            else:
                self.output_path.set(p)

    def log(self, t):
        self.console.insert("end", f"> {t}\n");
        self.console.see("end")

    def start_task(self):
        if not self.input_path.get(): return messagebox.showwarning("提示", "请先选择视频所在的文件夹")
        self.is_running = True
        self.btn_run.configure(state="disabled", text="正在全力合成中...")
        self.console.delete("1.0", "end")
        threading.Thread(target=self.engine_logic, daemon=True).start()

    def engine_logic(self):
        try:
            in_dir, out_dir = self.input_path.get(), self.output_path.get()
            vol = self.volume_boost.get()

            self.log("正在执行深度扫描...")
            video_files = []
            for r, d, fs in os.walk(in_dir):
                for f in fs:
                    # 排除已生成的成品文件
                    if f.lower().endswith(".mp4") and "[video]" not in f and "_merged" not in f:
                        video_files.append(os.path.join(r, f))

            if not video_files:
                self.log("❌ 未能在目录中找到有效的 MP4 视频文件。")
                return self.reset_ui()

            video_files.sort()
            self.log(f"成功识别到 {len(video_files)} 个片段，准备执行一键合并...")

            # 命名规则：[video] + [当前时间]
            now_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"[video]_{now_time}.mp4"
            output_full_path = os.path.join(out_dir, output_name)

            # 临时列表文件
            tmp_list_path = os.path.join(out_dir, f"fusion_list_{now_time}.txt")

            self.progress.set(0.1)

            # --- 修复路径语法问题，确保 f-string 中没有反斜杠 ---
            with open(tmp_list_path, "w", encoding="utf-8") as f:
                for v_path in video_files:
                    # 预处理：将路径中的反斜杠替换为正斜杠，并存入变量
                    safe_p = v_path.replace('\\', '/')
                    # 写入列表文件，f-string 内部只引用处理好的 safe_p 变量
                    f.write(f"file '{safe_p}'\n")

            self.log(f"任务启动：音量设定 +{vol}dB，正在调用 FFmpeg...")
            self.progress.set(0.3)

            # FFmpeg 命令执行 (0x08000000 屏蔽窗口)
            cmd = [
                self.ffmpeg_path, '-f', 'concat', '-safe', '0', '-i', tmp_list_path,
                '-c:v', 'copy',
                '-af', f'volume={vol}dB',
                '-c:a', 'aac', '-b:a', '192k',
                output_full_path, '-y'
            ]

            process = subprocess.run(
                cmd,
                creationflags=0x08000000,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if os.path.exists(tmp_list_path):
                os.remove(tmp_list_path)

            if process.returncode == 0:
                self.progress.set(1.0)
                self.log("✅ 处理成功完成！")
                self.log(f"保存路径: {output_full_path}")
                messagebox.showinfo("任务完成", f"合并已完成！\n\n文件名：{output_name}")
            else:
                self.log("❌ 合并失败。FFmpeg 报错详情：")
                self.log(process.stderr.decode('utf-8', 'ignore'))

        except Exception as e:
            self.log(f"🔥 程序运行异常: {str(e)}")
        finally:
            self.reset_ui()

    def reset_ui(self):
        self.btn_run.configure(state="normal", text="🚀 立即开始执行合并任务")
        self.is_running = False


if __name__ == "__main__":
    app = XiaomiFusionProfessional()
    app.mainloop()