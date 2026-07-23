import json

# These are imported so that eval() can recognize them as types below
from rule_builder.rules import Rule, True_, Has, HasAll, And, HasAny, Or
from worlds.spyro_aht import BossLairRule, BallGadget, LGDoorRule, InvincibilityGadget, SuperchargeGadget, \
    ShopCheckRule, LockedChestRule

regions = {}
########################################################################################################################
# load regions
file_in = open("1 - region list.txt", "r")
for line in file_in:
    line = line.strip()
    regions[line] = {
        "name": line,
        "connections": [],
        "access_rule": {},
        "locations": [],
        "gem_events": []
    }
file_in.close()

########################################################################################################################
# load region connections
file_in = open("2 - region connections.txt", "r")
for line in file_in:
    line = line.strip()
    region_from, region_to = line.split(" -> ")
    regions[region_from]["connections"].append(region_to)
file_in.close()

########################################################################################################################
# load region access
file_in = open("3 - region access.txt", "r")
for line in file_in:
    line = line.strip()
    region, rule = line.split(" | ")
    evaluated_rule: Rule = eval(rule)
    regions[region]["access_rule"] = evaluated_rule.to_dict()
file_in.close()

########################################################################################################################
# load locations
file_in = open("4 - locations.txt", "r")
for line in file_in:
    line = line.strip()
    region, loc_name, loc_id, loc_rule = line.split(" | ")
    options = []  # default, overridden below if an optionable location is encountered
    evaluated_rule: Rule = eval(loc_rule)

    if "Shop Item" in loc_name:
        options = [{
            "option": "shop_randomization",
            "value": 1
        }]
        if int(loc_name[-2:]) > 18:
            options.append({
                "option": "key_rings",
                "value": 0
            })
    elif "Firework" in loc_name:
        options = [{
            "option": "firework_checks",
            "value": 1
        }]

    regions[region]["locations"].append({
        "name": loc_name,
        "id": int(loc_id),
        "options": options,
        "access_rule": evaluated_rule.to_dict()
    })
file_in.close()

########################################################################################################################
# load gem events
file_in = open("5 - gem events.txt", "r")
for line in file_in:
    line = line.strip()
    region, event_name, event_rule = line.split(" | ")
    gem_amount = int(event_name.split(" ", 1)[0])  # ugly one-liner but it works
    evaluated_rule: Rule = eval(event_rule)

    regions[region]["gem_events"].append({
        "name": event_name,
        "gem_amount": gem_amount,
        "options": [],
        "access_rule": evaluated_rule.to_dict()
    })

########################################################################################################################
# output
file_out = open("test-locations.json", "w")
output = json.dumps(regions, indent=4)
file_out.write(output)