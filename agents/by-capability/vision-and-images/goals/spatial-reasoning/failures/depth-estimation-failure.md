# Depth Estimation Failure

## Issue: Monocular Depth Estimation Wrong; 3D Positioning Fails

**Frequency**: Common

**Symptoms**
- Objects appear closer/farther than actual
- Gripper collision with objects agent thought were far
- Depth ambiguity in images without stereo cues
- Relative depth wrong between foreground/background

**Root Cause**
Depth from single images is ambiguous without stereo/temporal cues. Models learn statistical priors ("larger objects farther") but fail on ambiguous cases (small far objects vs. large near objects). Training data rarely covers full depth range.

**Example**
```
Scenario: Robot navigation using monocular depth

Predicted depth: Small object at 3m
Actual: Small object at 30cm

Robot: Doesn't slow down → collision
Impact: Damage, safety risk
```

**Key Statistics**
- Depth error: 20-40% on ambiguous scenes
- Relative depth (one object closer than another): 70% accurate
- Absolute depth: 40-60% accurate

---

## Mitigation Strategies

1. **Stereo Confirmation**: Use stereo cameras; compare against monocular predictions
2. **Temporal Cues**: Use video sequences for depth consistency
3. **Conservative Margins**: Treat depth predictions as upper bounds (safer)
4. **Real Sensor Fallback**: Use LiDAR/ToF sensor when depth critical

### Metrics
- **Absolute Relative Error (Abs Rel)**: mean(|predicted - gt| / gt)
- **Depth Consistency**: Variance of depth across video frames

---

## Production Signals

- `vision.depth_error_ratio` > 0.3 → Alert
- `robot.collision_rate` spike → Investigate depth model

---

## References

- [Disp R-CNN: Stereo 3D Object Detection](https://arxiv.org/abs/1910.12033)
- [Depth Estimation Benchmarks](https://arxiv.org/abs/2103.02175)
