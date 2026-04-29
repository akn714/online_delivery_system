# Items Catalog - Structured inventory for the Online Delivery System

ITEMS_CATALOG = {
    "Grocery": [
        {"name": "White Bread", "price": 20, "unit": "piece"},
        {"name": "Bhuja Chana", "price": 100, "unit": "kg"},
        {"name": "Maggie", "price": [15, 56], "unit": "packet"},
        {"name": "Moongfali", "price": 160, "unit": "kg"},
        {"name": "Soyabean (Packet)", "price": 10, "unit": "packet"},
        {"name": "Soyabean (Open - Small)", "price": 100, "unit": "kg"},
        {"name": "Macaroni / Pasta", "price": 60, "unit": "kg"},
        {"name": "Sugar (Chini)", "price": 45, "unit": "kg"},
        {"name": "Glucose D", "price": [56, 89], "unit": "packet"},
        {"name": "Jam (Kissan Mixed Fruit)", "price": [25, 90], "unit": "bottle"},
        {"name": "Colgate Toothpaste", "price": [20, 70, 130], "unit": "piece"},
        {"name": "Closeup Toothpaste", "price": [20, 55], "unit": "piece"},
        {"name": "Sensodyne Toothpaste", "price": 140, "unit": "piece"},
        {"name": "Coffee (Nescafe)", "price": [10, 124, 235], "unit": "packet"},
        {"name": "Mustard Oil (Sarso Tel - Sudh Kolhu)", "price": 180, "unit": "liter"},
        {"name": "Fortune Oil", "price": 190, "unit": "liter"},
        {"name": "Garam Masala (Whole)", "price": 20, "unit": "packet"},
        {"name": "Garam Masala (Packet)", "price": 10, "unit": "packet"},
        {"name": "Kacha Chana", "price": 80, "unit": "kg"},
        {"name": "Makhana", "price": 130, "unit": "100 gm"},
        {"name": "Kaju (Cashew)", "price": 1000, "unit": "kg"},
        {"name": "Badam (Almond)", "price": 1000, "unit": "kg"},
        {"name": "Pista (Packet)", "price": 350, "unit": "packet"},
    ],
    "Stationary": [
        {"name": "Practical File (Physics)", "price": [30, 60], "unit": "piece"},
        {"name": "Practical File (Chemistry)", "price": [30, 60], "unit": "piece"},
        {"name": "Practical File (General)", "price": [30, 60], "unit": "piece"},
        {"name": "Pen", "price": [4, 5, 10], "unit": "piece"},
        {"name": "Pencil", "price": 5, "unit": "piece"},
        {"name": "Eraser", "price": 5, "unit": "piece"},
        {"name": "Sharpener", "price": 5, "unit": "piece"},
        {"name": "Drawing Book (Engineering) A3 (36 pages)", "price": 90, "unit": "piece"},
        {"name": "Drawing Book (Engineering) A3 (56 pages)", "price": 110, "unit": "piece"},
        {"name": "A4 Size Pages (500 sheets)", "price": 200, "unit": "pack"},
        {"name": "Stapler", "price": 50, "unit": "piece"},
        {"name": "Staple Pins", "price": 10, "unit": "box"},
        {"name": "Sticky Notes", "price": 20, "unit": "pack"},
        {"name": "Fevicol", "price": [10, 20, 50], "unit": "bottle"},
        {"name": "Double-Sided Tape", "price": [5, 10], "unit": "roll"},
        {"name": "Spiral Notebook (Plain)", "price": [80, 100, 140], "unit": "piece"},
        {"name": "Spiral Notebook (Lined)", "price": [80, 100, 140], "unit": "piece"},
        {"name": "Register (A4 Rough)", "price": [30, 40, 50], "unit": "piece"},
        {"name": "Register (A2)", "price": [30, 40, 50], "unit": "piece"},
        {"name": "Register (A1)", "price": [30, 40, 50], "unit": "piece"},
        {"name": "Graph Book", "price": 10, "unit": "piece"},
        {"name": "Cello Tape", "price": 5, "unit": "roll"},
        {"name": "Practical File Pages (Lined)", "price": 10, "unit": "pack"},
        {"name": "Practical File Pages (Plain)", "price": 10, "unit": "pack"},
        {"name": "Practical File Cover (Plastic)", "price": [5, 10], "unit": "piece"},
        {"name": "Practical File Cover (Cardboard)", "price": 20, "unit": "piece"},
        {"name": "Highlighter", "price": 20, "unit": "piece"},
    ],
    "Fruits": [
        {"name": "Banana", "price": 40, "unit": "kg"},
        {"name": "Pomegranate (Anaar)", "price": 180, "unit": "kg"},
        {"name": "Mango", "price": 100, "unit": "kg"},
        {"name": "Apple", "price": 200, "unit": "kg"},
        {"name": "Orange (Santara)", "price": 150, "unit": "kg"},
        {"name": "Papaya (Papita)", "price": 60, "unit": "kg"},
        {"name": "Kiwi", "price": 50, "unit": "piece"},
        {"name": "Coconut (Nariyal)", "price": 70, "unit": "piece"},
        {"name": "Grapes (Angoor)", "price": 150, "unit": "kg"},
    ],
}


def get_items_catalog() -> dict:
    """Return the items catalog."""
    return ITEMS_CATALOG


def get_all_items() -> list:
    """Return all items as a flat list with category."""
    all_items = []
    for category, items in ITEMS_CATALOG.items():
        for item in items:
            all_items.append({
                "category": category,
                "name": item["name"],
                "price": item["price"],
                "unit": item["unit"]
            })
    return all_items


def format_price(price) -> str:
    """Format price for display."""
    if isinstance(price, list):
        return f"₹{', ₹'.join(map(str, price))}"
    return f"₹{price}"