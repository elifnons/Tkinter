
import customtkinter as ctk

class SettingsWindow:
    def __init__(self, app):
        self.app = app
        self.set_win = ctk.CTkToplevel(self.app.root)
        self.set_win.title(self.app.tr("settings"))
        self.set_win.geometry("350x450")
        self.set_win.after(10, self.set_win.lift)
        self.set_win.grab_set()

        ctk.CTkLabel(self.set_win, text=self.app.tr("theme"), font=("Arial", 14, "bold")).pack(pady=10)

        themes = [("Classic", "#242424", "#3b3b3b", "white"),
                  ("Midnight", "#1a1a2e", "#16213e", "#e94560"),
                  ("Forest", "#1b3022", "#236940", "#ecf39e"),
                  ("Cyberpunk", "#2b213a", "#ff0055", "#00fff5"),
                  ("Sepia", "#3d2b1f", "#6f4e37", "#f5ebe0"),
                  ("pastel","#ffe4e9", "#d8bfd8", "#443d44" )]

        for name, bg, btn, txt in themes:
            ctk.CTkButton(self.set_win, text=name, width=150,
                          command=lambda b=bg, bt=btn, t=txt: self.change_theme(b, bt, t)).pack(pady=2)

        ctk.CTkLabel(self.set_win, text=self.app.tr("lang_sel"), font=("Arial", 14, "bold")).pack(pady=10)
        ctk.CTkButton(self.set_win, text="English", width=150, command=lambda: self.change_lang("en")).pack(pady=2)
        ctk.CTkButton(self.set_win, text="Türkçe", width=150, command=lambda: self.change_lang("tr")).pack(pady=2)

    def change_theme(self, bg, btn, txt):

        self.app.bg_color = bg
        self.app.btn_color = btn
        self.app.text_color = txt


        self.app.root.configure(fg_color=bg)


        self.app.show_main_menu()


        self.set_win.destroy()

    def change_lang(self, new_lang):
        self.app.lang = new_lang
        self.app.show_main_menu()
        self.set_win.destroy()