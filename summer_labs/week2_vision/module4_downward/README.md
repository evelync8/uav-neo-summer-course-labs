# Week 2 · Module 4 — Downward Camera (Gate Detection)

Find a gate beneath the drone with contour analysis and hover directly over it.

## What you'll learn

- **Masking the glowing gate** — isolating the bright gate edges below the drone.
- **Contours** — finding connected blobs with `cv2.findContours` and picking the largest.
- **Centroid + area** — reducing a blob to a center point and a size.
- **Visual servoing** — using pitch/roll to drive the gate's pixel error to zero.

## How it works

Once you have a binary mask of the bright pixels, you still need to answer "*where* is the
gate, and how do I fly over it?" Contours turn the mask into objects, and a control loop
turns an object's position into motion.

**From pixels to objects.** `cv2.findContours` traces the outline of each connected white
blob and returns them as lists of boundary points — one **contour** per object. Real scenes
have several blobs (noise, partial gates), so rank them by **area** (the pixels each
encloses) and keep the largest. That one filtering step rejects most noise for free.

**Reduce the object to a point.** A control loop cannot act on a whole contour, so collapse
it to its **centroid** — the average of its pixels, `(row, col)`. Now the gate is a single
point in the image.

**Servo onto it.** The **pixel error** is how far that centroid sits from the image center
`(240, 320)`. **Visual servoing** drives that error to zero: command **pitch** (forward/back)
from the row error and **roll** (left/right) from the column error, each scaled down so the
drone eases in. Which sign centers the drone depends on how the camera is mounted, so pick a
sign, watch which way it runs, and flip it if it diverges.

Why it matters: "detect an object, reduce it to an error, close a loop on that error" is the
same recipe the forward-camera gate labs and the Week 3 visual-servo capstone use. Master it
here on the easy downward view and the harder cases follow.

## Key terms

- **Contour** — the outline of a connected white region in a mask, stored as a list of boundary points. `cv2.findContours` returns one per blob.
- **Contour area** — the number of pixels the contour encloses; used to ignore small noise and pick the biggest object.
- **Centroid** — the center point of a contour, `(row, col)`. The `neo_lab`/`uav_utils` helper returns it for you.
- **Visual servoing** — controlling motion directly from what the camera sees: turn the pixel error (how far the target is from center) into a movement command.
- **Pitch** — tilting forward/back, which moves the drone forward/back. Used here together with roll to slide over the gate.
- **Pixel error** — `(target pixel) − (image center)`. Drive it to zero to center the drone over the gate.

## How to run

```bash
drone open_sim                          # launch the sim once
drone sim course/week2_vision/module4_downward/main.py            # all steps, your code
drone sim course/week2_vision/module4_downward/main_solution.py   # reference flight
```

Press **Enter** in the simulator window to start.

## Steps

1. **`step1_find_contours.py`** — count the glowing-edge contours below the drone
2. **`step2_largest_object.py`** — locate the largest gate and report its center & area
3. **`step3_track_object.py`** — fly pitch/roll to center the drone over the gate

## What to expect

The drone arms, climbs, finds the gate frame below it, then nudges itself until the gate is centered in the downward image, then lands.

## You're done when

- Step 1 prints a contour count of at least 1 when a gate is below.
- Step 2 prints a center `(row, col)` and an area in the hundreds-to-thousands.
- Step 3 moves until the gate center sits within `CENTER_TOL` pixels of the image center `(240, 320)`, holds for `HOLD_TIME`, then lands.

## If it doesn't work

| Symptom | Fix |
|---------|-----|
| `NameError: name 'image' is not defined` | Capture the frame: `image = drone.camera.get_downward_image()`. |
| 0 contours found | The gate isn't under the drone yet, or `V_MIN` is too high. Lower `V_MIN` or raise the launch height. |
| Drone drifts *away* from the gate | Your pitch or roll sign is inverted — flip it. The hint warns the correct sign depends on camera mounting. |
| Never settles (oscillates over the gate) | Lower `MAX_TILT`, or widen `CENTER_TOL` slightly. |

## Going further (optional)

- Use the gate **area** to also hold a target altitude: if the gate looks too small, descend; too big, climb.
- Replace `largest_bright_contour` with the square-shape filter (`neo_lab.largest_gate`) and see whether it rejects the long boundary lines.
- Add a simple derivative term (use `get_linear_velocity`) so the drone brakes as it nears center instead of overshooting.

---

Fill in the blanks in `tasks/`; completed references are in `solutions/` (try it yourself first!).
