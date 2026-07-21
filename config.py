import json

def load_config():
    with open("config.json", "r") as f:
        data = json.load(f)
    
    return data

