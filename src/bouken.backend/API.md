# API

api_key must be passed to all endpoints for access.

## Endpoints

##### GET /status?api_key=
    * Output: StatusResponse

##### POST /
    * Input: PartyMember[], challengeLevel float, api_key
    * Output: Map

##### GET /{id}?api_key=
    * Input: unique ID string for map
    * Output: Map

## Models

##### PartyMember class
    * Class: enum
    * Level: int
    * XP: int
    * Name: string
    * Stats: dict{StatType -> int}
    * Proficiencies: dict{ProficiencyType -> int}
    
##### StatType enum
    * (All DND stat names)
    
##### ProficiencyType enum
    * (All DND proficiency names)
    
##### EventType enum
    * MinorEncounter: 0
    * MajorEncounter: 1
    * NPCDiscussion: 2
    * Trap: 3
    * Treasure: 4
    * PartyInteraction: 5
    * Boss: 6
  
##### Point class
    * PosX: float
    * PosY: float

##### Dimensions class
    * Center: Point
    * Radius: float
    
##### Outcome class
    * Target: PartyMember
    * AffectedStat: StatType
    * Modification: int
    
##### Enemy class
    * Name: string
    * Description: string
    * ChallengeLevel: float
    * TestedStat: StatType
    * TestedProficiency: ProficiencyType
    * Stats: dict{StatType -> int}
    * Proficiencies: dict{ProficiencyType -> int}
    
##### Encounter class : Event class
    * Enemies: Enemy[]
    
##### Event class
    * Name: string
    * Description: string
    * Dimensions: Dimensions
    * EventType: EventType
    * ChallengeLevel: float
    * TestedStat: StatType
    * TestedProficiency: ProficiencyType
    * Reward: Outcome
    * Penalty: Outcome

##### Map class
    * Regions: dict{}
    * ChallengeLevel: float
    * Boss: Encounter
    
##### Region class
    * Events: dict{Point -> Event}
    * Description: string
    * Name: string
    * Dimensions: Dimensions



## DB Definition

#### BOUKEN_STATIC.DB

Armor
    NAME ARMOR_CATEGORY ARMOR_BASE MIN_STR DEX_BONUS MAX_BONUS STEALTH_DISADVANTAGE WEIGHT COST
Weapons
    NAME WEAPON_CATEGORY RANGE_CATEGORY RANGE ONE_HAND_DAMAGE TWO_HAND_DAMAGE DAMAGE_TYPE WEIGHT COST
Damage Types
    NAME DESC
Conditions (make from scratch)
    NAME DESC
Spells (make from scratch)
    NAME DESC RANGE DURATION CASTING_TIME LEVEL MAGIC_SCHOOL CLASS DAMAGE_TYPE DAMAGE VERBAL SOMATIC FOCUS BONUS_AFTER_LEVEL BONUS_EFFECT
Magic Schools
    NAME DESC
Abilities
    NAME DESC
Skills
    NAME DESC ABILITY
Traits (make from scratch)
    NAME DESC SITUATION BONUS
Monsters
    NAME SIZE TYPE ALIGNMENT ARMOR_CLASS HIT_POINTS HIT_DICE WALK_SPEED CLIMB_SPEED FLY_SPEED SWIM_SPEED STR DEX CON INT WIS CHA SKILLS LANGUAGES CHALLENGE_RATING DAMAGE_VULNERABILITIES DAMAGE_RESISTANCES DAMAGE_IMMUNITIES CONDITION_IMMUNITIES SAVING_THROWS
Classes
    NAME HIT_DIE STARTING_SKILL_AMOUNT STARTING_SKILL_OPTIONS STARTING_SKILLS SAVING_THROWS
LEVELS
    CLASS LEVEL REQUIRED_XP ABILITY_BONUSES SKILL_BONUSES CANTRIPS TOTAL_SPELLS LEVEL_1_SPELL_SLOTS LEVEL_2_SPELL_SLOTS LEVEL_3_SPELL_SLOTS LEVEL_4_SPELL_SLOTS LEVEL_5_SPELL_SLOTS LEVEL_6_SPELL_SLOTS LEVEL_7_SPELL_SLOTS LEVEL_8_SPELL_SLOTS LEVEL_9_SPELL_SLOTS ARCANE_RECOVERY
Races
    NAME LANGUAGES LANGUAGE_DESC STARTING_SKILLS SIZE SIZE_DESC AGE ALIGNMENT SPEED CHA_BONUS DEX_BONUS INT_BONUS STR_BONUS WIS_BONUS TRAITS
Languages
    NAME TYPE TYPICAL_SPEAKERS SCRIPT
Traps
    LEVEL SEVERITY NAME FIND DISABLE TARGET EFFECT
Encounters
    CHALLENGE_RATING PARTY_SIZE AVG_LEVEL MONSTER_COUNT
Names (characters, settings)
    TYPE NAME


#### BOUKEN_DYNAMIC.DB
