# Spyro: A Hero's Tail Archipelago
An implementation of the Archipelago randomizer for Spyro: A Hero's Tail for Playstation 2 and GameCube.

## What is randomized?
Regardless of YAML settings, all the following are randomized and exist as checks:
  - The 3 major game collectibles (dark gems, light gems, and dragon eggs).
  - Locked chests, including the ones that in vanilla game only give junk (like gems).
  - The elemental breath rewards from the first 3 bosses.
  - Minigame rewards, sort of (their rewards are able to be unrandomized, but they will always be checks)
  - Movement abilities from the 4 Elders (Double Jump, Pole Spin, Wing Shield, Wall Kick)

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
When the shop is randomized, vanilla game items will be replaced with items from Archipelago. These will either be items for Spyro AHT (if you're doing a solo randomizer seed), or potentially items for other games (if you are doing a multiworld).

Shop items will unlock progressively as you play through the seed, except the first item, which is always free (this is required to prevent a handful of seed generation issues). In your YAML, you will choose how much of the game's gems you intend to collect, and the price of your shop items will be derived from what you specify.

Once a shop item is unlocked, you can purchase it for free, meaning you will keep all gems you collect. The pause screen will display how many gems are possible to obtain, as well as how many you need to be at the percentage you specified in your YAML. You don't need to be exact, unless it is just barely possible to afford your next item and the item is important. If you are struggling to find gems, you may want to set your gem collection settings lower next seed. During the current run, you can repeat some minigames if wanted (Sparx ones give pretty decent gems quickly).

### How Were Enemy Calculations Done
No different to other things, except that I had to assume the player will kill all enemies exactly once each. Enemies respawn on death/reload so technically give infinite gems. So I had to make that assumption to calculate a final "total" gem amount.

Logic does not care *how* you get your gems, whether it be by killing one enemy 100 times to get 2,000 gems or by breaking enough baskets to 2,000. Depending on your settings, this may matter further down the line if you have a high value of gem collection set, but lower values gives you way more fleixbility on how you go about getting your gems.

The only risk you get from collecting gems quicker than expected is unlocking shop items earlier than expected. This will never break a seed, but may give you a faster-than-intended path to progress. Up to you how much you care about that.

Enemies are not the only thing that give repeatable gems, though...

### How Were the Sparx Gem Calculations Done?
Sparx minigames were tricky to deal with. Enemies give gems there, but due to how you play the minigames, it's nearly impossible to get consistent gem results from them. I played each one 4-6 times and averaged my results and considered that the "total" for each one. These numbers are listed below for those interested:
Dragonfly Falls: 695 for Dragon Egg, 828 for Light Gem
Sunken Ruins: 1,114 for Dragon Egg, 1,034 for Light Gem
Gloomy Glacier: 1,143 for Dragon Egg, 1,075 for Light Gem
Magma Falls: 1,313 for Dragon Egg, 1,076 for Light Gem

Blink and Sgt. Byrd also have gems in them and they are repeatable, but they are also far, far more consistent at giving those gems to you, so it is assumed you can deal with that without logic assumptions.

### Why This Design?
*to be written eventually...*