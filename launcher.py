# launcher.py

import tkinter as tk
import subprocess

def choose_mode():
    selected = None

    def select(option):
        nonlocal selected
        selected = option
        window.destroy()

    window = tk.Tk()
    window.title("Choose Assistant Mode")
    window.geometry("420x220+550+300")
    window.attributes("-topmost", True)
    window.lift()

    label = tk.Label(window, text="🧠 How would you like to use your AI assistant today?", font=("Segoe UI", 12), wraplength=380)
    label.pack(pady=20)

    btn_frame = tk.Frame(window)
    btn_frame.pack()

    btn1 = tk.Button(btn_frame, text="🖼️ Screenshot OCR Mode", width=22, font=("Segoe UI", 11),
                     command=lambda: select("ocr"))
    btn1.grid(row=0, column=0, padx=10)

    btn2 = tk.Button(btn_frame, text="📄 PDF (RAG) Mode", width=22, font=("Segoe UI", 11),
                     command=lambda: select("rag"))
    btn2.grid(row=0, column=1, padx=10)

    window.mainloop()
    return selected

if __name__ == "__main__":
    mode = choose_mode()

    if mode == "ocr":
        # Launch your current assistant
        subprocess.run(["python", "cluelyclone.py"])
    elif mode == "rag":
        subprocess.run(["python", "rag.py"])
    else:
        print("❌ No option selected. Exiting.")