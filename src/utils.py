import ctypes
import base64
import json
import os
from cryptography.fernet import Fernet
from datetime import datetime

FERNET_KEY = b'sDPp3RHHsVXY_IqpMNKR5jKXB9QmIWn56hINrpbP-ys='  # 示例密钥，应替换为安全密钥
cipher_suite = Fernet(FERNET_KEY)


def encrypt_data(data: dict) -> bytes:
    """encrypt data"""
    return cipher_suite.encrypt(json.dumps(data).encode('utf-8'))

def decrypt_data(encrypted: bytes) -> dict:
    """decrypt data"""
    return json.loads(cipher_suite.decrypt(encrypted).decode('utf-8'))

def load_high_score(difficulty="hard"):
    """加载指定难度的最高分（带简单加密）"""
    try:
        if os.path.exists("leaderboard.enc"):
            with open("leaderboard.enc", "rb") as f:
                encrypted_data = f.read()
                leaderboard_data = decrypt_data(encrypted_data)
                scores = [entry["score"] for entry in leaderboard_data.get(difficulty, [])]
                return max(scores) if scores else 0
        else:
            return 0
    except Exception as e:
        print(f"Error loading high score: {e}")
    return 0



def save_game_result(score, elapsed_time, difficulty):
    """保存游戏结果（带简单加密）"""
    try:
        # 加载或初始化数据
        try:
            with open("leaderboard.enc", "rb") as f:
                leaderboard_data = decrypt_data(f.read())
        except:
            leaderboard_data = {"easy": [], "hard": []}

        # 创建新记录
        new_entry = {
            "score": score,
            "time": float(f"{elapsed_time:.4f}"),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "difficulty": difficulty
        }

        # 更新数据
        leaderboard_data[difficulty].append(new_entry)

        # 加密保存
        with open("leaderboard.enc", "wb") as f:
            f.write(encrypt_data(leaderboard_data))

    except Exception as e:
        print(f"Error saving game result: {e}")


def set_english_input():
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()

        # English-America 0x0409
        ctypes.windll.user32.PostMessageW(hwnd, 0x50, 0, 0x0409)

    except :
        try:
            # Chinese (Simplified China) 0x0804
            ctypes.windll.user32.PostMessageW(hwnd, 0x50, 0, 0x0804)

            # Shift
            ctypes.windll.user32.keybd_event(0xA0, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xA0, 0, 2, 0)
        except:
            pass