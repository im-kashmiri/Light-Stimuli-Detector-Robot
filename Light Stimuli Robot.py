import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Initialize session state
if "robot_position" not in st.session_state:
    st.session_state.robot_position = np.array([20.0, 20.0])
    st.session_state.robot_direction = np.array([1.0, 0.0])

# Sidebar controls
light_x = st.sidebar.slider("Light X", 0, 100, 80)
light_y = st.sidebar.slider("Light Y", 0, 100, 80)
light_position = np.array([light_x, light_y])

# Sense and move
def sense_light(robot_pos, robot_dir):
    left_sensor = robot_pos + np.array([0, 2])
    right_sensor = robot_pos + np.array([0, -2])
    left_intensity = 1000 / (np.linalg.norm(light_position - left_sensor)**2 + 1)
    right_intensity = 1000 / (np.linalg.norm(light_position - right_sensor)**2 + 1)
    return left_intensity, right_intensity

def update_direction(l, r, current_dir):
    angle = np.pi / 18
    if l > r:
        rot = np.array([[np.cos(angle), -np.sin(angle)],
                        [np.sin(angle),  np.cos(angle)]])
    elif r > l:
        rot = np.array([[np.cos(-angle), -np.sin(-angle)],
                        [np.sin(-angle),  np.cos(-angle)]])
    else:
        rot = np.eye(2)
    new_dir = rot @ current_dir
    return new_dir / np.linalg.norm(new_dir)

# Move step
if st.button("Step Forward"):
    l, r = sense_light(st.session_state.robot_position, st.session_state.robot_direction)
    st.session_state.robot_direction = update_direction(l, r, st.session_state.robot_direction)
    st.session_state.robot_position += st.session_state.robot_direction

# Plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.plot(*light_position, 'yo', label='Light')
ax.plot(*st.session_state.robot_position, 'bo', label='Robot')
ax.legend()
st.pyplot(fig)
