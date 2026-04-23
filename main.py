
import customtkinter as ctk
from tkinter import messagebox
from database import Database
from translations import TRANSLATIONS
from auth_window import AuthWindow
from main_menu import MainMenu
from add_movie import AddMovieWindow
from list_windows import ListWindow, WatchedListWindow
from stats_window import StatsWindow
from settings_window import SettingsWindow



class MovieTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Tracker Pro 🎬")
        self.root.geometry("450x700")

        self.db = Database()
        self.lang = "en"
        self.bg_color = "#242424"
        self.btn_color = "#3b3b3b"
        self.text_color = "white"
        self.current_user = None

        self.show_auth_screen()

    def tr(self, key):
        return TRANSLATIONS[self.lang].get(key, key)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_auth_screen(self):
        AuthWindow(self)

    def show_main_menu(self):
        MainMenu(self)

    def show_add_movie(self):
        AddMovieWindow(self)


    def show_list_window(self):
        ListWindow(self)

    def show_watched_list(self):
        WatchedListWindow(self)

    def show_stats_window(self):
        StatsWindow(self)

    def show_settings_window(self):
        SettingsWindow(self)

    def clear_my_data(self):
        if messagebox.askyesno("Warning", self.tr("warn_reset")):
            self.db.query("DELETE FROM movies WHERE user_id = ?", (self.current_user,))
            messagebox.showinfo("Success", self.tr("succ_reset"))


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = MovieTrackerApp(root)
    root.mainloop()