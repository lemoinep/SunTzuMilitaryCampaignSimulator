# Sun Tzu Military Campaign Simulator

## Introduction

The Military Campaign Simulator is continually evolving; my future objective is to improve the program by incorporating insights from 'Guided by Sun Tzu’s War Tactics' 
and leveraging artificial intelligence tools. This will allow me to explore how classical strategies interact with modern AI-driven decision-making in complex and adaptive military simulations.

## About Saun Tzu

Sun Tzu (also spelled Sun Wu) was an ancient Chinese military strategist. His personal name was Wu, and his style was Ch‘ang-ch‘ing. 
He is traditionally believed to have lived during the 5th century B.C., with some sources placing his active period around 519-476 B.C. or noting his death around 496 B.C.. 
He was a native of the Ch‘i State, though some accounts state he was from Wu.
Sun Tzu is most famous as the author of The Art of War (孫子兵法), which is widely considered the first treatise on strategy in the world. 
This work, consisting of 13 chapters, was reportedly composed specifically for Ho Lu, the King of Wu...


## Detailed Python Program Descriptions

### MCS_001.py

This programm is an interactive graphical tool that models military campaign outcomes based on Sun Tzu's strategic principles. 
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

This programm is an advanced military campaign simulator, inspired by the principles of Sun Tzu. It models a confrontation between your forces and those of an enemy controlled by adaptive artificial intelligence (AI), in a dynamic environment affected by weather, terrain, fatigue, resources, espionage, and many other strategic factors.

#### General Program Description

- **Comprehensive graphical interface** including a detailed logs area, controls for configuring the simulation (number of turns, distribution of recruitment by unit type), as well as buttons for launching, clearing, saving, loading, and exporting the simulation.
- **Dynamic visualization** of simulation data, with a graph showing the evolution of forces, fatigue, morale, supplies, special actions, and the personality of the enemy AI turn by turn. - **Complete unit management system** (infantry, cavalry, archers, spies), with their own unique characteristics (attack, defense, speed, special effects).
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
It uses a battle engine inspired by Sun Tzu’s tactics for realistic combat outcomes. The user interface provides detailed logs, dynamic visualizations of key metrics, 
and controls for game settings and data management.

The enemy AI, implemented as EnhancedEnemyAI, operates with three possible personalities—aggressive, defensive, and deceptive—based on its recent battle performance against the player. 
It remembers the last five battles to adjust its strategy: becoming aggressive if frequently losing, defensive if under heavy pressure, or deceptive otherwise.
The AI also counters the player's troop composition by recruiting units strategically. During battles, it chooses tactics aligned with its personality, such as direct attacks, 
avoidance, or feints. After each engagement, the AI updates its memory, personality, and recruitment strategy, enabling continuous learning and adaptation.

#### Conceptual Diagram: Program Structure and Enemy AI Flow
 
+---------------------+ +----------------------------+
| CampaignState | | EnhancedEnemyAI |
+---------------------+ +----------------------------+
| - units |<>------| - personality |
| - enemy_units | | - memory (last 5 battles) |
| - resources | | - last_player_distribution |
| - morale / fatigue | | |
| - terrain / weather | +----------------------------+
| - enemy_ai -------->| decide_personality()
+---------------------+ observe_outcome()
suggest_enemy_recruit()
adjust_behavior()

+------------------------+
| CampaignSimulatorGUI |
+------------------------+
| - run_simulation() |-----> Controls battle turns and actions
| - log() | Calls AI decisions and battle resolution
| - resource_management() |
| - update_graph() |
+------------------------+

#### Enemy AI Decision Flow

[Start of Turn]
│
▼
Analyze last 5 battle outcomes from memory
│
▼
Calculate player's win rate
│
├───────────────┬────────────────┬───────────────┐
│ Win rate > 70%│ Win rate < 30% │ Else │
│ Aggressive AI │ Defensive AI │ Deceptive AI │
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

    If Aggressive → frontal attacks

    If Defensive → avoid combat

    If Deceptive → feints and ambushes
    │
    ▼
    Update memory with outcome of the battle
    │
    ▼
    [End of Turn → Next turn]





