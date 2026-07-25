import asyncio
import pkgutil
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, TextIO, override

import orjson

import Utils
from BaseClasses import Item, ItemClassification, MultiWorld, Region, CollectionState
from Options import OptionError
from rule_builder.rules import Has, Rule, True_, And, Or
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import icon_paths
from .options import RandomizeMovement, SpyroAHTOptions, StartingBreath, spyro_options_groups

icon_paths['spyro_aht'] = f'ap:{__name__}/icon.png'

minigame_locs = [
    {
        ("DV: Dragon Egg from Sgt. Byrd", "DV: Light Gem from Sgt. Byrd"),
        ("CD: Dragon Egg from Sgt. Byrd", "CD: Light Gem from Sgt. Byrd"),
        ("IC: Dragon Egg from Sgt. Byrd", "IC: Light Gem from Sgt. Byrd"),
        ("MM: Dragon Egg from Sgt. Byrd", "MM: Light Gem from Sgt. Byrd")
    },
    {
        ("CS: Dragon Egg from Blink", "CS: Light Gem from Blink"),
        ("CR: Dragon Egg from Blink", "CR: Light Gem from Blink"),
        ("FV: Dragon Egg from Blink", "FV: Light Gem from Blink"),
        ("DM: Dragon Egg from Blink", "DM: Light Gem from Blink")
    },
    {
        ("DF: Dragon Egg from Sparx", "DF: Light Gem from Sparx"),
        ("SR: Dragon Egg from Sparx", "SR: Light Gem from Sparx"),
        ("GG: Dragon Egg from Sparx", "GG: Light Gem from Sparx"),
        ("MFb: Dragon Egg from Sparx", "MFb: Light Gem from Sparx")
    },
    {
        ("CS: Dragon Egg from Fredneck", "CS: Light Gem from Fredneck"),
        ("CR: Dragon Egg from Turtle Mother", "CR: Light Gem from Turtle Mother"),
        ("FV: Dragon Egg from Peggy", "FV: Light Gem from Peggy"),
        ("SB: Dragon Egg from Wally", "SB: Light Gem from Wally")
    }
]

###############WORLD CLASS HELPER FUNCTIONS###############
def _load_file(file: str) -> Any:
    return orjson.loads(pkgutil.get_data(__name__, "data/" + file).decode("utf-8")) # type: ignore


def create_item_groups(item_data) -> dict[str, set[str]]:
    item_groups = defaultdict(set)
    for item in item_data:
        item_groups[item['group']].add(item['name'])
        
    return item_groups


def _location_name_to_id(location_data) -> dict[str, int]:
    loc_name_to_id = {}
    for region in location_data.values():
        for location in region['locations']:
            loc_name_to_id[location['name']] = location['id']
            
    return loc_name_to_id
loc_names_to_ids = _location_name_to_id(_load_file("locations.json"))

def create_location_groups(location_data) -> dict[str, set[str]]:
    level_lookup = {
        "DV": "Dragon Village",
        "CS": "Crocovile Swamp",
        "DF": "Dragonfly Falls",
        "CR": "Coastal Remains",
        "CD": "Cloudy Domain",
        "SR": "Sunken Ruins",
        "FV": "Frostbite Village",
        "GG": "Gloomy Glacier",
        "IC": "Ice Citadel",
        "SB": "Stormy Beach",
        "MM": "Molten Mount",
        "MFt": "Magma Falls Top",
        "MFb": "Magma Falls Bottom",
        "DM": "Dark Mine",
        "RL": "Red's Laboratory",
        "Moneybags": "Shop Items"
    }
    
    loc_groups = defaultdict(set)
    for region in location_data.values():
        for location in region['locations']:
            abbreviation = location['name'].split(': ')[0]
            if abbreviation in level_lookup:
                loc_groups[level_lookup[abbreviation]].add(location['name'])
    
    for minigame_type, minigame_list in zip(["Sgt. Byrd", "Blink", "Sparx", "Turret"], minigame_locs):
        for minigame_location in minigame_list:
            loc_groups[minigame_type].update(minigame_location)
        
    return loc_groups


class SpyroAHTWeb(WebWorld):
    option_groups = spyro_options_groups

class SpyroAHTWorld(World):
    """
    Spyro: A Hero's Tail is a 3D platformer and collect-a-thon released in 2004 for the Xbox, Playstation 2 and GameCube.
    """
    game = "Spyro: A Hero's Tail"
    origin_region_name = "START"

    options_dataclass = SpyroAHTOptions
    options: SpyroAHTOptions # type: ignore
    web = SpyroAHTWeb()
    
    item_data = _load_file("items.json")
    item_name_to_id = {i['name']: i['id'] for i in item_data}
    item_name_groups = create_item_groups(item_data)
    
    location_data = _load_file("locations.json")
    location_name_to_id = _location_name_to_id(location_data)
    location_name_groups = create_location_groups(location_data)
    
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        multiworld.early_items[player]['Double Jump'] = 1
        
        self._lg_doors = [70, 20, 95, 45]
        self._boss_lairs = [10, 20, 30, 40]
        self._gadget_costs = [8, 24, 40]  # ball, invincibility, supercharge
        self._starting_realms = []
        self._starting_breath = -1  # represents none
        self._classifications = {i['name']: ItemClassification(i['classification']) for i in _load_file("items.json")}
        self.shop_costs = []
            
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        """Override of World.collect which additionally handles gem events."""
        name = self.collect_item(state, item)
        if name:
            state.add_item(name, self.player)
            if "Gems" in item.name and "VictoryCon" not in item.name:
                gem_amount = int(item.name.split(" ")[0])
                
                if "Blink minigames" in item.name and self.options.blink_gems.value > 0:
                    state.add_item("Gems", item.player, count=gem_amount * (self.options.blink_gems/100))
                else:
                    state.add_item("Gems", item.player, count=gem_amount * (self.options.non_blink_gems/100))
            return True
        return False

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        """Override of World.remove which additionally handles gem events."""
        name = self.collect_item(state, item, True)
        if name:
            state.remove_item(name, self.player)

            if "Gems" in item.name:
                gem_amount = int(item.name.split(" ")[0])
                state.remove_item("Gems", item.player, count=gem_amount)
            return True
        return False

    def generate_early(self) -> None:
        passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if isinstance(passthrough, dict) and self.game in passthrough:
            self._apply_slot_data(passthrough[self.game])
            
        # prevents impossible/restrictive seeds TODO: investigate if this is truly necessary?
        if "Dragon Kingdom" not in self.options.starting_realms.value:
            if self.options.randomize_movement.value == 0 and self.options.shop_randomization.value == 0:
                raise OptionError("Can't start outside Dragon Kingdom if movement and shop randomization is off.")
        
        # silently fixing some goaling issues
        if len(self.options.goal.value) == 0:
            self.options.goal.value = ("Random",)
        if len(self.options.goal.value) > 10:
            raise OptionError("Too many goal entries - must be 10 or less.")

        # resolving random goal entries
        goal_choices = list(self.options.goal.valid_keys)  # copy that has "Random" removed so a random choice doesn't pick another Random
        goal_choices.remove("Random")
        
        # remove any goals excluded from random choice
        for excluded in self.options.exclude_from_goal:
            if excluded in goal_choices:
                goal_choices.remove(excluded)
        
        # figure out how many to randomly choose, then remove all duplicates + the random entry itself
        random_count = self.options.goal.value.count("Random")
        goal_set = set(self.options.goal.value)  # converting to set removes duplicates
        goal_set.remove("Random")
        
        # fill list with random choices, checking along the way to not randomly add one that's already in the list
        for _ in range(random_count):
            random_goal = random.choice(goal_choices)
            while random_goal in goal_set:
                random_goal = random.choice(goal_choices)
            goal_set.add(random_goal)
            
        self.options.goal.value = goal_set
            
        # goaling OptionErrors    
        if "Fireworks" in self.options.goal.value and not self.options.firework_checks.value:
            print("\"Fireworks\" was chosen as goal without firework_checks enabled. Enabling firework_checks automatically.")
            self.options.firework_checks.value = 1
        if "Shop Items" in self.options.goal.value and not self.options.shop_randomization.value:
            print(f"\"Shop Items\" was chosen as goal without shop_randomization enabled. Enabling shop_randomization automatically.")
            self.options.shop_randomization.value = 1
        
    def _apply_slot_data(self, slot_data: dict[str, Any]) -> None:
        self._ut_active = True
        
        self.options.death_link.value = slot_data['death_link']
        
        self.options.goal.value = slot_data['goal']
        self.options.exclude_from_goal.value = slot_data['exclude_from_goal']
        self.options.firework_checks.value = slot_data['firework_checks']
        self.options.vanilla_minigame_rewards.value = slot_data['vanilla_minigame_rewards']
        self.options.filler_items.value = slot_data['filler_items']
        
        self.options.starting_breath.value = slot_data['starting_breath']
        self.options.randomize_movement.value = slot_data['randomize_movement']
        self.options.starting_realms.value = slot_data['starting_realms']
        
        self.options.shop_randomization.value = slot_data['shop_randomization']
        self.options.gem_logic.value = slot_data['gem_logic']
        self.options.key_rings.value = slot_data['key_rings']
        self.options.non_blink_gems.value = slot_data['non_blink_gems']
        self.options.blink_gems.value = slot_data['blink_gems']
        self.options.double_gems.value = slot_data['double_gems']
        
        self._boss_lairs = slot_data['boss_lair_costs']
        self._lg_doors = slot_data['light_gem_door_costs']
        self._gadget_costs = slot_data['gadget_costs']

    def handle_goaling(self):
        # convert goal names to searchable form for location matching
        # in an ideal world, everything would be named in such a way that this isn't necessary, but...¯\_(ツ)_/¯
        convert = {"Fireworks": ": Firework", "Dragon Eggs": ": Dragon Egg", "Dark Gems": ": Dark Gem",
                   "Light Gems": ": Light Gem", "Gnasty Gnorc": "Defeat Gnasty Gnorc", "Ineptune": "Defeat Ineptune",
                   "Red": "Defeat Red", "Mecha-Red": "Defeat Mecha-Red", "Locked Chests": "locked chest", "Shop Items": "Shop Item"}
        victory_cons = []

        # a bit ugly to have triple nested loop but I don't think it's avoidable
        # needs to be "for every location in every region, check every enabled goal for matches" which is just inherently triple-nested
        count = 1
        for reg, region_data in _load_file("locations.json").items():
            for location in region_data["locations"]:
                for goal in self.options.goal.value:
                    if convert[goal] in location["name"]:
                        # skip if shop item is disabled from key rings being on
                        if "Shop Item" in location["name"] and int(location["name"][-2:]) > 18 and self.options.key_rings:
                            continue
                        self.get_region(reg).add_event(f"{location['name']} Victory{count}", f"VictoryCon{count}", rule=self.rule_from_dict(location['access_rule']))
                        victory_cons.append(f"VictoryCon{count}")
                        count += 1

        self.multiworld.completion_condition[self.player] = lambda state: state.has_all(victory_cons, self.player)
    
    def create_regions(self):
        # shop costs determined by multiple options
        if self.options.shop_randomization.value == 1:
            shop_item_count = 18 if self.options.key_rings.value else 56
            blink_total = 20028 * self.options.blink_gems.value // 100
            other_total = 122429 * self.options.non_blink_gems.value // 100
            base_price = (blink_total + other_total) // (shop_item_count-1)
            self.shop_costs.append(0)
            
            if self.options.gem_logic:  # gem logic
                for counter in range(shop_item_count-1):
                    self.shop_costs.append(base_price * (counter + 1))  # each item has incrementing price
                self.shop_costs[-1] = blink_total + other_total 
            else:  # no gem logic
                for counter in range(shop_item_count-1):
                    self.shop_costs.append(base_price)  # each item has same price
            
        if self.options.randomize_gadget_costs.value != 0:
            if self.options.randomize_gadget_costs.value == 2:  # shuffled:
                self.random.shuffle(self._gadget_costs)
            else:  # randomized:
                lmin, lmax = self.options.gadget_cost_min.value, self.options.gadget_cost_max.value
                if lmin > lmax:
                    lmin, lmax = lmax, lmin

                self._gadget_costs = [self.random.randint(lmin, lmax) for _ in range(3)]
            
        if self.options.randomize_boss_lair_door_costs.value != 0:  # if not default
            if self.options.randomize_boss_lair_door_costs.value == 2:  # shuffled:
                self.random.shuffle(self._boss_lairs)
            else:
                bmin, bmax = self.options.boss_lair_door_cost_min.value, self.options.boss_lair_door_cost_max.value
                if bmin > bmax:
                    bmin, bmax = bmax, bmin

                self._boss_lairs = [self.random.randint(bmin, bmax) for _ in range(4)]
            
            if self.options.boss_lair_forcing.value < 4:  # if not "unchanged"
                lowest = min(self._boss_lairs)
                low_index = self._boss_lairs.index(lowest)
                highest = max(self._boss_lairs)
                high_index = self._boss_lairs.index(highest)
                self._boss_lairs[low_index], self._boss_lairs[high_index] = self._boss_lairs[high_index], self._boss_lairs[low_index] 

        if self.options.randomize_light_gem_door_costs.value != 0:
            if self.options.randomize_light_gem_door_costs.value == 2:  # shuffled:
                self.random.shuffle(self._lg_doors)
            else:
                lmin, lmax = self.options.light_gem_door_cost_min.value, self.options.light_gem_door_cost_max.value
                if lmin > lmax:
                    lmin, lmax = lmax, lmin

                self._lg_doors = [self.random.randint(lmin, lmax) for _ in range(4)]

        data = _load_file("locations.json")

        self.multiworld.regions.extend(Region(r['name'], self.player, self.multiworld) for r in data.values())

        for r in data.values():
            region = self.get_region(r['name'])
            for con in r['connections']:
                c = self.get_region(con)
                entrance = f'{region.name}=>{c.name}'
                region.connect(c, entrance, rule=self.rule_from_dict(data[con]['access_rule']))

        for r in data.values():
            region = self.get_region(r['name'])
            f = {}
            for l in r['locations']:
                add = True
                for options in l.get('options', ()):
                    option = getattr(self.options, options['option'])
                    match options.get('operator', 'eq'):
                        case 'eq':
                            add = add and option.value == options['value']
                        case 'ne':
                            add = add and option.value != options['value']
                        case 'gt':
                            add = add and option.value > options['value']
                        case 'ge':
                            add = add and option.value >= options['value']
                        case 'lt':
                            add = add and option.value < options['value']
                        case 'le':
                            add = add and option.value <= options['value']
                if add:
                    f[l['name']] = l['id']
            region.add_locations(f)
            
        self.handle_goaling()

        # add gem events, only if shop is randomized with gem logic
        if self.options.shop_randomization and self.options.gem_logic:
            for reg, region_data in data.items():
                for gem_event in region_data["gem_events"]:
                    location_name = f"{reg}: {gem_event['name']}"
                    self.get_region(reg).add_event(location_name, gem_event['name'], rule=self.rule_from_dict(gem_event["access_rule"]))
    
    def create_item(self, name: str) -> Item:
        """Helper method for create_items which returns an Item object."""
        return Item(name, self._classifications[name], self.item_name_to_id[name], self.player)

    def setup_filler_list(self, item_data) -> tuple[list, list[list]]:
        """Helper method for generating a list of filler items, from which filler items will be chosen
        at random in create_items."""
        all_filler_items = [item for item in item_data if item["group"] == "Filler"]
        enabled_categories = []
        final_filler_choices = [[], [], [], []]  # list of 4 lists, one for each category
        for category in ["Dragon Eggs", "Breath Bombs", "Gem Packs", "Generics"]:
            if category in self.options.filler_items.value:
                enabled_categories.append(category)
                
        for filler_item in all_filler_items:
            if filler_item["name"] == "Gem Pack" and "Gem Packs" in enabled_categories:
                final_filler_choices[0].append(filler_item["name"])
            elif filler_item["name"] == "Dragon Egg" and "Dragon Eggs" in enabled_categories:
                final_filler_choices[1].append(filler_item["name"])
            elif "Bomb" in filler_item["name"] and "Breath Bombs" in enabled_categories:
                final_filler_choices[2].append(filler_item["name"])
            elif filler_item.get("type", "") == "Generic" and "Generics" in enabled_categories:
                final_filler_choices[3].append(filler_item["name"])
        
        return enabled_categories, final_filler_choices
    
    def create_items(self) -> None:
        item_data = _load_file("items.json")
        itempool = []
        
        minigames = 0
        for npc, npc_list in zip(["Sgt. Byrd", "Blink", "Sparx", "Turret"], minigame_locs):
            if npc in self.options.vanilla_minigame_rewards.value:
                for egg, light_gem in npc_list:
                    self.get_location(egg).place_locked_item(self.create_item("Dragon Egg"))
                    self.get_location(light_gem).place_locked_item(self.create_item("Light Gem"))
                minigames += 4
        
        starting = self.options.starting_breath.value
        for breath_num, breath_name in zip(range(4), ["Fire Breath", "Electric Breath", "Water Breath", "Ice Breath"]):
            if starting == breath_num:
                self.get_location("Starter Checks: Breath").place_locked_item(self.create_item(breath_name))
                self._starting_breath = breath_num
                break

        if self.options.randomize_movement.value == 0:
            self.get_location("Starter Checks: Swim").place_locked_item(self.create_item("Swim"))
            self.get_location("Starter Checks: Charge").place_locked_item(self.create_item("Charge"))
            self.get_location("Starter Checks: Glide").place_locked_item(self.create_item("Glide"))
        
        if len(self.options.starting_realms.value) == 0:  # randomize it
            self._starting_realms.append(self.random.choice(["Dragon Kingdom", "Lost Cities", "Icy Wilderness", "Volcanic Isle"]))
        else:
            self._starting_realms = self.options.starting_realms.value
            
        # add starting realm choices to start inventory, if not already in start inventory
        added_realms = []
        for realm in self._starting_realms:
            new_card = self.create_item(f"{realm} Access Card")
            if new_card not in self.multiworld.precollected_items[self.player]:  # don't add the card if the player already put it there
                self.push_precollected(new_card)
                added_realms.append(realm)
        
        for item in item_data:
            if item["group"] == "Filler":  # filler handled later
                continue
            if item['name'] in added_realms:  # exclude any access cards the player already added above
                continue
            
            add = True

            match item['name']:
                case "Fire Breath":
                    add = self._starting_breath != 0
                case "Electric Breath":
                    add = self._starting_breath != 1
                case "Water Breath":
                    add = self._starting_breath != 2
                case "Ice Breath":
                    add = self._starting_breath != 3
                case "Glide" | "Charge" | "Swim":
                    add = self.options.randomize_movement.value == 1

            for curr_option in item.get("option", ()):
                option = getattr(self.options, curr_option['option'])
                match curr_option.get('operator', 'eq'):
                    case 'eq':
                        add = add and option.value == curr_option['value']
                    case 'ne':
                        add = add and option.value != curr_option['value']
                    case 'gt':
                        add = add and option.value > curr_option['value']
                    case 'ge':
                        add = add and option.value >= curr_option['value']
                    case 'lt':
                        add = add and option.value < curr_option['value']
                    case 'le':
                        add = add and option.value <= curr_option['value']

            if add:
                count = item.get('count', 1)
                if item['name'] == 'Light Gem':  # dragon eggs are handled above separately since they are fully filler now
                    count -= minigames

                for _ in range(count):
                    itempool.append(self.create_item(item['name']))
                
        # add filler. Randomly chooses a category, then within the list of items for that category, randomly chooses one.
        filler_categories, filler_items = self.setup_filler_list(item_data)
        convert = {"Gem Packs": 0, "Dragon Egs": 1, "Breath Bombs": 2, "Generics": 3}
        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            random_category = self.random.choice(filler_categories)
            while random_category not in filler_categories:
                random_category = self.random.choice(filler_categories)
            filler_choices = filler_items[convert[random_category]]
            itempool.append(self.create_item(self.random.choice(filler_choices)))

        self.multiworld.itempool.extend(itempool)
  
    def set_rules(self) -> None:
        data = _load_file("locations.json")
        for r in data.values():
            for l in r['locations']:
                try:
                    loc = self.get_location(l['name'])
                except KeyError:
                    continue
                self.set_rule(loc, self.rule_from_dict(l['access_rule']))
    
    def fill_slot_data(self):
        r: dict[str, Any] = {
            "death_link": self.options.death_link.value,
            "goal": self.options.goal.value,
            "exclude_from_goal": self.options.exclude_from_goal.value,
            "firework_checks": self.options.firework_checks.value,
            "vanilla_minigame_rewards": self.options.vanilla_minigame_rewards.value,
            "filler_items": self.options.filler_items.value,

            "starting_breath": self.options.starting_breath.value,
            "randomize_movement": self.options.randomize_movement.value,
            "starting_realms": self._starting_realms,

            "shop_randomization": self.options.shop_randomization.value,
            "gem_logic": self.options.gem_logic.value,
            "key_rings": self.options.key_rings.value,
            "non_blink_gems": self.options.non_blink_gems.value,
            "blink_gems": self.options.blink_gems.value,
            "double_gems": self.options.double_gems.value,
            "shop_costs": self.shop_costs,

            "randomize_boss_lair_doors": self.options.randomize_boss_lair_door_costs.value,
            "boss_lair_costs": self._boss_lairs,
            "boss_lair_forcing": self.options.boss_lair_forcing.value,
            "randomize_light_gem_door_costs": self.options.randomize_light_gem_door_costs.value,
            "light_gem_door_costs": self._lg_doors,
            "randomize_gadget_costs": self.options.randomize_gadget_costs.value,
            "gadget_costs": self._gadget_costs,

            "hint_minigame_rewards": self.options.hint_minigame_rewards.value,
            "hint_boss_rewards": self.options.hint_boss_rewards.value,
            "easy_bosses": self.options.easy_bosses.value,
            "skip_cutscenes": self.options.skip_cutscenes.value,
            "skip_elevators": self.options.skip_elevators.value,
            "teleport_across_realms": self.options.teleport_across_realms.value,
            "open_world_mode": self.options.open_world_mode.value,
        }
        
        return r
    
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data
    
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        super().write_spoiler(spoiler_handle)
        
        if self.options.shop_randomization:
            spoiler_handle.write(f"Shop Prices:                     {self.shop_costs}\n")
        spoiler_handle.write(f"Boss Lair Costs:                 {self._boss_lairs}\n")
        spoiler_handle.write(f"Light Gem Door Costs:            {self._lg_doors}\n")
        spoiler_handle.write(f"Gadget Costs:                    {self._gadget_costs}\n")

###############LOGIC RULES###############
@dataclass
class BossLairRule(Rule[SpyroAHTWorld], game="Spyro: A Hero's Tail"):
    index: int

    @override
    def _instantiate(self, world: SpyroAHTWorld) -> Rule.Resolved:
        return Has("Dark Gem", world._boss_lairs[self.index]).resolve(world)


@dataclass
class LGDoorRule(Rule[SpyroAHTWorld], game="Spyro: A Hero's Tail"):
    index: int

    @override
    def _instantiate(self, world: SpyroAHTWorld) -> Rule.Resolved:
        return Has("Light Gem", world._lg_doors[self.index]).resolve(world)


@dataclass
class BallGadget(Rule[SpyroAHTWorld], game="Spyro: A Hero's Tail"):
    @override
    def _instantiate(self, world: SpyroAHTWorld) -> Rule.Resolved:
        return Has("Light Gem", world._gadget_costs[0]).resolve(world)


@dataclass
class InvincibilityGadget(Rule[SpyroAHTWorld], game="Spyro: A Hero's Tail"):
    @override
    def _instantiate(self, world: SpyroAHTWorld) -> Rule.Resolved:
        return Has("Light Gem", world._gadget_costs[1]).resolve(world)


@dataclass
class SuperchargeGadget(Rule[SpyroAHTWorld], game="Spyro: A Hero's Tail"):
    @override
    def _instantiate(self, world: SpyroAHTWorld) -> Rule.Resolved:
        return And(Has("Light Gem", world._gadget_costs[2]), Has("Charge")).resolve(world)


@dataclass
class LockedChestRule(Rule[SpyroAHTWorld], game="Spyro: A Hero's Tail"):
    level: str

    @override
    def _instantiate(self, world: SpyroAHTWorld) -> Rule.Resolved:
        if world.options.shop_randomization.value == 1:
            if world.options.key_rings.value == 1:
                if self.level == "Reds Laboratory": self.level = "Red's Laboratory"  # fixing from formatting in local data not having apostraphes
                return Has(f"{self.level} Key Ring", 1).resolve(world)
            else:
                return Has(f"Lockpick", 52).resolve(world)
        else:  # always true when shops are unrandomized
            return True_().resolve(world)
    
    
@dataclass
class ShopCheckRule(Rule[SpyroAHTWorld], game="Spyro: A Hero's Tail"):
    index: int
    
    #override
    def _instantiate(self, world: SpyroAHTWorld) -> Rule.Resolved:
        if world.options.gem_logic:  # if gem logic in use, check Gems pseudo-item
            cost_lookup = world.shop_costs[self.index]
            return Has("Gems", cost_lookup).resolve(world)
        else:
            return True_().resolve(world)  # always seen as accessible if gem logic is not in use

###############CLIENT###############
def _run_client(*args: str):
    import colorama
    from CommonClient import server_loop, gui_enabled, get_base_parser
    Utils.init_logging("Spyro: A Hero's Tail Client")

    async def _main(connect: str | None, password: str | None):
        from .context import SpyroAHTContext, tracker_loaded
        ctx = SpyroAHTContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        await ctx.exit_event.wait()
        ctx.watcher_event.set()
        ctx.server_address = None
        await ctx.shutdown()
    
    parser = get_base_parser()
    parsed_args = parser.parse_args(args)
    colorama.init()
    asyncio.run(_main(parsed_args.connect, parsed_args.password))
    colorama.deinit()

def run_client():
    from multiprocessing import Process
    Process(target=_run_client,name="SpyroAHTClient").start()

from worlds.LauncherComponents import Component, components
components.append(Component("Spyro AHT Client", func=run_client, icon='spyro_aht'))
