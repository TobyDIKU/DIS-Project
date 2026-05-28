"""Seed the database with categories, restaurants, menu items, users, and reviews."""

import random
from decimal import Decimal

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import Beverage, Category, FoodItem, Restaurant, Review, User

random.seed(42)

PRICE_MULTIPLIER = {1: Decimal("0.85"), 2: Decimal("1.00"), 3: Decimal("1.25")}

# ── Categories ────────────────────────────────────────────────────────────────

CATEGORY_DATA = [
    ("Asian",          "Japanese, Chinese, Korean, Thai, Vietnamese and more"),
    ("Italian",        "Pizza, pasta, risotto and classic Italian dishes"),
    ("Café",           "Coffee, brunch, sandwiches and cakes"),
    ("Fast Food",      "Burgers, wraps, fries and quick bites"),
    ("Nordic",         "Danish and Scandinavian classics with seasonal produce"),
    ("Middle Eastern", "Lebanese, Turkish, Moroccan and Levantine cuisine"),
    ("Indian",         "Curries, biryanis, tandoor dishes and street food"),
    ("Vegan",          "100% plant-based restaurants"),
]

# ── Menu item templates ───────────────────────────────────────────────────────
# (name, description, is_vegetarian, is_vegan, allergens, base_price_dkk)

FOOD_TEMPLATES: dict[str, dict[str, list]] = {
    "Asian": {
        "appetizer": [
            ("Spring Rolls", "Crispy vegetable spring rolls with sweet chili sauce", True, True, None, Decimal("45")),
            ("Gyoza", "Pan-fried pork and cabbage dumplings", False, False, "gluten, pork", Decimal("55")),
            ("Edamame", "Steamed salted soybeans", True, True, "soy", Decimal("35")),
            ("Miso Soup", "Traditional Japanese soup with tofu and wakame", True, True, "soy", Decimal("40")),
            ("Prawn Toast", "Deep-fried bread with seasoned prawn paste", False, False, "gluten, shellfish", Decimal("55")),
            ("Chicken Satay", "Grilled chicken skewers with peanut sauce", False, False, "peanuts", Decimal("65")),
        ],
        "main": [
            ("Pad Thai", "Stir-fried rice noodles with egg, tofu and peanuts", False, False, "peanuts, gluten", Decimal("115")),
            ("Ramen", "Rich pork broth with noodles, egg, chashu and nori", False, False, "gluten, egg", Decimal("125")),
            ("Chicken Teriyaki", "Grilled chicken with teriyaki glaze, steamed rice", False, False, "soy, gluten", Decimal("105")),
            ("Bibimbap", "Korean rice bowl with vegetables, egg and gochujang", False, False, "egg, soy", Decimal("110")),
            ("Green Curry", "Thai green curry with coconut milk and jasmine rice", False, False, "shellfish", Decimal("115")),
            ("Pho Bo", "Vietnamese beef noodle soup with fresh herbs", False, False, "gluten", Decimal("105")),
            ("Dumplings (8 pcs)", "Steamed pork and ginger dumplings", False, False, "gluten, pork", Decimal("95")),
            ("Tofu Stir-fry", "Wok-fried tofu with seasonal vegetables", True, True, "soy", Decimal("95")),
            ("Sushi Platter (12 pcs)", "Mixed nigiri and maki selection", False, False, "fish, gluten", Decimal("145")),
            ("Nasi Goreng", "Indonesian fried rice with chicken, egg and prawn crackers", False, False, "shellfish, egg", Decimal("100")),
        ],
        "side": [
            ("Steamed Rice", None, True, True, None, Decimal("25")),
            ("Fried Rice", "Wok-fried rice with egg and spring onion", False, False, "egg, soy", Decimal("35")),
            ("Kimchi", "Fermented spicy cabbage", True, True, None, Decimal("30")),
        ],
        "dessert": [
            ("Mochi Ice Cream", "Japanese rice cake filled with ice cream", False, False, "dairy", Decimal("55")),
            ("Matcha Cake", "Light sponge with matcha cream", False, False, "dairy, gluten, egg", Decimal("50")),
            ("Fried Banana", "Crispy fried banana with honey", True, True, None, Decimal("45")),
        ],
    },
    "Italian": {
        "appetizer": [
            ("Bruschetta", "Toasted bread with tomato, garlic and basil", True, True, "gluten", Decimal("55")),
            ("Burrata", "Fresh burrata with heirloom tomatoes and basil oil", False, False, "dairy", Decimal("85")),
            ("Arancini", "Fried risotto balls with mozzarella", False, False, "dairy, gluten, egg", Decimal("65")),
            ("Prosciutto e Melone", "Cured ham with cantaloupe melon", False, False, None, Decimal("75")),
            ("Caprese", "Buffalo mozzarella, tomato and basil", False, False, "dairy", Decimal("70")),
        ],
        "main": [
            ("Margherita Pizza", "San Marzano tomato, fior di latte, basil", False, False, "dairy, gluten", Decimal("110")),
            ("Pepperoni Pizza", "Tomato, mozzarella, spicy salami", False, False, "dairy, gluten", Decimal("125")),
            ("Spaghetti Carbonara", "Spaghetti, guanciale, egg yolk, pecorino", False, False, "dairy, gluten, egg", Decimal("120")),
            ("Penne Arrabbiata", "Penne with spicy tomato and garlic", True, True, "gluten", Decimal("100")),
            ("Lasagne al Forno", "Layered beef ragù, béchamel and pasta", False, False, "dairy, gluten, egg", Decimal("130")),
            ("Risotto ai Funghi", "Creamy porcini mushroom risotto", False, False, "dairy", Decimal("125")),
            ("Gnocchi al Pesto", "Potato gnocchi with basil pesto and pine nuts", False, False, "dairy, gluten, nuts", Decimal("115")),
            ("Saltimbocca", "Veal with prosciutto and sage in white wine sauce", False, False, "dairy", Decimal("155")),
            ("Linguine alle Vongole", "Linguine with clams, white wine and parsley", False, False, "shellfish, gluten", Decimal("140")),
        ],
        "side": [
            ("Insalata Verde", "Mixed green salad with lemon dressing", True, True, None, Decimal("40")),
            ("Focaccia", "Olive oil flatbread with rosemary", True, True, "gluten", Decimal("35")),
            ("Patatine Fritte", "Thin crispy fries with sea salt", True, True, None, Decimal("40")),
        ],
        "dessert": [
            ("Tiramisu", "Classic mascarpone and espresso dessert", False, False, "dairy, gluten, egg", Decimal("65")),
            ("Panna Cotta", "Vanilla cream with berry coulis", False, False, "dairy", Decimal("60")),
            ("Affogato", "Vanilla ice cream with a shot of espresso", False, False, "dairy", Decimal("50")),
        ],
    },
    "Café": {
        "appetizer": [
            ("Soup of the Day", "Ask your server for today's selection", True, False, None, Decimal("60")),
            ("Avocado Toast", "Sourdough with smashed avocado, chili flakes and seeds", True, True, "gluten", Decimal("75")),
            ("Smørrebrød (2 pcs)", "Open-face rye bread with seasonal toppings", False, False, "gluten", Decimal("80")),
        ],
        "main": [
            ("Club Sandwich", "Chicken, bacon, egg, lettuce, tomato on toasted bread", False, False, "gluten, egg, dairy", Decimal("105")),
            ("Caesar Salad", "Romaine, parmesan, croutons, anchovies, caesar dressing", False, False, "dairy, gluten, fish, egg", Decimal("100")),
            ("Quinoa Bowl", "Roasted vegetables, chickpeas, tahini dressing", True, True, "sesame", Decimal("110")),
            ("Croque Monsieur", "Ham and Gruyère toastie with béchamel", False, False, "dairy, gluten", Decimal("95")),
            ("Bagel with Salmon", "Toasted bagel, cream cheese, smoked salmon, capers", False, False, "dairy, gluten, fish", Decimal("95")),
            ("Eggs Benedict", "Poached eggs on English muffin with hollandaise", False, False, "dairy, gluten, egg", Decimal("105")),
            ("Granola Bowl", "House granola with yoghurt, fresh berries and honey", False, False, "dairy, gluten, nuts", Decimal("85")),
        ],
        "side": [
            ("Side Salad", "Mixed leaves with vinaigrette", True, True, None, Decimal("35")),
            ("Fries", "Classic salted fries", True, True, None, Decimal("35")),
        ],
        "dessert": [
            ("Cinnamon Roll", "Freshly baked with cream cheese glaze", False, False, "dairy, gluten, egg", Decimal("45")),
            ("Brownie", "Dense chocolate brownie, served warm", False, False, "dairy, gluten, egg", Decimal("40")),
            ("Carrot Cake", "Moist carrot cake with cream cheese frosting", False, False, "dairy, gluten, egg, nuts", Decimal("45")),
        ],
    },
    "Fast Food": {
        "appetizer": [
            ("Chicken Wings (6 pcs)", "Crispy wings with choice of sauce", False, False, "gluten", Decimal("65")),
            ("Mozzarella Sticks", "Breaded and fried with marinara dip", False, False, "dairy, gluten", Decimal("55")),
            ("Loaded Fries", "Fries with cheese sauce, jalapeños and sour cream", False, False, "dairy, gluten", Decimal("65")),
            ("Onion Rings", "Crispy battered onion rings", True, True, "gluten", Decimal("40")),
        ],
        "main": [
            ("Classic Burger", "Beef patty, lettuce, tomato, pickles, special sauce", False, False, "gluten, dairy, egg", Decimal("95")),
            ("Double Burger", "Two beef patties, cheese, caramelised onion", False, False, "gluten, dairy, egg", Decimal("115")),
            ("Chicken Burger", "Crispy fried chicken fillet, slaw and sriracha mayo", False, False, "gluten, dairy, egg", Decimal("95")),
            ("Veggie Burger", "Plant-based patty, avocado, tomato, lettuce", True, True, "gluten", Decimal("95")),
            ("Hot Dog", "Pork sausage in brioche bun with mustard and ketchup", False, False, "gluten", Decimal("65")),
            ("Shawarma Wrap", "Spiced chicken, garlic sauce, pickles in flatbread", False, False, "gluten, dairy", Decimal("80")),
            ("Fish & Chips", "Beer-battered cod with fries and tartar sauce", False, False, "gluten, fish, egg", Decimal("105")),
            ("Falafel Wrap", "Crispy falafel, hummus, salad in flatbread", True, True, "gluten, sesame", Decimal("75")),
        ],
        "side": [
            ("Fries", "Classic salted fries", True, True, None, Decimal("35")),
            ("Sweet Potato Fries", "Oven-baked sweet potato fries", True, True, None, Decimal("40")),
            ("Coleslaw", "Creamy cabbage and carrot slaw", False, False, "egg, dairy", Decimal("25")),
        ],
        "dessert": [
            ("Soft Serve", "Vanilla or chocolate soft ice cream", False, False, "dairy", Decimal("30")),
            ("Milkshake", "Thick shake in vanilla, chocolate or strawberry", False, False, "dairy", Decimal("45")),
        ],
    },
    "Nordic": {
        "appetizer": [
            ("Gravlax", "House-cured salmon with mustard dill sauce and rye croutons", False, False, "fish, gluten, mustard", Decimal("90")),
            ("Pickled Herring", "Marinated herring with rye bread and raw onion", False, False, "fish, gluten", Decimal("75")),
            ("Beetroot Salad", "Roasted beet, goat's cheese, walnuts and dill", False, False, "dairy, nuts", Decimal("80")),
            ("Smoked Mackerel Pâté", "On toasted rye with pickled cucumber", False, False, "fish, gluten", Decimal("80")),
        ],
        "main": [
            ("Frikadeller", "Danish pork meatballs with potato salad and pickled beet", False, False, "gluten, egg, dairy", Decimal("115")),
            ("Stegt Flæsk", "Crispy pork belly with parsley sauce and potatoes", False, False, "dairy", Decimal("130")),
            ("Smørrebrød Plate (3 pcs)", "Three open-face sandwiches with Nordic toppings", False, False, "gluten, fish, dairy", Decimal("120")),
            ("Salmon Fillet", "Pan-fried salmon, new potatoes, dill cream and cucumber", False, False, "fish, dairy", Decimal("150")),
            ("Vegetable Ragù", "Root vegetables in Nordic herb broth with barley", True, True, None, Decimal("110")),
            ("Elk Burger", "Elk patty, lingonberry jam, pickled onion and brioche", False, False, "gluten, dairy, egg", Decimal("145")),
        ],
        "side": [
            ("New Potatoes", "Buttered baby potatoes with dill", False, False, "dairy", Decimal("40")),
            ("Rye Bread", "Dark sourdough rye with butter", False, False, "gluten, dairy", Decimal("25")),
            ("Pickled Vegetables", "Seasonal pickles, house recipe", True, True, None, Decimal("30")),
        ],
        "dessert": [
            ("Æbleskiver", "Danish pancake balls with jam and icing sugar", False, False, "dairy, gluten, egg", Decimal("55")),
            ("Rødgrød", "Summer berry compote with cream", False, False, "dairy", Decimal("55")),
            ("Kanelsnegl", "Freshly baked cinnamon swirl", False, False, "dairy, gluten, egg", Decimal("40")),
        ],
    },
    "Middle Eastern": {
        "appetizer": [
            ("Hummus", "Creamy chickpea dip with olive oil, paprika and pita", True, True, "gluten, sesame", Decimal("55")),
            ("Mezze Platter", "Hummus, baba ghanoush, tabbouleh, olives and flatbread", True, True, "gluten, sesame", Decimal("90")),
            ("Fattoush", "Crispy bread salad with fresh herbs and sumac dressing", True, True, "gluten", Decimal("65")),
            ("Stuffed Vine Leaves", "Rice and herb-filled grape leaves", True, True, None, Decimal("60")),
            ("Labneh", "Strained yoghurt with za'atar and olive oil", False, False, "dairy", Decimal("55")),
        ],
        "main": [
            ("Shawarma Plate", "Spiced chicken with rice, salad and garlic sauce", False, False, "dairy, gluten", Decimal("110")),
            ("Lamb Kebab", "Grilled minced lamb with bulgur and grilled vegetables", False, False, "gluten", Decimal("130")),
            ("Falafel Plate", "Fried chickpea fritters, hummus, salad and flatbread", True, True, "gluten, sesame", Decimal("100")),
            ("Mansaf", "Slow-cooked lamb in jameed sauce with rice and pine nuts", False, False, "dairy, nuts", Decimal("145")),
            ("Shakshuka", "Eggs poached in spiced tomato sauce with bread", False, False, "egg, gluten", Decimal("90")),
            ("Kofta Curry", "Spiced beef meatballs in tomato sauce with rice", False, False, None, Decimal("115")),
        ],
        "side": [
            ("Pita Bread", "Warm fluffy pita, two pieces", True, True, "gluten", Decimal("20")),
            ("Tabbouleh", "Parsley, bulgur, tomato and lemon", True, True, "gluten", Decimal("40")),
            ("Rice", "Steamed basmati rice", True, True, None, Decimal("25")),
        ],
        "dessert": [
            ("Baklava", "Filo pastry with pistachios and honey syrup", False, False, "gluten, nuts, dairy", Decimal("50")),
            ("Kunafa", "Shredded pastry with sweet cheese and rosewater syrup", False, False, "dairy, gluten, nuts", Decimal("60")),
            ("Halva", "Sweet sesame confection with cardamom", True, True, "sesame, nuts", Decimal("40")),
        ],
    },
    "Indian": {
        "appetizer": [
            ("Samosa (2 pcs)", "Crispy pastry filled with spiced potatoes and peas", True, True, "gluten", Decimal("50")),
            ("Onion Bhaji", "Crispy spiced onion fritters with mint chutney", True, True, "gluten", Decimal("50")),
            ("Chicken Tikka", "Tandoor-marinated chicken skewers with raita", False, False, "dairy", Decimal("75")),
            ("Pappadum with Chutneys", "Crispy lentil crackers with three chutneys", True, True, None, Decimal("40")),
            ("Aloo Chaat", "Spiced potato salad with tamarind and yoghurt", False, False, "dairy", Decimal("60")),
        ],
        "main": [
            ("Butter Chicken", "Creamy tomato and cashew curry with basmati rice", False, False, "dairy, nuts", Decimal("120")),
            ("Lamb Rogan Josh", "Slow-cooked lamb in aromatic Kashmiri sauce with rice", False, False, None, Decimal("135")),
            ("Palak Paneer", "Fresh cheese in spiced spinach sauce", False, False, "dairy", Decimal("105")),
            ("Chana Masala", "Chickpeas in tangy tomato-spice gravy", True, True, None, Decimal("100")),
            ("Chicken Biryani", "Fragrant saffron rice with spiced chicken and fried onions", False, False, "dairy", Decimal("125")),
            ("Dal Tadka", "Yellow lentils tempered with cumin and garlic", True, True, None, Decimal("95")),
            ("Fish Curry", "Coastal-style coconut and tamarind fish curry", False, False, "fish", Decimal("130")),
            ("Paneer Tikka Masala", "Grilled cheese in rich tomato-cream sauce", False, False, "dairy", Decimal("110")),
        ],
        "side": [
            ("Naan", "Tandoor-baked flatbread", False, False, "dairy, gluten", Decimal("25")),
            ("Garlic Naan", "Naan with garlic butter and coriander", False, False, "dairy, gluten", Decimal("30")),
            ("Basmati Rice", "Steamed long-grain basmati", True, True, None, Decimal("25")),
            ("Raita", "Cooling yoghurt with cucumber and mint", False, False, "dairy", Decimal("25")),
        ],
        "dessert": [
            ("Gulab Jamun", "Soft milk dumplings in rose syrup", False, False, "dairy, gluten", Decimal("50")),
            ("Mango Kulfi", "Traditional Indian ice cream with mango", False, False, "dairy", Decimal("55")),
            ("Kheer", "Creamy rice pudding with cardamom and pistachios", False, False, "dairy, nuts", Decimal("50")),
        ],
    },
    "Vegan": {
        "appetizer": [
            ("Cashew Cheese Board", "House-made nut cheeses with crackers and fruit", True, True, "nuts, gluten", Decimal("80")),
            ("Edamame Guacamole", "Creamy edamame and avocado dip with tortilla chips", True, True, "gluten", Decimal("65")),
            ("Beetroot Carpaccio", "Thinly sliced beet with horseradish cream and capers", True, True, None, Decimal("70")),
            ("Lentil Soup", "Spiced red lentil soup with lemon and coriander", True, True, None, Decimal("65")),
            ("Stuffed Mushrooms", "Portobello filled with quinoa, sun-dried tomato and herbs", True, True, None, Decimal("70")),
        ],
        "main": [
            ("Buddha Bowl", "Roasted vegetables, chickpeas, avocado, tahini dressing", True, True, "sesame", Decimal("120")),
            ("Jackfruit Tacos (3 pcs)", "Pulled jackfruit with slaw, salsa and lime", True, True, "gluten", Decimal("115")),
            ("Tempeh Stir-fry", "Marinated tempeh with seasonal vegetables and noodles", True, True, "soy, gluten", Decimal("110")),
            ("Mushroom Risotto", "Creamy arborio rice with mixed mushrooms and white wine", True, True, None, Decimal("115")),
            ("Lentil Dal", "Slow-cooked red lentils with turmeric and coconut milk", True, True, None, Decimal("100")),
            ("Cauliflower Steak", "Roasted cauliflower with romesco sauce and crispy chickpeas", True, True, "nuts", Decimal("115")),
            ("Vegan Burger", "Black bean and beet patty with avocado and chipotle mayo", True, True, "gluten", Decimal("110")),
            ("Tofu Ramen", "Rich miso broth with silken tofu, noodles and nori", True, True, "soy, gluten", Decimal("110")),
        ],
        "side": [
            ("Sweet Potato Fries", "Oven-baked with smoked paprika", True, True, None, Decimal("45")),
            ("Side Salad", "Seasonal greens with lemon tahini dressing", True, True, "sesame", Decimal("40")),
            ("Sourdough Bread", "With olive oil and balsamic", True, True, "gluten", Decimal("30")),
        ],
        "dessert": [
            ("Chocolate Avocado Mousse", "Dark chocolate and avocado mousse with berries", True, True, None, Decimal("60")),
            ("Coconut Panna Cotta", "With mango coulis", True, True, None, Decimal("60")),
            ("Banana Nice Cream", "Blended frozen banana with peanut butter", True, True, "peanuts", Decimal("50")),
        ],
    },
}

# (name, description, is_alcoholic, volume_ml, is_hot, base_price_dkk)
# Tier multipliers: 1→×0.85, 2→×1.00, 3→×1.25
# "House Draft Beer" (base 28): tier1=23.80, tier2=28.00, tier3=35.00
# "Table Beer"       (base 35): tier1=29.75, tier2=35.00, tier3=43.75
# → Under-30 filter catches tier1+tier2 (House Draft) and tier1 (Table Beer)
# → Under-40 filter additionally catches tier3 (House Draft) and tier1+tier2 (Table Beer)
NON_ALCOHOLIC_TEMPLATES = [
    ("Still Water",     None,                                    False, None, False, Decimal("20")),
    ("Sparkling Water", None,                                    False,  330, False, Decimal("25")),
    ("Cola",            "Ice-cold classic",                      False,  330, False, Decimal("30")),
    ("Lemonade",        "Freshly squeezed with mint",            False, None, False, Decimal("35")),
    ("Orange Juice",    "Fresh-squeezed",                        False,  250, False, Decimal("35")),
    ("Iced Tea",        "Peach or lemon",                        False,  330, False, Decimal("35")),
    ("Filter Coffee",   None,                                    False,  250, True,  Decimal("30")),
    ("Americano",       None,                                    False,  250, True,  Decimal("35")),
    ("Flat White",      "Double espresso with steamed milk",     False,  200, True,  Decimal("40")),
    ("Oat Latte",       "Espresso with oat milk",                False,  300, True,  Decimal("45")),
    ("Chai Latte",      "Spiced tea with steamed milk",          False,  300, True,  Decimal("45")),
    ("Matcha Latte",    "Ceremonial grade matcha with oat milk", False,  300, True,  Decimal("50")),
]

ALCOHOLIC_TEMPLATES = [
    ("House Draft Beer", "Refreshing 500ml draught beer",        True,  500, False, Decimal("28")),
    ("Table Beer",       "Light 330ml beer, great with food",    True,  330, False, Decimal("35")),
    ("Danish Lager",     "Crisp local draft lager",              True,  330, False, Decimal("50")),
    ("Craft IPA",        "Local craft India Pale Ale",           True,  330, False, Decimal("60")),
    ("House Red Wine",   "Glass of house red",                   True,  150, False, Decimal("60")),
    ("House White Wine", "Glass of house white",                 True,  150, False, Decimal("60")),
]

# ── Restaurants ───────────────────────────────────────────────────────────────
# (name, address, description, price_tier, category_name)

RESTAURANT_DATA = [
    # Asian
    ("Sakura Garden",    "Nørrebrogade 45, 2200 København N",    "Authentic Japanese and pan-Asian cuisine in a cosy Nørrebro setting.", 1, "Asian"),
    ("Wok & Roll",       "Vesterbrogade 72, 1620 København V",   "Quick and flavourful Asian street food with generous portions.", 1, "Asian"),
    ("Golden Dragon",    "Istedgade 34, 1650 København V",       "Cantonese family restaurant with dim sum at weekends.", 1, "Asian"),
    ("Seoul Kitchen",    "Blågårdsgade 18, 2200 København N",    "Korean comfort food — bibimbap, fried chicken and soju cocktails.", 2, "Asian"),
    ("Pho House",        "Griffenfeldsgade 22, 2200 København N","Vietnamese staple serving pho, banh mi and fresh spring rolls.", 1, "Asian"),
    ("Bento Box",        "Fiolstræde 7, 1171 København K",       "Japanese bento sets and sushi rolls at lunch-friendly prices.", 2, "Asian"),
    ("Bamboo Bistro",    "Amagerbrogade 55, 2300 København S",   "Pan-Asian tapas with a twist on classic flavours.", 2, "Asian"),
    ("Chopsticks",       "Gothersgade 28, 1123 København K",     "Reliable Chinese takeaway favourite, open until midnight.", 1, "Asian"),
    ("Thai Corner",      "Frederiksberg Allé 12, 1820 Frederiksberg", "Fragrant Thai curries and pad thai in a tiny neighbourhood spot.", 1, "Asian"),
    ("Noodle Bar KBH",   "Studiestræde 14, 1455 København K",   "Ramen and udon noodle bar popular with students near KU.", 1, "Asian"),
    ("Dim Sum House",    "Ravnsborggade 8, 2200 København N",    "Handmade dim sum, steamed buns and Hong Kong milk tea.", 2, "Asian"),
    ("Umami",            "Smallegade 30, 2000 Frederiksberg",    "Modern Japanese izakaya with sake and sharing plates.", 2, "Asian"),
    ("Peking Garden",    "Borgergade 11, 1300 København K",      "Northern Chinese specialities with the signature roasted duck.", 2, "Asian"),
    # Italian
    ("Trattoria Roma",   "Vesterbrogade 102, 1620 København V",  "Family-run trattoria with handmade pasta and a long wine list.", 2, "Italian"),
    ("Napoli Express",   "Nørrebrogade 88, 2200 København N",    "Neapolitan pizza by the slice — fastest lunch in Nørrebro.", 1, "Italian"),
    ("La Dolce Vita",    "Istedgade 66, 1650 København V",       "Romantic Italian with wood-fired pizza and homemade tiramisu.", 2, "Italian"),
    ("Il Forno",         "Blågårdsgade 4, 2200 København N",     "Artisan sourdough pizza and natural wines in a candlelit space.", 3, "Italian"),
    ("Pasta Fresca",     "Gammel Kongevej 44, 1610 København V", "Fresh pasta made daily; choose your sauce from a seasonal menu.", 2, "Italian"),
    ("Osteria Venezia",  "Fiolstræde 15, 1171 København K",      "Venetian-inspired dishes: cicchetti, risotto and grilled fish.", 2, "Italian"),
    ("Gelato & Pizza",   "Amagerbrogade 30, 2300 København S",   "Student favourite with giant pizza slices and hand-churned gelato.", 1, "Italian"),
    ("Ristorante Toscana","Frederiksberg Allé 40, 1820 Frederiksberg","Tuscan classics in a garden setting — perfect for date nights.", 3, "Italian"),
    ("Pizza Pronto",     "Nørreport, 1358 København K",          "Budget-friendly takeaway pizza near Nørreport station.", 1, "Italian"),
    ("Carmelo",          "Smallegade 5, 2000 Frederiksberg",     "Neighbourhood Italian with generous portions and no fuss.", 2, "Italian"),
    ("Molino",           "Gothersgade 52, 1123 København K",     "Rustic Italian kitchen focusing on wood-fired dishes.", 2, "Italian"),
    ("Sapori d'Italia",  "Ravnsborggade 20, 2200 København N",   "Authentic Italian delicatessen and trattoria in one.", 2, "Italian"),
    # Café
    ("The Reading Room", "Studiestræde 6, 1455 København K",     "Beloved study café with great filter coffee and open sandwiches.", 1, "Café"),
    ("Grød KBH",         "Blågårdsgade 10, 2200 København N",    "Porridge café with sweet and savoury bowls and excellent pastries.", 1, "Café"),
    ("Kaffeplantagen",   "Vesterbrogade 18, 1620 København V",   "Speciality coffee roaster with sourdough toast and brunch plates.", 2, "Café"),
    ("The Yellow Door",  "Nørrebrogade 64, 2200 København N",    "Cosy neighbourhood café popular with KU students — great wifi.", 1, "Café"),
    ("Café Syd",         "Amagerbrogade 78, 2300 København S",   "Amager staple for brunch, smørrebrød and afternoon cake.", 1, "Café"),
    ("Atelier September","Gothersgade 30, 1123 København K",     "Minimalist café known for its avocado toast and ricotta pancakes.", 2, "Café"),
    ("Paludan Bogcafé",  "Fiolstræde 10, 1171 København K",      "Iconic bookshop café in the Latin Quarter — student staple since 1994.", 1, "Café"),
    ("Frederiksberg Kaffeebar","Frederiksberg Allé 55, 1820 Frederiksberg","Neighbourhood coffee bar with homemade cakes and sandwiches.", 1, "Café"),
    ("Den Gamle Mønt",   "Gammel Kongevej 20, 1610 København V", "Vintage-styled café with seasonal brunch and specialty teas.", 2, "Café"),
    ("Mag & Co",         "Borgergade 5, 1300 København K",       "Magazine café and co-working space with quality espresso.", 2, "Café"),
    ("Sortkaffe & Vinyl","Griffenfeldsgade 5, 2200 København N", "Record shop café with pour-over coffee and vinyl playing all day.", 1, "Café"),
    ("Baresso KBH",      "Nørreport, 1358 København K",          "Reliable café near Nørreport with quick lunch options.", 1, "Café"),
    ("Café Norden",      "Strøget 61, 1100 København K",         "Classic Strøget café with a great view and standard brunch fare.", 2, "Café"),
    # Fast Food
    ("Burger Shack",     "Istedgade 20, 1650 København V",       "Smash burgers and loaded fries — the best value burgers in Vesterbro.", 1, "Fast Food"),
    ("Kebabistan",       "Nørrebrogade 120, 2200 København N",   "Late-night shawarma and falafel with house garlic sauce.", 1, "Fast Food"),
    ("Hot Dog Republic", "Vesterbrogade 5, 1620 København V",    "Gourmet Danish hot dogs with creative toppings.", 1, "Fast Food"),
    ("Friske Fries",     "Blågårdsgade 30, 2200 København N",    "Belgian-style fries with 12 dipping sauces.", 1, "Fast Food"),
    ("Chicken House",    "Gothersgade 14, 1123 København K",     "Crispy fried chicken pieces, wraps and boxes.", 1, "Fast Food"),
    ("BurgerMe",         "Frederiksberg Allé 22, 1820 Frederiksberg","Better-burger joint with grass-fed beef and brioche buns.", 2, "Fast Food"),
    ("Pizza Slices Nørre","Nørreport, 1358 København K",         "Huge New York-style slices sold by the slice near Nørreport.", 1, "Fast Food"),
    ("Falafel Brothers", "Griffenfeldsgade 40, 2200 København N","Family-run falafel joint with homemade hummus and pickles.", 1, "Fast Food"),
    ("Taco Town",        "Gammel Kongevej 10, 1610 København V", "Tex-Mex tacos and burritos with a fresh salsa bar.", 1, "Fast Food"),
    ("The Wrap Factory", "Ravnsborggade 14, 2200 København N",   "Build-your-own wraps with fresh ingredients and house sauces.", 1, "Fast Food"),
    ("Fish'n'Chips CPH", "Borgergade 22, 1300 København K",      "Classic British-style fish and chips in the city centre.", 2, "Fast Food"),
    ("Smash & Grill",    "Amagerbrogade 15, 2300 København S",   "Smash burgers, onion rings and thick shakes.", 1, "Fast Food"),
    # Nordic
    ("Smørrebrød & Co",  "Fiolstræde 22, 1171 København K",      "Traditional Danish open sandwiches made with local produce.", 2, "Nordic"),
    ("Nordic Kitchen",   "Studiestræde 25, 1455 København K",    "New Nordic cuisine using foraged and seasonal Danish ingredients.", 3, "Nordic"),
    ("Røde Pølse Huset", "Vesterbrogade 88, 1620 København V",   "Classic Danish red sausage stand with all the toppings.", 1, "Nordic"),
    ("Havfruen Fisk",    "Gothersgade 70, 1123 København K",     "Fresh seafood restaurant focusing on Danish coastal catches.", 3, "Nordic"),
    ("Morgenstedet",     "Ravnsborggade 12, 2200 København N",   "Beloved Nørrebro lunch spot with daily changing Nordic menu.", 1, "Nordic"),
    ("Grønne Kælder",    "Smallegade 15, 2000 Frederiksberg",    "Vegetable-forward Nordic kitchen in a beautiful cellar space.", 2, "Nordic"),
    ("Det Kolde Bord",   "Frederiksberg Allé 68, 1820 Frederiksberg","Scandinavian cold table with herring, gravlax and pickles.", 2, "Nordic"),
    ("Fisketorvet",      "Amagerbrogade 100, 2300 København S",  "Fish market restaurant with fried plaice and shellfish platters.", 2, "Nordic"),
    ("Noma Nearby",      "Borgergade 44, 1300 København K",      "Inspired by New Nordic cooking but at accessible prices.", 2, "Nordic"),
    ("Bornholmsk",       "Griffenfeldsgade 16, 2200 København N","Specialties from the island of Bornholm — smoked fish and rye.", 2, "Nordic"),
    ("Landkøkken",       "Gammel Kongevej 62, 1610 København V", "Farm-to-table Nordic restaurant with a weekly changing menu.", 2, "Nordic"),
    ("Vinterstue",       "Blågårdsgade 38, 2200 København N",    "Cosy Nordic living-room restaurant with hearty winter dishes.", 2, "Nordic"),
    # Middle Eastern
    ("Byblos",           "Istedgade 48, 1650 København V",       "Lebanese cuisine with the best mezze in Vesterbro.", 2, "Middle Eastern"),
    ("Aladdin",          "Blågårdsgade 26, 2200 København N",    "Affordable falafel, shawarma and mixed plates in Nørrebro.", 1, "Middle Eastern"),
    ("Istanbul Grill",   "Vesterbrogade 130, 1620 København V",  "Turkish grill restaurant with doner kebab, köfte and pide.", 1, "Middle Eastern"),
    ("Al-Andalus",       "Nørrebrogade 95, 2200 København N",    "Moroccan-inspired tagines and couscous dishes.", 2, "Middle Eastern"),
    ("Petra",            "Amagerbrogade 42, 2300 København S",   "Jordanian home cooking — mansaf, maqluba and sweet knafeh.", 2, "Middle Eastern"),
    ("Levant",           "Frederiksberg Allé 30, 1820 Frederiksberg","Contemporary Levantine restaurant with creative small plates.", 2, "Middle Eastern"),
    ("Damascus Bakery",  "Griffenfeldsgade 30, 2200 København N","Syrian flatbread, pastries and savoury pies baked fresh daily.", 1, "Middle Eastern"),
    ("Sahara",           "Ravnsborggade 4, 2200 København N",    "North African grill with lamb, chicken and vegetable dishes.", 2, "Middle Eastern"),
    ("Oran",             "Smallegade 22, 2000 Frederiksberg",    "Algerian family restaurant with generous portions and low prices.", 1, "Middle Eastern"),
    ("The Mezze Bar",    "Gothersgade 42, 1123 København K",     "Sharing mezze plates and cocktails in a relaxed setting.", 2, "Middle Eastern"),
    ("Yayla",            "Gammel Kongevej 32, 1610 København V", "Anatolian cuisine: gözleme, pide and Turkish breakfast at weekends.", 1, "Middle Eastern"),
    ("Beirut Street Food","Studiestræde 33, 1455 København K",  "Fast and fresh Lebanese street food near the university.", 1, "Middle Eastern"),
    # Indian
    ("Maharaja Palace",  "Vesterbrogade 56, 1620 København V",   "Classic north Indian restaurant with an extensive curry menu.", 2, "Indian"),
    ("Curry Leaf",       "Nørrebrogade 38, 2200 København N",    "South Indian specialities including dosa, idli and coconut curries.", 1, "Indian"),
    ("Spice Route",      "Istedgade 80, 1650 København V",       "Pan-Indian kitchen with a good selection of vegetarian options.", 2, "Indian"),
    ("Bombay Nights",    "Amagerbrogade 22, 2300 København S",   "Bollywood-themed restaurant with generous Indian buffet at lunch.", 1, "Indian"),
    ("Tandoor House",    "Frederiksberg Allé 8, 1820 Frederiksberg","Tandoor specialist — great naan, tikka and seekh kebabs.", 2, "Indian"),
    ("Desi Dhaba",       "Griffenfeldsgade 48, 2200 København N","Punjabi home cooking at street food prices.", 1, "Indian"),
    ("Saffron",          "Gothersgade 60, 1123 København K",     "Upscale Indian dining with Mughal-inspired dishes and fine wine.", 3, "Indian"),
    ("Chutney & Spice",  "Blågårdsgade 42, 2200 København N",   "Casual Indian café with freshly made chutneys and thali plates.", 1, "Indian"),
    ("Masala Zone",      "Studiestræde 40, 1455 København K",    "Quick Indian with daily specials — popular with KU students.", 1, "Indian"),
    ("Ganges",           "Ravnsborggade 28, 2200 København N",   "River-side themed Indian restaurant with a relaxed atmosphere.", 2, "Indian"),
    ("Biryani House",    "Smallegade 10, 2000 Frederiksberg",    "Famous for their fragrant dum biryani and creamy kormas.", 2, "Indian"),
    ("Namaste KBH",      "Gammel Kongevej 50, 1610 København V", "Nepalese and Indian fusion with momos and butter chicken.", 1, "Indian"),
    ("Royal Curry",      "Borgergade 30, 1300 København K",      "Reliable city-centre Indian with a good value lunch menu.", 2, "Indian"),
    # Vegan
    ("Green Garden",     "Nørrebrogade 55, 2200 København N",    "Fully plant-based restaurant with seasonal global cuisine.", 2, "Vegan"),
    ("Roots",            "Vesterbrogade 40, 1620 København V",   "100% vegan kitchen with a focus on whole ingredients and bold flavours.", 2, "Vegan"),
    ("Plantiful",        "Blågårdsgade 6, 2200 København N",     "Bright and casual vegan café popular with health-conscious students.", 1, "Vegan"),
    ("The Seed",         "Frederiksberg Allé 16, 1820 Frederiksberg","Vegan fine dining with an inventive seasonal tasting menu.", 3, "Vegan"),
    ("Bowl Bar",         "Amagerbrogade 62, 2300 København S",   "Customisable grain bowls, smoothies and raw desserts.", 1, "Vegan"),
    ("Vegan Street Food","Griffenfeldsgade 12, 2200 København N","Street food-style vegan meals: wraps, burgers and loaded fries.", 1, "Vegan"),
    ("Sprout",           "Studiestræde 20, 1455 København K",    "Vegan café with amazing cakes and a great weekend brunch.", 2, "Vegan"),
    ("The Herbivore",    "Ravnsborggade 22, 2200 København N",   "Nørrebro's favourite vegan comfort food spot.", 1, "Vegan"),
    ("Zero Waste Kitchen","Smallegade 28, 2000 Frederiksberg",   "Plant-based cooking with a focus on reducing food waste.", 2, "Vegan"),
    ("Grøn Bistro",      "Gothersgade 8, 1123 København K",      "Elegant vegan bistro with natural wines and seasonal produce.", 2, "Vegan"),
    ("Happy Cow",        "Gammel Kongevej 70, 1610 København V", "Friendly neighbourhood vegan restaurant with large portions.", 1, "Vegan"),
    ("Earth Kitchen",    "Borgergade 12, 1300 København K",      "Globally inspired vegan cooking with a cosy atmosphere.", 2, "Vegan"),
    ("Plant Power",      "Istedgade 60, 1650 København V",       "Fast-casual vegan with burgers, wraps and shakes.", 1, "Vegan"),
]

DEMO_USERS = [
    ("alice",   "alice@alumni.ku.dk",   "password123"),
    ("bob",     "bob@alumni.ku.dk",     "password123"),
    ("charlie", "charlie@alumni.ku.dk", "password123"),
    ("diana",   "diana@alumni.ku.dk",   "password123"),
    ("erik",    "erik@alumni.ku.dk",    "password123"),
]

REVIEW_COMMENTS = [
    "Great food and very student-friendly prices!",
    "Solid choice for a quick lunch between lectures.",
    "Loved the atmosphere, will definitely come back.",
    "Good value for money — portions are generous.",
    "Nothing extraordinary but reliable and affordable.",
    "Hidden gem — highly recommend to fellow students.",
    "Service was a bit slow but the food made up for it.",
    "Perfect spot for a group dinner with classmates.",
    "My go-to place in the area.",
    "Decent food, reasonable prices for Copenhagen.",
    "Great vegetarian options!",
    "Came here with my study group — everyone loved it.",
    "The staff were super friendly and helpful.",
    "A bit noisy at peak hours but absolutely worth it.",
    "Excellent quality for the price point.",
    "Favourite lunch spot near campus!",
    "Very filling portions — perfect after a long study session.",
    "Consistently good every time I visit.",
    "Would have given 5 stars but the wait was long.",
    None,
    None,
    None,
]

ITEM_COUNTS = {
    "appetizer": (1, 2),
    "main":      (3, 5),
    "side":      (1, 2),
    "dessert":   (1, 2),
}


def seed() -> None:
    if db.session.execute(db.select(Category)).first():
        print("Database already seeded — skipping. Drop and recreate the tables to re-seed.")
        return

    print("Seeding categories...")
    cat_objects: dict[str, Category] = {}
    for name, desc in CATEGORY_DATA:
        cat = Category(name=name, description=desc)
        db.session.add(cat)
        cat_objects[name] = cat
    db.session.flush()

    print("Seeding restaurants and menu items...")
    restaurant_objects: list[Restaurant] = []
    for name, address, description, price_tier, cat_name in RESTAURANT_DATA:
        r = Restaurant(
            name=name,
            address=address,
            description=description,
            price_tier=price_tier,
            category=cat_objects[cat_name],
        )
        db.session.add(r)

        multiplier = PRICE_MULTIPLIER[price_tier]
        templates = FOOD_TEMPLATES[cat_name]

        for meal_type, items in templates.items():
            lo, hi = ITEM_COUNTS[meal_type]
            chosen = random.sample(items, min(random.randint(lo, hi), len(items)))
            for fname, fdesc, fveg, fvegan, fallergens, fbase in chosen:
                db.session.add(FoodItem(
                    restaurant=r,
                    name=fname,
                    description=fdesc,
                    price_dkk=fbase * multiplier,
                    type="food",
                    is_vegetarian=fveg,
                    is_vegan=fvegan,
                    allergens=fallergens,
                    meal_type=meal_type,
                ))

        chosen_beverages = (
            random.sample(ALCOHOLIC_TEMPLATES, random.randint(1, 2))
            + random.sample(NON_ALCOHOLIC_TEMPLATES, random.randint(2, 3))
        )
        for bname, bdesc, balc, bvol, bhot, bbase in chosen_beverages:
            db.session.add(Beverage(
                restaurant=r,
                name=bname,
                description=bdesc,
                price_dkk=bbase * multiplier,
                type="beverage",
                is_alcoholic=balc,
                volume_ml=bvol,
                is_hot=bhot,
            ))

        restaurant_objects.append(r)

    db.session.flush()

    print("Seeding users...")
    user_objects: list[User] = []
    for username, email, password in DEMO_USERS:
        u = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(u)
        user_objects.append(u)
    db.session.flush()

    print("Seeding reviews...")
    # Each user reviews ~35 random restaurants, weighted toward positive ratings
    ratings_pool = [3, 3, 4, 4, 4, 4, 5, 5, 5, 2]
    for user in user_objects:
        for restaurant in random.sample(restaurant_objects, 35):
            db.session.add(Review(
                user=user,
                restaurant=restaurant,
                rating=random.choice(ratings_pool),
                comment=random.choice(REVIEW_COMMENTS),
            ))

    db.session.commit()
    print(
        f"Done! Seeded {len(cat_objects)} categories, "
        f"{len(restaurant_objects)} restaurants, "
        f"{len(user_objects)} users, "
        f"{len(user_objects) * 35} reviews."
    )


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
