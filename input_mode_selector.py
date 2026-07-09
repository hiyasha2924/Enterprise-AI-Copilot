import tkinter as tk

def ask_input_mode():
    choice = None

    def select(mode):
        nonlocal choice
        choice = mode
        window.destroy()

    window = tk.Tk()
    window.title("Choose Input Mode")
    window.geometry("400x180+600+300")
    window.attributes("-topmost", True)
    window.lift()

    label = tk.Label(window, text="How would you like to give your instruction?", font=("Segoe UI", 12))
    label.pack(pady=20)

    btn_frame = tk.Frame(window)
    btn_frame.pack()

    speak_btn = tk.Button(btn_frame, text="🎤 Speak", font=("Segoe UI", 11), width=12, command=lambda: select("voice"))
    speak_btn.grid(row=0, column=0, padx=10)

    write_btn = tk.Button(btn_frame, text="⌨️ Type", font=("Segoe UI", 11), width=12, command=lambda: select("text"))
    write_btn.grid(row=0, column=1, padx=10)

    window.mainloop()
    return choice
