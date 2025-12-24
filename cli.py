"""
Command-line interface for the football league application.

Usage (from this folder):

    python cli.py

You will be prompted to log in, then can browse matches
by their status (played, live, upcoming).
"""

from __future__ import annotations

import getpass
import sys
import time
from typing import Callable

from app.services import AuthService, LeagueService


def prompt_login(auth: AuthService):
    print("=== Football League CLI ===")
    print("Please log in.")
    username = input("Username (email): ").strip()
    password = getpass.getpass("Password: ")

    user = auth.authenticate(username, password)
    if user is None:
        print("Invalid credentials. Exiting.")
        sys.exit(1)
    print(f"Welcome, {user.username}!")
    return user


def print_match_table(matches) -> None:
    if not matches:
        print("No matches found.")
        return

    print(
        f"{'ID':<3} {'Date':<10} {'Time':<5} {'Status':<8} "
        f"{'Home':<15} {'Score':<7} {'Away':<15}"
    )
    print("-" * 70)
    for m in matches:
        print(
            f"{m.id:<3} {m.date_str:<10} {m.time_str:<5} {m.status:<8} "
            f"{m.home_team:<15} {m.score_str:<7} {m.away_team:<15}"
        )


def menu_loop(league: LeagueService) -> None:
    actions: dict[str, Callable[[], None]] = {
        "1": lambda: print_match_table(league.get_matches("played")),
        "2": lambda: print_match_table(league.get_matches("live")),
        "3": lambda: print_match_table(league.get_matches("upcoming")),
        "4": lambda: watch_live_matches(league),
    }

    while True:
        print()
        print("Menu:")
        print("  1) Show played matches")
        print("  2) Show live matches")
        print("  3) Show upcoming matches")
        print("  4) Watch live matches (auto-refresh)")
        print("  q) Quit")
        choice = input("Select an option: ").strip().lower()
        if choice == "q":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            print()
            action()
        else:
            print("Invalid choice.")


def watch_live_matches(league: LeagueService, interval_seconds: int = 5) -> None:
    """
    Continuously display live matches with simulated score updates.

    Press Ctrl+C to return to the main menu.
    """
    print("Watching live matches. Press Ctrl+C to stop.")
    try:
        while True:
            # Simulate score updates then fetch current state
            league.simulate_live_updates()
            matches = league.get_matches("live")
            print()
            print("-" * 70)
            print(time.strftime("Updated at %H:%M:%S"))
            print_match_table(matches)
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nStopped watching live matches.")


def main() -> None:
    auth = AuthService()
    league = LeagueService()
    prompt_login(auth)
    menu_loop(league)


if __name__ == "__main__":
    main()


