from rich.table import Table
from rich.console import Console
from datetime import date

def display_table(objects, columns, title=None):
    console = Console()
    if not objects:
        return False

    table = Table(title=title or "Table")
    for col in columns:
        table.add_column(col, justify="left")
    for obj in objects:
        row = [str(getattr(obj, col, "")) for col in columns]
        table.add_row(*row)
    print("\n")
    console.print(table)
    print("\n")
    return True