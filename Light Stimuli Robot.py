import matplotlib.pyplot as plt
import numpy as np
import time

# Environment Setup
room_size = 100
light_position = np.array([80, 80])

# Robot Setup
robot_position = np.array([20.0, 20.0])
robot_direction = np.array([1.0, 0.0])  # Initially facing right
speed = 1.0

# Sensor positions relative to the robot (left and right)
sensor_offset = np.array([[0, 2], [0, -2]])

def sense_light(robot_pos, robot_dir):
    # Get left and right sensor positions
    perp = np.array([-robot_dir[1], robot_dir[0]])  # Perpendicular vector
    left_sensor = robot_pos + sensor_offset[0][1] * perp
    right_sensor = robot_pos + sensor_offset[1][1] * perp
    
    # Light intensity is inverse square of distance
    left_intensity = 1000 / (np.linalg.norm(light_position - left_sensor)**2 + 1)
    right_intensity = 1000 / (np.linalg.norm(light_position - right_sensor)**2 + 1)
    
    return left_intensity, right_intensity

def update_direction(left_intensity, right_intensity, current_dir):
    angle = np.pi / 18  # Turn angle = 10 degrees
    
    if left_intensity > right_intensity:
        # Turn left
        rotation = np.array([[np.cos(angle), -np.sin(angle)],
                             [np.sin(angle), np.cos(angle)]])
    elif right_intensity > left_intensity:
        # Turn right
        rotation = np.array([[np.cos(-angle), -np.sin(-angle)],
                             [np.sin(-angle), np.cos(-angle)]])
    else:
        # Go straight
        rotation = np.eye(2)
    
    new_dir = rotation @ current_dir
    return new_dir / np.linalg.norm(new_dir)

# Visualization function
def plot_environment(robot_pos, light_pos, step):
    plt.figure(figsize=(6, 6))
    plt.xlim(0, room_size)
    plt.ylim(0, room_size)
    plt.plot(*light_pos, 'yo', label="Light Source")
    plt.plot(*robot_pos, 'bo', label="Robot")
    plt.title(f"Step {step}")
    plt.legend()
    plt.grid(True)
    plt.show()

# Simulation Loop
for step in range(100):

    # Sense
    left, right = sense_light(robot_position, robot_direction)

    # Act
    robot_direction = update_direction(left, right, robot_direction)
    robot_position += robot_direction * speed

    # Show
    plot_environment(robot_position, light_position, step)
    time.sleep(0.1)

# Plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, room_size)
ax.set_ylim(0, room_size)
ax.plot(*light_position, 'yo', label="Light Source")
ax.plot(*st.session_state.robot_position, 'bo', label="Robot")
ax.set_title("Light-Chasing Robot")
ax.legend()
st.pyplot(fig)  # <- THIS IS CRITICAL

