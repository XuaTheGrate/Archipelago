import asyncio
from dataclasses import dataclass
import functools
import pkgutil
from collections import defaultdict
from typing import Any, TextIO, override

import orjson

from Options import OptionError
import Utils
from BaseClasses import Item, ItemClassification, MultiWorld, Region, CollectionState
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, Rule, True_, And, Or
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import icon_paths

from .options import RandomizeMovement, SpyroAHTOptions, RandomizeBreath, spyro_options_groups
from .client import rules

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


location_rules: dict[str, dict] = {}
_k = _load_file("locations.json")
for n, r in _k.items():
    location_rules[n] = r
    r['access_rule'] = rules.rule_from_dict(r['access_rule'])
    locs = []
    for l in r['locations']:
        l['access_rule'] = rules.rule_from_dict(l['access_rule'])
        locs.append(l)
    r['locations'] = locs

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

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        multiworld.early_items[player]['Double Jump'] = 1  # 
        
        self._lg_doors = [70, 20, 95, 45]
        self._boss_lairs = [10, 20, 30, 40]
        self._gadget_costs = [8, 24, 40]  # ball, invincibility, supercharge
        self._starting_realm = 0
        self._starting_breath = -1  # represents none
        self._classifications = {i['name']: ItemClassification(i['classification']) for i in _load_file("items.json")}
    
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        """Override of World.collect which additionally handles gem events."""
        name = self.collect_item(state, item)
        if name:
            state.add_item(name, self.player)
            if "Gems" in item.name:
                gem_amount = int(item.name.split(" ")[0])
                state.add_item("Gems", item.player, count=gem_amount)
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

    def rule_builder(self, full_rule):
        """Takes a string representation of a Gem event rule and converts it into a Rule object.
        To simplify this process, all rules sent to this method are of the format rule1 Or rule2 Or rule3,
        and it is assumed that each subrule is made up exclusively of either a single item or multiple items And'd together.
        For example, a valid string rule for this method would be 'Fire Breath Or Ice Breath And Charge or Double Jump'.
        This method would take that and appropriately convert it into an Or object which has 3 children:
        Has(Fire Breath), And(Has(Fire Breath), Has(Charge)), Has(Double Jump)."""
        or_rules = []

        for rule in full_rule.split(" or "):
            and_rules = []
            # pretty sure this whole loop can be generalized to not need separate cases if the subrule has "and"
            # buuuuuuuuuuuut my brain can't figure it out so I'm leaving it as-is. itworks.gif
            if rule.find("and") == -1:
                rule = rule.strip()
                
                # special cases
                if "Invincibility" in rule or "Supercharge" in rule:
                    cost = self._gadget_costs[int(rule[-1])]  # rule format provides gadget index in name
                    or_rules.append(Has("Light Gem", cost))
                    continue
                elif rule == "True_":
                    or_rules.append(True_())
                    continue
                else:
                    or_rules.append(Has(rule))
                    continue
            
            # subrule may potentially have multiple items to And together
            for rule2 in rule.split(" and "):
                rule2 = rule2.strip()
                
                # special cases
                if "Invincibility" in rule2 or "Supercharge" in rule2:
                    cost = self._gadget_costs[int(rule2[-1])]
                    and_rules.append(Has("Light Gem", cost))
                elif rule2 == "True_":
                    and_rules.append(True_())
                else:
                    and_rules.append(Has(rule2))

            or_rules.append(And(*and_rules))

        if len(or_rules) == 1:
            return or_rules[0]

        return Or(*or_rules)
    
    def generate_early(self) -> None:
        # TODO: this will probably get affected by new shop randomization. No longer will have at least 18 shop
        # TODO: in sphere 1 to have that be an option here. May need to force movement randomization
        if self.options.starting_realm.value != 0: # not dragon village
            if self.options.randomize_movement.value == 0 and self.options.shop_randomization.value == 0:
                raise OptionError("Cannot start outside Dragon Village if Movement and Shop randomization is off")

    def create_regions(self):
        if self.options.randomize_gadget_costs.value != 0:
            if self.options.randomize_gadget_costs.value == 2:  # shuffled:
                self.random.shuffle(self._gadget_costs)
            else:  # randomized:
                lmin, lmax = self.options.gadget_cost_min.value, self.options.gadget_cost_max.value
                if lmin > lmax:
                    lmin, lmax = lmax, lmin

                self._gadget_costs = [self.random.randint(lmin, lmax) for _ in range(3)]

        match self.options.starting_realm.value:
            case 4:  # Randomized:
                self._starting_realm = self.random.randint(0, 3)
                while self._starting_realm == self.options.goal.value:
                    self._starting_realm = self.random.randint(0, 3)
            case _:
                self._starting_realm = self.options.starting_realm.value

        if self.options.randomize_boss_lair_door_costs.value != 0:
            if self.options.randomize_boss_lair_door_costs.value == 2:  # shuffled:
                self.random.shuffle(self._boss_lairs)
            else:
                bmin, bmax = self.options.boss_lair_door_cost_min.value, self.options.boss_lair_door_cost_max.value
                if bmin > bmax:
                    bmin, bmax = bmax, bmin

                self._boss_lairs = [self.random.randint(bmin, bmax) for _ in range(4)]

            if self.options.goal.value != 4:
                highest = functools.reduce(max, self._boss_lairs)
                self._boss_lairs.remove(highest)
                if self.options.goal < 3:
                    self._boss_lairs.insert(self.options.goal.value, highest)
                else:
                    self._boss_lairs.append(highest)

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

        match self.options.goal.value:
            case 0 | 1 | 2 | 3:
                self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
            case 4:
                self.multiworld.completion_condition[self.player] = lambda state: state.has_all(
                    ("VictoryCon1", "VictoryCon2", "VictoryCon3", "VictoryCon4"), self.player)
        match self.options.goal.value:
            case 0:
                self.get_region("DVGnastyCave").add_event("DVDefeatGnasty", "Victory", rule=(
                    BossLairRule(0) & (Has("Fire Breath") | Has("Charge"))
                ))
            case 1:
                self.get_region("CRWateryTomb").add_event("CRDefeatIneptune", "Victory", rule=(
                    BossLairRule(1) & Has("Charge")
                ))
            case 2:
                self.get_region("FVRedChamber").add_event("FVDefeatRed", "Victory", rule=(
                    BossLairRule(2) & Has("Water Breath")
                ))
            case 3:
                self.get_region("RLMechaRed").add_event("RLDefeatMechaRed", "Victory", rule=(
                    BossLairRule(3) & Has("Fire Breath") & Has("Electric Breath") & Has("Double Jump")
                ))
            case 4:
                self.get_region("DVGnastyCave").add_event("DVDefeatGnasty", "VictoryCon1", rule=(
                    BossLairRule(0) & (Has("Fire Breath") | Has("Charge"))
                ))
                self.get_region("CRWateryTomb").add_event("CRDefeatIneptune", "VictoryCon2", rule=(
                    BossLairRule(1) & Has("Charge")
                ))
                self.get_region("FVRedChamber").add_event("FVDefeatRed", "VictoryCon3", rule=(
                    BossLairRule(2) & Has("Water Breath")
                ))
                self.get_region("RLMechaRed").add_event("RLDefeatMechaRed", "VictoryCon4", rule=(
                    BossLairRule(3) & Has("Fire Breath") & Has("Electric Breath") & Has("Double Jump")
                ))

        # set up gem events here
        file_in = open("setup/4 - gem events.txt", "r")
        for line in file_in:
            region_name, item_name, event_rule = line.split(" | ")
            event_name = f"{region_name}: {item_name}"
            self.get_region(region_name).add_event(event_name, item_name, rule=self.rule_builder(event_rule))
    
    def create_item(self, name: str) -> Item:
        """Helper method for create_items which returns an Item object."""
        return Item(name, self._classifications[name], self.item_name_to_id[name], self.player)
    
    def create_items(self) -> None:
        data = _load_file("items.json")
        itempool = []

        minigames = 0
        for npc, npc_list in zip(["Sgt. Byrd", "Blink", "Sparx", "Turret"], minigame_locs):
            if npc not in self.options.randomize_minigames.value:
                for egg, breath_loc in npc_list:
                    self.get_location(egg).place_locked_item(self.create_item("Dragon Egg"))
                    self.get_location(breath_loc).place_locked_item(self.create_item("Light Gem"))
                minigames += 4

        if self.options.firework_checks.value == 1:
            for _ in range(22):
                itempool.append(self.create_item("Gem Pack"))

        if self.options.randomize_breath.value == 0:
            self._starting_breath = 0
        elif self.options.randomize_breath.value == 1:
            self._starting_breath = self.random.randint(0, 3)
        else:
            self._starting_breath = -1

        breath_loc = self.get_location("Starter Checks: Breath")
        match self._starting_breath:
            case 0:
                breath_loc.place_locked_item(self.create_item("Fire Breath"))
            case 1:
                breath_loc.place_locked_item(self.create_item("Electric Breath"))
            case 2:
                breath_loc.place_locked_item(self.create_item("Water Breath"))
            case 3:
                breath_loc.place_locked_item(self.create_item("Ice Breath"))

        if self.options.randomize_movement.value == 0:
            self.get_location("Starter Checks: Swim").place_locked_item(self.create_item("Swim"))
            self.get_location("Starter Checks: Charge").place_locked_item(self.create_item("Charge"))
            self.get_location("Starter Checks: Glide").place_locked_item(self.create_item("Glide"))

        for item in data:
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
                if item['name'] in ('Dragon Egg', 'Light Gem'):
                    count -= minigames

                for _ in range(count):
                    itempool.append(self.create_item(item['name']))

        if self.options.realm_access.value == 2:
            access_cards = [
                "Dragon Village Access Card",
                "Coastal Remains Access Card",
                "Frostbite Village Access Card",
                "Stormy Beach Access Card"
            ]

            itempool.append(self.create_item("Gem Pack"))

            start = access_cards.pop(self._starting_realm)
            self.get_location("Starter Checks: Starting Realm Access").place_locked_item(self.create_item(start))
            for i in access_cards:
                itempool.append(self.create_item(i))

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
            "goal": self.options.goal.value,
            "skip_cutscenes": self.options.skip_cutscenes.value,
            "hint_boss_rewards": self.options.hint_boss_rewards.value,
            "hint_minigame_rewards": self.options.hint_minigame_rewards.value,
            "skip_elevators": self.options.skip_elevators.value,

            "realm_access": self.options.realm_access.value,
            "starting_realm": self._starting_realm,

            "key_rings": self.options.key_rings.value,
            "shop_randomization": self.options.shop_randomization.value,

            "randomize_boss_lair_doors": self.options.randomize_boss_lair_door_costs.value,
            "boss_lair_costs": self._boss_lairs,

            "randomize_light_gem_door_costs": self.options.randomize_light_gem_door_costs.value,
            "light_gem_door_costs": self._lg_doors,

            "randomize_gadget_costs": self.options.randomize_gadget_costs.value,
            "gadget_costs": self._gadget_costs,

            "randomize_minigames": self.options.randomize_minigames.value,
            "randomize_movement": self.options.randomize_movement.value,
            "randomize_breath": self.options.randomize_breath.value,
            "firework_checks": self.options.firework_checks.value,

            "easy_bosses": self.options.easy_bosses.value,

            "death_link": self.options.death_link.value,

            "teleport_across_realms": self.options.teleport_across_realms.value,
            "open_world_mode": self.options.open_world_mode.value
        }
        
        # TODO replace with new logic here?
        # if self.options.shop_randomization.value:
        #     if self.options.key_rings.value:
        #         r['randomized_shop_prices'] = [self.random.randint(smin, smax) for _ in range(19)]
        #     else:
        #         r['randomized_shop_prices'] = [self.random.randint(smin, smax) for _ in range(57)]
        return r
    
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        super().write_spoiler(spoiler_handle)
        spoiler_handle.write(f"Starting Realm:                  {self._starting_realm}\n")
        spoiler_handle.write(f"Randomized Gadget Costs:         {self._gadget_costs}\n")
        spoiler_handle.write(f"Randomized Boss Lair Costs:      {self._boss_lairs}\n")
        spoiler_handle.write(f"Randomized Light Gem Door Costs: {self._lg_doors}\n")

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
        return Has("Light Gem", world._gadget_costs[2]).resolve(world)


@dataclass
class LockedChestRule(Rule[SpyroAHTWorld], game="Spyro: A Hero's Tail"):
    level: int

    @override
    def _instantiate(self, world: SpyroAHTWorld) -> Rule.Resolved:
        if world.options.shop_randomization.value == 1:
            if world.options.key_rings.value == 1:
                return Has(f"{self.level} Key Ring", 1).resolve(world)
            else:
                return Has(f"Lockpick", 52).resolve(world)
        else:  # always true when shops are unrandomized
            return True_().resolve(world)


@dataclass
class RealmAccessRule(Rule[SpyroAHTWorld], game="Spyro: A Hero's Tail"):
    realm: int

    @override
    def _instantiate(self, world: SpyroAHTWorld) -> Rule.Resolved:
        if world.options.realm_access.value != 0:
            return Has(f"{self.realm} Access Card", 1).resolve(world)
        else:
            return True_().resolve(world)
    
    
@dataclass
class ShopCheckRule(Rule[SpyroAHTWorld], game="Spyro: A Hero's Tail"):
    index: int
    
    #override
    def _instantiate(self, world: SpyroAHTWorld) -> Rule.Resolved:
        return True_().resolve(world)

###############CLIENT###############
def _run_client(*args: str):
    import colorama
    from CommonClient import server_loop, gui_enabled, get_base_parser
    Utils.init_logging("Spyro: A Hero's Tail Client")

    async def _main(connect: str | None, password: str | None):
        from .context import SpyroAHTContext
        ctx = SpyroAHTContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
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
