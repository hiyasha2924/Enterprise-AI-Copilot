import tkinter as tk
from tkinter import scrolledtext
import pyperclip
import threading

class ChatPopup:
    def __init__(self, initial_instruction, screen_text, callback):
        self.window = tk.Tk()
        self.window.title("Cluely AI")
        self.window.geometry("900x500+300+200")
        self.window.resizable(True, True)

        self.chat_history = []  # stores (User, Assistant) messages
        self.screen_text = screen_text
        self.callback = callback

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.text_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, font=("Segoe UI", 12))
        self.text_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.text_area.config(state=tk.DISABLED)

        self.entry = tk.Entry(self.window, font=("Segoe UI", 12))
        self.entry.grid(row=1, column=0, sticky="ew", padx=10)
        self.entry.bind("<Return>", lambda e: self.send_message())

        button_frame = tk.Frame(self.window)
        button_frame.grid(row=2, column=0, pady=10)

        tk.Button(button_frame, text="📤 Send", command=self.send_message).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="📋 Copy Chat", command=self.copy_chat).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="❌ Close", command=self.window.destroy).pack(side=tk.LEFT, padx=10)

        self.entry.insert(0, initial_instruction)
        self.send_message()

    def copy_chat(self):
        chat_text = self.text_area.get("1.0", tk.END)
        pyperclip.copy(chat_text)

    def send_message(self):
        user_input = self.entry.get().strip()
        if not user_input:
            return

        self.chat_history.append(("User", user_input))
        self.update_chat_display("User", user_input)
        self.entry.delete(0, tk.END)

        self.update_chat_display("Assistant", "🤖 Thinking...")

        threading.Thread(target=self.get_assistant_response).start()

    def get_assistant_response(self):
        full_context = ""
        for role, msg in self.chat_history:
            prefix = "User:" if role == "User" else "Assistant:"
            full_context += f"{prefix} {msg.strip()}\n"

        full_prompt = f"{full_context.strip()}\n\nUse the following text as reference:\n{self.screen_text}"
        response = self.callback(full_prompt)

        self.chat_history.append(("Assistant", response))
        self.update_chat_display("Assistant", response, replace_last=True)

    def update_chat_display(self, role, message, replace_last=False):
        self.text_area.config(state=tk.NORMAL)
        if replace_last:
            self.text_area.delete("end-3l", tk.END)
        self.text_area.insert(tk.END, f"{role}: {message.strip()}\n\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.see(tk.END)

    def run(self):
        self.window.mainloop()
