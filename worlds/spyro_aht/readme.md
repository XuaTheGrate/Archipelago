# Spyro: A Hero's Tail Archipelago
An implementation of the Archipelago randomizer for Spyro: A Hero's Tail for Playstation 2 and GameCube.

## What is randomized?
Regardless of YAML settings, all the following are randomized and exist as checks:
  - The 3 major game collectibles (dark gems, light gems, and dragon eggs).
  - Locked chests, including the ones that in vanilla game only give junk (like gems).
  - The elemental breath rewards from the first 3 bosses.
  - Minigame rewards, sort of (their rewards are able to be unrandomized, but they will always be checks)
  - Movement abilities from the 4 Elders (Double Jump, Pole Spin, Wing Shield, Wall Kick)
    - Double Jump is guaranteed to be an early item you receive, because it is required for the vast majority of the randomizer's checks.

The following are randomizable via YAML settings:
  - Having fire breath.
  - The ability to charge, swim and glide.
  - The shop can be randomized (see the dedicated section below for details).
  - The cost to get into boss lairs and light gem doors, as well as for unlocking each gadget, are randomizable and shuffleable.
  - Access to the 4 realms can be set to require "access card" items, or to be unlocked from the start.
  - You can enable checks for flaming each of the 22 fireworks in the game.

## Setup Guide

##### Currently does not support PCSX2, but may change in the future.

1. Download the latest ``AR_Code.txt`` from https://github.com/BrinchEbsen/AHT_Archipelago.
   - The latest ``AR_Code.txt`` is also bundled with each release on this repo, for convenience.
2. Download and install the latest Spyro AHT .apworld file under the releases on this repo.
3. Toggle ``Enable Cheats`` in Dolphins settings.
4. Add the contents of ``AR_Code.txt`` into Dolphins cheats manager.
5. Launch the game.
6. Launch the client via Archipelago and connect to the multiworld (it will automatically hook into Dolphin).
7. Enjoy!

## Extra Notes

These are notes for getting the best experience on the GameCube version of
Spyro: A Hero's Tail on Dolphin.

#### Version

The latest release of Dolphin is recommended.

#### Graphics Settings

Dolphin has an issue with the game's depth-of-field effect which produces
glitchy graphics while underwater.
This issue can be fixed by disabling the settings "Store EFB Copies to Texture
Only" and "Defer EFB Copies to RAM" under Graphics->Hacks. This takes a big
toll on performance, so alternatively the effect can be disabled entirely by
enabling "Disable Fog" under Graphics->Enhancements, however this will obviously
disable the general fog effect as well.

#### Controls
For those unfamiliar with the GameCube version of the game, the button layout
is a bit weird, and might need remapping to match closer with other releases.

**A**: Jump
**X**: Charge
**Y**: Flame
**B**: Interact/Wing Shield

As there is no select button, you open the map screen by holding the **Z** button.

# Moneybags' Shop
Moneybags' shop is able to exist in 2 states: randomized and unrandomized.

## Unrandomized Shop
When the shop is unrandomized, it acts exactly as it does in the vanilla game, with one difference.
If you enable the "key rings" option, 14 key rings will replace lockpicks in the shop. Key rings are per-level and allow you to open all locked chests in that level.
When the shop is unrandomized, there are no checks for shop-related things.

## Randomized Shop
When the shop is randomized, vanilla game items will be replaced with items from Archipelago. These will either be items for Spyro AHT (if doing a solo seed), or potentially items for other games (if doing a multiworld). Shop items will unlock progressively as you play through the seed, except the first item, which is always free (this prevents restrictive start issues). This was made possible by the addition of **gem logic** to the randomizer.

### Gem Logic
The randomizer has awareness of when you can access which gems in each level, making it possible to take that into account when generating. In your YAML, you will choose how much of the game's gems you intend to collect, and the price of your shop items will be derived from what you specify. Once an item is unlocked, you can purchase it for free, meaning you will keep all gems you collect. This partially was to simplify the process of getting this system to work logically, and partially was a stylistic choice so you can think about the logic as your "total collected gems so far" instead of "the portion of gems I still have on hand".

The pause screen displays how many gems are possible to obtain in total, as well as how many are required to be at the percentage you specified in your YAML. You rarely will need to be exact. The logic **will** expect you to backtrack to previous areas, if they had gems you couldn't get at the time (especially relevant for gems from flameable fireworks). If you are struggling to find gems, you may want to set your gem collection settings lower next seed, and in the short-term, you can repeat some minigames if needed (Sparx ones are pretty efficient). The randomizer ultimately does not care *how* you get your gems, so do whatever you need to do :)

Next, this document will list a few notes on how the gem logic rules were decided on for a few types of things:
- Any basket, chest, etc. that is breakable with horn dive (from double jump) is expected to be. Double Jump is required for a LOT of the game's areas, so this *massively* simplified the gem logic rules by considering any gems obtainable immediately in any area to be called "immediates" internally.

- However, enemies will never expect you to horn dive to kill them, even though you can for many. This was to avoid expecting the player to risk extra damage just to take some poor gnorc's 20 gems (they have families, you monster!!!)

- Enemies are assumed to be killed exactly once each. This does mean if you can't kill an enemy right away in a level, the logic would expect you to backtrack later to kill them. This is not feasible for most players to keep track of, and we don't expect you to. It is expected that your gem count will desync from what logic see as maximally obtainable, by a possibly significant degree. This is why you should only set your gem collection YAML options high if you want to be expected to follow this strictly.

- Sparx minigames were hard to figure out, due to the high rate of variance in how many gems you will get from them (though the gems dropped from enemies appears to be consistent in itself). Each one was played 4-5 times and the gem amounts collected were averaged and used to determine the "total" for each.
  - Dragonly Falls: 695 for Dragon Egg, 828 for Light Gem
  - Sunken Ruins: 1,114 for Dragon Egg, 1,034 for Light Gem
  - Gloomy Glacier: 1,143 for Dragon Egg, 1,075 for Light Gem
  - Magma Falls: 1,313 for Dragon Egg, 1,076 for Light Gem

### Why This Design?
Previous versions of this randomize had all shop checks in logic in sphere 1, meaning anywhere from 18-56 shop items that the logic would expect you to buy *immediately*. This was never possible, so it was quite frequent players could get softlocked by having shop items that were too expensive, or if the player bought items in the wrong order with their limited gem income. This is a common problem for randomizers, and the most common solution is to logically space out the order the shop items will be bought, in some way. That is what the above design does :) There are some other side benefits of this system that are expected but hard to speak on with certainty, as this update is still new. The lead developer of this update (PhoenixAki) is always happy to discuss the reasoning for it all if you ping him in the server!