# Sun Tzu Military Campaign Simulator

## Introduction

The Military Campaign Simulator is continually evolving; my future objective is to improve the program by incorporating insights from *Guided by Sun Tzu’s War Tactics* and leveraging artificial intelligence tools.  
This will allow me to explore how classical strategies interact with modern AI-driven decision-making in complex and adaptive military simulations.

## About Sun Tzu

Sun Tzu (also spelled Sun Wu) was an ancient Chinese military strategist. His personal name was Wu, and his style was Ch‘ang-ch‘ing.  
He is traditionally believed to have lived during the 5th century B.C., with some sources placing his active period around 519-476 B.C. or noting his death around 496 B.C.  
He was a native of the Ch‘i State, though some accounts state he was from Wu.  
Sun Tzu is most famous as the author of *The Art of War* (孫子兵法), which is widely considered the first treatise on strategy in the world.  
This work, consisting of 13 chapters, was reportedly composed specifically for Ho Lu, the King of Wu...

## Detailed Python Program Descriptions

### MCS_001.py

This program is an interactive graphical tool that models military campaign outcomes based on Sun Tzu's strategic principles.  
Users can simulate multiple turns of conflict, observing the dynamic evolution of army forces, morale, fatigue, and supply levels.  
The program integrates classical military concepts such as planning, deception, numerical superiority, terrain advantages, and the use of spies.  
A detailed log records key decisions and events, helping users analyze strategic impacts turn by turn.  
The simulation reacts to random environmental factors like weather, terrain types, and enemy behavior to mimic realistic uncertainties.  
Integrated charts visualize the progression of critical variables over time, enhancing comprehension.  
Additionally, users can export results and logs as an Excel report for further analysis.  
The program guides through sound decision-making based on historical strategy while allowing experimentation with different scenarios.  
It provides a balanced mix of complexity and accessibility for enthusiasts of military history and strategic simulations.  
Perfect for learning and exploring the art of war through modern programming.

### MCS_002.py

This program is an advanced military campaign simulator, inspired by the principles of Sun Tzu.  
It models a confrontation between your forces and those of an enemy controlled by adaptive artificial intelligence (AI), in a dynamic environment affected by weather, terrain, fatigue, resources, espionage, and many other strategic factors.

#### General Program Description

- **Comprehensive graphical interface** including a detailed logs area, controls for configuring the simulation (number of turns, distribution of recruitment by unit type), as well as buttons for launching, clearing, saving, loading, and exporting the simulation.
- **Dynamic visualization** of simulation data, with a graph showing the evolution of forces, fatigue, morale, supplies, special actions, and the personality of the enemy AI turn by turn.
- **Complete unit management system** (infantry, cavalry, archers, spies), with their own unique characteristics (attack, defense, speed, special effects).
- **Realistic management of external conditions**: dynamic changes in terrain, weather, and the day/night cycle affect combat capabilities.
- **Advanced mechanics** such as supply line management, fatigue, morale corruption, espionage operations, the impact of local population support, and fortification maintenance.
- **Enemy controlled by adaptive AI**, which modifies its strategy, personality, and army composition to effectively counter the player.

#### Enemy AI (EnhancedEnemyAI) Explanation

This AI is designed to simulate an intelligent and evolving opponent rather than a reactive and static one.

- **Initial Personality**: The enemy starts with a strategic personality randomly chosen from "aggressive," "defensive," or "deceptive," which influences their behavior in combat (frontal attack, avoidance, feints).
- **Combat Memory**: The AI remembers the latest battle results (player victory or defeat), as well as the player's unit distribution during these battles.
- **Personality Adaptation**:
  - If the player wins frequently (more than 70% of recent battles), the AI adopts a more aggressive stance to counter.
  - If the player loses frequently (less than 30% victory), the AI becomes more defensive.
  - Otherwise, it adopts an ambiguous strategy, mixing feints and tricks.
- **Recruitment Counter-Strategy**: The AI observes the player's unit composition (for example, if they recruit a lot of infantry) and adapts its own composition to counter this tendency, for example, by strengthening their archers against heavy infantry.
- **Tactical Behavior**: In combat, the AI adjusts its tactics based on its current personality, choosing to be firm, cautious, or deceptive, with actions such as evasion, feinting, or confident attacks.

### MCS_003.py

The simulator features diverse unit types with unique attributes, an enemy AI that dynamically adapts by learning from recent battles, and considers environmental factors like terrain and weather.  
It uses a battle engine inspired by Sun Tzu’s tactics for realistic combat outcomes.  
The user interface provides detailed logs, dynamic visualizations of key metrics, and controls for game settings and data management.

The enemy AI, implemented as EnhancedEnemyAI, operates with three possible personalities—aggressive, defensive, and deceptive—based on its recent battle performance against the player.  
It remembers the last five battles to adjust its strategy: becoming aggressive if frequently losing, defensive if under heavy pressure, or deceptive otherwise.  
The AI also counters the player's troop composition by recruiting units strategically.  
During battles, it chooses tactics aligned with its personality, such as direct attacks, avoidance, or feints.  
After each engagement, the AI updates its memory, personality, and recruitment strategy, enabling continuous learning and adaptation.

---

#### Conceptual Diagram: Program Structure and Enemy AI Flow

```
+---------------------+        +----------------------------+
|    CampaignState    |        |    EnhancedEnemyAI         |
+---------------------+        +----------------------------+
| - units             |<>------| - personality              |
| - enemy_units       |        | - memory (last 5 battles)  |
| - resources         |        | - last_player_distribution |
| - morale / fatigue  |        |                            |
| - terrain / weather |        +----------------------------+
| - enemy_ai -------->|   decide_personality()
+---------------------+   observe_outcome()
                          suggest_enemy_recruit()
                          adjust_behavior()

+-------------------------+
| CampaignSimulatorGUI    |
+-------------------------+
| - run_simulation()      |-----> Controls battle turns and actions
| - log()                 |       Calls AI decisions and battle resolution
| - resource_management() |
| - update_graph()        |
+-------------------------+
```

---

#### Enemy AI Decision Flow

```
[Start of Turn]
      │
      ▼
Analyze last 5 battle outcomes from memory
      │
      ▼
Calculate player's win rate
      │
      ├───────────────┬────────────────┬───────────────┐
      │ Win rate > 70%│ Win rate < 30% │ Else          │
      │ Aggressive AI │ Defensive AI   │ Deceptive AI  │
      └───────────────┴────────────────┴───────────────┘
      │
      ▼
Observe player troop distribution
      │
      ▼
Decide recruitment to counter main player forces
      │
      ▼
During battle:
 - If Aggressive → frontal attacks
 - If Defensive → avoid combat
 - If Deceptive → feints and ambushes
      │
      ▼
Update memory with outcome of the battle
      │
      ▼
[End of Turn → Next turn]
```



### MCS_004.py

The Sun Tzu campaign simulator with Chess rules strategic AI combines timeless ancient military strategy principles with well-established strategic concepts from chess to create 
a powerful AI decision-making framework for military campaign simulations. Here is a detailed description of how these strategic implementations work:

#### Core Idea
The AI integrates two classic strategic frameworks:

- **Sun Tzu’s Principles:** Emphasize preparation, deception, flexible adaptation, and winning with minimal direct conflict. Concepts include controlling terrain, using deception and psychological advantage, managing morale and resources, and exploiting enemy weaknesses indirectly.
- **Chess Strategy Rules:** Focus on positional advantage, controlling the center, piece mobility, coordination, sacrifices, defense of key units (king safety), and tactical foresight including anticipating opponent moves.

#### How It Works in the Simulator

1. **Strategic Situation Assessment**  
   Each simulation turn, the AI evaluates the current battlefield state: forces’ strength, morale, terrain, weather conditions, time of day, and the recent history of actions.

2. **Chess-Inspired Tactical Recommendations**  
   Based on chess principles, the AI suggests:
   - Concentrating forces in key central or open areas to dominate the battlefield.
   - Exploiting mobility to maneuver quickly for surprise attacks.
   - Prioritizing defense when fatigued or outnumbered by fortifying or retreating.
   - Employing feints or sacrifices to lure the opponent into traps.
   - Coordinated multi-unit attacks for decisive breakthroughs.
   - Ensuring the “king” (headquarters or command) safety, particularly at night or in poor weather.
   - Using deception through misinformation and varied movement.

3. **Sun Tzu Tactical Layer**  
   The AI adds a layer of Sun Tzu tactics by:
   - Applying deception: feigning retreats, spreading misinformation.
   - Maintaining flexibility and adapting to environmental factors.
   - Targeting enemy supply lines to weaken them indirectly.
   - Distracting the enemy to reduce their focus or morale.
   - Allowing strategic retreats to avoid unnecessary losses.
   - Monitoring morale and adjusting behavior from aggressive to defensive or deceptive dynamically.

4. **Integration With Combat and Resource Mechanics**  
   These strategic layers interact with the core mechanics of the battle simulation, including:
   - Calculating power based on unit types, fatigue, special capabilities (like air superiority).
   - Applying fatigue, morale changes, and environmental modifiers (weather, terrain).
   - Managing resources such as recruiting forces, gold, and fortifications.
   - Simulating spy and sabotage operations affecting supplies and morale.

5. **Dynamic AI Personality**  
   The enemy AI personality evolves based on ongoing battles using memory of outcomes. This affects its strategic choices between aggressiveness, defense, or deception, making the combat less predictable and more realistic.

6. **Decision Support Output**  
   At each turn, the AI’s strategic recommendations (chess+Sun Tzu) are output as contextual advice to the player, helping guide recruitment, maneuvers, and tactical choices.

#### Strategic AI Benefits

- **Multi-Layered Thinking**  
   Combines high-level strategic principles with tactical chess-like precision for nuanced decision-making.
- **Adaptiveness**  
   Adapts to changing battlefield conditions and player behavior in real-time.
- **Psychological Warfare**  
   Uses deception and morale management to shape opponent behavior, echoing Sun Tzu’s “winning without fighting.”
- **Resource and Terrain Awareness**  
   Takes into account terrain, weather, fatigue, and resources, reflecting realistic military considerations.



---

#### Conceptual Diagram: Program Structure and Enemy AI Flow

```
+---------------------+        +----------------------------+
|    CampaignState    |        |    EnhancedEnemyAI         |
+---------------------+        +----------------------------+
| - units             |<>------| - personality              |
| - enemy_units       |        | - memory (last 5 battles)  |
| - resources         |        | - last_player_distribution |
| - morale / fatigue  |        |                            |
| - terrain / weather |        +----------------------------+
| - enemy_ai -------->|   decide_personality()
+---------------------+   observe_outcome()
                         suggest_enemy_recruit()
                         adjust_behavior()

+-------------------------+
|    ChessSunTzuAI        |
+-------------------------+
| - chess_principles      |
| - recommend()           |--- Generates strategic recommendations based on:
|                         |    forces, morale, terrain, weather, time, history
+-------------------------+

+------------------------------------------+
| CampaignSimulatorGUI                     |
+------------------------------------------+
| - run_simulation()                       |-----> Controls battle turns and simulation loop
| - log()                                  |       Invokes AI recommendations and battle resolution
| - resource_management()                  |       Updates state based on actions, events
| - update_graph()                         |       Displays forces, morale, AI evolution trends
| - display_chess_suntzu_recommendations() |
+------------------------------------------+

```

---

#### Enemy AI Decision Flow

```
+----------------------------+
| EnhancedEnemyAI            |
+----------------------------+
| 1) observe_outcome()       |
| 2) decide_personality()    |--- Personality: {aggressive, defensive, deceptive}
| 3) suggest_enemy_recruit() |    |                        
| 4) adjust_behavior() ------+----+-----> Behavior decisions:
+----------------------------+         - aggressive: confident attack
                                      - defensive: avoid/direct engagement
                                      - deceptive: feints, misdirection

```


#### Conclusion
This fusion of classical military wisdom and chess strategy into an AI module models complex, human-like strategic behavior for campaign simulation. 
It provides rich, evolving advice and responsive enemy tactics that deepen gameplay and simulate the art of war in a modern computational form.
This approach reflects modern trends where AI-driven strategic planning aligns timeless wisdom with algorithmic rigor to deliver sophisticated decision-support systems.


### MCS_005.py

Todo list: The next program is under construction to add additional artificial intelligence. I invite you to follow my progress.


