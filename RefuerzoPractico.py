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
            
            while state != self.goal and steps < 50:  # Límite de pasos
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
            
            # Print de progreso
            if ep % 100 == 0:
                avg_reward = np.mean(episode_rewards[-100:]) if ep > 0 else total_reward
                print(f"Episodio {ep}: Recompensa = {total_reward}, ε = {self.epsilon:.3f}, Avg = {avg_reward:.2f}")
        
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
        plt.savefig('training_results.png', dpi=300, bbox_inches='tight')
        print("Gráfica guardada como 'training_results.png'")
        plt.show()
    
    def plot_grid_world(self):
        """Visualización adicional del entorno GridWorld"""
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # Crear grid
        grid_display = np.zeros((self.grid_size, self.grid_size))
        
        # Marcar posiciones especiales
        grid_display[self.start] = 1
        grid_display[self.obstacle] = -1
        grid_display[self.goal] = 2
        
        im = ax.imshow(grid_display, cmap='RdYlBu', alpha=0.7)
        
        # Añadir texto
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (i, j) == self.start:
                    ax.text(j, i, 'S\n(Inicio)', ha='center', va='center', fontsize=12, fontweight='bold')
                elif (i, j) == self.goal:
                    ax.text(j, i, 'G\n(+10)', ha='center', va='center', fontsize=12, fontweight='bold')
                elif (i, j) == self.obstacle:
                    ax.text(j, i, 'X\n(-5)', ha='center', va='center', fontsize=12, fontweight='bold')
                else:
                    ax.text(j, i, f'({i},{j})', ha='center', va='center', fontsize=10, alpha=0.7)
        
        ax.set_title('GridWorld Environment')
        ax.set_xticks(range(self.grid_size))
        ax.set_yticks(range(self.grid_size))
        ax.grid(True, color='white', linewidth=2)
        
        plt.tight_layout()
        plt.savefig('gridworld_environment.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_model(self, filename='q_learning_model.pkl'):
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
        print(f"Modelo guardado como {filename}")
    
    def load_model(self, filename='q_learning_model.pkl'):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.Q = data['Q_table']
            print(f"Modelo cargado desde {filename}")
        else:
            print(f"Archivo {filename} no encontrado")

# Función principal mejorada
def main():
    print("=== ENTRENAMIENTO DE AGENTE GRIDWORLD ===")
    
    # Crear y entrenar agente
    agent = GridWorldAgent(alpha=0.5, gamma=0.9, epsilon=0.3)
    
    # Mostrar el entorno primero
    print("\n1. Visualizando el entorno GridWorld...")
    agent.plot_grid_world()
    
    print("\n2. Iniciando entrenamiento...")
    print("Parámetros: α=0.5, γ=0.9, ε=0.3, episodios=800")
    print("-" * 50)
    
    episode_rewards, episode_steps = agent.train(episodes=800)
    
    # Resultados
    print("\n" + "="*50)
    print("RESULTADOS DEL ENTRENAMIENTO")
    print("="*50)
    
    last_100_avg = np.mean(episode_rewards[-100:])
    last_50_avg = np.mean(episode_rewards[-50:])
    
    print(f"Recompensa promedio (últimos 100 episodios): {last_100_avg:.2f}")
    print(f"Recompensa promedio (últimos 50 episodios): {last_50_avg:.2f}")
    print(f"Recompensa máxima: {np.max(episode_rewards)}")
    print(f"Recompensa mínima: {np.min(episode_rewards)}")
    print(f"Éxitos (recompensa >= 10): {sum(r >= 10 for r in episode_rewards)}/{len(episode_rewards)}")
    
    # Obtener mejor ruta
    best_path, actions = agent.get_best_path()
    print(f"\nMejor ruta encontrada ({len(best_path)} pasos):")
    for i, (state, action) in enumerate(zip(best_path[:-1], actions)):
        print(f"  Paso {i+1}: {state} -> {action} -> {best_path[i+1]}")
    
    # Graficar resultados
    print("\n3. Generando gráficas...")
    agent.plot_training(episode_rewards)
    
    # Guardar modelo
    print("\n4. Guardando modelo...")
    agent.save_model()
    
    print("\n¡Entrenamiento completado!")
    return agent, episode_rewards

# Ejecutar solo si es el script principal
if __name__ == "__main__":
    try:
        trained_agent, rewards = main()
        
        # Verificar que las gráficas se crearon
        if os.path.exists('training_results.png'):
            print("✓ Gráfica 'training_results.png' creada exitosamente")
        if os.path.exists('gridworld_environment.png'):
            print("✓ Gráfica 'gridworld_environment.png' creada exitosamente")
        if os.path.exists('q_learning_model.pkl'):
            print("✓ Modelo 'q_learning_model.pkl' guardado exitosamente")
            
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        print("Asegúrate de tener matplotlib instalado: pip install matplotlib")