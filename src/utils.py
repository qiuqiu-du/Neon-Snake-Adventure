import ctypes
import json
from datetime import datetime


def load_high_score(difficulty="hard"):
    try:
        with open("leaderboard.json", "r") as f:
            leaderboard_data = json.load(f)
            scores = [entry["score"] for entry in leaderboard_data.get(difficulty, [])]
            return max(scores) if scores else 0
    except:
        return 0


def save_game_result(score, elapsed_time, difficulty):
    try:
        # Load existing data or initialize if file doesn't exist
        try:
            with open("leaderboard.json", "r") as f:
                leaderboard_data = json.load(f)
        except:
            leaderboard_data = {
                "easy": [],
                "hard": []
            }

        # Create new entry
        entry = {
            "score": score,
            "time": float(f"{elapsed_time:.4f}"),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "difficulty": difficulty
        }

        # Add entry to the appropriate difficulty list
        leaderboard_data[difficulty].append(entry)

        # Save with improved formatting
        with open("leaderboard.json", "w") as f:
            json.dump(
                leaderboard_data,
                f,
                indent=4,  # 4-space indentation
                ensure_ascii=False,  # Preserve non-ASCII characters
                sort_keys=True  # Sort dictionary keys alphabetically
            )

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