import json
from basics import Creature, KEYWORDS

# Load json (http://mtgjson.com/)
json_file = open("SOI.json")
set_json = json.load(json_file)["cards"]
for i in range(len(set_json)):
    for unwanted in ["artist", "flavor", "id", "imageName", "layout",
                     "multiverseid", "number", "type"]:
        try:
            set_json[i].pop(unwanted)
        except KeyError:
            continue
creature_jsons = [card for card in set_json if "Creature" in card["types"]]
for creature_json in creature_jsons:
    try:
        creature_json["keywords"] = [kw for kw in KEYWORDS if \
                                     kw in creature_json["text"]]
    except KeyError:
        continue
creature_list = [Creature(creature_json) for creature_json in creature_jsons]

