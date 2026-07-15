# Week 2 · Module 6 — Distance Estimation

Use a gate's apparent size to estimate how far away it is, then approach it. This
connects the pinhole math from Module 1 to live flight: a known real-world width
projects to a pixel width that shrinks with distance, so distance is recoverable.

## What you'll learn

- **Inverting perspective projection** — recovering distance from how big something looks.
- **Monocular range from a known size** — why one camera plus a known width gives distance.
- **Distance-driven approach** — using the estimate to decide when to stop.

## How it works

Module 1 projected a known 3-D size *down* to a pixel width. This module runs that arrow
*backward*: if you already know how wide the gate really is, its pixel width tells you how
far away it is.

**Size shrinks with distance.** From the pinhole model, an object of real width `W` at
distance `d` projects to a pixel width `w = FOCAL_PX · W / d`. Every term but `d` is known:
`W` is the gate's true width (`REAL_GATE_WIDTH`), `FOCAL_PX` is the camera's focal length in
pixels, and `w` you measure from the bounding box. Solve for the unknown and you get
**monocular range**: `d = FOCAL_PX · W / w`. One camera, no stereo, no depth sensor — just a
known size.

**Where FOCAL_PX comes from.** It is the focal length expressed in pixels, set by the image
width and the **field of view**: for a 640-pixel image with a ~90° horizontal FOV it is about
320 (half the width divided by `tan(½ FOV)`). A wider FOV means a smaller `FOCAL_PX`.

**Fly by the estimate.** Each frame, measure the width, compute the distance, and act on it:
keep the gate centered with yaw, add forward pitch to approach, and stop once the distance
drops to `STOP_DIST`. The estimate is only as good as your `W` and `FOCAL_PX`, so a wrong
constant shows up as a wrong stopping distance.

Why it matters: recovering 3-D information (range) from a 2-D image with a known reference is
a workhorse trick in robotics — the same idea behind sizing an AprilTag or a person from a
single camera.

## Key terms

- **Apparent (pixel) width** — how wide the gate looks in the image, in pixels. It grows as you get closer.
- **Focal length in pixels (FOCAL_PX)** — the camera's focal length expressed in pixels. For a 640-pixel-wide image with a ~90° horizontal field of view, it is about 320. (Half the width divided by tan(half the FOV).)
- **Monocular range estimation** — estimating distance from a single camera using a known object size: `distance = FOCAL_PX · real_width / pixel_width`.
- **Field of view (FOV)** — the angular width the camera sees. Wider FOV → smaller focal length in pixels.

## How to run

```bash
drone open_sim                          # launch the sim once
drone sim course/week2_vision/module6_distance_estimation/main.py            # all steps, your code
drone sim course/week2_vision/module6_distance_estimation/main_solution.py   # reference flight
```

Press **Enter** in the simulator window to start.

## Steps

1. **`step1_measure_width.py`** — measure the nearest cyan gate's apparent width in pixels
2. **`step2_estimate_range.py`** — convert width to distance and fly forward until close

## What to expect

Step 1 hovers and prints a pixel width. Step 2 flies toward the gate, keeping it
centered, and stops once the estimated distance reaches `STOP_DIST`, then lands.

## You're done when

- Step 1 prints a gate width of tens-to-low-hundreds of pixels.
- Step 2 flies forward, prints a shrinking distance, and stops at about `STOP_DIST` meters.

## If it doesn't work

| Symptom | Fix |
|---------|-----|
| `NameError: name 'image' is not defined` | Capture the frame: `image = drone.camera.get_color_image()`. |
| Distance is wildly wrong | Check `REAL_GATE_WIDTH` matches the sim's gate, and that `FOCAL_PX` is in pixels (not meters or degrees). |
| Stops too early/late | The estimate is only as good as `REAL_GATE_WIDTH` and `FOCAL_PX` — measure the real gate width in the sim and adjust. |
| Drone flies past the gate | Make sure you stop on `distance <= STOP_DIST`, and yaw to keep the gate centered while approaching. |

## Going further (optional)

- Calibrate `FOCAL_PX` empirically: hover a known distance from a gate, read the pixel width, and solve `FOCAL_PX = pixel_width · distance / real_width`.
- Use the gate **height** as a second, independent range estimate and average the two.
- Combine with Module 3's PID: feed the estimated distance error into a PID controller for a smooth stop instead of a hard cutoff.

---

Fill in the blanks in `tasks/`; completed references are in `solutions/` (try it yourself first!).
