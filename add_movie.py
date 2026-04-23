
import customtkinter as ctk
from tkinter import messagebox
from translations import TRANSLATIONS

class AddMovieWindow:
    def __init__(self, app):
        self.app = app
        add_win = ctk.CTkToplevel(self.app.root)
        add_win.title(self.app.tr("add"))
        add_win.geometry("350x300")
        add_win.after(10, add_win.lift)
        add_win.grab_set()

        genre_dict = TRANSLATIONS[self.app.lang]["genres"]
        display_genres = list(genre_dict.values())
        self.reverse_genre_map = {v: k for k, v in genre_dict.items()}

        ctk.CTkLabel(add_win, text=self.app.tr("m_title")).pack(pady=(20, 0))
        t_ent = ctk.CTkEntry(add_win, width=200)
        t_ent.pack(pady=10)

        ctk.CTkLabel(add_win, text=self.app.tr("genre")).pack()
        self.g_cmb = ctk.CTkComboBox(add_win, values=display_genres, width=200, state="readonly")
        self.g_cmb.pack(pady=10)

        def save():
            title_input = t_ent.get().strip()
            selected_display_name = self.g_cmb.get()

            if not title_input or not selected_display_name:
                messagebox.showerror("Error", self.app.tr("err_empty"))
                return


            query_check = "SELECT id FROM movies WHERE user_id=? AND UPPER(title) = UPPER(?)"
            existing_movie = self.app.db.query(query_check, (self.app.current_user, title_input)).fetchone()

            if existing_movie:
                messagebox.showwarning("Warning", self.app.tr("err_exists"))
                return

            db_genre_key = self.reverse_genre_map[selected_display_name]

            self.app.db.query("INSERT INTO movies (user_id, title, genre, rating, status) VALUES (?,?,?,?,?)",
                                (self.app.current_user, title_input, db_genre_key, 0, "To-Watch"))
            add_win.destroy()
            messagebox.showinfo("Success", self.app.tr("succ_add"))

        ctk.CTkButton(add_win, text=self.app.tr("save"), command=save, fg_color="#4CAF50").pack(pady=20)