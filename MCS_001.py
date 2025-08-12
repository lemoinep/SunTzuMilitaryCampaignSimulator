# Author(s): Dr. Patrick Lemoine
# Sun Tzu Military Campaign Simulator

import random
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import openpyxl

class CampaignSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Military Campaign Simulation")

        # Scrollable text area for logs
        self.log_text = ScrolledText(root, state='disabled', width=100, height=20, wrap='word')
        self.log_text.pack(padx=10, pady=5)

        # Plot area
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Forces / Morale / Fatigue / Supply Evolution")
        self.ax.set_xlabel("Turns")
        self.ax.set_ylabel("Values")
        self.ax.set_ylim(0, 1.2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(padx=10, pady=5)

        # Controls: number of turns, run, clear, export
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)

        tk.Label(control_frame, text="Number of Turns:").grid(row=0, column=0, padx=5)
        self.turns_var = tk.IntVar(value=7)
        self.turns_entry = tk.Entry(control_frame, width=5, textvariable=self.turns_var)
        self.turns_entry.grid(row=0, column=1)

        self.run_button = tk.Button(control_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.grid(row=0, column=2, padx=5)

        self.clear_button = tk.Button(control_frame, text="Clear Logs and Graphs", command=self.clear_logs_graph)
        self.clear_button.grid(row=0, column=3, padx=5)

        self.export_button = tk.Button(control_frame, text="Export Excel Report", command=self.export_excel, state='disabled')
        self.export_button.grid(row=0, column=4, padx=5)

        self.logs = []  # Log messages list
        self.sim_data = []  # Simulation data per turn
    
    def log(self, message):
        """Append a message to the log area."""
        self.logs.append(message)
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
        self.root.update()
    
    def clear_logs_graph(self):
        """Clear log messages and reset the graph."""
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
        """Export the simulation data to an Excel file."""
        if not self.sim_data:
            messagebox.showwarning("No Data", "No data available for export.")
            return
        filename = f"campaign_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Campaign Simulation"

        headers = ["Turn", "Forces", "Enemy Forces", "Morale", "Fatigue", "Supply", "Key Actions"]
        ws.append(headers)

        for record in self.sim_data:
            ws.append([
                record["turn"],
                record["forces"],
                record["enemy_forces"],
                round(record["morale"], 2),
                round(record["fatigue"], 2),
                round(record["supply"], 2),
                "; ".join(record["actions"])
            ])

        wb.save(filename)
        self.log(f"\nExcel report exported to: {filename}")
        messagebox.showinfo("Export Complete", f"Report saved as:\n{filename}")

    # The following methods implement the thematic sections based on your original logic:
    def general_planning_preparation(self, factors, military_elements):
        self.log("\n--- I. General Planning & Preparation ---")
        def evaluate_factors(factors_dict):
            return all(factors_dict.values())

        victory_fundamentals = evaluate_factors(factors)
        victory_military = evaluate_factors(military_elements)

        if victory_fundamentals and victory_military:
            self.log("Predict victory → Keep general")
            return True, ["Victory predicted, general retained"]
        else:
            self.log("Predict defeat → Dismiss general")
            return False, ["Defeat predicted, general dismissed"]

    def strategic_engagement_deception(self, enemy_force_superior, enemy_confident, enemy_angry):
        self.log("\n--- II. Strategic Engagement & Deception ---")
        actions = []
        if enemy_confident:
            actions.append("Prepare defense (enemy confident).")
        if enemy_force_superior:
            actions.append("Avoid frontal combat (enemy stronger).")
        if enemy_angry:
            actions.append("Provoke angry enemy by feigning weakness.")
        if not actions:
            actions.append("Execute feints and mixed tactics.")
        for a in actions:
            self.log(a)
        return actions

    def numerical_superiority_response(self, force_ratio):
        self.log("\n--- III. Numerical Superiority & Response ---")
        if force_ratio >= 10:
            action = "Encircle enemy."
        elif force_ratio >= 5:
            action = "Attack."
        elif force_ratio >= 2:
            action = "Split army: attack + diversion."
        elif force_ratio == 1:
            action = "Offer battle."
        elif 0.8 <= force_ratio < 1:
            action = "Avoid enemy."
        elif force_ratio < 0.8:
            action = "Flee."
        else:
            action = "Concentrate forces and request reinforcements."
        self.log(action)
        return [action]

    def generals_authority_soldier_morale(self, sovereign_interfering, army_restless, general_competent, general_faults):
        self.log("\n--- IV. General's Authority & Soldier Morale ---")
        notes = []
        if sovereign_interfering:
            notes.append("Sovereign interfering harms army.")
        if army_restless:
            notes.append("Army restless.")
        if general_competent and not sovereign_interfering:
            notes.append("Victory assured with competent general.")
        if general_faults:
            notes.append("Beware fatal general faults.")
        for n in notes:
            self.log(n)
        if not notes:
            self.log("Stable and favorable conditions.")
            notes.append("Stable and favorable conditions.")
        return notes

    def terrain_types_actions(self, terrain):
        self.log("\n--- V. Terrain Types & Actions ---")
        terrain_actions = {
            "accessible": "Occupy heights before enemy, protect supply.",
            "entangling": "Exit if enemy caught off guard.",
            "temporizing": "Do not camp, feign retreat.",
            "narrow passes": "Occupy positions, avoid enemy pursuit.",
            "distant positions": "Disadvantageous combat.",
            "dispersive": "Do not fight, unity of heart.",
            "easy": "No camp, maintain communication.",
            "contentious": "Attack if first possession, defend actively, use tricks.",
            "open": "Ally, maintain goodwill of neighbors.",
            "serious": "Ensure continuous supply.",
            "difficult": "No camping, rapid movement.",
            "hemmed-in": "Use stratagems, block exits, force fight to death.",
            "desperate": "Fight without hesitation, show desperation.",
            "salt marshes": "Quick passage near water.",
            "flat dry land": "Good position, danger ahead, safety behind.",
            "night battle": "Use fire and drum signals.",
            "day battle": "Use flags and banners."
        }
        act = terrain_actions.get(terrain.lower(), "Unknown terrain or no specific action.")
        self.log(f"Terrain '{terrain}': {act}")
        return [act]

    def attack_by_fire(self, prepared, favorable_season, favorable_wind):
        self.log("\n--- VI. Attack by Fire ---")
        if not prepared:
            self.log("Equipment not ready → no fire attack.")
            return False, ["No fire attack (equipment not ready)"]
        if not favorable_season or not favorable_wind:
            self.log("Unfavorable weather → wait.")
            return False, ["No attack, unfavorable weather conditions"]
        self.log("Fire attack executed: burning camp, supplies, arsenals, etc.")
        return True, ["Fire attack executed"]

    def use_of_spies(self, spying_budget_ok, enemy_info_available, spy_classes):
        self.log("\n--- VII. Use of Spies ---")
        if not spying_budget_ok:
            self.log("Insufficient espionage budget, army blind.")
            return False, ["Insufficient espionage"]
        if not enemy_info_available:
            self.log("Insufficient enemy info, seek better intelligence.")
            return False, ["Insufficient enemy intelligence"]
        self.log(f"Spies employed: {', '.join(spy_classes)}")
        return True, [f"Spies: {', '.join(spy_classes)}"]

    def update_graph(self):
        turns = [d["turn"] for d in self.sim_data]
        forces = [d["forces"]/10000 for d in self.sim_data]  # Normalized for plot
        enemy = [d["enemy_forces"]/10000 for d in self.sim_data]
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
        # Reset logs and data
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        self.logs.clear()
        self.sim_data.clear()
        self.export_button.config(state='disabled')

        try:
            turns = int(self.turns_var.get())
            if turns <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid number of turns, enter a positive integer.")
            return

        self.log("=== Starting Advanced Military Campaign Simulation ===")

        # Initial states
        morale = 0.7
        forces = 10000
        fatigue = 0.0
        supply = 1.0
        enemy_forces = 9500
        terrain = random.choice([
            "accessible", "entangling", "temporizing", "contentious",
            "hemmed-in", "desperate", "difficult", "open"
        ])
        spy_budget = True
        enemy_info = True
        spy_classes = ["Local", "Internal", "Converted"]
        general_competent = True
        sovereign_interfering = False

        for turn in range(1, turns + 1):
            self.log(f"\n--- Turn {turn} ---")

            heaven = random.choice([True, False])
            fatigue += random.uniform(0.05, 0.15)
            fatigue = min(fatigue, 1.0)

            if supply < 0.5:
                fatigue += 0.1
            morale_effective = morale - fatigue * 0.5 + (supply - 0.5) * 0.3
            morale_effective = max(0, min(morale_effective, 1))

            factors = {
                "Moral Influence": morale_effective > 0.5,
                "Heaven": heaven,
                "Earth": True,
                "Command": general_competent,
                "Method & Discipline": morale_effective > 0.6
            }
            military = {
                "Stronger Army": forces > enemy_forces,
                "Trained Officers & Soldiers": True,
                "Constant Reward and Punishment": morale_effective > 0.5
            }
            victory_prev, actions_I = self.general_planning_preparation(factors, military)

            enemy_confident = random.choice([True, False])
            enemy_angry = random.choice([True, False])
            enemy_force_superior = enemy_forces > forces

            actions_II = self.strategic_engagement_deception(enemy_force_superior, enemy_confident, enemy_angry)

            force_ratio = forces / enemy_forces if enemy_forces > 0 else float('inf')
            actions_III = self.numerical_superiority_response(force_ratio)

            general_faults = random.choice([True, False])
            notes_IV = self.generals_authority_soldier_morale(sovereign_interfering, fatigue > 0.6, general_competent, general_faults)

            actions_V = self.terrain_types_actions(terrain)

            prepared = supply > 0.4 and fatigue < 0.7
            season_favorable = heaven
            wind_favorable = random.choice([True, False])
            attack_fire_done, actions_VI = self.attack_by_fire(prepared, season_favorable, wind_favorable)

            spying_done, actions_VII = self.use_of_spies(spy_budget, enemy_info, spy_classes)

            # Logistics: supply consumption and fatigue effect
            supply_expense = random.uniform(0.07, 0.15) + fatigue * 0.05
            supply -= supply_expense
            supply = max(0, min(supply, 1))

            # Simulate losses and morale changes
            if victory_prev and not enemy_force_superior:
                enemy_losses = random.randint(300, 700)
                enemy_forces = max(0, enemy_forces - enemy_losses)
                morale_gain = 0.05 + (supply - 0.5) * 0.1
                morale = min(1, morale + max(0, morale_gain - fatigue * 0.2))
                self.log(f"Your army inflicted {enemy_losses} losses on the enemy.")
                self.log(f"Morale rises to {morale:.2f}.")
            else:
                losses = random.randint(400, 900)
                forces = max(0, forces - losses)
                morale_loss = 0.1 + fatigue * 0.2
                morale = max(0, morale - morale_loss)
                self.log(f"Your army suffers {losses} losses, morale drops to {morale:.2f}.")

            self.log(f"End of turn {turn} state: Forces={forces}, Enemy={enemy_forces}, Morale={morale:.2f}, Fatigue={fatigue:.2f}, Supply={supply:.2f}")

            # Save turn data
            all_actions = actions_I + actions_II + actions_III + notes_IV + actions_V + actions_VI + actions_VII
            self.sim_data.append({
                "turn": turn,
                "forces": forces,
                "enemy_forces": enemy_forces,
                "morale": morale,
                "fatigue": fatigue,
                "supply": supply,
                "actions": all_actions
            })

            self.update_graph()

            if forces == 0:
                self.log("Army destroyed, campaign ended.")
                break
            if enemy_forces == 0:
                self.log("Enemy defeated, campaign ended.")
                break

        self.log("\n=== Simulation Ended ===")
        self.log(f"Final state: Forces={forces}, Enemy={enemy_forces}, Morale={morale:.2f}, Fatigue={fatigue:.2f}, Supply={supply:.2f}")
        if forces > enemy_forces:
            self.log("Campaign successful! Congratulations!")
        else:
            self.log("Campaign lost or suspended.")
        
        self.export_button.config(state='normal')


if __name__ == "__main__":
    root = tk.Tk()
    app = CampaignSimulatorGUI(root)
    root.mainloop()
