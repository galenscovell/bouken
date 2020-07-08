==============================================================
High Level
==============================================================
System Design, Python, Docker/*Kubernetes, AWS/*Google Cloud, Java/Typescript, React (+ Phaser), HTML/SCSS, Redis, Git, Linux(Linode?), *SQLite

    
Backend: Python, Redis, SQLite. Task architecture (cloud?)
Frontend: React + Phaser, HTML/SCSS. Responsive design (mobile via ReactNative?)
Infra: Docker/Kubernetes deployed to cloud?

Redis - Cache intermediate content during generation, as well as results
SQLite - Save serialized results and metadata, tied to unique seed ID
    Creation Timestamp, Times Viewed, Score/Rating


==============================================================
MVP V1 - Pure Generation
==============================================================
* User creates party of characters up to max of 4
    * Characters have a class, level, name, ability scores, skills
* Frontend takes in team members, desired challenge level -> calls backend to generate maps
* Backend generates map:
    1) Hexagon overworld map: Regions + landscape features
    2) For each "dungeon" landscape feature (caves, temple, fortress, etc.), generate non-hexagon interior map
    3) Generate high-level story goal
    4) Create overworld events tying to high-level goal
    5) Create interior events tying to overworld and high-level goals
    6) Name overworld and interiors
* Frontend displays interactive map
    * Hover over events, landscape features etc. for details. Hovering over interior locations displays their map and events


==============================================================
Stretch V2 - Roguelike/Thunderstone
==============================================================
* Each "run" is keyed to a unique ID that the user uses to continue their run, eg. approot/yHihduiO98gh9. No need to register/track user credentials
* Users interact with map. At each event location they select which character in their party they wish to handle it (if single char event, there are also group events), and a die is rolled versus a target skill and ability. If successful there is possibility of a reward, otherwise they lose HP. Regardless the event is resolved and the user moves onto the next. When a map is completed the entire party gains XP, improving stats.
* Combat is a specific event type that is handled differently. Minimal turn-based: cycle through involved entities according to initiative, entities have a few actions based on class, level and abilities. In the end, just dice-rolling and effects.
* Player must clear a percentage of events in a region to clear it. Regions lock out other regions by locality. Once enough regions are completed, they face the boss of the map. Bosses are comprised of multiple events.
* Minimal resources (like Thunderstone): 


==============================================================
Aesthetic
==============================================================
Map font: Trattatello, Crimson, Copperplate, Aniron, or Luminari (serif)
    Natural elements: Trattatello
    Created elements: Crimson
    Ethereal, informative elements: Copperplate Gothic
Include compass rose


==============================================================
General
==============================================================
Abilities:
    (roll 4xD6 per stat, and remove the lowest)
    * [STR] Melee DMG, strength checks
    * [DEX] Range DMG, speed checks
    * [CON] HP, resistance checks
    * [WIS] Perception checks
    * [INT] Magic DMG, intelligence checks
    * [CHA] Persuasion checks

    Ability Modifiers:
        Ability of 2 or 3: -4
        Ability of 4 or 5: -3
        Ability of 6 or 7: -2
        Ability of 8 or 9: -1
        Ability of 10 or 11: +0
        Ability of 12 or 13: +1
        Ability of 14 or 15: +2
        Ability of 16 or 17: +3
        Ability of 18 or 19: +4

Skills:
    * Acrobatics (Dex)
    * Animal Handling (Wis)
    * Arcana (Int)
    * Athletics (Str)
    * Deception (Cha)
    * History (Int)
    * Insight (Wis)
    * Intimidation (Cha)
    * Investigation (Int)
    * Medicine (Wis)
    * Nature (Int)
    * Perception (Wis)
    * Performance (Cha)
    * Persuasion (Cha)
    * Religion (Int)
    * Sleight of Hand (Dex)
    * Stealth (Dex)
    * Survival (Wis)

Theme: gritty, hard fantasy in a cursed water world composed of numerous, moderately sized continents.

You are a small team of adventurers gathered to unearth the curse on the land. They make their way across varied environments collecting items, gaining proficiencies, leveling up and learning about the curse, which gradually makes the world more inhospitable.

The fundamental difficulty is both time (starvation with limited resources, and increasingly less available as envs become inhospitable) and making intelligent decisions on proficiency usage and battle tactics. Characters die easily and permanently. A smaller party moves faster and uses less resources but has fewer proficiencies and less power.

There is little dialogue. Clear icons are used and background lore is told via item descriptions and sporadic NPC interactions.

Permadeath, but some things carry over. Player unlocks new character classes and starting equipment -- which merely changes possible playstyles, not necessarily make things easier.

Ideas:
- Nemesis system (killed enemies return stronger and remember previous encounters)?
- Perhaps some curse/language knowledge transfers on death (time travel? clones?)


Overworld
- Displays region map
- Regions and dungeons open as minimaps, so overworld is always technically open
- Player must clear percentage of all regions to pass map/fight map boss
- Player hovers over regions for general detail/difficulty. Higher difficulty means more reward, including food
- Player clicks region to move there
- Player can analyze party stats in overworld

Region
- Once clicked, zoom in to region as player party moves there
- Region has possible minor event occur before main event (flavor text, trap, interaction, etc)
- Region has main event based on biome and landform
- Player can choose to forage/rest/train after events are resolved, each with a benefit and cost

Event
- Three main types: enemy encounter, NPC interaction, dungeon
- Enemy encounter is either monster or humanoid. Combat system TBD
- NPC interaction is encounter requiring strictly proficiencies. Can also be shops
- Dungeons are interior minimaps resembling LoZ dungeons, where each room is an event. Lots of loot and fighting, but also interactions and traps (why would we go into a dungeon while under time pressure? Loot sure, but maybe story related?)
