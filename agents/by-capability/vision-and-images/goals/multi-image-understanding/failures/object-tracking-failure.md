# Object Tracking Failure in Multi-Frame Sequences

## Issue: Model Cannot Maintain Consistent Object Track Across Multiple Frames; Loses or Confuses Identities

**Frequency**: Very Common

**Symptoms**
- Track switches (tracks swapped mid-video)
- ID fragmenting (one object becomes multiple tracks)
- Fragmentation (same object gets multiple IDs)
- High "ID switches" metric in benchmark evaluation

**Root Cause**
Tracking requires temporal consistency, appearance matching, and motion prediction. Naive frame-by-frame detection misses this. Motion prediction must be learned; appearance features must be consistent. Crowded scenes make this exponentially harder.

**Example**
```
Scenario: Crowd tracking in surveillance
Person A and Person B walk close, briefly occluded
Frame 1: A at (100, 200), B at (300, 200)
Frame 2: Brief occlusion
Frame 3: Model swaps IDs → A now at (300, 200), B at (100, 200)

Expected: Maintain identity across occlusion
Impact: Lost tracking; alert on wrong person
```

**Key Statistics**
- ID switches: 0.1-0.5 per person per video (lower is better)
- Fragmentation: 5-15% (tracks break and restart)
- Precision: 80-90%; Recall: 70-85%

---

## Mitigation Strategies

1. **Motion Models**: Kalman filter or constant-velocity motion prior
2. **Appearance Features**: Learn discriminative embeddings (ReID)
3. **Hungarian Matching**: Optimal assignment across frames
4. **Track Management**: Birth/death/merge logic for crowd dynamics

### Metrics
- MOTA (Multiple Object Tracking Accuracy)
- ID Switches (IDs per ground-truth track)
- Fragmentation (track fragments per GT object)

### Alerts
- ID switches >1 per object → P2
- Fragmentation >10% → P2

---

## References

- [MOT Challenge Benchmarks](https://arxiv.org/abs/1504.01169)
- [Tracking by Re-identification](https://arxiv.org/abs/2112.08713)
