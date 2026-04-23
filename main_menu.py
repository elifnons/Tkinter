
import customtkinter as ctk

class MainMenu:
    def __init__(self, app):
        self.app = app
        self.app.clear_screen()
        self.app.root.configure(bg=self.app.bg_color)

        ctk.CTkLabel(self.app.root, text=f"{self.app.tr('welcome')}, {self.app.current_user.upper()}",
                     font=("Arial", 18, "bold"), text_color=self.app.text_color).pack(pady=30)

        btns = [
            (self.app.tr("add"), self.app.show_add_movie),
            (self.app.tr("list"), self.app.show_list_window),
            (self.app.tr("watched"), self.app.show_watched_list),
            (self.app.tr("stats"), self.app.show_stats_window),
            (self.app.tr("settings"), self.app.show_settings_window),
            (self.app.tr("reset"), self.app.clear_my_data),
            (self.app.tr("logout"), self.app.show_auth_screen)
        ]

        for t, c in btns:
            bg_c = "#ec3b83" if t == self.app.tr("reset") else self.app.btn_color
            ctk.CTkButton(self.app.root, text=t, width=250, height=35, fg_color=bg_c,
                          text_color=self.app.text_color, command=c).pack(pady=8)