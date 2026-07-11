import json

def handle_multiple(the_rule, children):
    return {
        "rule": the_rule,
        "options": [],
        "filtered_resolution": "false",
        "children": children
    }

def handle_lgdoors_bosses(the_rule):
    return {
        "rule": the_rule[:-2],
        "options": [],
        "filtered_resolution": "false",
        "args": {
            "index": int(the_rule[-1])
        }
    }

def handle_gadgets_and_chest(the_rule, level = None):
    entry = {
        "rule": the_rule,
        "options": [],
        "filtered_resolution": "false",
        "args": {}
    }
    if the_rule == "LockedChestRule":
        entry['args'] = {
            "level": level
        }
    return entry

def handle_access_cards(the_item):
    return {
        "rule": "RealmAccessRule",
        "options": [],
        "filtered_resolution": "false",
        "args": {
            "realm": the_item.split(" ", 1)[1]
        }
    }

def handle_single_loc_rule(the_name, the_id, the_rule, the_option):
    if the_rule['args']['item_name'] in ["True_", "BallGadget", "InvincibilityGadget", "SuperchargeGadget"]:
        the_rule['rule'] = the_rule['args']['item_name']
        the_rule['args'].clear()

    return {
        "name": the_name,
        "id": the_id,
        "access_rule": the_rule,
        "options": the_option
    }

def handle_mult_loc_rules(the_rules, the_sep, the_name, the_id, the_option):
    return {
        "name": the_name,
        "id": the_id,
        "access_rule": {
            "rule": the_sep,
            "options": [],
            "filtered_resolution": "false",
            "children": the_rules  # probably needs editing?
        },
        "options": the_option
    }

def handle_special_case(the_case, the_rule):
    new_entry = {
        "rule": the_case,
        "options": [],
        "filtered_resolution": "false",
        "args": {}
    }
    if the_case == "LockedChestRule":
        new_entry["args"]["level"] = the_rule.split(" ", 1)[1]


    return new_entry

########################################################################################################################
# initialize regions and load connections
regions = {}
file_in = open("1 - region connections.txt", "r")

for line in file_in:
    split_line = line.split("|")
    region_name = split_line[0].strip()
    connections = []

    for c in split_line[1].strip().split(" "):
        if c != "NONE":
            connections.append(c)

    regions[region_name] = {
        "name": region_name,
        "connections": connections
    }
file_in.close()
########################################################################################################################
# load access rules
file_in = open("2 - region access.txt", "r")
for line in file_in:
    split_line = line.split("|")
    region_name = split_line[0].strip()
    items, rules = [], []

    for r in split_line[1].strip().split(", "):
        lov_rule = r.split(" ", 1)[0].strip()
        item = r.split(" ", 1)[1].strip()

        if "RealmAccessRule" in item:
            new_rule = handle_access_cards(item)
        elif "Boss" in item or "LGDoor" in item:
            new_rule = handle_lgdoors_bosses(item)
        elif "Gadget" in item:
            new_rule = handle_gadgets_and_chest(item)
        else:
            new_rule = {
                "rule": lov_rule,
                "options": [],
                "filtered_resolution": "false",
                "args": {
                    "item_name": item,
                    "count": 1
                }
            }
            if lov_rule == "True_": new_rule["args"].clear()  # this is the only difference

        rules.append(new_rule)

    if len(rules) == 1:
        regions[region_name]["access_rule"] = rules[0]
    else:
        regions[region_name]["access_rule"] = handle_multiple(split_line[2].strip(), rules)
file_in.close()
########################################################################################################################
# load locations
file_in = open("3 - locations.txt", "r")

for line in file_in:
    split_line = line.split("-", 1)
    region_name = split_line[0]
    region_locations = []

    for location_full in eval(split_line[1]):
        split_location = location_full.split("|")
        loc_name, loc_rule_full, loc_id = location_full.split("|")

        # assume this location has one rule at first, then check if there's more
        split_loc_rule = [loc_rule_full]
        for s in ["And", "Or"]:
            if loc_rule_full.find(s) != -1:
                split_loc_rule = loc_rule_full.split(s)
                sep = s

        split_loc_rule = [r.strip() for r in split_loc_rule]
        loc_rules, option = [], []

        # special cases at the location level. Will get appended regardless
        if "Firework" in loc_name:
            option.append({
                "option": "randomize_fireworks",
                "value": 1
            })
        elif "Shop Item" in loc_name:
            option.append({
                "option": "randomize_shop_items",
                "value": 1
            })
            if int(loc_name[-3:]) > 18:
                option.append({
                    "option": "key_rings",
                    "value": 0
                })
        elif "Defeat" in loc_name:
            option.append({
                "option": "realm_access",
                "value": 2
            })
        elif "Starting Realm" in loc_name:
            option.append({
                "option": "realm_access",
                "value": 0,
                "operator": "ne"
            })


        for curr_rule in split_loc_rule:
            # curr_rule will be a single requirement
            # e.g. in "Charge Or Glide", curr_rule would be "Charge" first, and then "Glide"

            # check if non-standard
            for case in ["True_", "BallGadget", "InvincibilityGadget", "SuperchargeGadget", "LockedChestRule"]:
                if case in curr_rule:
                    entry = handle_special_case(case, curr_rule)
                    loc_rules.append(entry)
                    break
            else:  # only happens if the above loop didn't find any special cases
                entry = {
                    "rule": "Has",
                    "options": [],
                    "filtered_resolution": "false",
                    "args": {
                        "item_name": curr_rule,
                        "count": 1
                    }
                }
                loc_rules.append(entry)

        # if here, all rules have been parsed
        # might only be 1 - easy to handle if so
        if len(loc_rules) == 1:
            region_locations.append({
                "name": loc_name.strip(),
                "id": int(loc_id),
                "options": option,
                "access_rule": loc_rules[0]
            })
        else:
            region_locations.append({
                "name": loc_name.strip(),
                "id": int(loc_id),
                "options": option,
                "access_rule": {
                    "rule": sep,
                    "options": [],
                    "filtered_resolution": "false",
                    "children": loc_rules
                }
            })

    regions[region_name]["locations"] = region_locations

###################################################################################
# output
file_out = open("test-locations.json", "w")
output = json.dumps(regions, indent=4)
output = output.replace('"filtered_resolution": "false"', '"filtered_resolution": false')  # ¯\_(ツ)_/¯
file_out.write(output)