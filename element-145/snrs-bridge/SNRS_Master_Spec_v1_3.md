# Sovereign Node Radius Stack (SNRS) Master Spec v1.3

## Status
Canonical federated working spec as of 2026-04-11.

## Core thesis
SNRS is a reuse-first, population-first infrastructure framework that converts vacant, incomplete, or dilapidated building stock into localized dignity nodes. Each node is a population-based service unit designed around seven foundational elements:

1. Shelter
2. Water
3. Energy
4. Health
5. Regenerative Food
6. Capability
7. Computation / Intelligence Infrastructure

The node is not a fixed-radius circle on a map. It is a population-based service unit with a variable geographic footprint determined by service population, catchment area, service density, and functional coherence.

## Design principles
- Reuse first where viable stock exists
- Population first, not land-tiling first
- Dignity over utility
- Causal logic only
- Buildings are recoverable inventory, not waste
- Food is structural, not optional
- Education is embedded in infrastructure
- Computation is the nervous system of the node

## Housing stock categories
- Ready to Convert
- Salvageable
- Strategic Hold
- Write-Off / Dismantle

## Three economic streams
1. Hard savings
2. Operating efficiency
3. Material recovery value

The base case must not rely on speculative data licensing.

## Material Recovery Module
SNRS treats decommissioned buildings as recoverable inventory. Material recovery must be modeled conservatively, by stock category, and as net recovery value after contamination, sorting, and refurbishment costs.

## Regenerative Food Layer
Agriculture is not optional. Each node is a habitat-production unit, not merely a housing/service unit. Phase 1 food modeling should remain conservative and treat food as a partial local offset, not full autarky.

Key food variables:
- food demand per person
- target local food offset percentage
- productive area
- yield by production mode
- agricultural labor absorption
- water demand
- wastewater_nutrient_recovery_rate
- fertilizer offset percentage
- food capex and opex

## Capability layer
The node trains the people who maintain and improve the node. Capability accumulation must be bounded and scenario-dependent.

Key capability variables:
- training participation rate
- local skill retention rate
- trust / uptake multiplier
- contractor dependence

## Computation / Intelligence Infrastructure
This is the node's nervous system. Phase 1 should model it conservatively as bounded node-level opex plus bounded efficiency offsets.

## Phase 1 simulation scope
Included:
- housing stock classification
- retrofit costs
- hard savings
- operating efficiency
- adoption dynamics
- capex timing
- bounded capability accumulation
- conservative health burden proxy
- conservative regenerative food module
- material recovery module
- sensitivity analysis

Excluded:
- humanoid robotics assumptions
- quantum assumptions
- interplanetary assumptions in base results
- speculative data licensing as required economics
- subjective trust / happiness metrics as headline outputs

## Node sizes to test
- 5,000
- 10,000
- 50,000
- 100,000
- 250,000
- 1,000,000

Also test:
- 100,000 flat node
- 100,000 as 5 × 20,000 coherent subclusters

## Scenario matrix
- Scenario A: Bare Retrofit Utility Recovery
- Scenario B: Dignity-Node Retrofit
- Scenario C: Fuller Sovereign Node

Each under:
- high-trust
- low-trust

## Monte Carlo parameter spine
### Housing stock
- category shares
- suitability scores
- time-to-occupancy
- category-specific retrofit burden

### Capex structure
- shell acquisition / takeover
- retrofit
- infrastructure wrapper
- energy / water systems
- digital / health systems
- material recovery capex offset

### Adoption dynamics
- logistic steepness k
- midpoint t_mid
- policy lag
- conversion lag
- abandonment / non-adoption rate

### Hard savings block
- vacancy drag reduction
- unstable housing burden reduction
- health burden proxy reduction
- utility burden reduction
- transport inefficiency reduction
- remediation avoided

### Capability block
- training participation
- skill retention
- trust multiplier
- contractor dependence
- maintenance cost reduction
- degradation mitigation

### Food block
- local food self-provision rate
- nutrition support proxy
- water demand
- nutrient recovery offset
- ag labor absorption

### Computation block
- node-level digital twin / control opex
- sensor integration cost
- bounded efficiency offsets

## Required outputs
- NPV distribution
- probability of positive NPV
- cash-positive year distribution
- capex by category
- material recovery capex offset
- occupied stock over time
- population served over time
- degradation trend
- local skill retention proxy
- local food self-provision rate
- nutrition support proxy
- annual water savings
- annual energy savings
- threshold chart showing minimum hard-savings level required for positive NPV by node size and governance condition

## Interpretation rule
Outputs are to be interpreted primarily as ordinal rankings and feasibility boundaries, not false-precision forecasts.

## Archival note
This file is the concise canonical spine for the federated SNRS workstream. Supporting white papers, addenda, ontology notes, and notebook drafts remain valuable as provenance, but this file should be treated as the source of truth for current architecture and simulation direction.
