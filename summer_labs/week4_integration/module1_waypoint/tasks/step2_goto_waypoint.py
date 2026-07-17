"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 4 · Module 1 — Step 2: Go To a Waypoint
Fly to a target point given as (right, up, forward) meters from the start. This is
your first controller that drives three axes at once: roll for right, pitch for
forward, throttle for up.
"""

import drone_core
import drone_utils as uav_utils

# -- Course setup: makes the shared `neo_lab` helper importable.
#    You don't need to read or change this block. --
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.realpath(__file__))
while _os.path.basename(_d) != "labs" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
import neo_lab

# -- Constants --------------------------------------------------------------
TARGET_RIGHT = 2.0
TARGET_FWD = 4.0
TARGET_HEIGHT = 3.0
KP_POS = 0.3 #0.15
KD_POS = 0.05 #0.5           # brake with velocity so you don't overshoot
ALT_KP = 0.12
ROLL_LIMIT = 0.25
PITCH_LIMIT = 0.25
THROTTLE_LIMIT = 0.5
POS_TOL = 0.5          # meters from target counted as arrived
SETTLE_SPEED = 0.25    # must slow below this to finish
HOLD_TIME = 1.5

# -- Module-level state -----------------------------------------------------
_x = 0.0
_z = 0.0
_hold = 0.0
_done = False

def reset():
    global _x, _z, _hold, _done
    _x = 0.0
    _z = 0.0
    _hold = 0.0
    _done = False


def update(drone):
    global _x, _z, _hold, _done
    if _done:
        return True
    ##################################
    #### START PUT CODE HERE #########

    # GOAL: fly to (TARGET_RIGHT, TARGET_HEIGHT, TARGET_FWD) and hold there.
    #
    # Tools: drone.physics.get_linear_velocity() -> (vx, vy, vz); drone.get_delta_time();
    #        neo_lab.height(drone); uav_utils.clamp(...); drone.flight.send_pcmd(...).
    #
    # Track right/forward position by integrating vx, vz like Step 1. Drive each
    # horizontal axis with a PD controller (gain KP_POS on position error and KD_POS on
    # velocity, which brakes you): roll for the right error, pitch for the forward error.
    # Hold height with a proportional term (ALT_KP). Clamp each to its limit. Finish when
    # both horizontal errors are under POS_TOL and speed is under SETTLE_SPEED for HOLD_TIME.

    vx, vy, vz = drone.physics.get_linear_velocity()
    dt = drone.get_delta_time()

    _x += vx * dt
    _z += vz * dt

    #altitute
    cur_height = neo_lab.height(drone)
    err_height = cur_height - TARGET_HEIGHT
    throttle = uav_utils.clamp(err_height*ALT_KP, -THROTTLE_LIMIT, THROTTLE_LIMIT)

    # x (right)
    err_x = TARGET_RIGHT - _x
    roll = uav_utils.clamp(err_x*KP_POS - KD_POS*vx, -ROLL_LIMIT, ROLL_LIMIT)

    # z (fwd)
    err_z = TARGET_FWD - _z
    pitch = uav_utils.clamp(err_z*KP_POS - KD_POS*vz, -PITCH_LIMIT, PITCH_LIMIT)

    speed = (vx ** 2 + vz ** 2) ** 0.5
    drone.flight.send_pcmd(pitch, roll, 0, throttle)
    print(f"err_x: {err_x} | err_z: {err_z}")

    if(abs(err_x) <= POS_TOL and abs(err_z) <= POS_TOL and speed <= SETTLE_SPEED):
        
        _hold += dt
        if(_hold >= HOLD_TIME):
            drone.flight.stop()
            _done = True
    # if abs(err_x) < POS_TOL and abs(err_z) < POS_TOL and speed < SETTLE_SPEED:
    #     _hold += dt
    # else:
    #     _hold = 0.0
    # if _hold >= HOLD_TIME:
    #     drone.flight.stop()
    #     print(f"[Step 2] Arrived: right={_x:.2f} forward={_z:.2f} m")
    #     _done = True
    # return _done
    

    # if(abs(err_x) <= POS_TOL):
    #     if(abs(err_z) <= POS_TOL):
    #         print("X and Z within error")
    #         print(f"X: {_x} | Z: {_z} | Height: {cur_height}")
    #         if(speed <= SETTLE_SPEED):
    #             _hold += dt
    #             if(_hold >= HOLD_TIME):
    #                 drone.flight.stop()
    #                 _done = True
    #     else:
    #         print("X within error, Z not within error")
    #         drone.flight.send_pcmd(0,roll,0,throttle)
    # else:
    #     if(abs(err_z) <= POS_TOL):
    #         print("X not within error, Z within error")
    #         drone.flight.send_pcmd(pitch, 0,0,throttle)
    #     else:
    #         print("X and Z not within error")
    #         drone.flight.send_pcmd(pitch, roll, 0, throttle)

        



    ###### END PUT CODE HERE #########
    ##################################
    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher(3.0)

    def start():
        _launcher.reset()
        reset()
        print("Step 2: Go To a Waypoint")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
