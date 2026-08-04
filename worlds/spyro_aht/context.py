from __future__ import annotations

import asyncio
import collections

import Utils
from CommonClient import ClientCommandProcessor, logger
from kvui import GameManager

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext

from NetUtils import ClientStatus, NetworkItem

from .client import GenericClient, DolphinClient
from .data import consts


class SpyroAHTCommands(ClientCommandProcessor):
    ctx: SpyroAHTContext
    
    async def _cmd_reset_client(self) -> bool:
        """Forcibly reconnect the client."""
        self.output("Resetting client...")
        if self.ctx.emu_client:
            self.ctx.emu_loop.cancel()
            await self.ctx.emu_client.disconnect()
        self.ctx.emu_loop = asyncio.create_task(self.ctx._emu_loop())
        return True

    # async def _cmd_debug_send(self, location: str) -> bool:
    #     await self.ctx.send_msgs([{"cmd": "LocationChecks","locations":[int(location)]}])
    #     return True

    async def _cmd_list_options(self) -> bool:
        # TODO: add open world mode once it's implemented
        # this is grossly repetitive, but it only runs when the player demands it so it's not a big deal
        # even if it was reformatted it'd still be the same amount of output and data lookup, it's just code cleanliness
        """Displays the options you set for this seed (in the same order as YAML). Data is sourced directly from slot data, so if something doesn't line up here, check your YAML for mistakes. Much of this info is also viewable in-game by pausing and pressing R/L."""
        
        # death link
        output = "enabled" if self.ctx.slot_data["death_link"] == 1 else "disabled"
        self.output(f"Death link is {output}.")
        
        self.output("---------------GOAL, CHECKS, & ITEMS---------------")
        # goal
        self.output(f"Your chose the following as your goal(s): {self.ctx.slot_data['goal']}.")
        # firework checks
        output = "enabled" if self.ctx.slot_data["firework_checks"] else "disabled"
        self.output(f"Firework checks are {output}.")
        # minigames
        output = ""
        for minigame_type in ["Sgt. Byrd", "Blink", "Turret", "Sparx"]:
            output += f"{minigame_type} rewards are {'randomized' if minigame_type in self.ctx.slot_data['vanilla_minigame_rewards'] else 'vanilla'}, "
        self.output(f"Minigames: {output[:-2]}.")
        # filler items
        output = ""
        for minigame_type in ["Dragon Eggs", "Breath Bombs", "Gem Packs", "Generic"]:
            if minigame_type in self.ctx.slot_data['filler_items']: output+= f"{minigame_type}, "
        self.output(f"Enabled Filler Item Tpes: {output[:-2]}.")
        
        self.output("---------------START OF GAME---------------")
        # movement & breath
        output = "randomized" if self.ctx.slot_data["randomize_movement"] == 1 else "not randomized"
        if self.ctx.slot_data['starting_breath'] == 4:
            output_2 = "no"
        else:
            convert = {0: "fire", 1: "electric", 2: "water", 3: "ice"}
            output_2 = convert[self.ctx.slot_data['starting_breath']]
        self.output(f"Movement abilities are {output} and you start with {output_2} breath.")
        # starting realm
        self.output(f"You chose to start with access to the following realm(s): {self.ctx.slot_data['starting_realms']}.")

        self.output("---------------SHOP---------------")
        # shop items & key rings
        output = "randomized" if self.ctx.slot_data["shop_randomization"] == 1 else "not randomized"
        output_2 = "enabled" if self.ctx.slot_data["key_rings"] == 1 else "not enabled"
        self.output(f"Shop items are {output} and key rings are {output_2}.")
        # gem logic
        output = "enabled" if self.ctx.slot_data["shop_randomization"] and self.ctx.slot_data["gem_logic"] else "disabled"
        self.output(f"Gem logic is {output}.")
        
        # shop randomization-related things
        if self.ctx.slot_data["shop_randomization"]:
            # non_blink_gems and blink_gems
            self.output(f"You chose to collect {self.ctx.slot_data['blink_gems']}% of Blink's gems and {self.ctx.slot_data['non_blink_gems']}% of non-Blink gems.")
            # shop prices
            self.output(f"This means your shop prices are {self.ctx.slot_data['shop_costs']}.")
            if self.ctx.slot_data["gem_logic"]:
                # double gems
                output = "enable" if self.ctx.slot_data['double_gems'] else "disable"
                self.output(f"You chose to {output} the Double Gems item.")
            
        self.output("---------------GATE AND GADGET COSTS---------------")
        # boss costs
        data = self.ctx.slot_data["boss_lair_costs"]
        self.output(f"The boss lair gates require, in vanilla realm order: {data[0]}, {data[1]}, {data[2]}, and {data[3]} Dark Gems.")
        # boss lair forcing
        data = self.ctx.slot_data["boss_lair_forcing"]
        convert = {0: "Gnasty Gnorc", 1: "Ineptune", 2: "Red", 3: "Mecha-Red", 4: "none of the bosses"}
        self.output(f"You chose to force {convert[data]} to have the highest boss lair cost.")
        # light gem doors
        data = self.ctx.slot_data["light_gem_door_costs"]
        self.output(f"The Light Gem doors require, in vanilla realm order: {data[0]}, {data[1]}, {data[2]}, and {data[3]} Light Gems.")
        # gadget costs
        data = self.ctx.slot_data["gadget_costs"]
        self.output(f"Ball gadget requires {data[0]} Light Gems, invincibility requires {data[1]} Light Gems, and supercharge requires {data[2]} Light Gems.")

        self.output("---------------QUALITY OF LIFE---------------")
        # hint rewards
        output = "will" if self.ctx.slot_data["hint_boss_rewards"] else "won't"
        output_2 = "will" if self.ctx.slot_data["hint_minigame_rewards"] else "won't"
        self.output(f"Boss rewards {output} be hinted and minigame rewards {output_2} be hinted.")
        # easy bosses
        output = "Boss Difficulty: "
        for boss in ["Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red"]:
            output += f"{boss} easy, " if boss in self.ctx.slot_data["easy_bosses"] else f"{boss} normal, "
        self.output(f"{output[:-2]}.")
        # skip cutscenes & elevators
        output = "can" if self.ctx.slot_data["skip_cutscenes"] else "can't"
        output_2 = "can" if self.ctx.slot_data["skip_elevators"] else "can't"
        self.output(f"Cutscenes {output} be skipped and elevators {output_2} be skipped.")
        # teleport across realms
        output = "can" if self.ctx.slot_data['teleport_across_realms'] else "can't"
        self.output(f"You {output} teleport across realms.")

        return True


class SpyroAHTContext(SuperContext):
    tags = {"AP"}
    items_handling = 0b111
    game = "Spyro: A Hero's Tail"
    command_processor = SpyroAHTCommands

    def __init__(self, server_address: str | None = None, password: str | None = None) -> None:
        super().__init__(server_address, password)
        if tracker_loaded:
            super().set_events_callback(self._event_update)
            super().set_callback(self._location_update)
        
        # these update whenever UT reports a new location or event is in logic
        self.loc_flag = False
        self.event_flag = False
        self._in_logic_events: list[str] = []
        self._in_logic_locations: list[str] = []
        
        # used for checking goal components
        self.goal_stuff_setup = False
        self.goal_list = None
        self.goal_tally, self.goal_target = 0, 0
        self.finished_goals = [False, False, False, False, False, False, False, False, False, False]

        self.emu_client: GenericClient = None # type: ignore
        self.emu_loop: asyncio.Task = None # type: ignore
        self.auth_ready = asyncio.Event()

        self.slot_data = {}
        self._seed = ""

        self._shop_items: list[NetworkItem] = []
        self._shop_items_received = asyncio.Event()

        self._handled_items: set[NetworkItem] = set()

        self._checked_boss_doors = set()
        self._checked_gem_doors = set()
        self._checked_gadgets = set()

        self._scouted_locations: set[int] = set()
    
    def make_gui(self) -> type[GameManager]:
        ui = super().make_gui()
        ui.base_title = "Spyro: A Hero's Tail Archipelago Client"
        return ui

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)
    
    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        
        match cmd:
            case 'Connected':
                self.slot_data = args['slot_data']
                if self.slot_data['death_link'] != 0:
                    self.tags.add("DeathLink")
                    Utils.async_start(self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}]))
                if self.emu_loop and not self.emu_loop.cancelled():
                    self.emu_loop.cancel()
                self.emu_loop = asyncio.create_task(self._emu_loop())
                self.auth_ready.set()
            case 'RoomInfo':
                self._seed = args['seed_name']
            case 'LocationInfo':
                if not self._shop_items_received.is_set():
                    self._shop_items = [NetworkItem(*item) for item in args['locations']]
                    self._shop_items_received.set()
            case 'PrintJSON':
                match args.get('type', ''):
                    case 'ItemSend':
                        if args['receiving'] == self.slot:
                            item = args['item']
                            self.emu_client.msg_queue.put_nowait((consts.COLOUR_WHITE, f'Received {self.item_names.lookup_in_slot(item.item, self.slot)} from {self.player_names[item.player]}'))
                    case 'Hint':
                        if args['found']: return
                        if args['receiving'] == self.slot:
                            item = args['item']
                            player = "your" if item.player == self.slot else f"{self.player_names[item.player]}'s"
                            location = self.location_names.lookup_in_slot(item.location, item.player)
                            msg = f"[Hint] Your {self.item_names.lookup_in_slot(item.item, self.slot)} is at {player} {location}"
                            self.emu_client.msg_queue.put_nowait((consts.COLOUR_WHITE, msg))
                        elif args['item'].player == self.slot:
                            item = args['item']
                            location = self.location_names.lookup_in_slot(item.location, self.slot)
                            player = self.player_names[args['receiving']]
                            msg = f"[Hint] {player}'s {self.item_names.lookup_in_slot(item.item, args['receiving'])} is at {location}"
                            self.emu_client.msg_queue.put_nowait((consts.COLOUR_WHITE, msg))
    
    async def start_emu_client(self):
        self.emu_client = DolphinClient()
        await self.emu_client.connect()
        await self.emu_client.apply_patch(self)
        await self.emu_client.ready.wait()
    
    async def _receive_items(self):
        from CommonClient import logger  # TODO: remove when done
        item_counts = collections.Counter(self.item_names.lookup_in_slot(i.item, self.slot) for i in self.items_received)
        for item in self.items_received:
            if item in self._handled_items: continue  # TODO: investigate here for cheat console things not sending?
            self._handled_items.add(item)
            match item.item:
                case 0xB:
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.Swim, True)
                case 0xC:
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.Glide, True)
                case 0xD:
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.Charge, True)
                case 0x1:
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.DoubleJump, True)
                case 0x2:
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.PoleSpin, True)
                case 0x3:
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.WingShield, True)
                case 0x4:
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.WallKick, True)
                case 0xE:
                    if not await self.emu_client.has_any_breath():
                        await self.emu_client.set_breath(consts.BREATH_FIRE)
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.FireBreath, True)
                case 0x5:
                    if not await self.emu_client.has_any_breath():
                        await self.emu_client.set_breath(consts.BREATH_ELECTRIC)
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.ElectricBreath, True)
                case 0x6:
                    if not await self.emu_client.has_any_breath():
                        await self.emu_client.set_breath(consts.BREATH_WATER)
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.WaterBreath, True)
                case 0x7:
                    if not await self.emu_client.has_any_breath():
                        await self.emu_client.set_breath(consts.BREATH_ICE)
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.IceBreath, True)
                case 0x8:
                    count = await self.emu_client.get_item_count(self.emu_client.addresses.DARK_GEM_COUNT)
                    if count < item_counts["Dark Gem"]:
                        await self.emu_client.set_item(self.emu_client.addresses.DARK_GEM_COUNT, count + 1)
                case 0x9:
                    count = await self.emu_client.get_item_count(self.emu_client.addresses.LIGHT_GEM_COUNT)
                    if count < item_counts["Light Gem"]:
                        await self.emu_client.set_item(self.emu_client.addresses.LIGHT_GEM_COUNT, count + 1)
                case 0xA:
                    count = await self.emu_client.get_item_count(self.emu_client.addresses.DRAGON_EGG_COUNT)
                    if count < item_counts["Dragon Egg"]:
                        await self.emu_client.set_item(self.emu_client.addresses.DRAGON_EGG_COUNT, count + 1)
                case 0x1C:
                    count = await self.emu_client.get_item_count(self.emu_client.addresses.g_NUM_LOCK_PICKS_RECEIVED)
                    if count < item_counts["Lockpick"]:
                        lc = await self.emu_client.get_item_count(self.emu_client.addresses.LOCKPICKS)
                        await self.emu_client.set_item(self.emu_client.addresses.g_NUM_LOCK_PICKS_RECEIVED, count + 1)
                        await self.emu_client.set_item(self.emu_client.addresses.LOCKPICKS, lc + 1)
                case 0xF:
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.SparxHealthUpgrade, True)
                case 0x19:
                    await self.emu_client.enable_butterfly_jar()
                case 0x1A:
                    #await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.DoubleGems, True)
                    await self.emu_client.toggle_double_gems(True)
                case 0x1B:
                    await self.emu_client.set_flag(self.emu_client.addresses.ABILITY_FLAGS, consts.AbilityFlags.Shockwave, True)
                case 0x1D:
                    count = await self.emu_client.get_item_count(self.emu_client.addresses.g_NUM_GEM_PACKS_RECEIVED)
                    if count < item_counts["Gem Pack"]:
                        await self.emu_client.set_item(self.emu_client.addresses.g_NUM_GEM_PACKS_RECEIVED, count + 1)
                        await self.emu_client.add_gem_pack()
                case 0x1E:
                    total = await self.emu_client.get_item_count(self.emu_client.addresses.g_NUM_FIRE_AMMO_RECEIVED)
                    if total < item_counts["Fire Bomb"]:
                        count = await self.emu_client.get_item_count(self.emu_client.addresses.FIRE_BOMBS)
                        await self.emu_client.set_item(self.emu_client.addresses.g_NUM_FIRE_AMMO_RECEIVED, total + 1)
                        await self.emu_client.set_item(self.emu_client.addresses.FIRE_BOMBS, count + 1)
                case 0x1F:
                    total = await self.emu_client.get_item_count(self.emu_client.addresses.g_NUM_ELECTRIC_AMMO_RECEIVED)
                    if total < item_counts["Electric Bomb"]:
                        count = await self.emu_client.get_item_count(self.emu_client.addresses.ELECTRIC_BOMBS)
                        await self.emu_client.set_item(self.emu_client.addresses.g_NUM_ELECTRIC_AMMO_RECEIVED, total + 1)
                        await self.emu_client.set_item(self.emu_client.addresses.ELECTRIC_BOMBS, count + 1)
                case 0x20:
                    total = await self.emu_client.get_item_count(self.emu_client.addresses.g_NUM_WATER_AMMO_RECEIVED)
                    if total < item_counts["Water Bomb"]:
                        count = await self.emu_client.get_item_count(self.emu_client.addresses.WATER_BOMBS)
                        await self.emu_client.set_item(self.emu_client.addresses.g_NUM_WATER_AMMO_RECEIVED, total + 1)
                        await self.emu_client.set_item(self.emu_client.addresses.WATER_BOMBS, count + 1)
                case 0x21:
                    total = await self.emu_client.get_item_count(self.emu_client.addresses.g_NUM_ICE_AMMO_RECEIVED)
                    if total < item_counts["Ice Bomb"]:
                        count = await self.emu_client.get_item_count(self.emu_client.addresses.ICE_BOMBS)
                        await self.emu_client.set_item(self.emu_client.addresses.g_NUM_ICE_AMMO_RECEIVED, total + 1)
                        await self.emu_client.set_item(self.emu_client.addresses.ICE_BOMBS, count + 1)
                case 0x22 | 0x23 | 0x24 | 0x25 | 0x26 | 0x27 | 0x28 | 0x29 | 0x2A | 0x2B | 0x2C | 0x2D | 0x2E | 0x2F:
                    bit = consts.KEY_RINGS.index(item.item)
                    address = self.emu_client.addresses.g_KEYRING_BITFIELD + (bit // 8)
                    data = await self.emu_client.get_item_count(address)
                    flag = 1 << (bit % 8)
                    data |= flag
                    await self.emu_client.set_item(address, data)
                case 0x30 | 0x31 | 0x32 | 0x33: # access cards
                    await self.emu_client.allow_realm_access(item.item)
                case 0x64 | 0x65 | 0x66 | 0x67 | 0x68 | 0x69 | 0x6A | 0x6B | 0x6C | 0x6D | 0x6E | 0x6F | 0x70 | 0x71 | 0x72 | 0x73 | 0x74 | 0x75 \
                | 0x76 | 0x77 | 0x78 | 0x79 | 0x7A | 0x7B | 0x7C | 0x7D | 0x7E | 0x7F | 0x80 | 0x81 | 0x82 | 0x83 | 0x84 | 0x85 | 0x86 | 0x87 | 0x88:
                    logger.info(f"received individual shop unlock with id {item.item}")
                case 0x89 | 0x8A | 0x8B | 0x8C | 0x8D | 0x8E | 0x8F | 0x90 | 0x91 | 0x92 | 0x93 | 0x94 | 0x95:
                    logger.info(f"received progressive shop unlock with id {item.item}")
                case 0x96 | 0x97 | 0x98 | 0x99 | 0x9A | 0x9B | 0x9C | 0x9D | 0x9E | 0x9F | 0xA0 | 0xA1 | 0xA2:
                    logger.info(f"received level shop unlock with id {item.item}")
                case 0xA3 | 0xA4 | 0xA5 | 0xA6:
                    logger.info(f"received realm shop unlock with id {item.item}")

    async def _check_doors(self):
        dark = await self.emu_client.get_item_count(self.emu_client.addresses.DARK_GEM_COUNT)
        for idx, cost in enumerate(self.slot_data['boss_lair_costs']):
            if idx in self._checked_boss_doors: continue
            if dark >= cost:
                self._checked_boss_doors.add(idx)
                msg = consts.COLOUR_RED, "SOMETHING WENT WRONG"
                match idx:
                    case 0:
                        msg = consts.COLOUR_WHITE, "You have enough Dark Gems for Gnasty's Lair!"
                    case 1:
                        msg = consts.COLOUR_WHITE, "You have enough Dark Gems for Ineptune's Lair!"
                    case 2:
                        msg = consts.COLOUR_WHITE, "You have enough Dark Gems for Red's Lair!"
                    case 3:
                        msg = consts.COLOUR_WHITE, "You have enough Dark Gems for Mecha-Red's Lair!"
                self.emu_client.msg_queue.put_nowait(msg)
        
        light = await self.emu_client.get_item_count(self.emu_client.addresses.LIGHT_GEM_COUNT)
        for idx, cost in enumerate(self.slot_data['light_gem_door_costs']):
            if idx in self._checked_gem_doors: continue
            if light >= cost:
                self._checked_gem_doors.add(idx)
                msg = consts.COLOUR_RED, "SOMETHING WENT WRONG"
                match idx:
                    case 0:
                        msg = consts.COLOUR_WHITE, "You have enough Light Gems for the door in Dragonfly Falls!"
                    case 1:
                        msg = consts.COLOUR_WHITE, "You have enough Light Gems for the door in Coastal Remains!"
                    case 2:
                        msg = consts.COLOUR_WHITE, "You have enough Light Gems for the door in Frostbite Village"
                    case 3:
                        msg = consts.COLOUR_WHITE, "You have enough Light Gems for the door in Dark Mine!"
                self.emu_client.msg_queue.put_nowait(msg)
        
        for idx, cost in enumerate(self.slot_data['gadget_costs']):
            if idx in self._checked_gadgets: continue
            if light >= cost:
                self._checked_gadgets.add(idx)
                msg = consts.COLOUR_RED, "SOMETHING WENT WRONG"
                match idx:
                    case 0:
                        msg = consts.COLOUR_WHITE, "You have enough Light Gems for the Ball Gadget!"
                    case 1:
                        msg = consts.COLOUR_WHITE, "You have enough Light Gems for the Invincibility Gadget!"
                    case 2:
                        msg = consts.COLOUR_WHITE, "You have enough Light Gems for the Supercharge Gadget!"
                self.emu_client.msg_queue.put_nowait(msg)

    async def _location_checks(self):
        locations = await self.emu_client.scan_locations(shop_items=self.slot_data['shop_randomization'] == 1, key_rings=self.slot_data['key_rings'] == 1)
        for c in {229, 230, 231, 232}:  # starter checks
            locations.add(c)
        locations -= self.checked_locations
        if locations:
            await self.send_msgs([{"cmd": "LocationChecks", "locations": locations}])
    
    async def _location_scouts(self):
        locations = set()
        if self.slot_data['hint_minigame_rewards']:
            for obj, loc in consts.MINIGAME_OBJECTIVES.items():
                flag = await self.emu_client.get_objective(obj)
                if flag:
                    locations.update(loc)
        
        if self.slot_data['hint_boss_rewards']:
            for obj, loc in consts.BOSS_OBJECTIVES.items():
                flag = await self.emu_client.get_objective(obj)
                if flag:
                    locations.add(loc)
        locations -= self._scouted_locations
        if locations:
            self._scouted_locations.update(locations)
            await self.send_msgs([{"cmd":"LocationScouts","locations":locations,"create_as_hint":2}])
    
    def _event_update(self, events: list[str]) -> bool:
        self._in_logic_events = events
        self.loc_flag = True
        return True  # does nothing but is required (and is documented as such by UT)
    
    def _location_update(self, locations: list[str]) -> bool:
        self._in_logic_locations = locations
        self.event_flag = True
        return True  # does nothing but is required (and is documented as such by UT)

    async def check_goal(self) -> bool:
        # self.finished_goals avoids re-checking goals that have already been found to be complete
        for goal in self.goal_list:
            if goal == "Gnasty Gnorc" and not self.finished_goals[0]:
                self.finished_goals[0] = await self.check_goal_component("defeating Gnasty Gnorc", [consts.BOSS_IDS[0]])
            if goal == "Ineptune" and not self.finished_goals[1]:
                self.finished_goals[1] = await self.check_goal_component("defeating Ineptune", [consts.BOSS_IDS[1]])
            if goal == "Red" and not self.finished_goals[2]:
                self.finished_goals[2] = await self.check_goal_component("defeating Red", [consts.BOSS_IDS[2]])
            if goal == "Mecha-Red" and not self.finished_goals[3]:
                self.finished_goals[3] = await self.check_goal_component("defeating Mecha-Red", [consts.BOSS_IDS[3]])
            if goal == "Fireworks" and not self.finished_goals[4]:
                self.finished_goals[4] = await self.check_goal_component("flaming all fireworks", consts.FIREWORK_IDS)
            if goal == "Dark Gems" and not self.finished_goals[5]:
                self.finished_goals[5] = await self.check_goal_component("breaking all Dark Gems", consts.DARK_GEM_IDS)
            if goal == "Dragon Eggs" and not self.finished_goals[6]:
                self.finished_goals[6] = await self.check_goal_component("collecting all Dragon Eggs", consts.DRAGON_EGG_IDS)
            if goal == "Light Gems" and not self.finished_goals[7]:
                self.finished_goals[7] = await self.check_goal_component("collecting all Light Gems", consts.LIGHT_GEM_IDS)
            if goal == "Locked Chests" and not self.finished_goals[8]:
                self.finished_goals[8] = await self.check_goal_component("opening all locked chests", consts.LOCKED_CHEST_IDS)
            if goal == "Shop Items" and not self.finished_goals[9]:
                if self.slot_data['key_rings'] == 0:  # no key rings = all 56 items
                    self.finished_goals[9] = await self.check_goal_component("buying all shop items", consts.SHOP_ITEM_IDS)
                else:  # yes key rings = only 18 items
                    self.finished_goals[9] = await self.check_goal_component("buying all shop items", consts.SHOP_ITEM_IDS[0:18])
        
        # tally goes +1 when a goal component is met. If that value matches however many goals there are, we're done!
        if self.goal_tally == self.goal_target:
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            return True
        
        return False

    async def check_goal_component(self, goal, loc_id_list) -> bool:
        from CommonClient import logger
        for goal_component_id in loc_id_list:
            if goal_component_id not in self.checked_locations:
                return False
        self.goal_tally += 1
        logger.info(f"Goal of {goal} has been met, nice work! If this was your only or final goal, the client should recognize that in a moment.")
        return True
    
    
    async def _emu_loop(self):
        has_goaled = False
        try:
            await self.auth_ready.wait()
            await self.start_emu_client()

            while not self.exit_event.is_set():
                if not self.server or self.server.socket.closed:
                    logger.info("Client disconnected")
                    await self.emu_client.disconnect()
                    return

                try:
                    await asyncio.wait_for(self.watcher_event.wait(), 1.0)
                except asyncio.TimeoutError:
                    pass
                self.watcher_event.clear()

                if await self.emu_client.should_process_checks():
                    # done here to ensure it's only all set up once connected
                    if not self.goal_stuff_setup:
                        self.goal_list = self.slot_data['goal']
                        self.goal_target = len(self.goal_list)
                        self.goal_stuff_setup = True
                        
                    if self.slot_data["death_link"] > 0:
                        await self._send_deathlink()
                    await self._receive_items()
                    await self._check_doors()
                    await self._location_checks()
                    await self._location_scouts()
                    if self.event_flag:
                        await self.emu_client.update_pause_gems(self, self._in_logic_events)
                    if self.loc_flag:
                        await self.emu_client.update_tracker(self, self._in_logic_locations)
                    if not has_goaled:
                        has_goaled = await self.check_goal()
        except Exception:
            logger.error("ERROR IN EMULATOR LOOP, PLEASE REPORT IN THE THREAD", exc_info=True)
    
    async def _send_deathlink(self):
        if await self.emu_client.export_deathlink():
            await self.send_death()

    async def _receive_deathlink(self, msg: str):
        self.emu_client.msg_queue.put_nowait((consts.COLOUR_RED, msg))
        await self.emu_client.import_deathlink(self.slot_data['death_link'])
    
    def on_deathlink(self, data: dict) -> None:
        Utils.async_start(self._receive_deathlink(data.get('cause') or f"{data['source']} died."))

    async def shutdown(self):
        if self.emu_loop:
            self.emu_loop.cancel()
        if self.emu_client:
            await self.emu_client.disconnect()
        return await super().shutdown()