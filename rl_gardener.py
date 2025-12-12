"""
RL GARDENER - A Tanuló Kertész
Q-Learning alapú adaptív szabályozás
"""
import numpy as np
import random
import matplotlib.pyplot as plt
from fluid_stratos import FluidSTRATOS

class RLGardener:
    def __init__(self, actions=None, alpha=0.1, gamma=0.9, epsilon=0.1):
        if actions is None:
            self.actions = ["WAIT", "RAISE_BARRIER", "LOWER_BARRIER", "DEEPEN_CHANNEL"]
        else:
            self.actions = actions
            
        self.q_table = {} # State -> {Action -> Value}
        self.alpha = alpha   # Learning rate
        self.gamma = gamma   # Discount factor
        self.epsilon = epsilon # Exploration rate
        
        # State discretization parameters
        self.energy_bins = [0.1, 0.2, 0.3, 0.4]
        self.viscosity_bins = [0.3, 0.7] # Low, Med, High
        
    def get_state(self, brain_energy, viscosity):
        """Diszkretizálja az állapotot"""
        e_state = np.digitize(brain_energy, self.energy_bins)
        v_state = np.digitize(viscosity, self.viscosity_bins)
        return (e_state, v_state)
    
    def get_q(self, state, action):
        return self.q_table.get(state, {}).get(action, 0.0)
    
    def choose_action(self, state):
        """Epsilon-Greedy választás"""
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        
        # Best action
        q_values = {a: self.get_q(state, a) for a in self.actions}
        # Random break ties
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]
        return random.choice(best_actions)
    
    def learn(self, state, action, reward, next_state):
        """Q-Table frissítése"""
        current_q = self.get_q(state, action)
        
        # Max Q for next state
        next_q_values = {a: self.get_q(next_state, a) for a in self.actions}
        max_next_q = max(next_q_values.values()) if next_q_values else 0.0
        
        # Q-Learning formula
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = new_q

def train_gardener(episodes=50, steps_per_episode=50):
    print(f"🤖 Kertész Tanítása ({episodes} epizód)...")
    
    gardener = RLGardener()
    rewards_history = []
    
    for ep in range(episodes):
        # Reset Env
        stratos = FluidSTRATOS(grid_size=(64, 64))
        
        # Random kezdeti viszkozitás (környezeti tényező)
        viscosity = random.random()
        stratos.set_viscosity(viscosity)
        
        # Kezdeti állapot
        barrier_strength = 0.5
        stratos.set_barrier((0,0), strength=barrier_strength, width=2.0, barrier_id="brain_shield")
        
        total_reward = 0
        
        # Kezdeti mérés
        e_brain, _ = stratos.get_state_metrics()
        state = gardener.get_state(e_brain, viscosity)
        
        for t in range(steps_per_episode):
            # 1. Action
            action = gardener.choose_action(state)
            
            # Apply Action
            if action == "RAISE_BARRIER":
                barrier_strength += 0.2
            elif action == "LOWER_BARRIER":
                barrier_strength -= 0.2
            elif action == "DEEPEN_CHANNEL":
                stratos.add_coupling("Intuition", "Logic", strength=2.0)
            elif action == "WAIT":
                pass
                
            # Clamp limits
            barrier_strength = np.clip(barrier_strength, 0.0, 2.5)
            stratos.set_barrier((0,0), strength=barrier_strength, width=2.0, barrier_id="brain_shield")
            
            # 2. Evolve
            stratos.evolve(steps=10) # 10 fizikai lépés egy döntés között
            
            # 3. Observe new state
            e_brain_new, entropy = stratos.get_state_metrics()
            next_state = gardener.get_state(e_brain_new, viscosity)
            
            # 4. Calculate Reward
            # Cél: Brain energia legyen 0.2 és 0.3 között
            if 0.2 <= e_brain_new <= 0.3:
                r = 1.0
            elif 0.15 <= e_brain_new <= 0.35:
                r = 0.1
            else:
                r = -1.0
                
            # Entrópia bónusz (ha nem túl kaotikus, de aktív)
            if entropy > 1.5:
                r += 0.2
            
            # 5. Learn
            gardener.learn(state, action, r, next_state)
            
            state = next_state
            total_reward += r
            e_brain = e_brain_new
            
        rewards_history.append(total_reward)
        if ep % 5 == 0:
            print(f"   Epizód {ep}: Reward = {total_reward:.1f} (Viscosity: {viscosity:.2f})")
            
    # Visualize Learning
    plt.figure(figsize=(10, 5))
    plt.plot(rewards_history, label='Total Reward')
    # Moving average
    window = 5
    if len(rewards_history) >= window:
        avg = np.convolve(rewards_history, np.ones(window)/window, mode='valid')
        plt.plot(range(window-1, len(rewards_history)), avg, 'r--', label='Moving Avg')
        
    plt.title('RL Gardener Learning Curve')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('learning_curve.png')
    print("📊 Learning curve saved to learning_curve.png")
    
    return gardener

if __name__ == "__main__":
    trained_gardener = train_gardener(episodes=60)
    print("✅ Tréning kész.")
