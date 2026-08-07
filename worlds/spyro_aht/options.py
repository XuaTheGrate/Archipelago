from dataclasses import dataclass

from Options import OptionSet, PerGameCommonOptions, Toggle, Choice, Range, OptionGroup, StartInventoryPool, OptionList, Visibility

###############UNGROUPED###############
class DeathLink(Choice):
    """Determines death link behavior.

    disabled: Disabled.
    Shielded: The Butterfly Jar will protect you from a DeathLink, if you have it.
    Enabled: Enabled fully."""
    display_name = "DeathLink"
    option_disabled = 0
    option_shielded = 1
    option_enabled = 2
    default = 0


###############GENERATION SETTINGS###############
class LoggingLevel(OptionSet):
    """Log messages are generated at various points during generations involving Spyro AHT. This option lets you
    decide which type of messages should be logged, by adding them to the list below. If left empty, no logging will be done.
    
    If you experience any issues with AHT generations and want to make a report in the Archipelago Discord server
    thread for AHT, please try to generate again with the maximal logging setting and upload it along with your report.
    This may save the developers some time and effort in narrowing down what the issue(s) are.
    
    Valid Options (roughly in order of importance to the average user):
    Warning: Warnings are generated whenever there are issues stemming from YAML settings that impact generation. It is
      advised to have this option selected, at minimum.
    Info: General information about the status of generation will be logged. For example, the log will include messages
      like "[Spyro AHT] Item Creation beginning." and "[Spyro AHT] Item Creation done."
    Debug: Extra information that is primarily meant to be helpful for developer debugging will be logged.
    MoreDebug: Even more debug information. Intended for developer use, but you can enable it if curious :)"""
    display_name = "Logging Level"
    valid_keys = ("Warning", "Info", "Debug", "MoreDebug")
    default = ("Warning",)
    

class AutoCorrections(Choice):
    """This option decides the behavior of the generator whenever YAML issues are encountered.
    
    halt: The generator will prioritize player choices by halting generation when an issue is encountered. This is ideal
      for solo or small multiworld generations, since issues can be resolved by the player without much impact on time. 
    fix: The generator will prioritize generation success by fixing issues automatically. Options which have situations
      which can lead to this have the automatic behavior detailed. This is ideal for larger multiworld generations, since
      a generation being halted after minutes (or longer) of generation time may not be ideal."""
    display_name = "Auto Corrections"
    option_halt = 0
    option_fix = 1
    default = 0


###############GOAL, CHECKS, AND ITEMS###############
class Goal(OptionList):
    """Determines the goal(s) of this seed. Your goal can contain as many or as few of the below as you like.
    For clarity, collectible-related goals are all determined based on the AHT checks, not their corresponding items.
    For example, "Dragon Eggs" as a goal means to check all 80 AHT locations which would have given a Dragon Egg in
    the vanilla game. This leads to an important warning that if your world allows the use of !collect, AHT goals can
    be registered unexpectedly, if !collect leads to goal-related AHT locations being checked. 

    Available Goals:
    Gnasty Gnorc/Ineptune/Red/Mecha-Red: Must defeat each boss you list below.
    Fireworks: Flame all 22 fireworks. firework_checks will be enabled automatically if auto_corrections is set to 'fix'.
    Dark Gems: Break all 40 Dark Gems.
    Dragon Eggs: Collect all 80 Dragon Eggs.
    Light Gems: Collect all 100 Light Gems.
    Locked Chests: Open all 52 locked chests.
    Shop Items: Buy all randomized shop items. shop_randomization will be enabled automatically if auto_corrections is set to 'fix'.
    Random: For each "Random" you include, a random goal from above will be chosen, excluding any from exclude_from_goal.
    
    If the list is empty and auto_corrections is set to 'fix', a single random choice will be made.
    If the list has too many entries and auto_corrections is set to 'fix', entries will be removed at random until in range."""
    display_name = "Goal"
    valid_keys = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red", "Fireworks", "Dark Gems", "Dragon Eggs", "Light Gems",
                  "Locked Chests", "Shop Items", "Random")
    default = ("Mecha-Red",)
    
    
class ExcludeFromGoal(OptionSet):
    """Goaling allows for random choices to be made if you enter "Random". This option lets you exclude certain
    goal types from this random choosing. For example, entering "Shop Items" below means "Shop Items" will never be
    chosen at random (but you could still choose "Shop Items" as a goal above).
    
    If too many goals are excluded to allow for enough random choices, and auto_corrections is set to 'fix', goals will be
    un-excluded at random until in range. If this doesn't resolve it, random choices will be skipped entirely.
    
    Valid Options: ["Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red", "Fireworks", "Dark Gems", "Dragon Eggs", "Light Gems", "Locked Chests", "Shop Items"]"""
    display_name= "Exclude From Goal"
    valid_keys = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red", "Fireworks", "Dark Gems", "Dragon Eggs", "Light Gems", "Locked Chests", "Shop Items")
    default = frozenset()
    

class OpenWorldMode(Choice):
    """In the vanilla game, you can only teleport to a remote shop pad once you have physically reached it.
    open_world_mode lets you choose from a variety of ways to alter this behavior. For example, you can choose to have
    teleport access to a given shop pad be locked behind an Archipelago item which unlocks it. open_world_mode has a
    dramatic impact on the logic of generated seeds, as you will be expected to utilize any and all unlocked shop pads
    to cleverly teleport around the game.
    
    Options:
    vanilla: Shops only unlocked by physically reaching them.
    full: Shop pads are unlocked from the start of the seed.
    randomized: Shop pads unlock through individual AP items. For example, "Dark Mine - Miner's Drop Shop Unlock".
    progressive_levels: Shop pads unlock per-level in the order you would reach them in the vanilla game.
      For example, "Progressive Crocovile Swamp Shop Unlock" would first unlock Perilous Pyramid, then Forgotten Temple,
      then Elder's Tree. The project's README has a reference list for progressive and reverse progressive shop ordering. 
    reverse_progressive_levels: Same as progressive_levels, but backwards vanilla order.
    full_level: All shop pads in a level will unlock at once through AP items. For example, "Sunken Ruins - Shop Unlock".
    full_realm: All shops in a realm will unlock at once through AP items. For example, "Icy Wilderness - Shop Unlock"."""
    display_name = "Open World Mode"
    option_vanilla = 0
    option_full = 1
    option_randomized = 2
    option_progressive_levels = 3
    option_reverse_progressive_levels = 4
    option_full_levels = 5
    option_full_realms = 6
    default = 0
    

class FireworkChecks(Toggle):
    """Enables 22 checks for flaming fireworks."""
    display_name = "Firework Checks"
    default = 0


class VanillaMinigameRewards(OptionSet):
    """Minigames are always enabled as checks. This option lets you decide if you want any type of minigame to reward
    their vanilla Dragon Eggs and Light Gems instead of having randomized rewards.
    
    Valid options: ["Sgt. Byrd", "Blink", "Turret", "Sparx"]"""
    display_name = "Vanilla Minigame Rewards"
    valid_keys = ("Sgt. Byrd", "Blink", "Turret", "Sparx")
    default = frozenset()


class FillerItems(OptionSet):
    """This option lets you choose the contents of your filler item pool. For each location which needs a filler item,
    a category from below will be chosen, and if needed, a random item from that category will then be chosen.

    Dragon Eggs: Dragon Eggs are considered filler because they are functionally useless in advancing the game.
      Even if disabled here, Dragon Eggs will be rewarded from minigames if you enable vanilla_minigame_rewards.
    Breath Bombs: Fire Bombs, Electric Bombs, Water Bombs, and Ice Bombs. Received bombs are only usable if you have that breath unlocked.
    Gem Packs: Each gives a random amount of gems (400-600 or 800-1200 if you have double gems). It is advised to
      disable gem packs if using gem_logic, as gem logic does not account for them.
    Generics: Empty items which do nothing, but have humorous names referencing things in the game and series. We're always
      looking for new suggestions if you have any!
    
    If the list is empty and auto_corrections is set to 'fix', the filler pool will default to only "Generics".

    Valid options: ["Dragon Eggs", "Breath Bombs", "Gem Packs", "Generics"]"""
    display_name = "Filler Items"
    valid_keys = ("Dragon Eggs", "Breath Bombs", "Gem Packs", "Generics")
    default = ("Dragon Eggs", "Breath Bombs", "Gem Packs", "Generics")

###############START OF GAME###############
class StartingBreath(Choice):
    """All seeds start with "Starter Checks: Breath". This option decides whether it will get pre-filled with a
    breath of your choice, or a random other item from Archipelago (which could potentially still be a breath).

    fire/electric/water/ice: force "Starter Checks: Breath" to be your breath of choice.
    none: randomize what goes into "Starter Checks: Breath"."""
    display_name = "Starting Breath"
    option_fire = 0
    option_electric = 1
    option_water = 2
    option_ice = 3
    option_none = 4
    default = 0


class RandomizeMovement(Toggle):
    """All seeds start with 3 "Starter Checks" for Glide, Swim, and Charge. This option decides whether they will each gets
    pre-filled with Glide/Swim/Charge, or random items from Archipelago (which could potentially still be a type of movement).

    If you don't want to randomize a subset of these, add them to start_inventory or start_inventory_from_pool."""
    display_name = "Randomize Movement"
    default = 0


class StartingRealms(OptionSet):
    """Realm access is controlled by "access card" items e.g. "Dragon Kingdom Access Card". Choose which realm(s) you will start with access cards for. 
    
    If the list is left empty and auto_corrections is set to 'fix', 1 random realm will be chosen for you.
    If open_world_mode is enabled and 'full', you will start with all 4 access cards.
    If open_world_mode is enabled and not 'full', starting realm access is still controlled by access cards. However, non-starting realms
      have their access granted once their "Depot" shop is unlocked. For example, "Frosty Depot" grants access to Icy Wilderness.
        - See pause_menu_patch for a potential alteration to this.
    
    Valid Options: ["Dragon Kingdom", "Lost Cities", "Icy Wilderness", "Volcanic Isle"]"""
    display_name = "Starting Realms"
    valid_keys = ("Dragon Kingdom", "Lost Cities", "Icy Wilderness", "Volcanic Isle")
    default = ("Dragon Kingdom",)
    
###############SHOP & GEM LOGIC###############
class ShopRandomization(Toggle):
    """Determines whether to randomize Moneybags' shop. If not randomized, it will function identically to the vanilla game. 

    If randomized, vanilla game shop items will be replaced with items from Archipelago. This has a few consequences:
        - Double Gems, if enabled, is permanent once received, as is the Butterfly Jar (it replenishes on death if depleted).
        - There is no limit to how many lockpicks you can hold. Same with ammo for breath bombs.
        - Shop item prices will be the same everywhere i.e. remote shop pads will not upcharge you."""
    display_name = "Shop Randomization"
    default = 0
    

class KeyRings(Toggle):
    """This option replaces lockpicks with level-specific key rings which will open all locked chests in that level.
    This indirectly decides how many items you will have in your shop.

    If shop_randomization is disabled: this decides whether key rings or lockpicks will be buyable.
      Locked chests you have access to will be in-logic immediately, like the vanilla game.
    If shop_randomization and key_rings are enabled: you will have 18 shop items, and 14 key rings will be placed into the world.
      Locked chests will be in-logic once its level's key ring is obtained.
    If shop_randomization is enabled and key_rings are disabled: you will have 56 shop items, and 52 lockpicks will be placed in the world.
      Locked chests will not be in-logic until you have all 52 lockpicks, to prevent situations of buying them in the 'wrong' order."""
    display_name = "Key Rings"
    default = 0

    
class GemLogic(Toggle):
    """This option is only used when shop_randomization is enabled. It determines whether the generator should track
    the accessibility of gems throughout the seed.
    
    disabled: the shop will price items equally and place them all in sphere 1. This can result in difficult
      or impossible seeds as it is infeasible to afford every item then. However, it does give you the choice of which order to buy them.
    enabled: shop items will instead display "Unlocked at X Gems". Once you have X gems, the item will be free to purchase.
      Prices will steadily increase so that you unlock them in a spread-out set order, instead of all in sphere 1. This is significantly
      safer and improves generation quality a bit, at the cost of losing the ability to choose which order you buy them.
    
    The formula below calculates your prices. The first item is always free due to inflation in the Dragon Kingdom (prevents restrictive starts).
    The formula is included for those who are math-inclined. If not, you can also can do test generation(s) to see your prices.
    
    ********************************FORMULA INFO (for the math nerds)********************************
    blink_gems_total = 20,028 * blink_gems%
    non_blink_enemies_total = 16,353 * non_blink_enemies%
    other_gems_total = 106,443 * other_gems%
    gem_total = blink_gems_total + non_blink_enemies_total + other_gems_total
    base_shop_price = gem_total / (number of shop items determined by key_rings - 1)

    If gem_logic is disabled, shop items will cost base_shop_price, rounded down if needed.
    If gem_logic is enabled, shop items will cost base_shop_price * 1, base_shop_price * 2, etc., each rounded down if needed.
    *************************************************************************************************"""
    display_name = "Gem Logic"
    default = 0


class BlinkGems(Range):
    """This option is used when both shop_randomization and gem_logic are enabled. It lets you decide what percentage of
    gems from Blink's minigames you want to be expected to collect. His minigames are frequently disliked/skipped, and
    they have significantly more gems than the other minigames, which is why this is an isolated option.
    
    For example, a value of 50 means being expected to collect approximately 50% of the gems available in each Blink minigame.
    His minigames contain 20,028 total, so this would result in an expectation of 10,014 gems. Set this to 0 if you
    intend to skip Blink minigames, whether that be from underground-air-a-phobia or because you excluded some/all of their locations."""
    display_name = "Blink Gems"
    range_start = 0
    range_end = 100
    default = 75


class NonBlinkEnemies(Range):
    """This option is used when both shop_randomization and gem_logic are enabled. It lets you decide what percentage of gems
    from enemies you want to be expected to collect. This only applies to enemies when playing as Spyro or Hunter.
    
    Gem logic assumes you will kill every enemy exactly once. This is nearly impossible to do accurately,
    since enemies respawn on death or reloads, and you likely won't be able to kill every enemy you come across on first visit.
    This option was introduced to mitigate this issue.
    
    This option works similarly to blink_gems. For example, a value of 40 means being expected to collect approximately
    40% of gems from enemies. This works out to be roughly 6,541 (enemies have 16,353 gems total)."""
    display_name = "Non-Blink Enemies"
    range_start = 0
    range_end = 100
    default = 75


class OtherGems(Range):
    """This option is used when both shop_randomization and gem_logic are enabled. It works similarly to blink_gems and 
    on_blink_enemies, but applying to all other sources of gems. This primarily consists of gems from breakable containers,
    Sgt. Byrd + Sparx minigames, and some misc. others (such as gems on the ground in levels).
    
    The total amount of "other" gems is 106,443. Like blink_gems and non_blink_enemies, a value of 35 means
    being expected to collect approximately 37,255 "other" gems.
    
    Note: it's hard to get consistent gems from Sparx minigames. Their totals were calculated as an average of 4-5 runs.
    The total for each worked out to be 1,523 -> 2,148 -> 2,218 -> 2,392."""
    display_name = "Other Gems"
    range_start = 0
    range_end = 100
    default = 75
    
    
class DoubleGems(Choice):
    """This option is only used if shop_randomization is enabled. It lets you decide if you want to disable Double Gems
    as an Archipelago item. This is primarily meant for runs with gem_logic enabled, because gem logic does not account
    for double gems, but you can disable it with gem_logic off if you'd rather more consistent gem income."""
    display_name = "Double Gems"
    option_enabled = 0
    option_disabled = 1
    default = 0

###############GATE & GADGET COSTS###############
class RandomizeBossLairDoorCosts(Choice):
    """Determines the Dark Gem cost for each boss lair.

    default: Each boss lair has their vanilla cost (10, 20, 30, 40).
    randomized: Randomly pick costs in the range defined by boss_lair_door_cost_min and boss_lair_door_cost_max.
    shuffle: Vanilla boss lair costs are shuffled between each other (still 10/20/30/40 but in a random order)."""
    display_name = "Randomize Boss Lair Requirements"
    option_default = 0
    option_randomized = 1
    option_shuffle = 2
    default = 0


class BossLairDoorCostMin(Range):
    """Minimum cost for boss lairs, if set to be random. Will be swapped with boss lair maximum if min > max and auto_corrections is set to 'fix'."""
    display_name = "Boss Lair Door Cost Minimum"
    range_start = 1
    range_end = 40
    default = 1


class BossLairDoorCostMax(Range):
    """Maximum cost for boss lairs, if set to be random. Will be swapped with boss lair minimum if min > max and auto_corrections is set to 'fix'."""
    display_name = "Boss Lair Door Cost Maximum"
    range_start = 1
    range_end = 40
    default = 40


class BossLairForcing(Choice):
    """This option lets you force a specific boss lair to have the highest Dark Gem cost of the generated costs.
    This is accomplished by swapping the most expensive cost of the highest boss lair with the one selected below.
    
    Selecting "unchanged" leaves boss lair costs untouched."""
    display_name = "Boss Lair Forcing"
    option_unchanged = 0
    option_gnasty_gnorc = 1
    option_ineptune = 2
    option_red = 3
    option_mecha_red = 4
    default = 0
    

class RandomizeLightGemDoorCosts(Choice):
    """Determines the Light Gem cost for each boss lair.

    default: Each door has their vanilla cost (20, 45, 70, 95).
    randomized: Randomly pick costs in the range defined by light_gem_door_cost_min and light_gem_door_cost_max.
    shuffle: Each door has their vanilla cost shuffled with the others (still 20/45/70/95 but in a random order)."""
    display_name = "Randomize Light Gem Door Cost"
    option_default = 0
    option_randomized = 1
    option_shuffle = 2
    default = 0


class LightGemDoorCostMin(Range):
    """Minimum cost for light gem doors, if set to be random. Will be swapped with light gem door maximum if min > max and auto_corrections is set to 'fix'."""
    display_name = "Minimum Light Gem Door Cost"
    range_start = 1
    range_end = 100
    default = 1


class LightGemDoorCostMax(Range):
    """Maximum cost for light gem doors, if set to be random. Will be swapped with light gem door minimum if min > max and auto_corrections is set to 'fix'."""
    display_name = "Maximum Light Gem Door Cost"
    range_start = 1
    range_end = 100
    default = 50


class RandomizeGadgetCosts(Choice):
    """Determines the Light Gem cost for each gadget.

    default: Each gadget has their vanilla cost (8, 24, 40).
    randomized: Randomly picks costs in the range defined by gadget_cost_min and gadget_cost_max.
    shuffle: Each gadget has their vanilla cost shuffled with the others (still 8/24/40 but in a random order)."""
    display_name = "Randomize Gadget Cost"
    option_default = 0
    option_randomized = 1
    option_shuffle = 2
    default = 0


class GadgetCostMin(Range):
    """Minimum cost for gadgets, if set to be random. Will be swapped with gadget maximum if min > max and auto_corrections is set to 'fix'."""
    display_name = "Minimum Gadget Cost"
    range_start = 1
    range_end = 100
    default = 8


class GadgetCostMax(Range):
    """Maximum cost for gadgets, if set to be random. Will be swapped with gadget minimum if min > max and auto_corrections is set to 'fix'."""
    display_name = "Maximum Gadget Cost"
    range_start = 1
    range_end = 100
    default = 40
    
###############QUALITY OF LIFE###############
class PauseMenuPatch(Choice):
    """The pause menu has 2 patches you can choose between which can help with escaping situations where you're stuck.
    Take note that each one has logic implications if using open_world_mode.
    
    Choices:
    open_shop: pressing Y will open the shop display without needing to go to a shop physically. You will be able to
      purchase items like at physical shops, and teleport to any shop you have unlocked. If open_world_mode is enabled and
      not 'full', having this enabled will auto-unlock your starting realm's "Depot" shop to prevent potential softlock scenarios.
    teleport_to_hub: pressing and holding Y will bring you to the current realm's realm teleporter.
      This alters realm access slightly, if open_world_mode is enabled and not 'full'. Instead of requiring a realm's "Depot"
      shop, realm access will be granted when *any* shop in that realm is unlocked. This is because you are expected to
      pause -> teleport to hub to get hub access."""
    display_name = "Pause Menu Patch"
    option_open_shop = 0
    option_teleport_to_hub = 1
    default = 0
    
    
class HintMinigameRewards(Toggle):
    """Whether to auto-hint a mini-game's reward when talking to its NPC."""
    display_name = "Hint Mini Game Rewards"
    default = 0


class HintBossRewards(Toggle):
    """Whether to auto-hint a boss's reward(s) when their gate is opened."""
    display_name = "Hint Boss Rewards"
    default = 0


class EasyBosses(OptionSet):
    """Toggles 'easy mode' for each boss, making them take triple damage to significantly shorten fights.
    Valid options: ["Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red"]"""
    display_name = "Easy Bosses"
    valid_keys = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red")
    default = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red")


class SkipCutscenes(Toggle):
    """Enables skipping most cutscenes with the Y button. In rare cases, this may have glitchy side effects."""
    display_name = "Auto Skip Cutscenes"
    default = 0


class SkipElevators(Toggle):
    """Enables skipping the long elevator waits to Cloudy Domain, Sunken Ruins and Magma Falls"""
    display_name = "Skip Elevators"
    default = 0


class TeleportAcrossRealms(Toggle):
    """Allows for teleporting to unlocked Moneybags shop pads in any realm, from any realm. For example, you could
    teleport directly from Dragonfly Falls to Dark Mine without needing to use a hub realm teleporter.
    
    This option is automatically enabled if you are using any value for open_world_mode besides "vanilla"."""
    display_name = "Teleport Across Realms"
    default = 0


@dataclass
class SpyroAHTOptions(PerGameCommonOptions):
    death_link: DeathLink
    logging_level: LoggingLevel
    auto_corrections: AutoCorrections
    start_inventory_from_pool: StartInventoryPool
    
    goal: Goal
    exclude_from_goal: ExcludeFromGoal
    open_world_mode: OpenWorldMode
    firework_checks: FireworkChecks
    vanilla_minigame_rewards: VanillaMinigameRewards
    filler_items: FillerItems
    
    starting_breath: StartingBreath
    randomize_movement: RandomizeMovement
    starting_realms: StartingRealms
    
    shop_randomization: ShopRandomization
    key_rings: KeyRings
    gem_logic: GemLogic
    blink_gems: BlinkGems
    non_blink_enemies: NonBlinkEnemies
    other_gems: OtherGems
    double_gems: DoubleGems
    
    randomize_boss_lair_door_costs: RandomizeBossLairDoorCosts
    boss_lair_door_cost_min: BossLairDoorCostMin
    boss_lair_door_cost_max: BossLairDoorCostMax
    boss_lair_forcing: BossLairForcing
    randomize_light_gem_door_costs: RandomizeLightGemDoorCosts
    light_gem_door_cost_min: LightGemDoorCostMin
    light_gem_door_cost_max: LightGemDoorCostMax
    randomize_gadget_costs: RandomizeGadgetCosts
    gadget_cost_min: GadgetCostMin
    gadget_cost_max: GadgetCostMax
    
    pause_menu_patch: PauseMenuPatch
    hint_minigame_rewards: HintMinigameRewards
    hint_boss_rewards: HintBossRewards
    easy_bosses: EasyBosses
    skip_cutscenes: SkipCutscenes
    skip_elevators: SkipElevators
    teleport_across_realms: TeleportAcrossRealms
    
    
spyro_options_groups = [
    OptionGroup("GENERATION SETTINGS", [
        LoggingLevel, AutoCorrections
    ]),
    OptionGroup("GOAL, CHECKS, AND ITEMS", [
        Goal, ExcludeFromGoal, OpenWorldMode, FireworkChecks, VanillaMinigameRewards, FillerItems
    ]),
    OptionGroup("START OF GAME", [
        StartingBreath, RandomizeMovement, StartingRealms
    ]),
    OptionGroup("SHOP & GEM LOGIC", [
        ShopRandomization, KeyRings, GemLogic, BlinkGems, NonBlinkEnemies, OtherGems, DoubleGems
    ]),
    OptionGroup("GATE & GADGET COSTS", [
        RandomizeBossLairDoorCosts, BossLairDoorCostMin, BossLairDoorCostMax, BossLairForcing,
        RandomizeLightGemDoorCosts, LightGemDoorCostMin, LightGemDoorCostMax,
        RandomizeGadgetCosts, GadgetCostMin, GadgetCostMax
    ]),
    OptionGroup("QUALITY OF LIFE", [
        PauseMenuPatch,
        HintMinigameRewards, HintBossRewards,
        EasyBosses,
        SkipCutscenes, SkipElevators,
        TeleportAcrossRealms
    ])
]