"""
Tkinter GUI for the football league application.

Run with:

    python gui.py
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from app.services import AuthService, LeagueService


REFRESH_INTERVAL_MS = 3000  # 3 seconds


class LoginWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Football League - Login")
        self.geometry("360x180")
        self.resizable(False, False)

        self.auth = AuthService()

        # UI
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Username (email):").grid(row=0, column=0, sticky="w")
        self.username_var = tk.StringVar(value="lina@gmail.com")
        username_entry = ttk.Entry(frame, textvariable=self.username_var, width=30)
        username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky="w")
        self.password_var = tk.StringVar(value="demodemo")
        password_entry = ttk.Entry(
            frame, textvariable=self.password_var, show="*", width=30
        )
        password_entry.grid(row=1, column=1, pady=5)

        login_btn = ttk.Button(frame, text="Login", command=self.handle_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.bind("<Return>", lambda _event: self.handle_login())

    def handle_login(self) -> None:
        username = self.username_var.get().strip()
        password = self.password_var.get()
        user = self.auth.authenticate(username, password)
        if user is None:
            messagebox.showerror("Login failed", "Invalid username or password.")
            return

        # Open main window
        self.destroy()
        main_window = MainWindow(user.username)
        main_window.mainloop()


class MainWindow(tk.Tk):
    def __init__(self, username: str) -> None:
        super().__init__()
        self.title(f"Football League - {username}")
        self.geometry("820x420")
        self.resizable(True, True)

        self.league = LeagueService()

        container = ttk.Frame(self, padding=10)
        container.pack(fill="both", expand=True)

        # Notebook with three tabs: played, live, upcoming
        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        self.tree_played = self._create_match_tab("Played matches")
        self.tree_live = self._create_match_tab("Live matches")
        self.tree_upcoming = self._create_match_tab("Upcoming matches")

        # Initial load
        self.refresh_all()
        # Schedule periodic refresh and live update simulation
        self.after(REFRESH_INTERVAL_MS, self.periodic_refresh)

    def _create_match_tab(self, title: str) -> ttk.Treeview:
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)

        columns = ("date", "time", "home", "score", "away", "status")
        tree = ttk.Treeview(
            frame, columns=columns, show="headings", height=10, selectmode="browse"
        )
        tree.pack(fill="both", expand=True)

        tree.heading("date", text="Date")
        tree.heading("time", text="Time")
        tree.heading("home", text="Home")
        tree.heading("score", text="Score")
        tree.heading("away", text="Away")
        tree.heading("status", text="Status")

        tree.column("date", width=80, anchor="center")
        tree.column("time", width=60, anchor="center")
        tree.column("home", width=180)
        tree.column("score", width=70, anchor="center")
        tree.column("away", width=180)
        tree.column("status", width=80, anchor="center")

        return tree

    def refresh_all(self) -> None:
        self._populate_tree(self.tree_played, "played")
        self._populate_tree(self.tree_live, "live")
        self._populate_tree(self.tree_upcoming, "upcoming")

    def _populate_tree(self, tree: ttk.Treeview, status: str) -> None:
        for item in tree.get_children():
            tree.delete(item)

        matches = self.league.get_matches(status)  # type: ignore[arg-type]
        for m in matches:
            tree.insert(
                "",
                "end",
                values=(
                    m.date_str,
                    m.time_str,
                    m.home_team,
                    m.score_str,
                    m.away_team,
                    m.status,
                ),
            )

    def periodic_refresh(self) -> None:
        # Update live scores then reload tables
        self.league.simulate_live_updates()
        self.refresh_all()
        self.after(REFRESH_INTERVAL_MS, self.periodic_refresh)


def main() -> None:
    login = LoginWindow()
    login.mainloop()


if __name__ == "__main__":
    main()


