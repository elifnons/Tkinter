
import customtkinter as ctk
from tkinter import messagebox
import sqlite3

class AuthWindow:
    def __init__(self, app):
        self.app = app
        self.app.clear_screen()
        self.app.root.configure(bg=self.app.bg_color)

        ctk.CTkLabel(self.app.root, text=self.app.tr("login_title"), font=("Helvetica", 22, "bold"),
                     text_color=self.app.text_color).pack(pady=60)

        ctk.CTkLabel(self.app.root, text=self.app.tr("user"), text_color=self.app.text_color).pack()
        self.user_ent = ctk.CTkEntry(self.app.root, width=200)
        self.user_ent.pack(pady=5)

        ctk.CTkLabel(self.app.root, text=self.app.tr("pass"), text_color=self.app.text_color).pack()
        self.pass_ent = ctk.CTkEntry(self.app.root, show="*", width=200)
        self.pass_ent.pack(pady=5)

        ctk.CTkButton(self.app.root, text=self.app.tr("login"), width=200, fg_color="#ec3b83",
                      command=self.login).pack(pady=10)
        ctk.CTkButton(self.app.root, text=self.app.tr("signup"), width=200, fg_color="#2a52be",
                      command=self.signup).pack(pady=5)

    def signup(self):
        user, pw = self.user_ent.get().strip(), self.pass_ent.get().strip()
        if not user or not pw:
            messagebox.showerror("Error", self.app.tr("err_empty"))
            return
        try:
            self.app.db.query("INSERT INTO users VALUES (?, ?)", (user, pw))
            messagebox.showinfo("Success", self.app.tr("succ_acc"))
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", self.app.tr("err_user"))

    def login(self):
        user, pw = self.user_ent.get().strip(), self.pass_ent.get().strip()
        res = self.app.db.query("SELECT * FROM users WHERE username=? AND password=?", (user, pw)).fetchone()
        if res:
            self.app.current_user = user
            self.app.show_main_menu()
        else:
            messagebox.showerror("Error", self.app.tr("err_auth"))