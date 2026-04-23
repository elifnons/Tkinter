
import customtkinter as ctk
from translations import TRANSLATIONS
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StatsWindow:
    def __init__(self, app):
        self.app = app
        self.s_win = ctk.CTkToplevel(self.app.root)
        self.s_win.title(self.app.tr("stats"))
        self.s_win.geometry("500x750")
        self.s_win.after(10, self.s_win.lift)
        self.s_win.configure(fg_color=self.app.bg_color)


        data = self.app.db.query(
            "SELECT genre, COUNT(*) FROM movies WHERE user_id=? AND status='Watched' GROUP BY genre",
            (self.app.current_user,)
        ).fetchall()

        total = self.app.db.query(
            "SELECT COUNT(*) FROM movies WHERE user_id=? AND status='Watched'",
            (self.app.current_user,)
        ).fetchone()[0]

        ctk.CTkLabel(self.s_win, text=self.app.tr("genre_dist"),
                     font=("Arial", 20, "bold"), text_color=self.app.text_color).pack(pady=20)

        if total == 0:
            ctk.CTkLabel(self.s_win, text=self.app.tr("no_data"), text_color=self.app.text_color).pack()
            return


        genres_display = []
        counts = []
        for genre_key, count in data:

            display_name = TRANSLATIONS[self.app.lang]["genres"].get(genre_key, genre_key)
            genres_display.append(display_name)
            counts.append(count)


        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor(self.app.bg_color)
        ax.set_facecolor(self.app.bg_color)


        wedges, texts, autotexts = ax.pie(
            counts,
            labels=genres_display,
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.Pastel1.colors,
            textprops={'color': self.app.text_color}
        )


        ax.axis('equal')


        canvas = FigureCanvasTkAgg(fig, master=self.s_win)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.configure(background=self.app.bg_color)
        canvas_widget.pack(pady=10, fill="both", expand=True)
        canvas.draw()


        summary_frame = ctk.CTkScrollableFrame(self.s_win, fg_color="transparent", height=200)
        summary_frame.pack(fill="x", padx=20, pady=10)

        for name, count in zip(genres_display, counts):
            perc = count / total

            row = ctk.CTkFrame(summary_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)

            ctk.CTkLabel(row, text=f"{name} ({count})", text_color=self.app.text_color).pack(side="left")

            prog = ctk.CTkProgressBar(summary_frame, width=250)
            prog.set(perc)
            prog.pack(pady=(0, 10))