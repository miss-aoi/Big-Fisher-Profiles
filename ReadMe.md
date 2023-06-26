# Big Fishing Profile

This profile set is designed to catch all Big Fish until level 90.

## Setup

- Install ExBuddy from here: https://github.com/LlamaMagic/ExBuddy
    - This repo is needed as it includes support for many newer fishing abilities that are used in the profiles like Thaliak's Favor, Surface Slap, Prize Catch, Makeshift Bait, etc
    - You will want to replace the git url managed by RepoBuddy, remove the ExBuddy folder in Plugins, then restart RebornBuddy
- Install __LlamaLibrary from here: https://github.com/nt153133/__LlamaLibrary/
- Install Lisbeth from here: https://www.siune.io/
- Install AutoHook from here: https://github.com/InitialDet/AutoHook
- Copy the below string and import as Custom Preset in AutoHook

AH_H4sIAAAAAAAACu2ZXW+bMBSG/wrydTKl66Rp3KUkbSKlaySYdjHtwoEDWDE28oc0VPW/z24GoZRxVXF1bt/X58MWD6DjZ3JUoMF8pxWQkNyxYnnPdAlqmSiWnptlYgtNFuTAtHnK7ygzmoS/nslW0BOHjIRGWVgQb/xLsT5RTk3JqAjiCrhxwTspzz+BngdBrbwXxjLDpPiPv9kluxEraWrwNgm/3Hz99lbrUvbN2CgpipFMF2OqjcuKiUYuC3y11e1QfdNMax+gAJFR1Ywk7LyplrpFE111a4Zn9L5C29sPDZHVRlad42NImFOu4dVeWyMfpUzLtlpf+9ytfBK8eZV6Ja5JYqtymkLMad2X9xkIw1LKI6pN39hI6zY4bMU9o/V71R/IkRoGIoWh7rsaq30A45/7rU5pfQ16pH8SVsEGOHVHuPq0chITQ8kfWWkrL6t+aCsOwsfk2Mh6nRtQEbVFed35QD+wijnz5mUxSSAYB3CwbQDZQ/aQvVnZE6l775ggLhWrauQP+UP+5uQvknUNKnefcmQP2UP25mTvgVP38VNBJBX+eSJ9SN+89DUqcLMX4QcviZIWBy+IICI4K4I7yAqoJIcg8sNTQAQRQURwVgT3KQT3FBTDP1BkD9mblb2ju/djwlaBv0nB8QuOX3D8Mid+7rKZ1ZAFD/LUIH1IH9L3wfT9fvkLTWrmoC4jAAA=

Open "Start.xml" and change the 0 to 1 for each Big fish you want.

Some of the fish in locations in game are very, very specific and ExFish doesn't always seem to go to exactly the same position. Because of this, it is advised to keep an eye on the character to see if they need to be moved a little in order to hit the appropriate fishing spot.

All fish with timed window have the time check shifted to one hour earlier on the Start.xml profile. This is so you can get bait (if needed) and get to the spot so that time is spent fishing for those with short windows rather than getting there. So if you get to a fishing spot and sit for a few minutes, double check if it's a timed window first.

ExBuddy's implementation of fishing does not always respect the tug type mentioned in a profile. The logic for this works for most big fish, but will only use Powerful Hookset for any !!! tug type, even if Precision Hookset is specific in the OrderBot profile. I'm not really great at CSharp code, so we're using AutoHook instead to handle using the correct hook method for the few cases where it is needed with mooched fish..

## Disclaimer

This profile set is still a work in progress, so use at your own risk and I'm not responsible if it does anything not fun.

### La Noscea
- [x] Eastern La Noscea
- [x] Lower La Noscea
- [x] Middle La Noscea
- [x] Western La Noscea
- [x] Upper La Noscea
- [x] Outer La Noscea
- [x] Lower Decks
- [x] Upper Decks
- [x] Mist

### The Black Shroud
- [x] New Gridania
- [x] Old Gridania
- [x] Central Shroud
- [x] East Shroud
- [x] South Shroud
- [x] North Shroud
- [x] The Lavender Beds

### Thanalan
- [x] Western Thanalan
- [x] Central Thanalan
- [x] Eastern Thanalan
- [x] Southern Thanalan
- [x] Northern Thanalan
- [x] The Goblet

### Coerthas
- [x] Coerthas Central Highlands
- [x] Coerthas Western Highlands

### Mor Dhona
- [x] Mor Dhona

### Abalathia's Spine
- [x] The Sea of Clouds
- [x] Azys Lla

### Dravania
- [x] The Dravanian Forelands
- [x] The Dravanian Hinterlands
- [x] The Churning Mists

### Gyr Abania
- [x] Rhalgr's Reach
- [x] The Fringes
- [x] The Peaks
- [x] The Lochs

### Othard
- [x] The Ruby Sea
- [x] Yanxia
- [x] The Azim Steppe
- [x] The Doman Enclave

### Hingashi
- [x] Kugane
- [x] Shirogane

### Norvrandt
- [x] The Crystarium
- [x] Eulmore
- [x] Lakeland
- [x] Kholusia
- [x] Amh Araeng
- [x] Il Mheg
- [x] The Rak'tika Greatwood
- [x] The Tempest

### The North Empty
- [x] Old Sharlayan
- [x] Labyinthos

### Ilsabard
- [x] Radz-at-Han
- [x] Thavnair
- [x] Garlemald

### The Sea of Stars
- [x] Mare Lametorum
- [x] Ultima Thule

### The World Unsundered
- [x] Elpis

### The High Seas
- [x] Galadion Bay
- [x] The Southern Strait of Merlthor
- [x] The Northern Strait of Merlthor
- [x] Rhotano Sea
- [x] The Cieldalaes
- [x] The Bloodbrine Sea
- [x] The Rothlyt Sound

### TODO:
- More testing

## Looking to Donate? ♡
I love Lattes: [BuyMeCoffee](https://buymeacoffee.com/miss_aoi)
