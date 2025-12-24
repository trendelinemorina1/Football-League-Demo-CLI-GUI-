# Football-League-Demo-CLI-GUI-

This is a small, well-structured demo application that exposes the same
football league data and logic through both:

- **CLI interface** (`cli.py`)
- **Tkinter GUI interface** (`gui.py`)

The app uses **SQLite** for persistent storage and has a very simple
authentication system.

- **Default user**
  - Username: `lina@gmail.com`
  - Password: `demodemo`

After logging in, you can browse a small set of Italian Serie A matches,
grouped into:

- **Played** – finished matches with final scores
- **Live** – matches in progress; scores are **simulated and updated periodically**
- **Upcoming** – matches scheduled in the future with date and kickoff time

All data and business logic are shared between the CLI and GUI.

---

### 1. Requirements

- **Python 3.10+**
- No external dependencies; only the Python standard library is used.

On Windows, Python should already include `tkinter`. If you get an error
about `tkinter` missing, install Python with Tcl/Tk support.

---

### 2. Project structure

- **`app/db.py`**: SQLite database configuration, schema creation, and seeding.
- **`app/models.py`**: Simple dataclass models for `User` and `Match`.
- **`app/services.py`**: Business logic (authentication and league services).
- **`cli.py`**: Command-line interface for login and browsing matches.
- **`gui.py`**: Tkinter GUI for login and browsing matches with live updates.
- **`league.db`**: SQLite database file (auto-created on first run).

The architecture keeps a **clear separation** between:

- **Database layer** (`app/db.py`)
- **Domain models** (`app/models.py`)
- **Business logic** (`app/services.py`)
- **Interfaces** (`cli.py`, `gui.py`)

---

### 3. First-time setup

From the project root (`C:\Users\besni\OneDrive\Desktop\Db` in your case):

```bash
python --version
```

Make sure it shows Python 3.10 or newer.

No further setup is required. The SQLite database file `league.db`
will be created and seeded automatically the first time you run
either the CLI or GUI.

---

### 4. Running the CLI

From the project root:

```bash
python cli.py
```

You will see prompts:

1. **Login**
   - Username: `lina@gmail.com`
   - Password: `demodemo`
2. **Menu**
   - `1` – Show played matches
   - `2` – Show live matches
   - `3` – Show upcoming matches
   - `4` – Watch live matches with auto-refresh (Ctrl+C to stop)
   - `q` – Quit

The "watch live matches" option periodically **simulates goals** and
prints the updated table.

---

### 5. Running the GUI

From the project root:

```bash
python gui.py
```

Steps:

1. A **login window** appears (pre-filled with the default credentials).
2. After successful login, the **main window** opens.
3. The main window contains three tabs:
   - **Played matches**
   - **Live matches**
   - **Upcoming matches**
4. Scores for **live** matches are simulated and refreshed every few
   seconds automatically.

---

### 6. Notes and extensibility

- The current authentication uses **plain-text passwords** for simplicity.
  For a real application you would add password hashing and better security.
- New match types, leagues, or views can be added by extending
  `app/models.py` and `app/services.py`, while the CLI and GUI can
  remain thin layers over the same core logic.
