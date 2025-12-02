from App.models import Item

def get_menu_text():
    items = Item.query.all()
    if not items:
        return "The menu is currently empty."
    menu_lines = ["Available Items:"]
    for item in items:
        menu_lines.append(f"- {item.name}: ${item.price:.2f}")
    return "\n".join(menu_lines)