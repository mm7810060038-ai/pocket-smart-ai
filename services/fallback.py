def _money(value):
    return f"₹{value:,.0f}"


def home_fallback(data):
    budget = float(data["budget"])
    products = [
        {"name": "LED Ceiling Light", "platform": "IKEA", "price": min(1499, budget * .15), "url": "https://www.ikea.com/in/en/"},
        {"name": "Decorative Table Lamp", "platform": "Amazon", "price": min(1299, budget * .12), "url": "https://www.amazon.in/"},
        {"name": "Ceiling Fan", "platform": "Flipkart", "price": min(2499, budget * .22), "url": "https://www.flipkart.com/"},
        {"name": "Accent Decor", "platform": "Amazon", "price": min(999, budget * .10), "url": "https://www.amazon.in/"},
    ]
    products = [dict(p, price=round(max(1, p["price"]), 2)) for p in products]
    return {"title": "Home Budget Suggestions", "summary": f"Sample ideas for a {data['style']} {data['room']} within {_money(budget)}.", "items": products}


def party_fallback(data):
    budget = float(data["budget"])
    guests = int(data["guests"])
    food = round(budget * .55, 2)
    decor = round(budget * .20, 2)
    venue = round(budget * .25, 2)
    return {
        "title": "Party Budget Plan",
        "summary": f"A sample allocation for {guests} guests and a {data['event_type']} in {data['venue']}.",
        "allocation": [{"category": "Food", "amount": food}, {"category": "Decor", "amount": decor}, {"category": "Venue", "amount": venue}],
        "items": [
            {"name": "Food ordering options", "platform": "Swiggy / Zomato", "price": food, "url": "https://www.swiggy.com/"},
            {"name": "Venue / stay options", "platform": "OYO", "price": venue, "url": "https://www.oyorooms.com/"},
            {"name": "Party decoration ideas", "platform": "Amazon", "price": decor, "url": "https://www.amazon.in/"},
        ],
    }


def jewelry_fallback(data):
    budget = float(data["budget"])
    return {
        "title": "Jewelry Suggestions",
        "summary": f"Sample {data['style']} jewelry ideas for {data['occasion']} within {_money(budget)}.",
        "items": [
            {"name": "Minimal necklace set", "platform": "Amazon", "price": round(min(budget * .45, 2499), 2), "url": "https://www.amazon.in/"},
            {"name": "Statement earrings", "platform": "Flipkart", "price": round(min(budget * .25, 1499), 2), "url": "https://www.flipkart.com/"},
            {"name": "Bracelet / bangle set", "platform": "Amazon", "price": round(min(budget * .20, 999), 2), "url": "https://www.amazon.in/"},
        ],
    }
