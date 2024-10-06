import pyautogui
from pynput import keyboard
import os
from datetime import datetime
import time 
import random
import tkinter as tk
from threading import Thread

# Tạo các thư mục nếu chưa tồn tại
os.makedirs("data_2/up", exist_ok=True)
os.makedirs("data_2/right", exist_ok=True)
os.makedirs("data_2/down", exist_ok=True)
os.makedirs("data_2/auto", exist_ok=True)

# Biến toàn cục để lưu trạng thái mặc định là auto
global screenshot_state
screenshot_state = "auto"

# Hàm chụp màn hình và lưu vào thư mục tương ứng
def capture_screenshot(folder):
    screenshot = pyautogui.screenshot()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot.save(f"data_2/{folder}/{timestamp}.png")
    # print(f"Screenshot taken and saved in {folder} folder!")

# Hàm chụp màn hình tự động mỗi 1 giây
def auto_capture_screenshot():
    while True:
        capture_screenshot(screenshot_state)
        time.sleep(2)
    return

# Hàm xử lý khi một phím được nhấn
def on_press(key):
    global screenshot_state
    try:
        # Nếu phím mũi tên lên được nhấn, chụp màn hình và lưu vào thư mục up
        if key == keyboard.Key.up:
            screenshot_state = "up"
            time.sleep(random.uniform(0.2, 0.4))            
            capture_screenshot(screenshot_state)
            screenshot_state = "auto"
        # Nếu phím mũi tên phải được nhấn, chụp màn hình và lưu vào thư mục right
        elif key == keyboard.Key.right:
            screenshot_state = "right"
            time.sleep(random.uniform(0.3, 0.5))            
            capture_screenshot(screenshot_state)
            screenshot_state = "auto"
        # Nếu phím mũi tên xuống được nhấn, chụp màn hình và lưu vào thư mục down
        elif key == keyboard.Key.down:
            screenshot_state = "down"
            time.sleep(random.uniform(0.3, 0.7))            
            capture_screenshot(screenshot_state)
            screenshot_state = "auto"
    except AttributeError:
        pass

# Hàm để bắt đầu và kết thúc phần ghi lại
def start_recording():
    try:
        auto_capture_thread = Thread(target=auto_capture_screenshot)
        auto_capture_thread.start()
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("Recording stopped.")

# Giao diện để bắt đầu và kết thúc phần ghi lại
def start_button_clicked():
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    recording_thread = Thread(target=start_recording)
    recording_thread.start()

def stop_button_clicked():
    stop_button.config(state="disabled")
    start_button.config(state="normal")
    os._exit(0)

root = tk.Tk()
root.title("Screenshot Recorder")

start_button = tk.Button(root, text="Start Recording", command=start_button_clicked)
start_button.pack()

stop_button = tk.Button(root, text="Stop Recording", command=stop_button_clicked, state="disabled")
stop_button.pack()

root.mainloop()