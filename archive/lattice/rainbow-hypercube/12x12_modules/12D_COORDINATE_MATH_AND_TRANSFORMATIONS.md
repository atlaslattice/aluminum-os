---
title: "12D Coordinate Math & Transformations"
version: "1.0"
date: "2026-05-31"
status: candidate
---

# 12D Coordinate Math & Transformations

## 1. Basic Representation

A 12D coordinate is a 12-tuple of integers in range [0, 11]:

```python
coord = (d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12)
```

## 2. Normalization

To work in continuous space [0.0, 1.0]:

```python
def normalize(coord):
    return tuple(d / 11.0 for d in coord)

def denormalize(norm_coord):
    return tuple(int(round(n * 11)) for n in norm_coord)
```

## 3. Projections to Common 3-Axis Systems

### GrokBrain E/C/D Projection

E (Epistemic) ≈ average of D9, D10, D12  (learning, governance, emergence)
C (Content) ≈ average of D2, D4, D7, D10  (compute, form, habitat, governance)
D (Depth) ≈ average of D1, D5, D8, D12  (foundation, life, coherence, transcendence)

### Operational X/Y/Z Projection

Can be mapped using the House/Container/State model from the operational lattice.

### Periodic Table 2.0 12x12 Projection

Period can be derived from strength across D1–D6 vs D7–D12.
Group can be derived from dominant functional archetype dimensions.

## 4. Distance & Resonance in 12D

Simple Euclidean distance (normalized):

```python
import math

def distance_12d(c1, c2):
    norm1 = normalize(c1)
    norm2 = normalize(c2)
    return math.sqrt(sum((a - b)**2 for a, b in zip(norm1, norm2)))
```

Resonance score (inverse distance, higher = more resonant):

```python
def resonance_12d(c1, c2):
    return 1.0 - distance_12d(c1, c2)
```

## 5. Transformation Between Views

When moving between different 3-axis projections, it is often useful to lift to full 12D first, then re-project.

This preserves information and avoids lossy direct mappings.

---

*This reference will grow as we develop more sophisticated 12D operations.*
