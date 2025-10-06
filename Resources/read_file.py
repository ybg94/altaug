import json

def read_json_data():
    filepath = 'src/modifiers.json'
    active_affixes = []
    base_names = []
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        if 'bases' in data and isinstance(data['bases'], list):
            for base in data['bases']:
                if isinstance(base, dict) and 'name' in base:
                    base_names.append(base['name'])

        if 'modifiers' in data and isinstance(data['modifiers'], list):
            for modifier in data['modifiers']:
                if isinstance(modifier, dict) and modifier.get('active') == 1 and 'name' in modifier and 'affix' in modifier:
                    active_affixes.append((modifier['name'], modifier['affix']))

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return [], []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return [], []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [], []
    
    return active_affixes, base_names