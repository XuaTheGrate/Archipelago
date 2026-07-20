from dataclasses import dataclass

from Options import OptionSet, PerGameCommonOptions, Toggle, Choice, Range, OptionGroup, StartInventoryPool

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

###############GOAL, CHECKS, AND ITEMS###############
class Goal(Choice):
    """Determines your goal boss, or to require all 4 bosses."""
    display_name = "Goal"
    option_gnasty_gnorc = 0
    option_ineptune = 1
    option_red = 2
    option_mecha_red = 3
    option_all = 4
    default = 3


class FireworkChecks(Toggle):
    """Whether to enable checks for flaming fireworks. Fire breath is required for surprisingly few things in this game,
    so enabling this helps make fire breath more important. This option adds +22 filler items."""
    display_name = "Firework Checks"
    default = 0


class RandomizeMinigames(OptionSet):
    """The list below contains which minigames will be given randomized rewards. If you would like a certain type
    of minigame to be guaranteed their vanilla Dragon Egg & Light Gem rewards, take them out of the list below.

    Valid options: ["Sgt. Byrd", "Blink", "Turret", "Sparx"]
    """
    display_name = "Randomize Minigames"
    valid_keys = ("Sgt. Byrd", "Blink", "Turret", "Sparx")
    default = ("Sgt. Byrd", "Blink", "Turret", "Sparx")


class FillerItems(OptionSet):
    """Choose what will make up your filler item pool. The randomizer picks from your choices here at random, for
    every location which needs a filler item. There is always a minimum of 101 such locations.
    
    Dragon Eggs: Dragon Eggs are functionally useless in Archipelago, because the extras that they unlock are
    unlocked when you collect the in-game Dragon Eggs, regardless of what they were randomized into. Dragon Eggs
    given from minigames which are unrandomized (see randomize_minigames) are still given even if omitted here.
    
    Breath Bombs: random vanilla game bomb items. Only usable if you have that breath unlocked.
    
    Gem Packs: give a random amount of gems (400-600 or 800-1200 if you have double gems). It is strongly advised
    to remove these if you are using shop randomization, because gem logic does not account for gem packs. You would
    be collecting gems faster than logic expects, to varying degrees depending on how many gem packs get created.
    
    Generic: Empty items which do nothing, but have humorous names referencing characters or things in the series.
    There are 12 total (6 chosen each seed, or all 12 if this is the only filler), so these will likely make up the
    majority of your filler pool if enabled. This option is chosen automatically if the list is left empty.
    
    Valid options: ["Dragon Eggs", "Breath Bombs", "Gem Packs", "Generic"]"""
    display_name = "Filler Items"
    valid_keys = ("Dragon Eggs", "Breath Bombs", "Gem Packs", "Generic")
    default = ("Dragon Eggs", "Breath Bombs", "Gem Packs", "Generic")

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
    """Whether to randomize the ability to glide, swim, and charge.
    If not randomized, your 3 movement starter checks will award these abilities.
    If you don't want to randomize a subset of these, add them to your start inventory."""
    display_name = "Randomize Movement"
    default = 0


class StartingRealm(Choice):
    """Access to a realm is granted when you possess the "access card" item for each one's respective first level.
    This option lets you decide which realm you will start in upon creating your save file.
    If you would like to start with access to multiple realms, add their access cards to
    start_inventory or start_inventory_from_pool. The one selected here will still be where you physically start.
    """
    default = 0
    display_name = "Starting Realm"
    option_dragon_kingdom = 0
    option_lost_cities = 1
    option_icy_wilderness = 2
    option_volcanic_isle = 3
    option_randomized = 4
    
###############SHOP###############
class ShopRandomization(Toggle):
    """Determines whether to randomize Moneybags' shop. If not randomized, it will function identically to the vanilla
    game, with one difference. If you enable key rings, 14 unique key rings will replace lockpicks in the shop. 

    If the shop is randomized, vanilla game items will be replaced with items from Archipelago.
    Shop items will progressively unlock as you collect gems throughout the seed. Once a shop item is unlocked, you can
    redeem it for free. This approach has some behind-the-scenes benefits detailed in the project's GitHub README.
    
    This has a few consequences worth noting:
        a) Double Gems, if enabled, is permanent once received, as is the Butterfly Jar (it replenishes on death if depleted).
        b) There is no limit on how many lockpicks you can hold at once. Same with ammo for breath bombs.
        c) If key rings are enabled, the world will have 14 level-specific key rings, instead of 52 lockpicks.

    Item prices are determined by gem_collection below."""
    display_name = "Randomize Shop Items"
    default = 0


class KeyRings(Toggle):
    """This option enables level-specific key rings which will open all locked chests in that level.

    If your shop is randomized, and key rings are enabled: you will have 18 shop items, and 14 key rings will
    be placed randomly in the world.

    If your shop is randomized and key rings are disabled: you will have 56 shop items, and 52 lockpicks will be placed
    randomly in the world.

    If your shop is not randomized: key rings or lockpicks will be buyable in the shop depending on this option.
    """
    display_name = "Key Rings"
    default = 0


class GemCollection(Range):
    """This option is only used if you have shop randomization on, and lets you limit how much of each area's
    gems you need to collect. For example, a value of 50 means logic will expect you to always collect approximately
    50% of accessible gems. The amount you are expected to have is visible on the pause screen.
    ***Note that Blink minigames are separately decided below with blink_gems.***

    This option contributes to determining your shop item prices. Moneybags always offers your first shop item for free.
    Inflation has hit the Dragon Kingdom strong, and he thinks he'll get more customers in by offering a loss-leader
    (it's actually to prevent a number of restrictive starts). Other shop items will be priced based on a formula taking
    into account this option, blink_gems, and your number of shop items. You can do a test generation to check your
    shop prices, or if you are math-inclined, the formula is below. For more info, see the project's README.

    ********************************FORMULA INFO (for the math nerds)********************************
    non_blink_gems = 122,429 * gem_collection%, rounded down
    blink_gems = 20,028 * blink_gems%, rounded down
    base_shop_price = (non_blink_gems + blink_gems) / (number of shop items - 1), rounded down
    Prices will be base_shop_price * 1, base_shop_price * 2, etc. for all n shop items. The final item will be
    (non_blink_gems + blink_gems) which accounts for all the rounding down.

    Example: 60 for gem_collection and 40 for blink_gems, on a seed with 18 shop items, would give prices
    of 4,792 -> 9,584 -> 14,376 -> ... -> 81,468.
    *************************************************************************************************"""
    display_name = "Gem Collection"
    range_start = 1
    range_end = 100
    default = 50


class BlinkGems(Range):
    """This option is only used when the shop is randomized, and pairs with gem_collection. This option isolates Blink's
    minigame gems, because his contain more than the other types (Blink has 20,028, Sparx has 3,671, Sgt. Byrd has 8,281).
    
    This option works identically to gem_collection. For example, a 40 below means collecting 40% of Blink's minigame
    gems, which is 8,011. Set this option to 0 if you intend to skip Blink minigames, whether that be on principle, 
    from underground-air-a-phobia, or because you excluded enough Blink minigame locations to justify it.
    """
    display_name = "Blink Gems"
    range_start = 0
    range_end = 100
    default = 50

    
class DoubleGems(Choice):
    """This option is only used if you have shop randomization on.
    The shop randomization functionality interacts awkwardly with Double Gems. Double Gems is NOT accounted for
    during generation logic, meaning if you were to receive Double Gems in a seed, you would begin collecting gems
    2x faster than the seed is expecting. This is not a problem, per se, but can lead to you skipping ahead of the
    intended logic for the seed.
    
    To remedy this, you can choose to eliminate Double Gems from your item pool using this option. This keeps your
    gem collection stable throughout the seed and ensures you will stay following the intended logic for your seed."""
    display_name = "Double Gems"
    option_disabled = 0
    option_enabled = 1
    default = 1

###############GATE & GADGET COSTS###############
class RandomizeBossLairDoorCosts(Choice):
    """Determines Dark Gem cost for each boss lair.
    Whichever boss is your goal (if not all bosses) will always be the most expensive.

    default: Each boss lair has their vanilla cost (10, 20, 30, 40).
    randomized: Randomly picks costs in the range defined by boss_lair_door_cost_min and boss_lair_door_cost_max.
    shuffle: Each boss lair has their vanilla cost shuffled with the others (10, 20, 30, 40).
    """
    display_name = "Randomize Boss Lair Requirements"
    option_default = 0
    option_randomized = 1
    option_shuffle = 2
    default = 0


class BossLairDoorCostMin(Range):
    """Minimum cost for boss lairs, if set to be random."""
    display_name = "Boss Lair Door Cost Minimum"
    range_start = 1
    range_end = 40
    default = 1


class BossLairDoorCostMax(Range):
    """Maximum cost for boss lairs, if set to be random."""
    display_name = "Boss Lair Door Cost Maximum"
    range_start = 1
    range_end = 40
    default = 40


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
    """Minimum cost for light gem doors, if set to be random."""
    display_name = "Minimum Light Gem Door Cost"
    range_start = 1
    range_end = 100
    default = 1


class LightGemDoorCostMax(Range):
    """Maximum cost for light gem doors, if set to be random."""
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
    """Minimum cost for gadgets, if set to be random."""
    display_name = "Minimum Gadget Cost"
    range_start = 1
    range_end = 100
    default = 8


class GadgetCostMax(Range):
    """Maximum cost for gadgets, if set to be random."""
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


class OpenWorldMode(Toggle):
    """NOT CURRENTLY SUPPORTED LOGICALLY. Turning this on will enable the patch, but logic will not
    utilize it. This allows for teleporting to any Moneybags' shop pad from the start of your file.
    Only left in for development testing purposes."""
    display_name = "Open World Mode"
    default = 0


@dataclass
class SpyroAHTOptions(PerGameCommonOptions):
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
    
    goal: Goal
    firework_checks: FireworkChecks
    randomize_minigames: RandomizeMinigames
    filler_items: FillerItems
    
    starting_breath: StartingBreath
    randomize_movement: RandomizeMovement
    starting_realm: StartingRealm
    
    shop_randomization: ShopRandomization
    key_rings: KeyRings
    gem_collection: GemCollection
    blink_gems: BlinkGems
    double_gems: DoubleGems
    
    randomize_boss_lair_door_costs: RandomizeBossLairDoorCosts
    boss_lair_door_cost_min: BossLairDoorCostMin
    boss_lair_door_cost_max: BossLairDoorCostMax
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
    # open_world_mode: OpenWorldMode
    
    
spyro_options_groups = [
    OptionGroup("GOAL, CHECKS, AND ITEMS", [
        Goal, FireworkChecks, RandomizeMinigames, FillerItems
    ]),
    OptionGroup("START OF GAME", [
        StartingBreath, RandomizeMovement, StartingRealm
    ]),
    OptionGroup("SHOP", [
        ShopRandomization, KeyRings, GemCollection, BlinkGems, DoubleGems
    ]),
    OptionGroup("GATE & GADGET COSTS", [
        RandomizeBossLairDoorCosts, BossLairDoorCostMin, BossLairDoorCostMax,
        RandomizeLightGemDoorCosts, LightGemDoorCostMin, LightGemDoorCostMax,
        RandomizeGadgetCosts, GadgetCostMin, GadgetCostMax
    ]),
    OptionGroup("QUALITY OF LIFE", [
        HintMinigameRewards, HintBossRewards,
        EasyBosses,
        SkipCutscenes, SkipElevators,
        TeleportAcrossRealms# , OpenWorldMode
    ])
]