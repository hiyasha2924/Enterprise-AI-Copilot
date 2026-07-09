import tkinter as tk

def get_user_prompt():
    prompt_text = None

    def submit():
        nonlocal prompt_text
        prompt_text = entry.get().strip()
        window.destroy()

    window = tk.Tk()
    window.title("Cluely Prompt")
    window.geometry("500x150+500+300")
    window.attributes("-topmost", True)
    window.focus_force()
    window.lift()

    label = tk.Label(window, text="What should I do with the extracted text?", font=("Segoe UI", 12))
    label.pack(pady=10)

    entry = tk.Entry(window, width=60, font=("Segoe UI", 12))
    entry.pack(pady=5)
    entry.focus()

    btn = tk.Button(window, text="OK", command=submit, font=("Segoe UI", 10))
    btn.pack(pady=10)

    window.bind('<Return>', lambda event: submit())
    window.mainloop()

    return prompt_text
