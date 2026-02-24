import requests
import json
import time

SCRYFALL_SEARCH_URL = "https://api.scryfall.com/cards/search"


# ------------------------------------------------------------
# Fetch cards from Scryfall
# ------------------------------------------------------------

def fetch_planechase_cards(unique_mode="cards"):
    """
    Fetch all Planechase cards (Planes + Phenomena).
    unique_mode:
        "cards"  -> one entry per unique card name
        "prints" -> one entry per printing
    """
    query = 't:plane OR t:phenomenon'

    params = {
        "q": query,
        "unique": unique_mode,
        "order": "name"
    }

    cards = []
    response = requests.get(SCRYFALL_SEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()

    cards.extend(data["data"])

    while data.get("has_more"):
        time.sleep(0.1)  # polite rate limit
        response = requests.get(data["next_page"])
        response.raise_for_status()
        data = response.json()
        cards.extend(data["data"])

    return cards


# ------------------------------------------------------------
# Text Parsing
# ------------------------------------------------------------

def split_oracle_text(oracle_text):
    """
    Splits oracle text into:
    - main_effect
    - chaos_effect

    Chaos trigger starts with:
    'Whenever chaos ensues,'
    """

    if not oracle_text:
        return None, None

    chaos_marker = "Whenever chaos ensues,"

    if chaos_marker in oracle_text:
        before, after = oracle_text.split(chaos_marker, 1)

        main_effect = before.strip()
        chaos_effect = after.strip()

        return main_effect, "Whenever you roll 🌀, " + chaos_effect

    return oracle_text.strip(), None


# ------------------------------------------------------------
# Classification
# ------------------------------------------------------------

def get_planechase_type(card):
    type_line = card.get("type_line", "")

    if type_line.startswith("Plane"):
        return "Plane"
    elif "Phenomenon" in type_line:
        return "Phenomenon"
    else:
        return "Unknown"


def get_source(card):
    """
    Classify the product source.
    """
    set_type = card.get("set_type")
    set_name = card.get("set_name", "")

    if set_type == "secret_lair":
        return "Secret Lair"
    elif set_type == "promo":
        return "Promo / Event"
    elif set_type == "planechase":
        return "Planechase Product"
    elif set_type == "masters":
        return "Masters Set"
    elif set_type == "expansion":
        return "Expansion"
    else:
        return set_name


# ------------------------------------------------------------
# Transformation
# ------------------------------------------------------------

def transform_card(card):
    oracle_text = card.get("oracle_text", "")
    main_effect, chaos_effect = split_oracle_text(oracle_text)

    return {
        "name": card.get("name"),
        "plane_type": get_planechase_type(card),
        "image": card.get("image_uris", {}).get("large"),
        "main_effect": main_effect,
        "chaos_effect": chaos_effect,
        "source": get_source(card),
        "set_code": card.get("set"),
        "set_name": card.get("set_name"),
        "set_type": card.get("set_type"),
        "collector_number": card.get("collector_number"),
        "oracle_id": card.get("oracle_id")
    }


# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------

def main(output_path="deck.json", unique_mode="cards"):
    """
    unique_mode:
        "cards"  -> one per unique card
        "prints" -> one per printing
    """

    print("Fetching Planechase cards...")
    cards = fetch_planechase_cards(unique_mode=unique_mode)

    print(f"Transforming {len(cards)} cards...")
    transformed = [transform_card(card) for card in cards]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transformed, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(transformed)} entries to {output_path}")


if __name__ == "__main__":
    # Change to "prints" if you want every printing instead of unique cards
    main(unique_mode="cards")