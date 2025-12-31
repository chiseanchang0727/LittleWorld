# User Scenarios

This document describes the various scenarios and use cases for LittleWorld.

## Scenario 1: Character Observation
**Description:** AI character observes the world within vision radius  
**Actors:** AI Character  
**Steps:**
1. Character calls `make_decision(world_state, personality)`
2. AI decides to observe (returns `Decision(type=ActionType.OBSERVE, radius=100)`)
3. Character calls `observe(radius)` which returns visible entities
4. Character updates internal state with observations

**Notes:**
- Vision radius is configurable
- Only entities within radius are visible
- Observation results inform future decisions

---

## Scenario 2: Character Movement
**Description:** AI character moves based on AI decision  
**Actors:** AI Character  
**Steps:**
1. Character calls `make_decision(world_state, personality)`
2. AI decides to move (returns `Decision(type=ActionType.MOVE, dx=5, dy=0)`)
3. Character executes movement via `move(dx, dy)`
4. Character position updates in real-time

**Notes:**
- Movement happens continuously in real-time
- Decisions are made periodically (every 3 seconds by default)
- Movement respects screen boundaries

---

## Scenario 3: Character Communication
**Description:** Two AI characters communicate with each other  
**Actors:** AI Character A, AI Character B  
**Steps:**
1. Character A observes Character B within vision radius
2. Character A decides to communicate (returns `Decision(type=ActionType.COMMUNICATE, target="character_b", message="...")`)
3. Character A calls `communication(target, message)`
4. Character B receives the message
5. Character B may decide to respond in next decision cycle

**Notes:**
- Communication requires characters to be within vision radius
- Messages are generated based on personality
- Communication can be one-way or conversational

---

## Scenario 4: Player Movement
**Description:** Player character moves using keyboard input  
**Actors:** Player  
**Steps:**
1. Player presses arrow keys or WASD
2. `PlayerCharacter.handle_input(keys)` processes input
3. Character moves in real-time based on key presses
4. Movement is immediate and continuous

**Notes:**
- Player has direct control (no AI decision needed)
- Movement is smooth and responsive

---

## Scenario 5: Player-AI Communication
**Description:** Player talks to AI character  
**Actors:** Player, AI Character  
**Steps:**
1. Player types a message (TBD: input mechanism)
2. Player character sends message to nearby AI character
3. AI character receives message
4. AI character processes message and may respond
5. Response is displayed to player

**Notes:**
- Need to implement player input mechanism
- AI character responds based on personality and context

---

## Scenario 6: Character Interaction
**Description:** AI character interacts with objects or environment  
**Actors:** AI Character  
**Steps:**
1. Character observes an object within vision radius
2. Character decides to interact (returns `Decision(type=ActionType.INTERACT, target="object_id", interaction_type="pickup")`)
3. Character calls `interact(target, interaction_type)`
4. Interaction affects world state or character state

**Notes:**
- Interaction types TBD (pickup, use, examine, etc.)
- Objects in environment TBD

---

## Scenario 7: Multiple Characters in World
**Description:** Multiple AI characters exist and interact simultaneously  
**Actors:** Multiple AI Characters, Player  
**Steps:**
1. World contains multiple AI characters
2. Each character makes decisions independently
3. Characters can observe each other
4. Characters can communicate with each other
5. Player can interact with any character

**Notes:**
- All characters update in real-time
- Each character has independent decision cycle
- Characters may form relationships over time

---

## Future Scenarios (To Be Implemented)
- Character memory/persistence
- Character relationships
- Environmental objects and interactions
- Database storage of actions
- Local model fine-tuning

