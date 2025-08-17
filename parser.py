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
    
    # Extract height and weight from any table
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            tds = row.find_all("td")
            
            # Check for height row
            if len(tds) >= 2 and "height" in tds[0].text.strip().lower():
                height_value = tds[1].text.strip()
                if "'" in height_value:
                    feet, inches = height_value.split("'")
                    inches = inches.replace('"', '').strip()
                    player_data["height"] = f"{feet},{inches}" if inches else feet
            
            # Check for weight row
            if len(tds) >= 2 and "weight" in tds[0].text.strip().lower():
                weight_value = tds[1].text.strip()
                if "kg" in weight_value:
                    try:
                        player_data["weight"] = int(weight_value.replace("kg", "").strip())
                    except ValueError:
                        pass
    
    # Attribute mapping with common variations
    attribute_map = {
        "corners": "Corners",
        "crossing": "Crossing",
        "dribbling": "Dribbling",
        "finishing": "Finishing",
        "first touch": "First Touch",
        "heading": "Heading",
        "long shots": "Long Shot",
        "long throws": "Long Throws",
        "marking": "Marking",
        "passing": "Passing",
        "penalty taking": "Penalty Taking",
        "tackling": "Tackling",
        "technique": "Technique",
        "aggression": "Aggression",
        "anticipation": "Anticipation",
        "bravery": "Bravery",
        "composure": "Composure",
        "concentration": "Concentration",
        "decisions": "Decisions",
        "determination": "Determination",
        "flair": "Flair",
        "leadership": "Leadership",
        "off the ball": "Off the Ball",
        "positioning": "Positioning",
        "teamwork": "Teamwork",
        "vision": "Vision",
        "work rate": "Work Rate",
        "acceleration": "Acceleration",
        "agility": "Agility",
        "balance": "Balance",
        "jumping reach": "Jumping Reach",
        "natural fitness": "Natural Fitness",
        "pace": "Pace",
        "stamina": "Stamina",
        "strength": "Strength",
        "aerial reach": "Aerial Reach",
        "command of area": "Command of Area",
        "communication": "Communication",
        "eccentricity": "Eccentricity",
        "handling": "Handling",
        "kicking": "Kicking",
        "one on ones": "One on Ones",
        "punching": "Punching",
        "reflexes": "Reflexes",
        "rushing": "Rushing",
        "throwing": "Throwing"
    }
    
    # Extract attributes from tables
    for table in soup.find_all("table"):
        # Skip empty tables
        if not table.find("tr"):
            continue
            
        # Process each row
        for row in table.find_all("tr")[1:]:  # Skip header row
            cols = row.find_all("td")
            if len(cols) < 2:
                continue
                
            # Handle both 2-column and 3-column formats
            if len(cols) == 3:
                # Format: Attribute | ? | Value
                attr_name = cols[0].text.strip().lower()
                attr_value = cols[2].text.strip()
            else:
                # Format: Attribute | Value
                attr_name = cols[0].text.strip().lower()
                attr_value = cols[1].text.strip()
            
            # Map to normalized name
            if attr_name in attribute_map:
                norm_name = attribute_map[attr_name]
                if attr_value.isdigit():
                    player_data["attributes"][norm_name] = int(attr_value)
    
    return player_data