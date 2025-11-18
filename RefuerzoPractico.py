import numpy as np
import random
import matplotlib.pyplot as plt
import pickle
import os

class GridWorldAgent:
    def __init__(self, grid_size=3, alpha=0.5, gamma=0.9, epsilon=0.2):
        self.grid_size = grid_size
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.actions = ["up", "down", "left", "right"]
        self.Q = np.zeros((grid_size, grid_size, len(self.actions)))
        
        # Definir entorno
        self.reward_map = np.array([
            [0, 0, 0],
            [0, -5, 0],
            [0, 0, 10]
        ])
        self.start = (0, 0)
        self.goal = (2, 2)
        self.obstacle = (1, 1)
    
    def move(self, state, action):
        i, j = state
        if action == "up" and i > 0:
            i -= 1
        elif action == "down" and i < self.grid_size - 1:
            i += 1
        elif action == "left" and j > 0:
            j -= 1
        elif action == "right" and j < self.grid_size - 1:
            j += 1
        return (i, j)
    
    def train(self, episodes=1000):
        episode_rewards = []
        episode_steps = []
        
        for ep in range(episodes):
            state = self.start
            total_reward = 0
            steps = 0
            
            while state != self.goal and steps < 50:
                # Selección de acción ε-greedy
                if random.random() < self.epsilon:
                    action_idx = random.randint(0, len(self.actions) - 1)
                else:
                    action_idx = np.argmax(self.Q[state])
                
                action = self.actions[action_idx]
                new_state = self.move(state, action)
                
                # Recompensa
                reward = self.reward_map[new_state]
                
                # Actualización Q-Learning
                future_q = 0 if new_state == self.goal else np.max(self.Q[new_state])
                self.Q[state][action_idx] += self.alpha * (
                    reward + self.gamma * future_q - self.Q[state][action_idx]
                )
                
                total_reward += reward
                steps += 1
                state = new_state
                
                # Terminar si choca con obstáculo o llega a la meta
                if state == self.obstacle or state == self.goal:
                    break
            
            episode_rewards.append(total_reward)
            episode_steps.append(steps)
            
            # Reducir exploración gradualmente
            if ep % 200 == 0 and ep > 0:
                self.epsilon = max(0.01, self.epsilon * 0.9)
        
        return episode_rewards, episode_steps
    
    def get_best_path(self):
        state = self.start
        path = [state]
        actions_taken = []
        
        max_steps = 10
        steps = 0
        
        while state != self.goal and steps < max_steps:
            action_idx = np.argmax(self.Q[state])
            action = self.actions[action_idx]
            state = self.move(state, action)
            path.append(state)
            actions_taken.append(action)
            steps += 1
            
            if state == self.obstacle or state == self.goal:
                break
        
        return path, actions_taken
    
    def plot_training(self, episode_rewards):
        # Asegurar que la carpeta static existe
        os.makedirs('static', exist_ok=True)
        
        plt.style.use('seaborn-v0_8')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Gráfica 1: Evolución de recompensas
        window = 50
        if len(episode_rewards) >= window:
            moving_avg = [np.mean(episode_rewards[i-window:i]) for i in range(window, len(episode_rewards))]
            ax1.plot(range(window, len(episode_rewards)), moving_avg, 'b-', linewidth=2, label=f'Media móvil ({window} episodios)')
        
        ax1.plot(episode_rewards, 'g-', alpha=0.3, label='Recompensa por episodio')
        ax1.set_xlabel('Episodio')
        ax1.set_ylabel('Recompensa')
        ax1.set_title('Evolución de las Recompensas durante el Entrenamiento')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfica 2: Política aprendida
        policy = np.argmax(self.Q, axis=2)
        action_symbols = ['↑', '↓', '←', '→']
        policy_symbols = np.empty((self.grid_size, self.grid_size), dtype=object)
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                policy_symbols[i, j] = action_symbols[policy[i, j]]
        
        # Crear mapa de calor con anotaciones
        im = ax2.imshow(policy, cmap='viridis', alpha=0.7)
        
        # Añadir símbolos de acciones
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                ax2.text(j, i, policy_symbols[i, j], 
                        ha='center', va='center', fontsize=20, fontweight='bold',
                        color='white' if policy[i, j] in [0, 1] else 'black')
                
                # Marcar posiciones especiales
                if (i, j) == self.start:
                    ax2.text(j, i, 'S', ha='center', va='bottom', fontsize=16, fontweight='bold', color='red')
                elif (i, j) == self.goal:
                    ax2.text(j, i, 'G', ha='center', va='top', fontsize=16, fontweight='bold', color='red')
                elif (i, j) == self.obstacle:
                    ax2.text(j, i, 'X', ha='center', va='top', fontsize=16, fontweight='bold', color='red')
        
        ax2.set_title('Política Aprendida\n(↑:up, ↓:down, ←:left, →:right)')
        ax2.set_xticks(range(self.grid_size))
        ax2.set_yticks(range(self.grid_size))
        plt.colorbar(im, ax=ax2, label='Acción')
        
        plt.tight_layout()
        plt.savefig('static/rewards.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Gráfica de entrenamiento guardada en static/rewards.png")
    
    def plot_trajectory(self, path):
        """Generar gráfica de trayectoria"""
        # Asegurar que la carpeta static existe
        os.makedirs('static', exist_ok=True)
        
        plt.figure(figsize=(6, 6))
        
        # Dibujar grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i, j) == self.start:
                    plt.text(j, i, 'S', ha='center', va='center', fontsize=20, fontweight='bold')
                    plt.gca().add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color='lightblue'))
                elif (i, j) == self.goal:
                    plt.text(j, i, 'G', ha='center', va='center', fontsize=20, fontweight='bold')
                    plt.gca().add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color='lightgreen'))
                elif (i, j) == self.obstacle:
                    plt.text(j, i, 'X', ha='center', va='center', fontsize=20, fontweight='bold')
                    plt.gca().add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=True, color='lightcoral'))
                else:
                    plt.gca().add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, fill=False, edgecolor='gray'))
        
        # Dibujar trayectoria
        if len(path) > 1:
            x_coords = [coord[1] for coord in path]
            y_coords = [coord[0] for coord in path]
            plt.plot(x_coords, y_coords, 'ro-', linewidth=2, markersize=8)
        
        plt.xlim(-0.5, self.grid_size-0.5)
        plt.ylim(-0.5, self.grid_size-0.5)
        plt.gca().invert_yaxis()
        plt.title('Trayectoria del Agente')
        plt.savefig('static/trajectory.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Gráfica de trayectoria guardada en static/trajectory.png")
    
    def save_model(self, filename='static/modelo_entrenado.pkl'):
        # Asegurar que la carpeta existe
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'wb') as f:
            pickle.dump({
                'Q_table': self.Q,
                'alpha': self.alpha,
                'gamma': self.gamma,
                'epsilon': self.epsilon,
                'training_params': {
                    'grid_size': self.grid_size,
                    'actions': self.actions
                }
            }, f)
        print(f"✓ Modelo guardado en {filename}")
    
    def load_model(self, filename='static/modelo_entrenado.pkl'):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.Q = data['Q_table']
            print(f"✓ Modelo cargado desde {filename}")
        else:
            print(f"✗ Archivo {filename} no encontrado")