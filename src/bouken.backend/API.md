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
