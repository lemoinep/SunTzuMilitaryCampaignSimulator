# Author(s): Dr. Patrick Lemoine
# Sun Tzu Military Campaign Simulator

import random
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import openpyxl



# Data classes for Units and Enemy AI Types
class UnitType:
    def __init__(self, name, count, attack, defense, speed, special=None):
        self.name = name
        self.count = count
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.special = special or {}  # Dict for special effects like 'espionage'


class EnemyAI:
    def __init__(self, personality):
        self.personality = personality  # aggressive, defensive, deceptive

    def adjust_behavior(self, player_forces, enemy_forces, morale):
        # Modify enemy confidence & tactics based on personality
        if self.personality == "aggressive":
            return {"confidence": True, "avoid": False, "feint": random.choice([True, False])}
        elif self.personality == "defensive":
            avoid = enemy_forces < player_forces
            return {"confidence": False, "avoid": avoid, "feint": False}
        else:  # deceptive
            return {"confidence": random.choice([True, False]),
                    "avoid": random.choice([True, False]),
                    "feint": True}



class CampaignSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Military Campaign Simulator - Guided by Sun Tzu's War Tactics")

        # Logging area
        self.log_text = ScrolledText(root, state='disabled', width=100, height=20, wrap='word')
        self.log_text.pack(padx=10, pady=5)

        # Plot setup
        self.fig = Figure(figsize=(9, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Forces / Morale / Fatigue / Supply Evolution")
        self.ax.set_xlabel("Turns")
        self.ax.set_ylabel("Values")
        self.ax.set_ylim(0, 1.2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(padx=10, pady=5)

        # Control panel
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)

        tk.Label(control_frame, text="Number of Turns:").grid(row=0, column=0, padx=5)
        self.turns_var = tk.IntVar(value=10)
        self.turns_entry = tk.Entry(control_frame, width=5, textvariable=self.turns_var)
        self.turns_entry.grid(row=0, column=1)

        self.run_button = tk.Button(control_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=0, column=2, padx=5)

        self.clear_button = tk.Button(control_frame, text="Clear Logs and Graphs", command=self.clear_logs_graph)
        self.clear_button.grid(row=0, column=3, padx=5)

        self.export_button = tk.Button(control_frame, text="Export Excel Report", command=self.export_excel, state='disabled')
        self.export_button.grid(row=0, column=4, padx=5)

        # Simulation data
        self.logs = []
        self.sim_data = []

        # Initialize advanced simulation parameters
        self.init_advanced_parameters()

    def init_advanced_parameters(self):
        # Unit types with attributes
        self.units = {
            "infantry": UnitType("Infantry", 5000, attack=5, defense=5, speed=3),
            "cavalry": UnitType("Cavalry", 3000, attack=8, defense=4, speed=7),
            "archers": UnitType("Archers", 2000, attack=6, defense=3, speed=4),
            "spies": UnitType("Spies", 100, attack=0, defense=1, speed=6, special={"espionage": 9})
        }
        self.enemy_units = {
            "infantry": UnitType("Infantry", 4800, attack=5, defense=5, speed=3),
            "cavalry": UnitType("Cavalry", 2800, attack=8, defense=4, speed=7),
            "archers": UnitType("Archers", 2200, attack=6, defense=3, speed=4),
            "spies": UnitType("Spies", 90, attack=0, defense=1, speed=6, special={"espionage": 8})
        }

        # Leadership quality (0 to 1)
        self.leadership_quality = 0.85

        # Campaign resources
        self.resources = {"gold": 1000, "recruit_points": 150, "fortification": 0}

        # Enemy AI personality
        self.enemy_ai = EnemyAI(random.choice(["aggressive", "defensive", "deceptive"]))

        # Terrain and weather states
        self.terrain_types = ["accessible", "entangling", "temporizing", "contentious",
                            "hemmed-in", "desperate", "difficult", "open", "salt marshes", "flat dry land"]
        self.weather_conditions = ["clear", "rainy", "foggy", "windy", "stormy"]
        self.day_night_cycle = ["day", "night"]

        # Campaign phases
        self.campaign_phase = 1

        # Other game state
        self.fatigue = 0.0
        self.supply = 1.0
        self.morale = 0.7  # base morale
        self.enemy_morale = 0.6
        self.spy_effectiveness = 0.0  # Will affect morale/supply disruption etc.

        self.current_terrain = random.choice(self.terrain_types)
        self.current_weather = random.choice(self.weather_conditions)
        self.current_time = random.choice(self.day_night_cycle)

    def log(self, message):
        self.logs.append(message)
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
        self.root.update()

    def clear_logs_graph(self):
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        self.logs.clear()
        self.sim_data.clear()
        self.ax.clear()
        self.ax.set_title("Forces / Morale / Fatigue / Supply Evolution")
        self.ax.set_xlabel("Turns")
        self.ax.set_ylabel("Values")
        self.ax.set_ylim(0, 1.2)
        self.canvas.draw()
        self.export_button.config(state='disabled')
        self.log("Logs and graphs cleared.\n")

    def export_excel(self):
        if not self.sim_data:
            messagebox.showwarning("No Data", "No data available for export.")
            return
        filename = f"campaign_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Campaign Simulation"

        headers = ["Turn", "Forces Total", "Enemy Forces Total", "Morale", "Enemy Morale",
                   "Fatigue", "Supply", "Resources Gold", "Recruit Points", "Fortification", "Terrain",
                   "Weather", "Time", "Key Actions"]
        ws.append(headers)

        for record in self.sim_data:
            ws.append([
                record["turn"],
                record["forces_total"],
                record["enemy_forces_total"],
                round(record["morale"], 2),
                round(record["enemy_morale"], 2),
                round(record["fatigue"], 2),
                round(record["supply"], 2),
                record["resources"]["gold"],
                record["resources"]["recruit_points"],
                record["resources"]["fortification"],
                record["terrain"],
                record["weather"],
                record["time"],
                "; ".join(record["actions"])
            ])

        wb.save(filename)
        self.log(f"\nExcel report exported to: {filename}")
        messagebox.showinfo("Export Complete", f"Report saved as:\n{filename}")

    # Concept 1: Advanced Sun Tzu Tactics
    def sun_tzu_advanced_tactics(self, turn, enemy_morale, enemy_forces, player_forces):
        actions = []
        # Distract or taunt enemy
        if enemy_morale > 0.7 and turn % 3 == 0:
            actions.append("Distract enemy before battle to reduce focus.")
            enemy_morale -= 0.1  # effect
        # Give enemy route to retreat if advantage is strong
        if player_forces > enemy_forces * 1.2 and enemy_morale < 0.4:
            actions.append("Allow enemy a retreat route to avoid desperate combat.")
            enemy_morale += 0.05  # slight boost to enemy morale to encourage retreat
        # Target enemy resources
        if enemy_forces > player_forces and turn % 4 == 0:
            actions.append("Target enemy supply lines to weaken them.")
            enemy_forces -= int(enemy_forces * 0.05)  # reduce enemy forces indirectly
        # False retreat to lure enemy
        if enemy_forces > player_forces and enemy_morale > 0.5 and turn % 5 == 0:
            actions.append("Feign a retreat to lure enemy into an ambush.")
            # Simulate ambush success chance
            if random.random() > 0.5:
                actions.append("Ambush successful! Enemy suffers heavy losses.")
                enemy_forces -= int(enemy_forces * 0.1)
            else:
                actions.append("Ambush failed, troops confused.")
        return actions, max(0, min(enemy_morale, 1)), max(0, enemy_forces)

    # Concept 2: Battle resolution by Unit Types
    def resolve_battle(self):
        # Calculate total attack and defense for player and enemy
        player_power = 0
        enemy_power = 0

        for ut in self.units.values():
            player_power += ut.attack * ut.count * (1 - self.fatigue * 0.5)
        for eut in self.enemy_units.values():
            enemy_power += eut.attack * eut.count * (1 - self.fatigue * 0.5)

        # Add morale effect (amplifies attack)
        player_power *= (1 + self.morale * 0.3)
        enemy_power *= (1 + self.enemy_morale * 0.3)

        # Terrain effect example: "difficult" terrain reduces cavalry and archers effectiveness
        if self.current_terrain in ["difficult", "entangling", "hemmed-in"]:
            # Reduce cavalry and archers attack by 30% for both sides
            for ut in ["cavalry", "archers"]:
                if ut in self.units:
                    player_power -= self.units[ut].attack * self.units[ut].count * 0.3
                if ut in self.enemy_units:
                    enemy_power -= self.enemy_units[ut].attack * self.enemy_units[ut].count * 0.3

        return max(0, int(player_power)), max(0, int(enemy_power))

    # Concept 3: Supply line vulnerabilities & random disruption
    def supply_line_event(self):
        event_message = None
        # 10% chance supply line disrupted if enemy spies present and supply low
        enemy_spy_effectiveness = self.enemy_units["spies"].count / 2000  # scaled factor
        disruption_chance = 0.1 + enemy_spy_effectiveness
        if random.random() < disruption_chance and self.supply < 0.6:
            fatigue_penalty = random.uniform(0.1, 0.2)
            self.fatigue += fatigue_penalty
            self.fatigue = min(self.fatigue, 1.0)
            event_message = f"Supply line disrupted! Fatigue increased by {fatigue_penalty:.2f}."
        return event_message

    # Concept 4: Dynamic Morale calculation with leadership and spy influence
    def calculate_morale(self):
        leadership_bonus = (self.leadership_quality - 0.5) * 0.3
        spy_bonus = (self.spy_effectiveness - 0.5) * 0.2
        weather_penalty = -0.1 if self.current_weather in ["stormy", "foggy"] else 0
        # Overall morale formula
        morale = self.morale - self.fatigue * 0.5 + (self.supply - 0.5) * 0.4 + leadership_bonus + spy_bonus + weather_penalty
        return max(0, min(morale, 1))

    # Concept 5: Enemy AI adapts behavior
    def enemy_decision(self, player_forces_total, enemy_forces_total, morale):
        behavior = self.enemy_ai.adjust_behavior(player_forces_total, enemy_forces_total, morale)
        return behavior

    # Concept 6: Update environment effects on combat
    def environment_effects(self):
        effects = []
        # Night reduces hit chance for both sides
        if self.current_time == "night":
            effects.append("Combat effectiveness reduced due to night time.")
            self.fatigue += 0.05
        if self.current_weather == "rainy":
            effects.append("Rain reduces archer effectiveness.")
            # Reduce archers count (representing inefficiency)
            self.units["archers"].count = max(0, self.units["archers"].count - 50)
            self.enemy_units["archers"].count = max(0, self.enemy_units["archers"].count - 60)
        if self.current_weather == "windy":
            effects.append("Wind affects projectile weapons unpredictably.")
            # Random impact on archers attack strength could be added
        return effects

    # Concept 7: Multi-phase campaign resource management
    def resource_management(self):
        # Spend resources each turn for recruitment and fortification maintenance
        recruit_gain = int(self.resources["recruit_points"] * 0.1)
        gold_spent = int(recruit_gain * 2)
        if self.resources["gold"] >= gold_spent:
            self.resources["gold"] -= gold_spent
            # Recruit infantry by default
            self.units["infantry"].count += recruit_gain
            self.log(f"Recruited {recruit_gain} infantry using {gold_spent} gold.")
        else:
            self.log("Not enough gold to recruit new troops.")

        # Fortification maintenance
        if self.resources["fortification"] > 0:
            fort_maintenance_cost = 20
            if self.resources["gold"] >= fort_maintenance_cost:
                self.resources["gold"] -= fort_maintenance_cost
                self.fatigue = max(0, self.fatigue - 0.05)
                self.log("Fortifications maintained, reducing fatigue.")
            else:
                self.fatigue += 0.05
                self.log("Failed to maintain fortifications, fatigue increases.")

    # Concept 8: Spy operations expansion
    def advanced_spy_operations(self):
        actions = []
        if self.units["spies"].count > 0:
            # Chance to sabotage enemy supply or lower morale
            sabotage_chance = 0.2 * (self.units["spies"].count / 100)
            if random.random() < sabotage_chance:
                supply_damage = random.uniform(0.05, 0.15)
                self.enemy_supply = max(0, self.supply - supply_damage)  # enemy supply affected
                actions.append("Spies sabotaged enemy supply lines successfully.")
                # Also reduce enemy morale
                self.enemy_morale = max(0, self.enemy_morale - 0.05)
            # Chance to spread misinformation
            misinformation_chance = 0.25 * (self.units["spies"].count / 100)
            if random.random() < misinformation_chance:
                actions.append("Spies spread misinformation, confusing enemy command.")
                # Enemy morale penalty
                self.enemy_morale = max(0, self.enemy_morale - 0.07)
        else:
            actions.append("No spies available for operations.")
        # Calculate spy effectiveness (scaled)
        self.spy_effectiveness = min(1.0, self.units["spies"].count / 150)
        return actions

    # Concept 9: Battle aftermath effects
    def battle_aftermath(self, player_losses, enemy_losses):
        # Local population support adjust
        pop_support_change = (enemy_losses - player_losses) / 10000
        # Modify recruit_points based on support
        self.resources["recruit_points"] += int(pop_support_change * 50)
        self.resources["recruit_points"] = max(50, self.resources["recruit_points"])
        if pop_support_change > 0:
            self.log("Local population support increased! Recruit points grew.")
        else:
            self.log("Population fearful of losses, recruit points declined.")

        # Political stability example (simple fatigue effect)
        if self.fatigue > 0.8:
            self.log("High fatigue causing political unrest! Reduced resource gains.")
            self.resources["gold"] = max(0, self.resources["gold"] - 50)

    # Concept 10: Basic Learning AI (enemy adapts to player's loss ratios)
    def update_enemy_ai(self, player_losses, enemy_losses):
        # Simple heuristic: if player losing more, enemy shifts to aggressive
        if player_losses > enemy_losses:
            self.enemy_ai.personality = "aggressive"
        elif player_losses < enemy_losses:
            self.enemy_ai.personality = "defensive"
        else:
            self.enemy_ai.personality = "deceptive"
        self.log(f"Enemy AI adjusts strategy to {self.enemy_ai.personality} based on battle outcomes.")

    def calculate_total_forces(self, units_dict):
        return sum(u.count for u in units_dict.values())

    def update_graph(self):
        turns = [d["turn"] for d in self.sim_data]
        forces = [d["forces_total"] / 20000 for d in self.sim_data]  # normalized
        enemy = [d["enemy_forces_total"] / 20000 for d in self.sim_data]
        morale = [d["morale"] for d in self.sim_data]
        fatigue = [d["fatigue"] for d in self.sim_data]
        supply = [d["supply"] for d in self.sim_data]

        self.ax.clear()
        self.ax.plot(turns, forces, label='Your Forces (Normalized)')
        self.ax.plot(turns, enemy, label='Enemy Forces (Normalized)')
        self.ax.plot(turns, morale, label='Morale')
        self.ax.plot(turns, fatigue, label='Fatigue')
        self.ax.plot(turns, supply, label='Supply')
        self.ax.set_title("Forces / Morale / Fatigue / Supply Evolution")
        self.ax.set_xlabel("Turns")
        self.ax.set_ylabel("Values")
        self.ax.set_ylim(0, 1.2)
        self.ax.legend()
        self.canvas.draw()

    def run_simulation(self):
        # Reset
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        self.logs.clear()
        self.sim_data.clear()
        self.export_button.config(state='disabled')

        self.init_advanced_parameters()  # Reset parameters for fresh start

        try:
            turns = int(self.turns_var.get())
            if turns <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid number of turns, enter a positive integer.")
            return

        self.log(f"=== Starting Advanced Military Campaign Simulation (Enemy AI: {self.enemy_ai.personality}) ===")
        for turn in range(1, turns + 1):
            self.log(f"\n--- Turn {turn} ---")

            # Cycle environment states dynamically every turn (simulate day/night, weather)
            if turn % 3 == 0:
                self.current_weather = random.choice(self.weather_conditions)
            if turn % 2 == 0:
                self.current_time = "day" if self.current_time == "night" else "night"
            # Random terrain change with low chance
            if random.random() < 0.1:
                self.current_terrain = random.choice(self.terrain_types)

            # Environment effects
            env_effects = self.environment_effects()
            for e in env_effects:
                self.log(e)

            # Supply line events
            supply_event = self.supply_line_event()
            if supply_event:
                self.log(supply_event)

            # Advanced Sun Tzu tactics
            advanced_actions, self.enemy_morale, new_enemy_forces = self.sun_tzu_advanced_tactics(
                turn, self.enemy_morale, self.calculate_total_forces(self.enemy_units),
                self.calculate_total_forces(self.units)
            )
            self.enemy_units_total = new_enemy_forces
            for aa in advanced_actions:
                self.log(aa)

            # Spy operations
            spy_actions = self.advanced_spy_operations()
            for sa in spy_actions:
                self.log(sa)

            # Resource management
            self.resource_management()

            # Calculate morale with leadership and spy effects
            self.morale = self.calculate_morale()

            # Resolve battle
            player_power, enemy_power = self.resolve_battle()

            # Enemy decision & behavior
            enemy_behavior = self.enemy_decision(player_power, enemy_power, self.enemy_morale)

            # Incorporate enemy AI behavior to influence battle result
            if enemy_behavior["avoid"]:
                self.log("Enemy chooses to avoid direct confrontation.")
                enemy_power *= 0.8
            if enemy_behavior["feint"]:
                self.log("Enemy performs feints and misdirection.")
                player_power *= 0.9

            # Calculate losses proportional to relative power
            if player_power > enemy_power:
                enemy_losses = int((player_power - enemy_power) * 0.1)
                player_losses = int(enemy_power * 0.05)
                self.log(f"Your army inflicted {enemy_losses} losses to the enemy.")
                self.log(f"Your army suffered {player_losses} losses.")
            else:
                player_losses = int((enemy_power - player_power) * 0.1)
                enemy_losses = int(player_power * 0.05)
                self.log(f"Your army suffered {player_losses} losses.")
                self.log(f"Enemy suffered {enemy_losses} losses.")

            # Apply losses to units proportionally
            def apply_losses(units, losses):
                total = self.calculate_total_forces(units)
                if total == 0:
                    return
                loss_ratio = losses / total
                for ut in units.values():
                    lost = int(ut.count * loss_ratio)
                    ut.count = max(0, ut.count - lost)

            apply_losses(self.units, player_losses)
            apply_losses(self.enemy_units, enemy_losses)

            # Update fatigue and supply for repeated exertion
            fatigue_gain = 0.05 + player_losses / 20000
            self.fatigue = min(1, self.fatigue + fatigue_gain)
            supply_consumption = 0.1 + fatigue_gain * 0.5
            self.supply = max(0, self.supply - supply_consumption)

            # Update battle aftermath effects
            self.battle_aftermath(player_losses, enemy_losses)

            # Update Enemy AI behavior based on battle results
            self.update_enemy_ai(player_losses, enemy_losses)

            # End of turn status log
            self.log(f"End of turn {turn}:")
            self.log(f"  Your force counts: Infantry={self.units['infantry'].count}, Cavalry={self.units['cavalry'].count}, Archers={self.units['archers'].count}, Spies={self.units['spies'].count}")
            self.log(f"  Enemy force counts: Infantry={self.enemy_units['infantry'].count}, Cavalry={self.enemy_units['cavalry'].count}, Archers={self.enemy_units['archers'].count}, Spies={self.enemy_units['spies'].count}")
            self.log(f"  Morale: You={self.morale:.2f}, Enemy={self.enemy_morale:.2f}")
            self.log(f"  Fatigue: {self.fatigue:.2f}, Supply level: {self.supply:.2f}")
            self.log(f"  Resources: Gold={self.resources['gold']}, Recruit Points={self.resources['recruit_points']}, Fortifications={self.resources['fortification']}")
            self.log(f"  Terrain: {self.current_terrain}, Weather: {self.current_weather}, Time: {self.current_time}")

            # Save data for plotting and export
            self.sim_data.append({
                "turn": turn,
                "forces_total": self.calculate_total_forces(self.units),
                "enemy_forces_total": self.calculate_total_forces(self.enemy_units),
                "morale": self.morale,
                "enemy_morale": self.enemy_morale,
                "fatigue": self.fatigue,
                "supply": self.supply,
                "resources": self.resources.copy(),
                "terrain": self.current_terrain,
                "weather": self.current_weather,
                "time": self.current_time,
                "actions": advanced_actions + spy_actions
            })

            self.update_graph()

            # Check win/loss conditions
            if self.calculate_total_forces(self.units) == 0:
                self.log("Your army has been destroyed! Campaign lost.")
                break
            if self.calculate_total_forces(self.enemy_units) == 0:
                self.log("Enemy army defeated! Campaign won!")
                break

        # End of simulation summary
        self.log("\n=== Simulation Ended ===")
        player_forces_left = self.calculate_total_forces(self.units)
        enemy_forces_left = self.calculate_total_forces(self.enemy_units)
        self.log(f"Final forces - You: {player_forces_left}, Enemy: {enemy_forces_left}")
        if player_forces_left > enemy_forces_left:
            self.log("Campaign successful! Congratulations!")
        else:
            self.log("Campaign lost or suspended.")

        self.export_button.config(state='normal')


if __name__ == "__main__":
    root = tk.Tk()
    app = CampaignSimulatorGUI(root)
    root.mainloop()
