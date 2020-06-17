System Design, Python, Docker, *Kubernetes, AWS, *Google Cloud, Java/Typescript, HTML/CSS, *React, SASS, Redis, Git, Linux, *Postgres


Fantasy Quest Generator: User provides team size, levels, classes, and desired difficulty. Returns series of generated stages (interior, exterior) in a connected map. Enemy encounters, NPC interactions, bosses, traps, treasure, autogenerated quest title, etc. Rendered in minimal pixellated form. Events on map are hoverable to show full details.
    ? Use DND data (self-parsed or API)
    ? Use markov-chains based on parsed DND data to make odd and hilarious

    
Backend: Python interacting with Redis, Postgres and serverless task system via GCP
Frontend: React, HTML and SCSS. Responsive design (mobile via ReactNative?)
Infra: Docker/Kubernetes deployed to GCP cluster

Redis - Cache intermediate content during generation, as well as results
Postgres - Save serialized results and metadata, tied to unique seed ID
    Creation Timestamp, Times Viewed, Score/Rating



Need to parse events from the following and map them to stats, proficiencies and outcomes:
    https://old.reddit.com/r/d100/comments/7mg1vd/lets_build_side_quest_hooks/
    https://archive.org/stream/tsr09234dungeonmastersdesignkit/tsr09234%20-%20Dungeon%20Master%27s%20Design%20Kit_djvu.txt
    https://donjon.bin.sh/fantasy/adventure/



    
MVP -
    * Frontend takes in specific parameters: team size, average level, number of areas
    * Frontend displays interesting loading screen (backend results as they complete with juicy fx?)
    * Backend creates generation task
        * Pull associated DND details from API, cache results
        * Create map object with defined number of areas: github.com/galenscovell/Cartographer
        * Split areas into subareas randomly and based on overall size. Name subareas. Some are interiors (caves, houses, temples, ruins, etc) and others exteriors (grasslands, mountains, hills, bodies of water, etc)
        * Assign appropriate DND data events (conversations, traps, treasure, etc) to subareas at random
        * Construct enemy encounters from DND data with appropriate stats and assign them to appropriate subareas at random
        * Construct boss encounter for the area and the associated reward
        * Generate funny, cool name that captures the essence of the map
        * Generate unique ID and save serialized map and metadata to DB
    * Frontend allows user to hover over map details (with juicy fx, obv)
    * Frontend allows user to rate map

Aesthetic:
    Map font: Trattatello, Crimson, Copperplate, Aniron, or Luminari (serif)
        Natural elements: Trattatello
        Created elements: Crimson
        Ethereal, informative elements: Copperplate Gothic
    Include compass rose




Stretch - 
    * Each "run" is keyed to a unique ID that the user uses to continue their run, eg. approot/yHihduiO98gh9. Each run has characters in their party (each character is just a class with collection of proficiencies and stats, a level and name). The deeds they accomplish (events successful) are recorded and displayed somewhere (end of game).
    * Users interact with the maps. At each event location, they select which character in their party they wish to handle it, and a die is rolled versus a target proficiency and stats. If successful, there is possibility of a reward, otherwise they lose HP. Regardless the event is resolved and the user moves onto the next. When a map is completed the entire party gains XP, improving traits and stats.
    * Combat is minimally interactive. Mobs have stats that are rolled against characters and their proficiences.
    * A run has amassed treasure. Users use treasure to heal at inns, revive dead characters, and buy items.
    * Run has score calculated by events successfully completed, treasure collected, etc.

    Stats:
        (roll 4xD6 per stat, and remove the lowest)
        * [STR] Melee DMG, strength checks
        * [DEX] Range DMG, speed checks
        * [CON] HP, resistance checks
        * [WIS] Perception checks
        * [INT] Magic DMG, intelligence checks
        * [CHA] Persuasion checks
    Proficiencies:
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