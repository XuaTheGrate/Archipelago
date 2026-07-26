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
    Fireworks: Flame all 22 fireworks. If chosen, firework_checks will be automatically enabled.
    Dark Gems: Break all 40 Dark Gems.
    Dragon Eggs: Collect all 80 Dragon Eggs.
    Light Gems: Collect all 100 Light Gems.
    Locked Chests: Open all 52 locked chests.
    Shop Items: Buy all randomized shop items (depends on key_rings). If chosen, shop_randomization will be automatically enabled.
    This can have dramatic consequences on the seed, due to multiple other options stemming from shop_randomization.
    
    Random: For each "Random" below, a random goal from above will be chosen. If the list is empty, 1 random goal will be chosen."""
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
    
    Valid Options: ["Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red", "Fireworks", "Dark Gems", "Dragon Eggs", "Light Gems",
    "Locked Chests", "Shop Items"]"""
    display_name= "Exclude From Goal"
    valid_keys = ("Gnasty Gnorc", "Ineptune", "Red", "Mecha-Red", "Fireworks", "Dark Gems", "Dragon Eggs", "Light Gems",
                  "Locked Chests", "Shop Items")
    default = frozenset()
    

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
    The extras they unlock are unlockable with cheat codes, if you want them without adding eggs to the filler pool.
    Even if you disable them here, Dragon Eggs will still be rewarded from minigames if you choose to force vanilla rewards above.
    
    Breath Bombs: Fire Bombs, Electric Bombs, Water Bombs, and Ice Bombs. Received bombs are only usable if you have that breath unlocked.

    Gem Packs: Each gives a random amount of gems (400-600 or 800-1200 if you have double gems). It is advised to not
    include these if using shop randomization with gem logic, because gem logic does not account for gem packs.

    Generics: Empty items which do nothing, but have humorous names referencing things in the game and series.
    This option is chosen automatically if the list is left empty.

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
    """Access to a realm is granted when you possess its "access card" item. For example, the "Dragon Kingdom
    Access Card" item grants access to the Dragon Kingdom realm.
    
    This option lets you choose which realm(s) to start with access to. Their access cards will be added to your start
    inventory. This is equivalent to putting the card(s) in your start inventory yourself.
    
    If the list is left empty, a random starting realm will be chosen for you.
    
    Valid Options: ["Dragon Kingdom", "Lost Cities", "Icy Wilderness", "Volcanic Isle"]"""
    display_name = "Starting Realms"
    valid_keys = ("Dragon Kingdom", "Lost Cities", "Icy Wilderness", "Volcanic Isle")
    default = ("Dragon Kingdom",)
    
###############SHOP###############
class ShopRandomization(Toggle):
    """Determines whether to randomize Moneybags' shop. If not randomized, it will function identically to the vanilla game. 

    If randomized, vanilla game shop items will be replaced with items from Archipelago. This has a few consequences:
        - Double Gems, if enabled, is permanent once received, as is the Butterfly Jar (it replenishes on death if depleted).
        - There is no limit on how many lockpicks you can hold at once. Same with ammo for breath bombs.
        - If key rings are enabled, the world will have 14 level-specific key rings, instead of 52 lockpicks.
        - Shop item prices will be the same everywhere i.e. remote shop pads will not upcharge you.
    The above information applies regardless of which type of shop randomization you choose below in gem_logic."""
    display_name = "Shop Randomization"
    default = 0
    
    
class GemLogic(Toggle):
    """This option determines which of the 2 types of shop randomization your seed will use, when shop_randomization is enabled.

    If gem_logic is disabled, there will be no logic used to determine when you can afford shop items, meaning the generator
    will expect you to buy all shop items at the start of the run. Since this is infeasible, you will have to choose the
    order you buy them as you collect gems. This means you risk getting stuck (requiring extra gem grinding to resolve)
    if you choose a suboptimal order, but those who want to have a choice in their item ordering may prefer this anyway.

    If gem_logic is enabled, shop items will be unlocked in a set order, with each one being purchasable for free once
    you collect enough gems to unlock it (prices will be listed as "unlocked at X gems"). The generator accomplishes this
    by keeping track of how many gems are accessible at all times. Items will have steadily increasing prices, which
    avoids the possibility of buying them in the "wrong" order, but you lose the ability to choose the order you buy them."""
    display_name = "Gem Logic"
    default = 0


class KeyRings(Toggle):
    """This option enables level-specific key rings which will open all locked chests in that level, which indirectly
    determines how many items you have in your shop.

    If your shop is not randomized: key rings or lockpicks will be buyable in the shop depending on this option.

    If your shop is randomized, and key rings are enabled: you will have 18 shop items, and 14 key rings will
    be placed randomly in the world.

    If your shop is randomized and key rings are disabled: you will have 56 shop items, and 52 lockpicks will be placed
    randomly in the world.
    """
    display_name = "Key Rings"
    default = 0


class NonBlinkGems(Range):
    """This option is only used if your shop is randomized. This option, along with blink_gems, determines how much of the
    game's gems you want to be expected to collect. blink_gems handles gems from Blink minigames, while non_blink_gems handles
    the rest of the game's gems. For example, non_blink_gems being 50 means being expected to collect 50% of all gems outside
    of Blink minigames. if you have gem_logic enabled, the amount you are expected to have is visible on the pause screen.
     
    This option contributes to determining your shop item prices. Moneybags always offers your first shop item for free,
    which prevents a number of restrictive starts. Other items will be priced in accordance to the formula below, which
    factors in a few things. If you are not math-inclined, you can always do some test generations to see how your shop reacts.

    ********************************FORMULA INFO (for the math nerds)********************************
    non_blink_total = 122,429 * non_blink_gems%, rounded down
    blink_total = 20,028 * blink_gems%, rounded down
    base_shop_price = (non_blink_total + blink_total) / (number of shop items - 1), rounded down

    If gem_logic is disabled, shop items will each cost base_shop_price.
    If gem_logic is enabled, shop items will each cost base_shop_price * 1, base_shop_price * 2, etc. for all N shop items.
    *************************************************************************************************"""
    display_name = "Non Blink Gems"
    range_start = 1
    range_end = 100
    default = 50


class BlinkGems(Range):
    """This option is only used when the shop is randomized, and pairs with non_blink_gems. This option isolates Blink's
    minigame gems, because his contain notably more than the other types.
    
    This option works identically to non_blink_gems. For example, setting this to 40 means collecting 40% of Blink's minigame
    gems, which is 8,011. Set this option to 0 if you intend to skip Blink minigames, whether that be from
    underground-air-a-phobia or because you excluded enough Blink minigame locations to justify it.
    """
    display_name = "Blink Gems"
    range_start = 0
    range_end = 100
    default = 50

    
class DoubleGems(Choice):
    """This option is only used if your shop is randomized with gem logic.
    
    Gem logic does not currently support double gems, meaning if you were to receive double gems mid-run, you would
    collect gems 2x faster than the generated logic expects. This is not a problem per se, but can lead to you skipping
    ahead of the intended logic for the seed. This option allows you to eliminate Double Gems from your item pool, which
    ensures you have a consistent gem collection rate."""
    display_name = "Double Gems"
    option_disabled = 0
    option_enabled = 1
    default = 1

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
    visibility = Visibility.none


@dataclass
class SpyroAHTOptions(PerGameCommonOptions):
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
    
    goal: Goal
    exclude_from_goal: ExcludeFromGoal
    firework_checks: FireworkChecks
    vanilla_minigame_rewards: VanillaMinigameRewards
    filler_items: FillerItems
    
    starting_breath: StartingBreath
    randomize_movement: RandomizeMovement
    starting_realms: StartingRealms
    
    shop_randomization: ShopRandomization
    gem_logic: GemLogic
    key_rings: KeyRings
    non_blink_gems: NonBlinkGems
    blink_gems: BlinkGems
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
    open_world_mode: OpenWorldMode
    
    
spyro_options_groups = [
    OptionGroup("GOAL, CHECKS, AND ITEMS", [
        Goal, ExcludeFromGoal, FireworkChecks, VanillaMinigameRewards, FillerItems
    ]),
    OptionGroup("START OF GAME", [
        StartingBreath, RandomizeMovement, StartingRealms
    ]),
    OptionGroup("SHOP", [
        ShopRandomization, GemLogic, KeyRings, NonBlinkGems, BlinkGems, DoubleGems
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
        TeleportAcrossRealms, OpenWorldMode
    ])
]