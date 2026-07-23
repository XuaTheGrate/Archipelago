from rule_builder.rules import True_, Has, HasAll, HasAny, And, Or
from worlds.spyro_aht import BossLairRule, BallGadget, LGDoorRule, ShopCheckRule, InvincibilityGadget, SuperchargeGadget, LockedChestRule
types = [True_, Has, HasAll, HasAny, And, Or, BossLairRule, BallGadget, LGDoorRule, ShopCheckRule, InvincibilityGadget, SuperchargeGadget, LockedChestRule]

file_in = open("worlds/spyro_aht/setup/2 - region access.txt", "r")
region_access = True
for line in file_in:
    region = line.split(" | ")[0]
    access_rule = line.split(" | ")[1].strip()
    try:
        evaluated_rule = eval(access_rule)
    except:
        print(f"region {region}'s access rule of {access_rule} error'd.")
        region_access = False
        break
    finally:
        if type(evaluated_rule) not in types:
            print(f"region {region}'s access rule of {access_rule} didn't have a matching type in the list.")
            region_access = False
            break
file_in.close()

file_in = open("worlds/spyro_aht/setup/3 - locations.txt", "r")
locations = True
for line in file_in:
    region = line.split(" | ")[0]
    access_rule = line.split(" | ")[3].strip()
    try:
        evaluated_rule = eval(access_rule)
    except:
        print(f"location {line.split(" | ")[1]}'s access rule of {access_rule} error'd.")
        locations = False
        break
    finally:
        if type(evaluated_rule) not in types:
            print(f"location {line.split(" | ")[1]}'s access rule of {access_rule} didn't have a matching type in the list.")
            locations = False
            break
file_in.close()

file_in = open("worlds/spyro_aht/setup/4 - gem events.txt", "r")
gem_events = True
for line in file_in:
    region = line.split(" | ")[0]
    access_rule = line.split(" | ")[2].strip()
    try:
        evaluated_rule = eval(access_rule)
    except:
        print(f"gem event {line.split(" | ")[1]}'s access rule of {access_rule} error'd.")
        gem_events = False
        break
    finally:
        if type(evaluated_rule) not in types:
            print(f"gem event {line.split(" | ")[1]}'s access rule of {access_rule} didn't have a matching type in the list.")
            gem_events = False
            break
file_in.close()

if region_access and locations and gem_events:
    print("-----SUCCESS-----")
    print("done! look at you go, programmer boy ^.^")
else:
    print("-----FAILED-----")
    print("failed...try again, programmer boy :(")