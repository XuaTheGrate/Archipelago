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

###############GOAL AND LOCATIONS/CHECKS###############
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
    """Whether to enable checks for flaming fireworks.
    Fire breath is required for surprisingly few things
    in this game, so enabling this helps make fire breath
    more important."""
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
    """Determines whether to randomize Moneybags' shop. If not randomized, it will contain vanilla game items sold at
    vanilla prices. 2 things of note:
    1) Lockpicks can be purchased with no limit, unless you enable key rings, in which case 14 unique key rings replace lockpicks.
    2) Double Gems is a permanent effect once purchased, as is the Butterfly Jar (it replenishes on death if depleted).

    If the shop is randomized, it functions very differently.
    1) Vanilla game items will be replaced with items from Archipelago.
    2) Shop items will progressively unlock as you collect gems throughout the seed. Once a shop item is unlocked, you
    can redeem it for free. This approach has some behind-the-scenes benefits detailed in the project's GitHub README.

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


class TotalGems(Toggle):
    """This option is only used if you have shop randomization on. This option lets you limit how much of each area's
    gems you need to collect. For example, a value of 50 means logic will expect you to always collect approximately
    50% of accessible gems. The amount you are expected to have is visible on the pause screen.

    This option contributes to determining your shop item prices. If you'd like to calculate it yourself, the formula
    is below, but you can also check in-game with a test generation. For more info, see the project's README on GitHub.

    It is advised to not set this value too high unless you are a completionist or otherwise really know what you're doing.
    The higher it's set, the less wiggle room you have for skipping gems in areas.

    ********************************FORMULA INFO (for the math nerds)********************************
    base_shop_price = (142,500 * total_gems% / number of shop items), rounded down
    Randomized shop items are priced at base_shop_price -> base_shop_price * 2 -> base_shop_price * 3 -> etc.

    For example, a value of 50 for total_gems on a seed with 18 shop items would give shop prices of
    3,958 -> 7,916 -> 11,874 -> 15,832 -> etc.
    *************************************************************************************************
    Minimum value is 1
    Maximum value is 100"""
    display_name = "Total Gems"
    default = 50

    
class DoubleGems(Choice):
    """This option is only used if you have shop randomization on.
    The new shop randomization functionality interacts awkwardly with Double Gems. Double Gems is NOT accounted for
    during generation logic, meaning if you were to receive Double Gems in a seed, you would begin collecting gems
    2x faster than the seed is expecting. This is not a problem, per se, but can lead to you skipping ahead of the
    intended logic for the seed.
    
    To remedy this, you can choose to eliminate Double Gems from your item pool using this option. This keeps your
    gem collection stable throughout the seed and ensures you will stay following the intended logic for your seed."""
    display_name = "Double Gems"
    option_enabled = 0
    option_disabled = 1
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
    
    randomize_breath: RandomizeBreath
    randomize_movement: RandomizeMovement
    realm_access: RealmAccess
    starting_realm: StartingRealm
    
    shop_randomization: ShopRandomization
    key_rings: KeyRings
    total_gems: TotalGems
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
    OptionGroup("GOAL & LOCATIONS/CHECKS", [
        Goal, FireworkChecks, RandomizeMinigames
    ]),
    OptionGroup("START OF GAME", [
        RandomizeBreath, RandomizeMovement, RealmAccess, StartingRealm
    ]),
    OptionGroup("SHOP", [
        ShopRandomization, KeyRings, TotalGems, DoubleGems
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