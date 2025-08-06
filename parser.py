from bs4 import BeautifulSoup

def parse_player_html(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    # Initialize with default values
    player_data = {
        "attributes": {},
        "height": "",
        "weight": 75  # Default weight
    }
    
    # Extract height
    height_row = soup.find("td", string="Height")
    if height_row:
        height_td = height_row.find_next_sibling("td")
        if height_td:
            height_value = height_td.text.strip()
            # Convert to our format (6'0" -> "6,0")
            if "'" in height_value:
                feet, inches = height_value.split("'")
                inches = inches.replace('"', '').strip()
                player_data["height"] = f"{feet},{inches}" if inches else feet
    
    # Extract weight
    weight_row = soup.find("td", string="Weight")
    if weight_row:
        weight_td = weight_row.find_next_sibling("td")
        if weight_td:
            weight_value = weight_td.text.strip()
            if "kg" in weight_value:
                player_data["weight"] = int(weight_value.replace("kg", "").strip())
    
    # Attribute mapping
    attribute_map = {
        "Corners": "Corners",
        "Crossing": "Crossing",
        "Dribbling": "Dribbling",
        "Finishing": "Finishing",
        "First Touch": "First Touch",
        "Heading": "Heading",
        "Long Shots": "Long Shot",
        "Passing": "Passing",
        "Technique": "Technique",
        "Aggression": "Aggression",
        "Anticipation": "Anticipation",
        "Bravery": "Bravery",
        "Composure": "Composure",
        "Concentration": "Concentration",
        "Decisions": "Decisions",
        "Determination": "Determination",
        "Flair": "Flair",
        "Leadership": "Leadership",
        "Off The Ball": "Off the Ball",
        "Positioning": "Positioning",
        "Teamwork": "Teamwork",
        "Vision": "Vision",
        "Work Rate": "Work Rate",
        "Acceleration": "Acceleration",
        "Agility": "Agility",
        "Balance": "Balance",
        "Jumping Reach": "Jumping Reach",
        "Natural Fitness": "Natural Fitness",
        "Pace": "Pace",
        "Stamina": "Stamina",
        "Strength": "Strength"
    }
    
    # Extract attributes from tables
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")[1:]  # Skip header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                attr_name = cols[0].text.strip()
                attr_value = cols[2].text.strip()
                
                # Map to our attribute names
                if attr_name in attribute_map:
                    norm_name = attribute_map[attr_name]
                    if attr_value.isdigit():
                        player_data["attributes"][norm_name] = int(attr_value)
    
    return player_data