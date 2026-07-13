from dataclasses import dataclass

from Options import OptionSet, PerGameCommonOptions, Toggle, Choice, Range, OptionGroup

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
    option_gnorc = 0
    option_ineptune = 1
    option_red = 2
    option_mechared = 3
    option_all = 4
    default = 3


class FireworkChecks(Toggle):
    """Whether to enable checks for flaming fireworks. Fire breath is required for surprisingly few things in this game,
    so enabling this helps make fire breath more important. This option adds +22 filler items."""
    display_name = "Randomize Fireworks"
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
    unlocked when you collect the in-game Dragon Eggs, regardless of what they were randomized into.
    
    Breath Bombs: random vanilla game bomb items. Only usable if you have that breath unlocked.
    
    Gem Packs: give a random amount of gems (400-600 or 800-1200 if you have double gems). It is strongly advised
    to remove these if you are using shop randomization, because gem logic does not account for gem packs. You would
    be collecting gems faster than logic expects, to varying degrees depending on how many gem packs get created.
    
    Generic: Empty items which do nothing, but have humorous names referencing characters or things in the series.
    There are 12 total (6 will be chosen each seed), so these will likely make up the majority of your filler pool
    if enabled. This option is chosen automatically if the list is left empty.
    
    Valid options: ["Dragon Eggs", "Breath Bombs", "Gem Packs", "Generic"]"""
    display_name = "Filler Items"
    valid_keys = ("Dragon Eggs", "Breath Bombs", "Gem Packs", "Generic")
    default = ("Dragon Eggs", "Breath Bombs", "Gem Packs", "Generic")

###############START OF GAME###############
class RandomizeBreath(Choice):
    """Determines breath starting behavior.
    "Starter Check: Breath" will either give your starting breath,
    or a random other item, if you choose "none".

    default: Start with fire breath.
    random: Start with a random breath.
    none: Start with no breath.
    """
    display_name = "Starting Breath"
    option_default = 0
    option_randomized = 1
    option_none = 2
    default = 0


class RandomizeMovement(Toggle):
    """Whether to randomize the ability to glide, swim, and charge.
    If not randomized, your 3 movement starter checks will award these abilities.
    If you don't want to randomize a subset of these, add them to your start inventory."""
    display_name = "Randomize Movement"
    default = 0


class RealmAccess(Choice):
    """Whether to allow access to all realms at all times or to shuffle realm "Access Card" items into the world.
    Setting this to 'always' removes the "Defeat <boss name>" checks, as they would normally reward
    realm access. You still will need to beat any goal-related bosses (and they will still reward their breath checks).
    Randomized realm access adds 1 filler item because Mecha-Red does not give a realm access card.
    """
    display_name = "Realm Access"
    option_always = 0
    option_randomized = 2
    default = 0


class StartingRealm(Choice):
    """Determines which realm you will start in, or to have it randomly chosen."""
    default = 0
    display_name = "Starting Realm"
    option_dragon_village = 0
    option_coastal_remains = 1
    option_frostbite_village = 2
    option_stormy_beach = 3
    option_randomized = 4
    
###############SHOP###############
class ShopRandomization(Toggle):
    """Determines whether to randomize Moneybags' shop. If not randomized, it will function identically to the vanilla
    game, with one difference. If you enable key rings, 14 unique key rings will replace lockpicks in the shop. 

    If the shop is randomized, vanilla game items will be replaced with items from Archipelago.
    Shop items will progressive unlock as you collect gems throughout the seed. Once a shop item is unlocked, you can
    redeem it for free. This approach has some behind-the-scenes benefits detailed in the project's GitHub README.
    
    This has a few consequences worth noting:
        a) Double Gems, if enabled, is permanent once received, as is the Butterfly Jar (it replenishes on death if depleted).
        b) There is no limit on how many lockpicks you can hold at once. Same with ammo for breath bombs.
        c) If key rings are enabled, the world will have 14 level-specific key rings, instead of 52 lockpicks.

    Item prices are determined by total_gems below."""
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


class TotalGems(Range):
    """This option is only used if you have shop randomization on, and lets you limit how much of each area's
    gems you need to collect. For example, a value of 50 means logic will expect you to always collect approximately
    50% of accessible gems. The amount you are expected to have is visible on the pause screen.
    ***Note that Blink minigames are separately decided below with blink_gems.***

    This option contributes to determining your shop item prices. If you'd like to calculate it yourself, the formula
    is below, but you can also check in-game with a test generation. For more info, see the project's README on GitHub.

    It is advised to not set this value too high unless you are a completionist or otherwise really know what you're doing.
    The higher it's set, the less wiggle room you have for skipping gems in areas.

    ********************************FORMULA INFO (for the math nerds)********************************
    non_minigame_gems = 124,235 * total_gems%, rounded down
    blink_gems = 18,222 * blink_gems%, rounded down
    base_shop_price = (non_minigame_gems + blink_gems) / number of shop items, rounded down
    Shop items are priced at base_shop_price -> base_shop_price * 2 -> base_shop_price * 3 -> etc.

    Example: 60 for total_gems and 40 for blink_gems, on a seed with 18 shop items, would give shop
    prices of 4,546 -> 9,092 -> 13,638 -> etc. with the final item equaling (non_minigame_gems + blink_gems).
    *************************************************************************************************"""
    display_name = "Total Gems"
    range_start = 1
    range_end = 100
    default = 50


class BlinkGems(Range):
    """This option is only used if you have shop randomization on, and is intended to pair with randomize_minigames.

    Even if you exclude a minigame type with randomize_minigames, you would still be expected to collect gems in
    them, due to how shop prices are calculated in total_gems. This option lets you specify a different percentage,
    if wanted, of gems to collect from Blink minigames, as they have significantly more gems than other minigames.
    For comparison, Sgt. Byrd has approximately 3,671 gems total, Sparx has 8,281, and Blink has 18,222.
    
    For example, if you specify 40 below, you'd be expected to collect 40% of all gems from Blink minigames, rounded
    down. That would be 18,222 * 40% = 7,288.8 -> 7,288. Set this option to 0 if you intend to skip Blink minigames.
    There is no similar option for Sgt. Byrd and Sparx because it is significantly less effort and time to collect
    their gems, and the smaller amounts are much more reasonably able to be made up for through other means.
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
    In rare cases, this may have glitchy side-effects."""
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
    
    goal: Goal
    firework_checks: FireworkChecks
    randomize_minigames: RandomizeMinigames
    filler_items: FillerItems
    
    randomize_breath: RandomizeBreath
    randomize_movement: RandomizeMovement
    realm_access: RealmAccess
    starting_realm: StartingRealm
    
    shop_randomization: ShopRandomization
    key_rings: KeyRings
    total_gems: TotalGems
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
    open_world_mode: OpenWorldMode
    
    
spyro_options_groups = [
    OptionGroup("GOAL, CHECKS, AND ITEMS", [
        Goal, FireworkChecks, RandomizeMinigames, FillerItems
    ]),
    OptionGroup("START OF GAME", [
        RandomizeBreath, RandomizeMovement, RealmAccess, StartingRealm
    ]),
    OptionGroup("SHOP", [
        ShopRandomization, KeyRings, TotalGems, BlinkGems, DoubleGems
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
        TeleportAcrossRealms, OpenWorldMode
    ])
]