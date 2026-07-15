# Week 2 · Module 5 — Color Segmentation (Seek a Gate)

Segment the cyan gates from the blue background, then search for, center, and approach one.

## What you'll learn

- **HSV color masking** — isolating the cyan gates from the blue wall by hue, robust to lighting.
- **Bounding boxes** — the upright rectangle around a contour, and its width/height.
- **Shape filtering** — keeping only gate-shaped (square) contours, rejecting the glowing lines.
- **Yaw-to-center then approach** — turning to face a gate before driving toward it.

## How it works

Color detection sounds easy until the lighting changes. This module picks a color the robust
way, then turns "I see a gate" into "fly to it."

**Pick the color in HSV, not BGR.** Raw camera pixels are Blue/Green/Red, but brightness is
smeared across all three channels, so a shadow shifts all of them at once. **HSV** separates
**H**ue (which color), **S**aturation (how vivid), and **V**alue (how bright). Choosing by
hue means a shadowed cyan and a bright cyan share almost the same H, so a hue range
(`CYAN_LOWER..CYAN_UPPER`) reliably grabs the gate and rejects the blue wall beside it.
`cv2.inRange` returns a binary mask of the in-range pixels — **color segmentation**.

**Describe the blob with a box.** The largest cyan contour gets a **bounding box**
`(x, y, w, h)` — the smallest upright rectangle around it. Its center says where the gate is;
its width `w` says how big it looks (Module 6 turns that into distance). The long glowing
boundary lines are also cyan, so a shape filter keeps only roughly square contours: a real
gate has an **aspect ratio** near 1, a boundary line is very elongated.

**Turn to face, then approach.** The horizontal gap between the box center and the image
center is a yaw error — **yaw** (rotate in place) to close it. Only once the gate is roughly
centered do you add forward **pitch**, or you drive past it at an angle. With no gate in
view, spin slowly to search. That "search → center → approach" loop is the skeleton of gate
racing.

Why it matters: choosing features that survive lighting changes, then sequencing search /
aim / approach, is exactly what the drone does to fly a course of gates.

## Key terms

- **HSV** — a color space with **H**ue (which color), **S**aturation (how vivid), **V**alue (how bright). Picking a color by hue is far more robust to lighting than picking it in raw BGR.
- **Color segmentation** — keeping only the pixels whose color falls in a chosen range. `cv2.inRange(hsv, LOWER, UPPER)` returns a binary mask of those pixels.
- **Bounding box** — the smallest upright rectangle around a contour, returned as `(x, y, w, h)` (top-left corner plus width and height).
- **Aspect ratio** — width ÷ height. A gate is roughly square (ratio near 1); a long glowing boundary line is very elongated, which is how the helper tells them apart.
- **Yaw** — rotating in place (turning left/right) without moving. Used to point the drone at the gate before flying toward it.
- **Approach control** — only adding forward speed once the gate is centered, so you drive toward it rather than past it.

## How to run

```bash
drone open_sim                          # launch the sim once
drone sim course/week2_vision/module5_color_segmentation/main.py            # all steps, your code
drone sim course/week2_vision/module5_color_segmentation/main_solution.py   # reference flight
```

Press **Enter** in the simulator window to start.

## Steps

1. **`step1_hsv_mask.py`** — measure how much of the image is cyan gate
2. **`step2_bounding_box.py`** — find the largest cyan gate's bounding box
3. **`step3_seek_gate.py`** — spin to find a gate, center it with yaw, fly toward it

## What to expect

The drone hovers and reports, then turns until a gate is centered and flies forward until the gate fills enough of the view ('Reached the gate').

## You're done when

- Step 1 prints a cyan coverage fraction (small but nonzero when a gate is in front).
- Step 2 prints a bounding box `(x, y, w, h)` with a width of tens-to-low-hundreds of pixels.
- Step 3 turns until the gate is centered, flies forward until the box width reaches `TARGET_WIDTH`, prints that it reached the gate, and lands.

## If it doesn't work

| Symptom | Fix |
|---------|-----|
| `NameError: name 'image' is not defined` | Capture the frame: `image = drone.camera.get_color_image()` (the **forward** camera here). |
| Coverage is ~0 | The cyan range may miss this scene's hue. Print `hsv` stats or widen `CYAN_LOWER/UPPER` slightly. |
| Picks up the blue wall too | The wall is blue (hue ~108), gates cyan (~85). Tighten the upper hue bound. |
| Spins forever, never centers | Make sure you reduce yaw as the error shrinks, and that `MIN_AREA` isn't rejecting the real gate. |
| Flies past the gate | Only add `APPROACH_PITCH` once `abs(gate_col - COL_CENTER) < CENTER_TOL`. |

## Going further (optional)

- Center the gate vertically too (use the box's `y`/`h`) by adding throttle, so you fly through the middle, not the top.
- Replace the bang-bang "centered? then go" rule with a smooth approach speed proportional to how centered you are.
- Detect when you've passed *through* the gate (it leaves the frame) and immediately search for the next one.

---

Fill in the blanks in `tasks/`; completed references are in `solutions/` (try it yourself first!).
