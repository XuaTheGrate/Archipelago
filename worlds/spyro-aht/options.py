from dataclasses import dataclass

from Options import OptionSet, PerGameCommonOptions, Toggle, Choice, Range, OptionGroup


class RandomizeSgtByrdMinigames(Toggle):
    """Whether to enable randomized locations for Sgt. Byrd's mini-games.
    If set to 'false', they will not be AP locations, and you will get the vanilla Dragon Eggs and Light Gems."""
    display_name = "Randomize Sgt. Byrd Mini Games"
    default = 1


class RandomizeBlinkMinigames(Toggle):
    """Whether to enable randomized locations for Blink's mini-games.
    If set to 'false', they will not be AP locations, and you will get the vanilla Dragon Eggs and Light Gems."""
    display_name = "Randomize Blink Mini Games"
    default = 0


class RandomizeTurretMinigames(Toggle):
    """Whether to enable randomized locations for the turret mini-games.
    If set to 'false', they will not be AP locations, and you will get the vanilla Dragon Eggs and Light Gems."""
    display_name = "Randomize Turret Mini Games"
    default = 1


class RandomizeSparxMinigames(Toggle):
    """Whether to enable randomized locations for Sparx's mini-games.
    If set to 'false', they will not be AP locations, and you will get the vanilla Dragon Eggs and Light Gems."""
    display_name = "Randomize Sparx Mini Games"
    default = 1


class HintMinigameRewards(Toggle):
    """Whether to auto-hint a mini-game's reward when talking to its NPC."""
    display_name = "Hint Mini Game Rewards"
    default = 1


class HintBossRewards(Toggle):
    """Whether to auto-hint a boss's reward(s) when their gate is opened."""
    display_name = "Hint Boss Rewards"
    default = 0


class RandomizeBreath(Choice):
    """Determines breath starting behavior.
    
    default: Start with fire breath.
    random: Start with a random breath.
    none: Start with no breath. Adds a starting check.
    """
    display_name = "Starting Breath"
    option_default = 0
    option_randomized = 1
    option_none = 2
    default = 0

class RandomizeMovement(Toggle):
    """Whether to randomize the ability to glide, swim, and charge.
    If you don't want to randomize a subset of these, add them to your start inventory."""
    display_name = "Randomize Movement"
    default = 0

class RandomizeFireworks(Toggle):
    """Whether to enable randomized locations for flaming fireworks.
    Each one requires fire breath."""
    display_name = "Randomize Fireworks"
    default = 0


class RandomizeShopItems(Toggle):
    """Whether to randomize the items in Moneybags' shop.
    If enabled, vanilla game items will be replaced with items from AP,
    and many of the vanilla shop items will be placed in other locations.

    Some consequences of this include:
    - If key rings are disabled, lock-picks have no upper limit. You can view your amount
    of lock-picks in the pause menu under 'Abilities'.
    - Butterfly Jar (Health Refill) will heal you automatically and refill after a death.
    - Double Gems is permanent once obtained."""
    display_name = "Randomize Shop Items"
    default = 0

class ShopPricesMin(Range):
    """The minimum price for shop items."""
    display_name = "Minimum Shop Price"
    range_start = 1
    range_end = 10000
    default = 500


class ShopPricesMax(Range):
    """The maximum price for shop items."""
    display_name = "Maximum Shop Price"
    range_start = 1
    range_end = 10000
    default = 5000


class KeyRings(Toggle):
    """Enable level-specific key rings for locked chests.
    Once a level's key ring is obtained, all chests within it can be opened.
    If Moneybags' shop is not randomized, key rings will be purchasable, otherwise they will
    be placed elsewhere in the world."""
    display_name = "Key Rings"
    default = 0


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
    """Minimum cost for boss lairs."""
    display_name = "Boss Lair Door Cost Minimum"
    range_start = 1
    range_end = 40
    default = 1


class BossLairDoorCostMax(Range):
    """Maximum cost for boss lairs."""
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
    """Minimum cost for light gem doors."""
    display_name = "Minimum Light Gem Door Cost"
    range_start = 1
    range_end = 100
    default = 1


class LightGemDoorCostMax(Range):
    """Maximum cost for light gem doors."""
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
    """Minimum cost for gadgets."""
    display_name = "Minimum Gadget Cost"
    range_start = 1
    range_end = 100
    default = 8


class GadgetCostMax(Range):
    """Maximum cost for gadgets."""
    display_name = "Maximum Gadget Cost"
    range_start = 1
    range_end = 100
    default = 40


class RealmAccess(Choice):
    """Whether to allow access to all realms at all times or to shuffle "Access Card" items into the world.
    Setting this to 'always' disables the locations for defeating each boss, as they would normally reward
    realm access. Breath rewards from bosses stays enabled.
    """
    display_name = "Realm Access"
    option_always = 0
    option_randomized = 2
    default = 0


class StartingRealm(Choice):
    """Determines which realm you will start in, or make it random."""
    default = 0
    display_name = "Starting Realm"
    option_dragon_village = 0
    option_coastal_remains = 1
    option_frostbite_village = 2
    option_stormy_beach = 3
    option_randomized = 4


class EasyBosses(OptionSet):
    """Toggles 'easy mode' for each boss, making them take triple damage to shorten fights considerably.
    Valid options: ["Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red"]"""
    display_name = "Easy Bosses"
    valid_keys = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red")
    default = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red")


class Goal(Choice):
    """Determines your goal boss, or to require all 4 bosses."""
    display_name = "Goal"
    option_gnorc = 0
    option_ineptune = 1
    option_red = 2
    option_mechared = 3
    option_all = 4
    default = 3


class SkipCutscenes(Toggle):
    """Enable skipping most cutscenes with the Y button.
    In rare cases, this may have glitchy side-effects."""
    display_name = "Auto Skip Cutscenes"
    default = 0


class SkipElevators(Toggle):
    """Enable a patch to skip the long elevator waits to Cloudy Domain, Sunken Ruins and Magma Falls"""
    display_name = "Skip Elevators"
    default = 1


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

class ShopUnlockMode(Toggle):
    """This feature is currently being worked on. Description soon™ once finalized."""
    display_name = "Shop Unlock Mode"
    default = 0


class TeleportAnywhere(Toggle):
    """Allows for teleporting to unlocked Moneybags shop pads in any realm.
    For example, you could teleport directly from Dragonfly Falls to Dark Mine
    without needing to use a hub realm teleporter."""
    display_name = "Teleport Anywhere"
    default = 0


class OpenWorldMode(Toggle):
    """Allows for teleporting to any Moneybags' shop pad from the start of your file.
    NOT CURRENTLY SUPPORTED LOGICALLY. Enabling this option will enable the behavior, which skips
    significant amounts of logic requirements. Only left in for development purposes currently."""
    display_name = "Unlock All Shops"
    default = 0


@dataclass
class SpyroAHTOptions(PerGameCommonOptions):
    randomize_sgt_byrd_minigames: RandomizeSgtByrdMinigames
    randomize_blink_minigames: RandomizeBlinkMinigames
    randomize_turret_minigames: RandomizeTurretMinigames
    randomize_sparx_minigames: RandomizeSparxMinigames

    randomize_breath: RandomizeBreath
    randomize_movement: RandomizeMovement

    randomize_fireworks: RandomizeFireworks

    key_rings: KeyRings

    randomize_shop_items: RandomizeShopItems
    shop_prices_min: ShopPricesMin
    shop_prices_max: ShopPricesMax

    randomize_light_gem_door_costs: RandomizeLightGemDoorCosts
    light_gem_door_cost_min: LightGemDoorCostMin
    light_gem_door_cost_max: LightGemDoorCostMax

    randomize_boss_lair_doors: RandomizeBossLairDoorCosts
    boss_lair_door_cost_min: BossLairDoorCostMin
    boss_lair_door_cost_max: BossLairDoorCostMax

    randomize_gadget_costs: RandomizeGadgetCosts
    gadget_cost_min: GadgetCostMin
    gadget_cost_max: GadgetCostMax

    realm_access: RealmAccess
    starting_realm: StartingRealm

    easy_bosses: EasyBosses
    goal: Goal
    hint_minigame_rewards: HintMinigameRewards
    hint_boss_rewards: HintBossRewards
    skip_cutscenes: SkipCutscenes
    skip_elevators: SkipElevators

    death_link: DeathLink

    shop_unlock_mode: ShopUnlockMode
    teleport_anywhere: TeleportAnywhere
    unlock_all_shops: UnlockAllShops

options_groups = [
    OptionGroup("GOAL & LOCATIONS", [
        Goal,
        RandomizeSgtByrdMinigames,
        RandomizeBlinkMinigames,
        RandomizeTurretMinigames,
        RandomizeSparxMinigames,
        RandomizeFireworks
    ]),
    OptionGroup("START OF GAME", [
        RandomizeBreath,
        RandomizeMovement,
        RealmAccess,
        StartingRealm
    ]),
    OptionGroup("COSTS", [
        RandomizeBossLairDoorCosts, BossLairDoorCostMin, BossLairDoorCostMax,
        RandomizeLightGemDoorCosts, LightGemDoorCostMin, LightGemDoorCostMax,
        RandomizeGadgetCosts, GadgetCostMin, GadgetCostMax
    ]),
    OptionGroup("SHOP", [
        RandomizeShopItems,
        ShopPricesMin, ShopPricesMax,
        KeyRings,
        UnlockAllShops,
        ShopUnlockMode
    ]),
    OptionGroup("QUALITY OF LIFE", [
        HintMinigameRewards, HintBossRewards,
        SkipCutscenes, SkipElevators,
        TeleportAnywhere, EasyBosses
    ])
]