import mujoco
import mujoco.viewer
import time

model = mujoco.MjModel.from_xml_path("Physics_Sim/Triple_tube.xml")
data = mujoco.MjData(model)

print("qpos:", data.qpos)
print("gravity:", model.opt.gravity)

with mujoco.viewer.launch_passive(model, data) as viewer:
    # viewer.opt.frame = mujoco.mjtFrame.mjFRAME_BODY # Should put a coordinate frame on each body

    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(model.opt.timestep)


# """Here is my controller version of the code:"""


# import mujoco
# import mujoco.viewer
# import time

# model = mujoco.MjModel.from_xml_path('Physics_Sim/Single_tube_with_actuator.xml')
# data = mujoco.MjData(model)

# print(data.qpos)

# # 1. Define your PID gains
# kp = 20.0
# ki = 0.5  # Your integral term gain
# kd = 2.0

# # 2. Track persistent variables for integration
# integral_error = 0.0
# last_error = 0.0
# target_angle = 0.0  # (Example target in radians)

# with mujoco.viewer.launch_passive(model, data) as viewer:
#     while viewer.is_running():
#         # Get current state from MuJoCo (assuming single joint at index 0)
#         current_angle = data.qpos[0]
#         current_velocity = data.qvel[0]

#         # if target_angle < 1.57:
#         #     target_angle += 0.001
#         # elif target_angle >= 1.57:
#         #     target_angle = 0.0

        
#         error = target_angle - current_angle
        
#         integral_error += error * model.opt.timestep
        
#         integral_error = max(-2.0, min(integral_error, 2.0))
        
#         torque_command = (kp * error) + (ki * integral_error) - (kd * current_velocity)
        
#         # Send the calculated torque directly to the motor
#         data.ctrl[0] = torque_command

#         mujoco.mj_step(model, data)
#         viewer.sync()
#         time.sleep(model.opt.timestep)
