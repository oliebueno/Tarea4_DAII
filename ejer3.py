import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Definición de la función de Rastrigin


def rastrigin(x, y):
    return x**2 + y**2 - 10 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)) + 20


# Parámetros del enjambre
X, Y, Z = 1.0, 9.0, 2.0  # Valores de ejemplo para X, Y, Z
num_particles = 4
iterations = 10

# Inicialización de partículas
particles = [
    {'position': np.array([0.0, X + 1.0]), 'velocity': np.array([0.0, (Z + 1.0) / 2.0]),
     'best_position': None, 'best_value': float('inf')},
    {'position': np.array([Y + 1.0, 0.0]), 'velocity': np.array([(Z + 1.0) / 2.0, 0.0]),
     'best_position': None, 'best_value': float('inf')},
    {'position': np.array([0.0, -X - 1.0]), 'velocity': np.array([0.0, (Z + 1.0) / 2.0]),
     'best_position': None, 'best_value': float('inf')},
    {'position': np.array([-Y - 1.0, 0.0]), 'velocity': np.array([(Z + 1.0) / 2.0, 0.0]),
     'best_position': None, 'best_value': float('inf')}
]

# Parámetros de PSO
w = 0.5  # Inercia
c1 = 1.5  # Coeficiente cognitivo
c2 = 1.5  # Coeficiente social

# Inicialización de la mejor posición global
global_best_position = None
global_best_value = float('inf')

# Función para actualizar las partículas


def update_particles(iteration):
    global global_best_position, global_best_value
    for particle in particles:
        # Evaluar la función objetivo
        value = rastrigin(particle['position'][0], particle['position'][1])

        # Actualizar la mejor posición personal
        if value < particle['best_value']:
            particle['best_value'] = value
            particle['best_position'] = particle['position'].copy()

        # Actualizar la mejor posición global
        if value < global_best_value:
            global_best_value = value
            global_best_position = particle['position'].copy()

    for particle in particles:
        # Actualizar la velocidad
        r1, r2 = np.random.rand(2)
        cognitive_velocity = c1 * r1 * \
            (particle['best_position'] - particle['position'])
        social_velocity = c2 * r2 * \
            (global_best_position - particle['position'])
        particle['velocity'] = w * particle['velocity'] + \
            cognitive_velocity + social_velocity

        # Actualizar la posición
        particle['position'] += particle['velocity']

    # Imprimir los valores de cada partícula
    for i, particle in enumerate(particles):
        print(f"Iteración {iteration}: Partícula {i+1}")
        print(f"  Posición: {particle['position']}")
        print(f"  Velocidad: {particle['velocity']}")
        print(f"  Mejor posición personal: {particle['best_position']}")
    print(f"Mejor posición global: {global_best_position}\n")


# Configuración de la gráfica
fig, ax = plt.subplots()
xdata, ydata = [], []
scat = ax.scatter([], [], c='red')


def init():
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    return scat,


def update(frame):
    update_particles(frame)
    xdata = [p['position'][0] for p in particles]
    ydata = [p['position'][1] for p in particles]
    scat.set_offsets(np.c_[xdata, ydata])
    return scat,


ani = FuncAnimation(fig, update, frames=iterations,
                    init_func=init, blit=True, repeat=False)
plt.show()
