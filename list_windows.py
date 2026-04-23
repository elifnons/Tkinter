
import customtkinter as ctk
from tkinter import ttk, messagebox
from translations import TRANSLATIONS
class ListWindow:
    def __init__(self, app):
        self.app = app
        self.l_win = ctk.CTkToplevel(self.app.root)
        self.l_win.title(self.app.tr("list"))
        self.l_win.geometry("550x500")
        self.l_win.after(10, self.l_win.lift)


        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", borderwidth=0)
        style.map("Treeview", background=[('selected', '#ec3b83')])

        self.tree = ttk.Treeview(self.l_win, columns=("ID", "Title", "Genre"), show='headings')
        self.tree.heading("ID", text=self.app.tr("id"))
        self.tree.heading("Title", text=self.app.tr("title"))
        self.tree.heading("Genre", text=self.app.tr("genre"))

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        self.load_data()

        btn_frame = ctk.CTkFrame(self.l_win, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text=self.app.tr("mark_w"), command=self.mark_watched, fg_color="#4CAF50").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text=self.app.tr("del"), fg_color="#ec3b83", command=self.delete_item).pack(side="left", padx=10)

    def load_data(self):
        query = "SELECT id, title, genre FROM movies WHERE user_id=? AND status='To-Watch'"
        for r in self.app.db.query(query, (self.app.current_user,)):

            translated_genre = TRANSLATIONS[self.app.lang]["genres"].get(r[2], r[2])

            display_row = (r[0], r[1], translated_genre)
            self.tree.insert("", "end", values=display_row)

    def mark_watched(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel)['values']

        rate_win = ctk.CTkToplevel(self.l_win)
        rate_win.geometry("280x200")
        rate_win.after(10, rate_win.lift)
        rate_win.grab_set()

        ctk.CTkLabel(rate_win, text=f"{self.app.tr('title')}: {item[1]}").pack(pady=10)
        score_label = ctk.CTkLabel(rate_win, text="Score: 5")
        score_label.pack()
        score_slider = ctk.CTkSlider(rate_win, from_=0, to=10, number_of_steps=10,
                                     command=lambda v: score_label.configure(text=f"Score: {int(v)}"))
        score_slider.set(5)
        score_slider.pack(pady=10)

        def confirm():
            self.app.db.query("UPDATE movies SET status='Watched', rating=? WHERE id=?", (int(score_slider.get()), item[0]))
            self.tree.delete(sel)
            rate_win.destroy()

        ctk.CTkButton(rate_win, text=self.app.tr("confirm"), command=confirm, fg_color="#2196F3").pack(pady=10)

    def delete_item(self):
        sel = self.tree.selection()
        if not sel: return
        if messagebox.askyesno("Confirm", self.app.tr("confirm_del")):
            mid = self.tree.item(sel)['values'][0]
            self.app.db.query("DELETE FROM movies WHERE id = ?", (mid,))
            self.tree.delete(sel)

class WatchedListWindow:
    def __init__(self, app):
        self.app = app
        self.w_win = ctk.CTkToplevel(self.app.root)
        self.w_win.title(self.app.tr("watched"))
        self.w_win.geometry("550x500")
        self.w_win.after(10, self.w_win.lift)
        self.w_win.grab_set()
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", borderwidth=0)

        style.map("Treeview", background=[('selected', '#ec3b83')])
        self.tree = ttk.Treeview(self.w_win, columns=("ID", "Title", "Genre", "Rating"), show='headings')
        self.tree.heading("ID", text=self.app.tr("id"))
        self.tree.heading("Title", text=self.app.tr("title"))
        self.tree.heading("Genre", text=self.app.tr("genre"))
        self.tree.heading("Rating", text=self.app.tr("score"))
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        query = "SELECT id, title, genre, rating FROM movies WHERE user_id=? AND status='Watched'"
        for r in self.app.db.query(query, (self.app.current_user,)):
            self.tree.insert("", "end", values=r)

        ctk.CTkButton(self.w_win, text=self.app.tr("del_h"), fg_color="#ec3b83", command=self.delete_item).pack(pady=10)

    def delete_item(self):
        sel = self.tree.selection()
        if not sel: return
        if messagebox.askyesno("Confirm", self.app.tr("confirm_del")):
            mid = self.tree.item(sel)['values'][0]
            self.app.db.query("DELETE FROM movies WHERE id = ?", (mid,))
            self.tree.delete(sel)
            self.w_win.lift()