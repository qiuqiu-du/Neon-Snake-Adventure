import ctypes

def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))


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