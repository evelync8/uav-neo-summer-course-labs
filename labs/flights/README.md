# Sim-to-real test flights

Two short autonomous flights that run with the **same code** in the simulator and on
the real drone. They exist to check that code developed in the sim behaves on real PX4
hardware, not to teach a concept.

| Flight | What it does | How the waypoint/motion is produced |
|---|---|---|
| A - Waypoint | takeoff, fly to a point offset from takeoff, land | `drone.flight.goto_position(...)` - PX4's position controller on real, a hidden velocity controller in sim |
| B - Maneuver | takeoff, fly a body-velocity maneuver, land | `neo_lab.send_velocity(...)` - velocity setpoint on real, velocity-to-tilt inner loop in sim |
| Shape | takeoff, trace a repeating shape, land | open-loop patterns via `send_velocity`, or waypoint polygons via `goto_position`; pick the shape/mode in `shape_flight/step_shape.py` |

The `shape_flight` is the portable counterpart to `uav_neo_ros2_driver/shape_node.py`,
which draws the same shapes by talking to MAVROS directly (a ROS 2 learning example,
real drone only).

## Running

```bash
drone open_sim                                     # launch the sim once
drone sim course/flights/waypoint_flight/main.py   # Flight A in the simulator
drone sim course/flights/maneuver_flight/main.py   # Flight B in the simulator
```

On the real drone the same files run on the Pi. Bring up the stack **without the
manual-teleop mux** (it would publish velocity setpoints that fight the autonomy
setpoints), then run the script (no `-s`, so it selects the real drone):

```bash
ros2 launch uav_neo_ros2_driver teleop.launch.py manual:=false   # mavros + relays, no mux
python3 main.py                                                   # from each flight folder
```

Press the START button on the Xbox controller to begin the program, BACK to stop it.

Enter user-program mode to begin: press ENTER in the sim window, or the START button on
the Xbox controller on the real drone.

## Safety model on the real drone

These flights publish setpoints straight to the flight controller (they do not go through
the manual-teleop mux). The safety layer is the **RC pilot**:

1. The safety pilot arms and switches to OFFBOARD on the RC transmitter. Software never
   arms or changes modes on its own (except the autonomous landing below).
2. The safety pilot overrides at any time by switching out of OFFBOARD.
3. Flight A ends by commanding PX4's `AUTO.LAND`; Flight B lands with a descent setpoint.

## Required before Flight A on real hardware: lower the PX4 speed limits

Flight A uses PX4's own position controller, so its speed is set by PX4 parameters, **not**
by the library's speed cap. The dev-drone defaults (`MPC_XY_CRUISE = 5`, `MPC_XY_VEL_MAX =
12` m/s) are far too fast for an indoor waypoint. Before flying, lower them, e.g.:

```bash
ros2 param set /mavros/param MPC_XY_CRUISE 0.6
ros2 param set /mavros/param MPC_XY_VEL_MAX 1.0
ros2 param set /mavros/param MPC_Z_VEL_MAX_UP 0.6
ros2 param set /mavros/param MPC_Z_VEL_MAX_DN 0.6
```

Set them in QGroundControl instead if you prefer, and persist them into the params file in
`px4_params/`. Flight B's speed is capped by the library (`MAX_SPEED = 0.5` m/s), so it does
not depend on these.
