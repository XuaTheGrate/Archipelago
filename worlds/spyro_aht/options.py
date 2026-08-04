from dataclasses import dataclass

from Options import OptionSet, PerGameCommonOptions, Toggle, Choice, Range, OptionGroup, StartInventoryPool, OptionList, Visibility

###############UNGROUPED###############
class DeathLink(Choice):
    """Determines death link behavior.

    disabled: Disabled.
    Shielded: The Butterfly Jar will protect you from a DeathLink, if you have it.
    Enabled: Enabled fully.
    """
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
    
    Valid Options:
    Info: General information about the status of generation will be logged. For example, the log will include messages
    like "[Spyro AHT] Item Creation beginning." and "[Spyro AHT] Item Creation done."
    Warning: Warnings are generated whenever there are issues stemming from YAML settings that impact generation. It is
    advised to have this option selected, at minimum.
    Debug: Extra information that is primarily meant to be helpful for developer debugging will be logged.
    MoreDebug: Even more debug information. Intended for developer use, but you can enable it if curious :)
    """
    display_name = "Logging Level"
    valid_keys = ("Info", "Warning", "Debug", "MoreDebug")
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
    Gnasty Gnorc: Defeat Gnasty Gnorc.
    Ineptune: Defeat Ineptune.
    Red: Defeat Red.
    Mecha-Red: Defeat Mecha-Red.
    Fireworks: Flame all 22 fireworks. firework_checks will be enabled automatically if disabled and auto_corrections is set to 'fix'.
    Dark Gems: Break all 40 Dark Gems.
    Dragon Eggs: Collect all 80 Dragon Eggs.
    Light Gems: Collect all 100 Light Gems.
    Locked Chests: Open all 52 locked chests.
    Shop Items: Buy all randomized shop items (depends on key_rings). shop_randomization will be enabled automatically if
    disabled and auto_corrections is set to 'fix'.
    Random: For each "Random" you include, a random goal from above will be chosen.
    
    If the list is empty and auto_corrections is set to 'fix', a single random choice will be made.
    If the list has too many entries and auto_corrections is set to 'fix', entries will be removed at random until in range.
    If there are not enough available goals for random selections and auto_corrections is set to 'fix', random selections will be skipped."""
    display_name = "Goal"
    valid_keys = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red", "Fireworks", "Dark Gems", "Dragon Eggs", "Light Gems",
                  "Locked Chests", "Shop Items", "Random")
    default = ("Mecha-Red",)
    
    
class ExcludeFromGoal(OptionSet):
    """Goaling allows for random choices to be made if you enter "Random". This option lets you exclude certain
    goal types from this random choosing. For example, if you enter "Shop Items" here, "Shop Items" will only be
    part of your goal if you explicitly choose it (it will never be chosen at random). This option only excludes goals
    from random choices - for example, putting "Gnasty Gnorc" below will still allow you to explicitly choose Gnasty Gnorc
    as a goal above.
    
    If too many goals are excluded to allow for enough random choices and auto_corrections is set to 'fix', goals will be
    un-excluded at random until in range.
    
    Valid Options: ["Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red", "Fireworks", "Dark Gems", "Dragon Eggs", "Light Gems",
    "Locked Chests", "Shop Items"]"""
    display_name= "Exclude From Goal"
    valid_keys = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red", "Fireworks", "Dark Gems", "Dragon Eggs", "Light Gems",
                  "Locked Chests", "Shop Items")
    default = frozenset()
    

class OpenWorldMode(Choice):
    """In the vanilla game, you can only teleport to a remote shop pad once you have physically reached it.
    The AHT randomizer is capable of unlocking remote shop pads early so you can teleport to them without that requirement.
    This has a dramatic impact on the logic of a seed, as you may be expected to, for example, teleport deep into
    a level and play portions of it forwards or backwards from that point.
    
    **put notes here about if I have to give any realm cards early or similar**
     
    Options:
    off: leaves the vanilla game shop unlock method in place.
    
    full: all shop pads are unlocked from the start of the seed.
    
    randomized: shop pads will be unlocked individually by AP items. For example, you could get
    "Dark Mine - Miner's Drop Unlock" which allows you to teleport ot the Miner's Drop shop pad.
    
    progressive_per_level: shop pads will be unlocked per-level in the order you would reach them if playing the vanilla game.
    For example, you could get "Progressive Crocovile Swamp Shop Unlock". The project's README has a reference list for
    situations where it is not obvious what the "next" shop is for a level. 
    
    reverse_progressive_per_level: same as progressive_per_level, but backwards per level, unlocking the shop "furthest"
    into the level first, and going backwards towards the entrance.
    
    full_per_level: all shops in the given level will unlock at the same time. For example, you could get
    "Full Dark Mine Shop Unlock" which unlocks all shops in Dark Mine.
    
    full_per_realm: all shops in the given realm will unlock at the same time. For example, you could get
    "Lost Cities Shop Unlock" which unlocks all shops in Coastal Remains, Sunken Ruins, and Cloudy Domain."""
    display_name = "Open World Mode"
    option_off = 0
    option_full = 1
    option_randomized = 2
    option_progressive_levels = 3
    option_reverse_progressive_levels = 4
    option_full_levels = 5
    option_full_realms = 6
    default = 0
    

class FireworkChecks(Toggle):
    """Whether to enable checks for flaming fireworks."""
    display_name = "Firework Checks"
    default = 0


class VanillaMinigameRewards(OptionSet):
    """Minigames are always enabled as checks, but this option lets you decide if you want any of them to reward
    their vanilla Dragon Eggs and Light Gems instead of being randomized into something else.
    
    Valid options: ["Sgt. Byrd", "Blink", "Turret", "Sparx"]
    """
    display_name = "Vanilla Minigame Rewards"
    valid_keys = ("Sgt. Byrd", "Blink", "Turret", "Sparx")
    default = frozenset()


class FillerItems(OptionSet):
    """This option lets you choose the contents of your filler item pool. For each location which needs a filler item,
    a filler item will be chosen at random out of the list you provide below.

    Dragon Eggs: Dragon Eggs are considered filler because they are functionally useless in advancing the game.
    Even if you disable them here, Dragon Eggs will still be rewarded from minigames if you choose to force vanilla rewards above.
    
    Breath Bombs: Fire Bombs, Electric Bombs, Water Bombs, and Ice Bombs. Received bombs are only usable if you have that breath unlocked.

    Gem Packs: Each gives a random amount of gems (400-600 or 800-1200 if you have double gems). It is advised to not
    include these if using shop randomization with gem logic, because gem logic does not account for gem packs.

    Generics: Empty items which do nothing, but have humorous names referencing things in the game and series.
    
    If the list is empty and auto_corrections is set to 'fix', the filler pool will default to only "Generics".

    Valid options: ["Dragon Eggs", "Breath Bombs", "Gem Packs", "Generics"]"""
    display_name = "Filler Items"
    valid_keys = ("Dragon Eggs", "Breath Bombs", "Gem Packs", "Generics")
    default = ("Dragon Eggs", "Breath Bombs", "Gem Packs", "Generics")

###############START OF GAME###############
class StartingBreath(Choice):
    """All seeds start with a "Starter Checks: Breath". This option decides whether it will get pre-filled with a
    breath of your choice, or a random other item from Archipelago (which could potentially still be a breath).

    fire/electric/water/ice: Start with that breath.
    none: Start with no breath.
    """
    display_name = "Starting Breath"
    option_fire = 0
    option_electric = 1
    option_water = 2
    option_ice = 3
    option_none = 4
    default = 0


class RandomizeMovement(Toggle):
    """All seeds start with 3 "Starter Checks" for types of movement (glide, swim, and charge). This option decides whether
    they will get pre-filled with glide/swim/charge, or random items from Archipelago (which could potentially still be
    a type of movement).

    If you don't want to randomize a subset of these, add them to your start inventory."""
    display_name = "Randomize Movement"
    default = 0


class StartingRealms(OptionSet):
    """Access to a realm is granted when you possess its "access card" item. For example, "Dragon Kingdom Access Card"
    grants access to the Dragon Kingdom realm. This option lets you choose which realm(s) to start with access to.
    Their access cards will be added to your start inventory. This is equivalent to putting the card(s) in your start
    inventory yourself, except you can have a random one chosen for you if the list is left empty.
    
    Valid Options: ["Dragon Kingdom", "Lost Cities", "Icy Wilderness", "Volcanic Isle"]"""
    display_name = "Starting Realms"
    valid_keys = ("Dragon Kingdom", "Lost Cities", "Icy Wilderness", "Volcanic Isle")
    default = ("Dragon Kingdom",)
    
###############SHOP & GEM LOGIC###############
class ShopRandomization(Toggle):
    """Determines whether to randomize Moneybags' shop. If not randomized, it will function identically to the vanilla game. 

    If randomized, vanilla game shop items will be replaced with items from Archipelago. This has a few consequences:
        - Double Gems, if enabled, is permanent once received, as is the Butterfly Jar (it replenishes on death if depleted).
        - There is no limit on how many lockpicks you can hold at once. Same with ammo for breath bombs.
        - Shop item prices will be the same everywhere i.e. remote shop pads will not upcharge you.
        
    The above information applies regardless of your setting of gem_logic."""
    display_name = "Shop Randomization"
    default = 0
    

class KeyRings(Toggle):
    """This option enables level-specific key rings which will open all locked chests in that level, which indirectly
    determines how many items you have in your shop.

    If your shop is not randomized: key rings or lockpicks will be buyable in the shop.

    If your shop is randomized, and key rings are enabled: you will have 18 shop items, and 14 key rings will
    be placed randomly in the world.

    If your shop is randomized and key rings are disabled: you will have 56 shop items, and 52 lockpicks will be placed
    randomly in the world.
    """
    display_name = "Key Rings"
    default = 0

    
class GemLogic(Toggle):
    """This option determines whether the generator should utilize logic rules to track the accessibility of gems throughout the seed.
    
    If disabled, the shop will price items equally and place them all in sphere 1. This can result in difficult
    or impossible seeds because it is infeasible to afford every item then, but does give you the choice of which order to buy them.

    If enabled, shop items will instead display "Unlocked at X Gems". Once you have X gems, the item will be free to purchase,
    with prices steadily increasing so that you unlock them in a set order. This spreads the shop checks out through the
    seed, but has the downside of you losing the choice of which order to unlock items.
    
    Either way, the formula below is used to calculate your shop item prices. The first item is always free due to inflation in the Dragon Kingdom.
    The formula is included for those who are math-inclined and want to follow it, or you can do test generations to see your prices.
    
    ********************************FORMULA INFO (for the math nerds)********************************
    blink_gems_total = 20,028 * blink_gems%
    non_blink_enemies_total = 16,153 * non_blink_enemies%
    other_gems_total = 106,643 * other_gems%
    gem_total = blink_gems_total + non_blink_enemies_total + other_gems_total
    base_shop_price = gem_total / (number of shop items determined by key_rings - 1)

    If gem_logic is disabled, shop items will cost base_shop_price, rounded down if needed.
    If gem_logic is enabled, shop items will cost base_shop_price * 1, base_shop_price * 2, etc., rounded down if needed.
    *************************************************************************************************
    """
    display_name = "Gem Logic"
    default = 0


class BlinkGems(Range):
    """This option is used when shop_randomization and gem_logic are enabled. It lets you decide what percentage of
    gems from Blink's minigames you want to be expected to collect. His minigames are frequently disliked/skipped, and
    they have significantly gems than the other minigames, which is why this is an isolated option.
    
    For example, a value of 50 means being expected to collect approximately 50% of the gems available in each Blink minigame.
    His minigames contain 20,028 total, so this would result in an expectation of 10,014 gems. Set this to 0 if you
    intend to skip Blink minigames, whether that be from underground-air-a-phobia or because you excluded some/all of their checks.
    """
    display_name = "Blink Gems"
    range_start = 0
    range_end = 100
    default = 75


class NonBlinkEnemies(Range):
    """This option is used when shop_randomization and gem_logic are enabled. It lets you decide what percentage of gems
    from enemies you want to be expected to collect. This only applies to enemies when playing as Spyro.
    
    Gem logic assumes you will kill every enemy exactly once. This is nearly impossible to do accurately,
    since enemies respawn on death or reloads, and you won't be able to kill every enemy you come across on first visit,
    due to the nature of randomizers. This option was introduced to mitigate this issue.
    
    This option works similarly to blink_gems. For example, a value of 40 means being expected to collect approximately
    40% of gems from enemies. This works out to be roughly 6,461 (enemies have 16,153 gems total)."""
    display_name = "Non-Blink Enemies"
    range_start = 0
    range_end = 100
    default = 75


class OtherGems(Range):
    """This option is used when shop_randomization and gem_logic are enabled. It works similarly to blink_gems and non_blink_enemies,
    but applying to all other sources of gems. This primarily consists of gems from breakable containers and from
    Sgt. Byrd + Sparx minigames, plus some misc. others (such as gems on the ground in levels).
    
    The total amount of "other" gems is 106,643. Like blink_gems and non_blink_enemies, a value of 35 means
    being expected to collect approximately 37,325 "other" gems.
    
    Note: it's hard to get consistent gems from Sparx minigames. Their total was calculated as an average of 4-5 runs through
    each one's Dragon Egg + Light Gem forms. The total for each worked out to be 1,523 -> 2,148 -> 2,218 -> 2,392."""
    display_name = "Other Gems"
    range_start = 0
    range_end = 100
    default = 75
    
    
class DoubleGems(Choice):
    """This option is only used if your shop is randomized with gem logic.
    
    Gem logic does not currently support double gems, meaning if you were to receive double gems mid-run, you would
    collect gems 2x faster than the generated logic expects. This is not a problem per se, but can lead to you skipping
    ahead of the intended logic for the seed. This option allows you to eliminate Double Gems from your item pool, which
    ensures you have a consistent gem collection rate."""
    display_name = "Double Gems"
    option_enabled = 0
    option_disabled = 1
    default = 0

###############GATE & GADGET COSTS###############
class RandomizeBossLairDoorCosts(Choice):
    """Determines Dark Gem cost for each boss lair.

    default: Each boss lair has their vanilla cost (10, 20, 30, 40).
    randomized: Randomly picks costs in the range defined by boss_lair_door_cost_min and boss_lair_door_cost_max.
    shuffle: The vanilla boss lair costs are shuffled between each other (i.e. still 10/20/30/40 but in a random order).
    """
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
    
    Selecting "unchanged" leaves boss lair costs untouched."""
    display_name = "Boss Lair Forcing"
    option_gnasty_gnorc = 0
    option_ineptune = 1
    option_red = 2
    option_mecha_red = 3
    option_unchanged = 4
    default = 4
    

class RandomizeLightGemDoorCosts(Choice):
    """Determines Light Gem door costs.

    default: Each door has their vanilla cost (20, 45, 70, 95).
    randomized: Randomly picks costs in the range defined by light_gem_door_cost_min and light_gem_door_cost_max.
    shuffle: Each door has their vanilla cost shuffled with the others (20, 45, 70, 95).
    """
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
    """Determines gadget costs.

    default: Each gadget has their vanilla cost (8, 24, 40).
    randomized: Randomly picks costs in the range defined by gadget_cost_min and gadget_cost_max.
    shuffle: Each door has their vanilla cost shuffled with the others (8, 24, 40).
    """
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
class HintMinigameRewards(Toggle):
    """Whether to auto-hint a mini-game's reward when talking to its NPC."""
    display_name = "Hint Mini Game Rewards"
    default = 0


class HintBossRewards(Toggle):
    """Whether to auto-hint a boss's reward(s) when their gate is opened."""
    display_name = "Hint Boss Rewards"
    default = 0


class EasyBosses(OptionSet):
    """Toggles 'easy mode' for each boss, making them take triple damage to shorten fights considerably.
    Valid options: ["Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red"]"""
    display_name = "Easy Bosses"
    valid_keys = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red")
    default = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red")


class SkipCutscenes(Toggle):
    """Enable skipping most cutscenes with the Y button.
    In rare cases, this may have glitchy side effects."""
    display_name = "Auto Skip Cutscenes"
    default = 0


class SkipElevators(Toggle):
    """Enable a patch to skip the long elevator waits to Cloudy Domain, Sunken Ruins and Magma Falls"""
    display_name = "Skip Elevators"
    default = 0


class TeleportAcrossRealms(Toggle):
    """Allows for teleporting to unlocked Moneybags shop pads in any realm, from any realm.
    For example, you could teleport directly from Dragonfly Falls to Dark Mine
    without needing to use a hub realm teleporter."""
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
        HintMinigameRewards, HintBossRewards,
        EasyBosses,
        SkipCutscenes, SkipElevators,
        TeleportAcrossRealms
    ])
]