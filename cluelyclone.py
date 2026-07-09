import pyautogui
from PIL import Image
import pytesseract
import time
from popup import ChatPopup
from llm import ask_llm
from input_mode_selector import ask_input_mode

def get_screenshot_text():
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    return pytesseract.image_to_string(Image.open("screenshot.png"))

# ⏳ Wait 10 seconds before capturing screen
print("⏳ Waiting 10 seconds...")
time.sleep(10)

# 📸 Get screen text
screen_text = get_screenshot_text()

if not screen_text.strip():
    popup = ChatPopup("⚠️ No text detected on screen.", "", lambda _: "Try again.")
    popup.run()
else:
    # 🎤 Ask user for input mode
    mode = ask_input_mode()

    if mode == "voice":
        from voice_prompt import get_voice_prompt
        user_prompt = get_voice_prompt()
        if not user_prompt:
            from prompt import get_user_prompt
            user_prompt = get_user_prompt()
    elif mode == "text":
        from prompt import get_user_prompt
        user_prompt = get_user_prompt()
    else:
        user_prompt = None

    if not user_prompt:
        popup = ChatPopup("❗ No instruction provided.", screen_text, lambda _: "Prompt missing.")
        popup.run()
    else:
        chat = ChatPopup(user_prompt, screen_text, ask_llm)
        chat.run()
