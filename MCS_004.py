# Author(s): Dr. Patrick Lemoine
# Sun Tzu campaign simulator with Chess rules strategic AI

import random
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import openpyxl
import json
import numpy as np

class UnitType:
    def __init__(self, name, count, attack, defense, speed, special=None):
        self.name = name
        self.count = count
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.special = special or {}

class EnhancedEnemyAI:
    def __init__(self, personality, memory_len=5):
        self.personality = personality    # 'aggressive', 'defensive', 'deceptive'
        self.memory_len = memory_len
        self.memory = []
        self.last_player_distribution = [0.7, 0.15, 0.1, 0.05, 0, 0, 0]
    def observe_outcome(self, player_win, player_dist):
        self.memory.append({'player_win': player_win, 'player_dist': player_dist})
        if len(self.memory) > self.memory_len:
            self.memory.pop(0)
        self.last_player_distribution = player_dist
    def decide_personality(self):
        n = len(self.memory)
        if n < self.memory_len:
            return
        wins = [m['player_win'] for m in self.memory]
        win_rate = sum(wins) / n
        if win_rate > 0.7:
            self.personality = "aggressive"
        elif win_rate < 0.3:
            self.personality = "defensive"
        else:
            self.personality = "deceptive"
    def suggest_enemy_recruit(self):
        p = self.last_player_distribution
        max_index = p.index(max(p))
        weights = list(p)
        # Anti-counter strategy
        if max_index == 0:
            weights = [p[0]*0.7, p[1]+0.1, p[2]+0.2, p[3], p[4], p[5], p[6]]
        elif max_index == 1:
            weights = [p+0.1, p[1]*0.7, p[2], p[3]+0.2, p[4], p[5], p[6]]
        elif max_index == 2:
            weights = [p+0.2, p[1], p[2]*0.7, p[3]+0.1, p[4], p[5], p[6]]
        else:
            weights = p
        norm = sum(weights)
        if norm == 0:
            return [0.7, 0.15, 0.1, 0.05, 0, 0, 0]
        return [round(x/norm, 2) for x in weights]
    def adjust_behavior(self, player_forces, enemy_forces, morale):
        self.decide_personality()
        return {
            "confidence": self.personality == "aggressive",
            "avoid": self.personality == "defensive",
            "feint": self.personality == "deceptive" or random.random() < 0.1
        }

class ChessSunTzuAI:
    """AI module combining Chess strategy and Sun Tzu principles"""
    def __init__(self):
        self.chess_principles = [
            "control_center", "mobility", "king_safety", "create_threats",
            "coordinate_all_units", "anticipate_counter", "defend_weakness",
            "sacrifice_for_advantage", "deception"
        ]
    def recommend(self, player_forces, enemy_forces, morale, terrain, weather, time, last_actions):
        recommendations = []
        # Control the center - position advantage
        if terrain in ["accessible", "open"] and player_forces > enemy_forces:
            recommendations.append("Concentrate your forces in central or open areas to dominate the battlefield and control the terrain.")
        # Mobility and surprise attack
        if weather not in ["stormy", "foggy"] and morale > 0.6:
            recommendations.append("Use mobility to maneuver swiftly and surprise the enemy where they are weakest.")
        # Defense if fatigued or outnumbered
        if morale < 0.4 or player_forces < enemy_forces:
            recommendations.append("Protect vulnerable units, avoid direct confrontation, fortify positions, or prepare a strategic retreat.")
        # Feint and sacrifice
        if random.random() < 0.2 or (morale > 0.5 and terrain == "contentious"):
            recommendations.append("Feign a retreat or sacrifice a small force to lure the enemy into a trap and shift the balance of power.")
        # Coordinated threats
        if player_forces > enemy_forces and random.random() < 0.5:
            recommendations.append("Launch coordinated attacks on enemy weaknesses, focusing units for a decisive breakthrough.")
        # King safety
        if time == "night" or weather == "foggy":
            recommendations.append("Ensure the safety of your headquarters/command, and avoid surprise attacks at night or in poor weather.")
        # Deception and adaptation
        if random.random() < 0.3:
            recommendations.append("Employ misinformation, concealment, and varied movement to confuse the opponent.")
        return recommendations

class CampaignState:
    def __init__(self):
        self.init_state()
    def init_state(self, infantry=3000, mech_infantry=1500, tank=500, artillery=300,
                   missiles=100, aircraft=200, spies=100,
                   enemy_inf=2800, enemy_mech=1400, enemy_tank=450, enemy_artillery=320,
                   enemy_missiles=90, enemy_aircraft=180, enemy_spy=90,
                   leadership=0.85, personality=None):
        self.units = {
            "infantry": UnitType("Infantry", infantry, 6, 5, 4),
            "mechanized_infantry": UnitType("Mechanized Infantry", mech_infantry, 8, 6, 6),
            "tank": UnitType("Tank", tank, 15, 12, 5),
            "artillery": UnitType("Artillery", artillery, 10, 3, 2, {"indirect_fire": True}),
            "missiles": UnitType("Missiles", missiles, 20, 1, 8, {"long_range": True}),
            "aircraft": UnitType("Aircraft", aircraft, 18, 7, 12, {"air_superiority": True}),
            "spies": UnitType("Spies", spies, 0, 1, 6, {"espionage": 9}),
        }
        self.enemy_units = {
            "infantry": UnitType("Infantry", enemy_inf, 6, 5, 4),
            "mechanized_infantry": UnitType("Mechanized Infantry", enemy_mech, 8, 6, 6),
            "tank": UnitType("Tank", enemy_tank, 15, 12, 5),
            "artillery": UnitType("Artillery", enemy_artillery, 10, 3, 2, {"indirect_fire": True}),
            "missiles": UnitType("Missiles", enemy_missiles, 20, 1, 8, {"long_range": True}),
            "aircraft": UnitType("Aircraft", enemy_aircraft, 18, 7, 12, {"air_superiority": True}),
            "spies": UnitType("Spies", enemy_spy, 0, 1, 6, {"espionage": 8}),
        }
        self.leadership_quality = leadership
        self.resources = {"gold": 2000, "recruit_points": 300, "fortification": 0}
        self.enemy_ai = EnhancedEnemyAI(personality or random.choice(["aggressive", "defensive", "deceptive"]))
        self.terrain_types = ["accessible", "entangling", "temporizing", "contentious", "hemmed-in", "desperate", "difficult", "open", "urban", "mountain", "forest"]
        self.weather_conditions = ["clear", "rainy", "foggy", "windy", "stormy"]
        self.day_night_cycle = ["day", "night"]
        self.fatigue = 0.0
        self.supply = 1.0
        self.morale = 0.7
        self.enemy_morale = 0.6
        self.spy_effectiveness = 0.0
        self.current_terrain = random.choice(self.terrain_types)
        self.current_weather = random.choice(self.weather_conditions)
        self.current_time = random.choice(self.day_night_cycle)
        self.enemy_units_total = self.calculate_total_forces(self.enemy_units)
    def calculate_total_forces(self, units_dict):
        return sum(unit.count for unit in units_dict.values())

class CampaignSimulatorGUI:
    LOG_COLORS = {
        'info': 'black', 'victory': 'blue', 'defeat': 'red', 'recruitment': 'green',
        'sabotage': 'orange', 'spy': 'purple', 'event': 'brown'
    }
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Military Campaign Simulator - Sun Tzu & Chess AI")
        self.fullscreen = False
        self.state = CampaignState()
        self.log_text = ScrolledText(root, state='disabled', width=120, height=22, wrap='word')
        self.log_text.pack(padx=10, pady=5)
        self.fig = Figure(figsize=(12, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Forces / Morale / Fatigue / Supply / Actions / AI Evolution")
        self.ax.set_xlabel("Turns")
        self.ax.set_ylabel("Values")
        self.ax.set_ylim(0, 1.2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(padx=10, pady=5)
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)
        tk.Label(control_frame, text="Number of Turns:").grid(row=0, column=0, padx=5)
        self.turns_var = tk.IntVar(value=10)
        self.turns_entry = tk.Entry(control_frame, width=5, textvariable=self.turns_var)
        self.turns_entry.grid(row=0, column=1)
        tk.Label(control_frame, text="Recruitment % - Inf/MechIn/Tank/Artillery/Missiles/Aircraft/Spy (e.g. 40/20/10/10/10/5/5):").grid(row=1, column=0, padx=5)
        self.recruit_dist_var = tk.StringVar(value="40/20/10/10/10/5/5")
        self.recruit_dist_entry = tk.Entry(control_frame, width=20, textvariable=self.recruit_dist_var)
        self.recruit_dist_entry.grid(row=1, column=1)
        self.run_button = tk.Button(control_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=0, column=2, padx=5)
        self.clear_button = tk.Button(control_frame, text="Clear Logs and Graphs", command=self.clear_logs_graph)
        self.clear_button.grid(row=0, column=3, padx=5)
        self.export_button = tk.Button(control_frame, text="Export Excel Report", command=self.export_excel, state='disabled')
        self.export_button.grid(row=0, column=4, padx=5)
        self.save_button = tk.Button(control_frame, text="Save", command=self.save_campaign)
        self.save_button.grid(row=1, column=2, padx=5)
        self.load_button = tk.Button(control_frame, text="Load", command=self.load_campaign)
        self.load_button.grid(row=1, column=3, padx=5)
        self.full_button = tk.Button(control_frame, text="Full Screen", command=self.toggle_fullscreen)
        self.full_button.grid(row=1, column=4, padx=5)
        self.logs = []
        self.sim_data = []
        self.init_advanced_parameters()
        self.chess_ia = ChessSunTzuAI()  # Chess & Sun Tzu AI

    def log(self, message, event_type="info"):
        self.logs.append(message)
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n", event_type)
        self.log_text.tag_config(event_type, foreground=self.LOG_COLORS.get(event_type, 'black'))
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
        self.root.update_idletasks()

    def clear_logs_graph(self):
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state='disabled')
        self.logs.clear()
        self.sim_data.clear()
        self.ax.clear()
        self.ax.set_title("Forces / Morale / Fatigue / Supply / Actions / AI Evolution")
        self.ax.set_xlabel("Turns")
        self.ax.set_ylabel("Values")
        self.ax.set_ylim(0, 1.2)
        self.canvas.draw()
        self.export_button.config(state='disabled')
        self.log("Logs and graphs cleared.", event_type="event")

    def export_excel(self):
        if not self.sim_data:
            messagebox.showwarning("No Data", "No data available for export.")
            return
        filename = f"campaign_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Campaign Simulation"
        headers = ["Turn", "Total Forces", "Enemy Total Forces", "Morale", "Enemy Morale",
                   "Fatigue", "Supply", "Resources Gold", "Recruit Points", "Fortifications", "Terrain",
                   "Weather", "Time", "Key Actions", "Special Actions", "Enemy AI Personality"]
        ws.append(headers)
        for record in self.sim_data:
            ws.append([
                record["turn"], record["forces_total"], record["enemy_forces_total"],
                round(record["morale"], 2), round(record["enemy_morale"], 2),
                round(record["fatigue"], 2), round(record["supply"], 2),
                record["resources"]["gold"], record["resources"]["recruit_points"],
                record["resources"]["fortification"], record["terrain"],
                record["weather"], record["time"],
                "; ".join(record["actions"]),
                record.get("special_actions", 0),
                record.get("enemy_ai", "unknown")
            ])
        wb.save(filename)
        self.log(f"Excel report exported to: {filename}", event_type="event")
        messagebox.showinfo("Export Complete", f"Report saved as:\n{filename}")

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)

    def save_campaign(self):
        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if file:
            data = {
                "sim_data": self.sim_data,
                "state": {
                    "resources": self.state.resources,
                    "units": {k: v.count for k, v in self.state.units.items()},
                    "enemy_units": {k: v.count for k, v in self.state.enemy_units.items()},
                    "morale": self.state.morale,
                    "enemy_morale": self.state.enemy_morale,
                    "fatigue": self.state.fatigue,
                    "supply": self.state.supply,
                    "leadership_quality": self.state.leadership_quality,
                    "enemy_ai": self.state.enemy_ai.personality,
                    "current_terrain": self.state.current_terrain,
                    "current_weather": self.state.current_weather,
                    "current_time": self.state.current_time,
                }
            }
            with open(file, "w") as f:
                json.dump(data, f)
            self.log(f"Campaign saved ({file})", event_type="event")

    def load_campaign(self):
        file = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if file:
            with open(file, "r") as f:
                data = json.load(f)
            self.sim_data = data["sim_data"]
            loaded = data["state"]
            self.state.resources = loaded["resources"]
            for k, c in loaded["units"].items():
                self.state.units[k].count = c
            for k, c in loaded["enemy_units"].items():
                self.state.enemy_units[k].count = c
            self.state.morale = loaded["morale"]
            self.state.enemy_morale = loaded["enemy_morale"]
            self.state.fatigue = loaded["fatigue"]
            self.state.supply = loaded["supply"]
            self.state.leadership_quality = loaded["leadership_quality"]
            self.state.enemy_ai.personality = loaded["enemy_ai"]
            self.state.current_terrain = loaded["current_terrain"]
            self.state.current_weather = loaded["current_weather"]
            self.state.current_time = loaded["current_time"]
            self.update_graph()
            self.log("Campaign loaded successfully.", event_type="event")

    def init_advanced_parameters(self):
        self.state.init_state()

    def display_chess_suntzu_recommendations(self):
        recs = self.chess_ia.recommend(
            self.calculate_total_forces(self.state.units),
            self.calculate_total_forces(self.state.enemy_units),
            self.state.morale,
            self.state.current_terrain,
            self.state.current_weather,
            self.state.current_time,
            self.logs[-5:] if len(self.logs) >= 5 else self.logs
        )
        for r in recs:
            self.log("AI Recommendation: " + r, event_type="event")

    
    def update_graph(self):
        turns = [d["turn"] for d in self.sim_data]
        forces = [d["forces_total"] / 30000 for d in self.sim_data]  # Normalize max likely force size
        enemy = [d["enemy_forces_total"] / 30000 for d in self.sim_data]
        morale = [d["morale"] for d in self.sim_data]
        fatigue = [d["fatigue"] for d in self.sim_data]
        supply = [d["supply"] for d in self.sim_data]
        actions_count = [d.get("special_actions", 0) for d in self.sim_data]
        personality_map = {"aggressive":1.0, "deceptive":0.5, "defensive":0.0}
        ia_vals = [personality_map.get(d.get("enemy_ai","deceptive"), 0.5) for d in self.sim_data]
        unit_names = ["infantry", "mechanized_infantry", "tank", "artillery", "missiles", "aircraft", "spies"]
        player_compo = []
        for d in self.sim_data:
            total_f = d["forces_total"] if d["forces_total"] > 0 else 1
            compo = []
            for un in unit_names:
                val = self.state.units[un].count / total_f if total_f > 0 else 0
                compo.append(val)
            player_compo.append(compo)
        player_compo = np.array(player_compo).T
        self.ax.clear()
        self.ax.plot(turns, forces, label='Your Forces (Normalized)', color='blue')
        self.ax.plot(turns, enemy, label='Enemy Forces (Normalized)', color='red')
        self.ax.plot(turns, morale, label='Morale', color='darkgreen')
        self.ax.plot(turns, fatigue, label='Fatigue', color='brown')
        self.ax.plot(turns, supply, label='Supply', color='orange')
        self.ax.plot(turns, actions_count, label='Special Actions', color='purple')
        self.ax.plot(turns, ia_vals, 'm--', label='Enemy AI Personality (1=Agg,0.5=Dec,0=Def)')
        bottom = np.zeros(len(turns))
        colors = ['#559966', '#9763a6', '#e6d44a', '#ffa500', '#4a90e2', '#c04adb', '#555555']
        labels = ['Infantry', 'Mechanized Infantry', 'Tanks', 'Artillery', 'Missiles', 'Aircraft', 'Spies']
        for idx, (un, color, label) in enumerate(zip(unit_names, colors, labels)):
            self.ax.fill_between(turns, bottom, bottom + player_compo[idx], color=color, alpha=0.3, step="pre", label=label)
            bottom += player_compo[idx]
        self.ax.set_title("Forces / Morale / Fatigue / Supply / Actions / AI Evolution")
        self.ax.set_xlabel("Turns")
        self.ax.set_ylabel("Normalized Values")
        self.ax.set_ylim(0, 1.2)
        self.ax.legend(loc='upper right')
        self.canvas.draw()


    
    def resolve_battle(self):
        player_power = 0
        enemy_power = 0
        for ut in self.state.units.values():
            power = ut.attack * ut.count * (1 - self.state.fatigue * 0.5)
            if ut.special.get("air_superiority"):
                power *= 1.2
            player_power += power
        for eut in self.state.enemy_units.values():
            power = eut.attack * eut.count * (1 - self.state.fatigue * 0.5)
            if eut.special.get("air_superiority"):
                power *= 1.2
            enemy_power += power
        # Terrain effect reduces effectiveness of mechanized and tank forces in difficult terrain
        if self.state.current_terrain in ["difficult", "entangling", "hemmed-in"]:
            for ut in ["mechanized_infantry", "tank", "artillery"]:
                if ut in self.state.units:
                    player_power -= self.state.units[ut].attack * self.state.units[ut].count * 0.3
                if ut in self.state.enemy_units:
                    enemy_power -= self.state.enemy_units[ut].attack * self.state.enemy_units[ut].count * 0.3
        return max(0, int(player_power)), max(0, int(enemy_power))


    
    def sun_tzu_advanced_tactics(self, turn, enemy_morale, enemy_forces, player_forces):
        actions = []
        if enemy_morale > 0.7 and turn % 3 == 0:
            actions.append("Distract enemy before battle to reduce focus.")
            enemy_morale -= 0.1
        if player_forces > enemy_forces * 1.2 and enemy_morale < 0.4:
            actions.append("Allow enemy a retreat route to avoid desperate combat.")
            enemy_morale += 0.05
        if enemy_forces > player_forces and turn % 4 == 0:
            actions.append("Target enemy supply lines to weaken them.")
            enemy_forces -= int(enemy_forces * 0.05)
        if enemy_forces > player_forces and enemy_morale > 0.5 and turn % 5 == 0:
            actions.append("Feign a retreat to lure enemy into an ambush.")
            if random.random() > 0.5:
                actions.append("Ambush successful! Enemy suffers heavy losses.")
                enemy_forces -= int(enemy_forces * 0.1)
            else:
                actions.append("Ambush failed, troops confused.")
        return actions, max(0, min(enemy_morale, 1)), max(0, enemy_forces)

    
    
    
    def supply_line_event(self):
        event_message = None
        enemy_spy_effectiveness = self.state.enemy_units["spies"].count / 2000
        disruption_chance = 0.1 + enemy_spy_effectiveness
        if random.random() < disruption_chance and self.state.supply < 0.6:
            fatigue_penalty = random.uniform(0.1, 0.2)
            self.state.fatigue += fatigue_penalty
            self.state.fatigue = min(self.state.fatigue, 1.0)
            event_message = f"Supply line disrupted! Fatigue increased by {fatigue_penalty:.2f}."
        return event_message
    
    def calculate_morale(self):
        leadership_bonus = (self.state.leadership_quality - 0.5) * 0.3
        spy_bonus = (self.state.spy_effectiveness - 0.5) * 0.2
        weather_penalty = -0.1 if self.state.current_weather in ["stormy", "foggy"] else 0
        morale = self.state.morale - self.state.fatigue * 0.5 + (self.state.supply - 0.5) * 0.4 + leadership_bonus + spy_bonus + weather_penalty
        return max(0, min(morale, 1))

    def enemy_decision(self, player_forces_total, enemy_forces_total, morale):
        return self.state.enemy_ai.adjust_behavior(player_forces_total, enemy_forces_total, morale)

    def environment_effects(self):
        effects = []
        if self.state.current_time == "night":
            effects.append("Combat effectiveness reduced due to night time.")
            self.state.fatigue += 0.05
        if self.state.current_weather == "rainy":
            effects.append("Rain reduces artillery and aircraft effectiveness.")
            if "artillery" in self.state.units:
                self.state.units["artillery"].count = max(0, self.state.units["artillery"].count - 20)
            if "artillery" in self.state.enemy_units:
                self.state.enemy_units["artillery"].count = max(0, self.state.enemy_units["artillery"].count - 15)
            if "aircraft" in self.state.units:
                self.state.units["aircraft"].count = max(0, self.state.units["aircraft"].count - 30)
            if "aircraft" in self.state.enemy_units:
                self.state.enemy_units["aircraft"].count = max(0, self.state.enemy_units["aircraft"].count - 25)
        if self.state.current_weather == "windy":
            effects.append("Wind affects projectile weapons unpredictably.")
        return effects

    def resource_management(self, recruit_dist):
        recruit_gain = int(self.state.resources["recruit_points"] * 0.1)
        gold_spent = int(recruit_gain * 5)  # Modern units cost more gold
        recruit_types = ["infantry", "mechanized_infantry", "tank", "artillery", "missiles", "aircraft", "spies"]
        if self.state.resources["gold"] >= gold_spent and recruit_gain > 0:
            self.state.resources["gold"] -= gold_spent
            for i, typ in enumerate(recruit_types):
                rcount = int(recruit_gain * recruit_dist[i] / 100)
                self.state.units[typ].count += rcount
                if rcount > 0:
                    self.log(f"Recruited {rcount} {typ.replace('_', ' ')}.", event_type="recruitment")
        else:
            self.log("Not enough gold to recruit new troops.", event_type="defeat")
        if self.state.resources["fortification"] > 0:
            fort_maintenance_cost = 50
            if self.state.resources["gold"] >= fort_maintenance_cost:
                self.state.resources["gold"] -= fort_maintenance_cost
                self.state.fatigue = max(0, self.state.fatigue - 0.05)
                self.log("Fortifications maintained, reducing fatigue.", event_type="event")
            else:
                self.state.fatigue += 0.05
                self.log("Failed to maintain fortifications, fatigue increases.", event_type="defeat")

    def advanced_spy_operations(self):
        actions = []
        if self.state.units["spies"].count > 0:
            sabotage_chance = 0.2 * (self.state.units["spies"].count / 100)
            if random.random() < sabotage_chance:
                supply_damage = random.uniform(0.05, 0.15)
                self.state.supply = max(0, self.state.supply - supply_damage)
                actions.append("Spies sabotaged enemy supply lines successfully.")
                self.state.enemy_morale = max(0, self.state.enemy_morale - 0.05)
            misinformation_chance = 0.25 * (self.state.units["spies"].count / 100)
            if random.random() < misinformation_chance:
                actions.append("Spies spread misinformation, confusing enemy command.")
                self.state.enemy_morale = max(0, self.state.enemy_morale - 0.07)
        else:
            actions.append("No spies available for operations.")
        self.state.spy_effectiveness = min(1.0, self.state.units["spies"].count / 150)
        return actions

    def battle_aftermath(self, player_losses, enemy_losses):
        pop_support_change = (enemy_losses - player_losses) / 10000
        self.state.resources["recruit_points"] += int(pop_support_change * 50)
        self.state.resources["recruit_points"] = max(50, self.state.resources["recruit_points"])
        if pop_support_change > 0:
            self.log("Local population support increased! Recruit points grew.", event_type="victory")
        else:
            self.log("Population fearful of losses, recruit points declined.", event_type="defeat")
        if self.state.fatigue > 0.8:
            self.log("High fatigue causing political unrest! Reduced resource gains.", event_type="defeat")
            self.state.resources["gold"] = max(0, self.state.resources["gold"] - 100)

    def update_enemy_ai(self, player_losses, enemy_losses):
        player_win = player_losses < enemy_losses
        recruit_dist = [self.state.units[t].count for t in ["infantry","mechanized_infantry","tank","artillery","missiles","aircraft","spies"]]
        total = sum(recruit_dist)
        player_dist = [x / total if total > 0 else 0 for x in recruit_dist]
        self.state.enemy_ai.observe_outcome(player_win, player_dist)
        self.log(f"Enemy AI shifts to {self.state.enemy_ai.personality} strategy based on battle outcomes.", event_type="spy")

    def calculate_total_forces(self, units_dict):
        return sum(u.count for u in units_dict.values())

    def apply_losses(self, units, losses):
        total = self.calculate_total_forces(units)
        if total == 0 or losses == 0:
            return
        loss_ratio = min(1, losses / total)
        for ut in units.values():
            lost = int(ut.count * loss_ratio)
            ut.count = max(0, ut.count - lost)
            
    def environment_effects(self):
        effects = []
        if self.state.current_time == "night":
            effects.append("Combat effectiveness reduced due to night time.")
            self.state.fatigue += 0.05
        if self.state.current_weather == "rainy":
            effects.append("Rain reduces artillery and aircraft effectiveness.")
            if "artillery" in self.state.units:
                self.state.units["artillery"].count = max(0, self.state.units["artillery"].count - 20)
            if "artillery" in self.state.enemy_units:
                self.state.enemy_units["artillery"].count = max(0, self.state.enemy_units["artillery"].count - 15)
            if "aircraft" in self.state.units:
                self.state.units["aircraft"].count = max(0, self.state.units["aircraft"].count - 30)
            if "aircraft" in self.state.enemy_units:
                self.state.enemy_units["aircraft"].count = max(0, self.state.enemy_units["aircraft"].count - 25)
        if self.state.current_weather == "windy":
            effects.append("Wind affects projectile weapons unpredictably.")
        return effects


    # Only run_simulation() is updated to include the Sun Tzu Chess AI:

    def run_simulation(self):
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state='disabled')
        self.logs.clear()
        self.sim_data.clear()
        self.export_button.config(state='disabled')
        self.init_advanced_parameters()
        try:
            turns = int(self.turns_var.get())
            if turns <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid number of turns, please enter a positive integer.")
            return
        recruit_dist = self.parse_recruit_dist(self.recruit_dist_var.get())
        self.log(f"=== Starting Modern Military Campaign Simulation (Enemy AI: {self.state.enemy_ai.personality}) ===", event_type="info")
        for turn in range(1, turns + 1):
            self.log(f"\n--- Turn {turn} ---", event_type="info")
            if turn % 3 == 0:
                self.state.current_weather = random.choice(self.state.weather_conditions)
            if turn % 2 == 0:
                self.state.current_time = "day" if self.state.current_time == "night" else "night"
            if random.random() < 0.1:
                self.state.current_terrain = random.choice(self.state.terrain_types)
            env_effects = self.environment_effects()
            for e in env_effects:
                self.log(e, event_type="event")
            supply_event = self.supply_line_event()
            if supply_event:
                self.log(supply_event, event_type="sabotage")
            advanced_actions, self.state.enemy_morale, new_enemy_forces = self.sun_tzu_advanced_tactics(
                turn, self.state.enemy_morale, self.calculate_total_forces(self.state.enemy_units),
                self.calculate_total_forces(self.state.units)
            )
            self.state.enemy_units_total = new_enemy_forces
            for aa in advanced_actions:
                self.log(aa, event_type="event")
            spy_actions = self.advanced_spy_operations()
            for sa in spy_actions:
                self.log(sa, event_type="spy")
            self.resource_management(recruit_dist)
            self.state.morale = self.calculate_morale()
            player_power, enemy_power = self.resolve_battle()
            enemy_behavior = self.enemy_decision(player_power, enemy_power, self.state.enemy_morale)
            if enemy_behavior["avoid"]:
                self.log("Enemy chooses to avoid direct confrontation.", event_type="event")
                enemy_power *= 0.8
            if enemy_behavior["feint"]:
                self.log("Enemy performs feints and misdirection.", event_type="spy")
                player_power *= 0.9
            if player_power > enemy_power:
                enemy_losses = int((player_power - enemy_power) * 0.1)
                player_losses = int(enemy_power * 0.05)
                self.log(f"Your army inflicted {enemy_losses} losses to the enemy.", event_type="victory")
                self.log(f"Your army suffered {player_losses} losses.", event_type="defeat")
            else:
                player_losses = int((enemy_power - player_power) * 0.1)
                enemy_losses = int(player_power * 0.05)
                self.log(f"Your army suffered {player_losses} losses.", event_type="defeat")
                self.log(f"Enemy suffered {enemy_losses} losses.", event_type="victory")
            self.apply_losses(self.state.units, player_losses)
            self.apply_losses(self.state.enemy_units, enemy_losses)
            fatigue_gain = 0.05 + player_losses / 30000
            self.state.fatigue = min(1, self.state.fatigue + fatigue_gain)
            supply_consumption = 0.1 + fatigue_gain * 0.5
            self.state.supply = max(0, self.state.supply - supply_consumption)
            self.battle_aftermath(player_losses, enemy_losses)
            self.update_enemy_ai(player_losses, enemy_losses)
            self.display_chess_suntzu_recommendations()  # <<<<< Chess/Sun Tzu AI invoked here!
            self.log(f"End of turn {turn}:", event_type="info")
            self.log(f"  Your unit counts: Infantry={self.state.units['infantry'].count}, Mechanized Infantry={self.state.units['mechanized_infantry'].count}, Tanks={self.state.units['tank'].count}, Artillery={self.state.units['artillery'].count}, Missiles={self.state.units['missiles'].count}, Aircraft={self.state.units['aircraft'].count}, Spies={self.state.units['spies'].count}", event_type="info")
            self.log(f"  Enemy unit counts: Infantry={self.state.enemy_units['infantry'].count}, Mechanized Infantry={self.state.enemy_units['mechanized_infantry'].count}, Tanks={self.state.enemy_units['tank'].count}, Artillery={self.state.enemy_units['artillery'].count}, Missiles={self.state.enemy_units['missiles'].count}, Aircraft={self.state.enemy_units['aircraft'].count}, Spies={self.state.enemy_units['spies'].count}", event_type="info")
            self.log(f"  Morale: You={self.state.morale:.2f}, Enemy={self.state.enemy_morale:.2f}", event_type="info")
            self.log(f"  Fatigue: {self.state.fatigue:.2f}, Supply level: {self.state.supply:.2f}", event_type="info")
            self.log(f"  Resources: Gold={self.state.resources['gold']}, Recruit Points={self.state.resources['recruit_points']}, Fortifications={self.state.resources['fortification']}", event_type="info")
            self.log(f"  Terrain: {self.state.current_terrain}, Weather: {self.state.current_weather}, Time: {self.state.current_time}", event_type="info")
            self.sim_data.append({
                "turn": turn,
                "forces_total": self.calculate_total_forces(self.state.units),
                "enemy_forces_total": self.calculate_total_forces(self.state.enemy_units),
                "morale": self.state.morale,
                "enemy_morale": self.state.enemy_morale,
                "fatigue": self.state.fatigue,
                "supply": self.state.supply,
                "resources": self.state.resources.copy(),
                "terrain": self.state.current_terrain,
                "weather": self.state.current_weather,
                "time": self.state.current_time,
                "actions": advanced_actions + spy_actions,
                "special_actions": len(advanced_actions + spy_actions),
                "enemy_ai": self.state.enemy_ai.personality
            })
            self.update_graph()
            if self.calculate_total_forces(self.state.units) == 0:
                self.log("Your army has been destroyed! Campaign lost.", event_type="defeat")
                break
            if self.calculate_total_forces(self.state.enemy_units) == 0:
                self.log("Enemy army defeated! Campaign won!", event_type="victory")
                break
        self.log("\n=== Simulation Ended ===", event_type="event")
        player_forces_left = self.calculate_total_forces(self.state.units)
        enemy_forces_left = self.calculate_total_forces(self.state.enemy_units)
        self.log(f"Final forces - You: {player_forces_left}, Enemy: {enemy_forces_left}", event_type="info")
        if player_forces_left > enemy_forces_left:
            self.log("Campaign successful! Congratulations!", event_type="victory")
        else:
            self.log("Campaign lost or suspended.", event_type="defeat")
        self.export_button.config(state='normal')

    def parse_recruit_dist(self, dist):
        try:
            result = [int(x) for x in dist.strip().split('/')]
        except:
            result = [40,20,10,10,10,5,5]
        total = sum(result)
        if total != 100 and total > 0:
            ratio = [x*100//total for x in result]
            return ratio + [0]*(7 - len(ratio))
        return result + [0]*(7 - len(result))


if __name__ == "__main__":
    root = tk.Tk()
    app = CampaignSimulatorGUI(root)
    root.mainloop()
