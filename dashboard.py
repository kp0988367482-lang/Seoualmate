"""Playform AI 3-second dashboard demo."""

import importlib
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import Any

HAS_RICH = False
Console: Any = None
Table: Any = None
Panel: Any = None
Progress: Any = None
SpinnerColumn: Any = None
BarColumn: Any = None
TextColumn: Any = None
box: Any = None

try:
    rich_console = importlib.import_module("rich.console")
    rich_table = importlib.import_module("rich.table")
    rich_panel = importlib.import_module("rich.panel")
    rich_progress = importlib.import_module("rich.progress")
    rich_box = importlib.import_module("rich.box")

    Console = getattr(rich_console, "Console")
    Table = getattr(rich_table, "Table")
    Panel = getattr(rich_panel, "Panel")
    Progress = getattr(rich_progress, "Progress")
    SpinnerColumn = getattr(rich_progress, "SpinnerColumn")
    BarColumn = getattr(rich_progress, "BarColumn")
    TextColumn = getattr(rich_progress, "TextColumn")
    box = rich_box
    HAS_RICH = True
except ModuleNotFoundError:
    HAS_RICH = False


class FallbackConsole:
    """Simple console shim used when rich is unavailable."""

    @staticmethod
    def print(*args, **kwargs) -> None:
        print(*args)


class Dashboard3Sec:
    """Lightweight CLI dashboard for the Playform demo."""

    def __init__(self) -> None:
        self.console = Console() if HAS_RICH else FallbackConsole()
        self.start_time = datetime.now()

    def print_stunning_header(self) -> None:
        if not HAS_RICH:
            print("\n" + "=" * 60)
            print("PLAYFORM AI - 3-second dashboard")
            print("=" * 60 + "\n")
            return

        header = r"""
  ____  _            __                         
 |  _ \| | __ _ _   _/ _| ___  _ __ _ __ ___   
 | |_) | |/ _` | | | | |_ / _ \| '__| '_ ` _ \  
 |  __/| | (_| | |_| |  _| (_) | |  | | | | | | 
 |_|   |_|\__,_|\__, |_|  \___/|_|  |_| |_| |_| 
                |___/                           
        """

        self.console.print(
            Panel(
                header,
                title="3-second attention system",
                subtitle="GitHub + Antigravity AI",
                border_style="bold cyan",
            )
        )

    def show_agent_status(self) -> None:
        if not HAS_RICH:
            print("\nYouTube Agent   -> Ready")
            print("SaaS Agent      -> Ready")
            print("Marketing Agent -> Ready\n")
            return

        table = Table(title="AI Agent Status", box=box.ROUNDED)
        table.add_column("Agent", style="cyan bold")
        table.add_column("Status", style="green")
        table.add_column("Task", style="magenta")
        table.add_column("Output", style="yellow")

        rows = [
            ("YouTube", "Running", "script generation", "3 scripts/day"),
            ("SaaS", "Running", "feature shipping", "1 feature/day"),
            ("Marketing", "Running", "campaign automation", "20 posts/day"),
        ]

        for row in rows:
            table.add_row(*row)

        self.console.print(table)

    def show_statistics(self) -> None:
        if not HAS_RICH:
            print("Metrics:")
            print("  YouTube views/day: 5,432")
            print("  Monthly features: 12+")
            print("  Marketing reach: 50K+")
            print("  System uptime: 99.9%\n")
            return

        table = Table(title="System Metrics", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green bold")
        table.add_column("Trend", style="magenta")

        metrics = [
            ("YouTube views", "5,432/day", "+23%"),
            ("Feature deploys", "12+/month", "+8%"),
            ("Marketing reach", "50K+", "+45%"),
            ("Uptime", "99.9%", "stable"),
        ]

        for metric in metrics:
            table.add_row(*metric)

        self.console.print(table)

    def show_next_run(self) -> None:
        if not HAS_RICH:
            print("Next run: in ~6 hours")
            print("Triggered by GitHub Actions\n")
            return

        panel_content = """
Next automated cycle
--------------------
UTC: 18:00
Local: 03:00 (+9)
Trigger: GitHub Actions schedule
Infra: Firebase + CI pipeline
        """
        self.console.print(
            Panel(
                panel_content,
                title="Scheduler",
                border_style="yellow",
                expand=False,
            )
        )

    def show_quick_commands(self) -> None:
        if not HAS_RICH:
            print("Quick commands:")
            print("  python master.py")
            print("  python dashboard.py")
            print("  git push origin main\n")
            return

        commands = """
[1] Demo mode       -> python master.py
[2] Refresh display -> python dashboard.py
[3] Push pipeline   -> git push origin main
        """
        self.console.print(
            Panel(
                commands,
                title="Quick Commands",
                border_style="green",
                expand=False,
            )
        )

    def show_animated_progress(self) -> None:
        if not HAS_RICH:
            print("Preparing systems...\n")
            return

        tasks = [
            "YouTube pipeline",
            "SaaS pipeline",
            "Marketing pipeline",
            "GitHub Actions",
            "Firebase deploy",
        ]

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=20),
            TextColumn("[progress.percentage]{task.percentage:.0f}%"),
        ) as progress:
            for task in tasks:
                task_id = progress.add_task(task, total=100)
                for _ in range(100):
                    progress.update(task_id, advance=1)
                    time.sleep(0.01)

    def show_final_message(self) -> None:
        if not HAS_RICH:
            print("Playform AI is ready.")
            print("Run: python master.py\n")
            return

        final = """
System status: 100% ready

What happens next:
- Agent workflow orchestration
- Metrics and KPI tracking
- 6-hour recurring automation
- Automatic deployment

Start now: python master.py
        """

        self.console.print(
            Panel(
                final,
                title="Dashboard Ready",
                border_style="bold magenta",
            )
        )

    def run_3sec_demo(self) -> None:
        self.print_stunning_header()
        time.sleep(0.3)

        self.show_agent_status()
        time.sleep(0.3)

        self.show_statistics()
        time.sleep(0.3)

        self.show_animated_progress()
        time.sleep(0.2)

        self.show_next_run()
        time.sleep(0.2)

        self.show_quick_commands()
        time.sleep(0.2)

        self.show_final_message()


def install_rich() -> None:
    print("Installing rich for enhanced dashboard output...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=False)


def main() -> None:
    if not HAS_RICH:
        print("rich is not installed. Falling back to plain output.")

    dashboard = Dashboard3Sec()
    dashboard.run_3sec_demo()

    print("\n" + "=" * 60)
    print("Choose next action")
    print("[1] Demo mode (python master.py)")
    print("[2] Production mode (python master.py)")
    print("[3] Show dashboard again")
    print("[Q] Quit")
    print("=" * 60)

    choice = input("\nSelect (1-3/Q): ").strip().upper()

    if choice == "1":
        os.system("python master.py")
    elif choice == "2":
        os.system("python master.py")
    elif choice == "3":
        main()
    elif choice == "Q":
        print("Bye")


if __name__ == "__main__":
    main()

