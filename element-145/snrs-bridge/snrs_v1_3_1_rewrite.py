# SNRS v1.3.1 (rewrite) — phase-1 Monte Carlo scaffold
# Focus: comparative validity, causal flows, distributionally-correct subcluster aggregation.

import numpy as np
import pandas as pd
from scipy.stats import triang

# ----------------------------
# Globals / constants
discount_rate = 0.03
years = 100
persons_per_unit = 1.5

baseline_energy_cost = 300.0   # USD/unit/year
baseline_water_cost = 150.0    # USD/unit/year
baseline_maintenance = 500.0   # USD/unit/year

annual_food_cost_per_person = 1200.0
baseline_fertilizer_cost_per_person = 50.0

# ----------------------------
def rtri(a, m, b, rng: np.random.Generator):
    """Sample scalar triangular(a, m, b) using scipy triang with explicit RNG."""
    c = (m - a) / (b - a)
    return triang.rvs(c, loc=a, scale=(b - a), random_state=rng)

def discount_factors():
    t = np.arange(years + 1)
    return 1.0 / ((1.0 + discount_rate) ** t)

scenario_mult = {
    "A": {"wrapper_capex": 0.8, "hard_savings": 1.0, "eff_savings": 1.0, "policy_lag": 1.0, "participation": 1.0, "degradation": 1.0},
    "B": {"wrapper_capex": 1.0, "hard_savings": 1.2, "eff_savings": 1.1, "policy_lag": 0.9, "participation": 1.1, "degradation": 0.9},
    "C": {"wrapper_capex": 1.2, "hard_savings": 1.4, "eff_savings": 1.2, "policy_lag": 0.8, "participation": 1.2, "degradation": 0.8},
}

trust_mult = {
    "high": {"policy_lag_factor": 0.8, "aband_factor": 0.5, "participation_factor": 1.2},
    "low":  {"policy_lag_factor": 1.5, "aband_factor": 2.0, "participation_factor": 0.7},
}

# ----------------------------
def simulate_node_once(node_pop: int, scenario: str, trust: str, S_hard: float,
                       rng: np.random.Generator,
                       overhead_policy_lag=1.0, overhead_maintenance=1.0, capex_efficiency=1.0,
                       adoption_asymptote=0.8,
                       include_writeoff_recovery=False):
    """
    One Monte Carlo draw for a single node. Returns scalar NPV (USD), plus terminal-year physical outputs.
    Phase-1: conversion-based material recovery is modeled causally; write-off recovery is excluded by default.
    """
    sm = scenario_mult[scenario]
    tm = trust_mult[trust]

    include_food = (scenario != "A")
    include_comp = (scenario != "A")

    # ---- draws (shares)
    p_ready = rtri(0.2, 0.3, 0.4, rng)
    p_salv  = rtri(0.3, 0.4, 0.5, rng)
    p_wo    = rtri(0.05, 0.1, 0.15, rng)
    tot = p_ready + p_salv + p_wo
    p_ready, p_salv, p_wo = p_ready/tot, p_salv/tot, p_wo/tot

    # ---- costs / recovery
    C_ready = rtri(20000, 35000, 60000, rng)
    C_salv  = rtri(50000, 80000, 120000, rng)

    R_ready = rtri(1000, 2500, 5000, rng)
    R_salv  = rtri(5000, 10000, 15000, rng)
    R_wo    = rtri(2000, 4000, 8000, rng)

    # ---- other draws
    f_energy = rtri(0.2, 0.3, 0.4, rng)
    f_water  = rtri(0.3, 0.4, 0.5, rng)
    H_save   = rtri(200, 350, 500, rng)

    T80      = rtri(40, 55, 70, rng)
    lag_conv = rtri(1, 2, 3, rng)
    lag_pol0 = rtri(2, 3.5, 5, rng)
    lag_policy = lag_pol0 * tm["policy_lag_factor"] * sm["policy_lag"] * overhead_policy_lag
    lag_total = int(round(lag_conv + lag_policy))

    deg_base = rtri(0.01, 0.02, 0.03, rng)
    aband0   = rtri(0.005, 0.01, 0.02, rng)
    aband_rate = aband0 * tm["aband_factor"]

    part0 = rtri(0.1, 0.2, 0.3, rng)
    part_rate = part0 * tm["participation_factor"] * sm["participation"]
    if not include_comp:
        part_rate = 0.0

    retention = rtri(0.5, 0.65, 0.8, rng)
    red_maint = rtri(0.05, 0.1, 0.15, rng)
    red_deg   = rtri(0.1, 0.2, 0.3, rng)

    if include_food:
        food_offset = rtri(0.1, 0.2, 0.3, rng)
        nutrient_recovery = rtri(0.1, 0.25, 0.4, rng)
        fert_offset = rtri(0.05, 0.1, 0.2, rng)
        food_opex_p = rtri(20, 50, 100, rng)
    else:
        food_offset = nutrient_recovery = fert_offset = food_opex_p = 0.0

    if include_comp:
        comp_opex_p = rtri(10, 25, 50, rng)
        comp_offset = rtri(0.01, 0.03, 0.05, rng)
    else:
        comp_opex_p = comp_offset = 0.0

    reuse_richness = rtri(0.5, 1.0, 1.5, rng)

    # ---- weighted averages
    recoverable_share = p_ready + p_salv
    C_avg = (p_ready*C_ready + p_salv*C_salv) / recoverable_share
    # Conversion recovery applies only to converted classes:
    R_conv_avg = (p_ready*R_ready + p_salv*R_salv) / recoverable_share

    # Optional: if you want write-off recovery, you'd need a demolition flow; we default off.
    # Keeping include_writeoff_recovery flag reserved for future pass.
    _ = R_wo
    _ = include_writeoff_recovery

    # ---- stock cap and adoption
    max_units = (node_pop / persons_per_unit) * reuse_richness
    target_households = node_pop / persons_per_unit

    t = np.arange(years + 1)
    k = 4.0 / T80
    t_mid = 0.8 * T80
    f_served = 1.0 / (1.0 + np.exp(-k * (t - t_mid)))

    effective_f = np.zeros(years + 1)
    if lag_total <= years:
        effective_f[lag_total:] = f_served[:(years + 1 - lag_total)]

    cumulative_desired = adoption_asymptote * target_households * effective_f
    cumulative_units = np.minimum(cumulative_desired, max_units)

    occupied = np.zeros(years + 1)
    for i in range(1, years + 1):
        new_units = max(0.0, cumulative_units[i] - cumulative_units[i - 1])
        occupied[i] = occupied[i - 1] * (1.0 - aband_rate) + new_units

    # ---- capability
    if part_rate > 0:
        trained = part_rate * np.minimum(t / 20.0, 1.0)
        retained = trained * retention
        maint_factor = 1.0 - retained * red_maint
        deg_factor = 1.0 - retained * red_deg
    else:
        maint_factor = np.ones(years + 1)
        deg_factor = np.ones(years + 1)

    effective_deg = deg_base * deg_factor * sm["degradation"]

    # ---- annual flows
    annual_capex = np.zeros(years + 1)
    annual_benefit = np.zeros(years + 1)
    annual_maint = np.zeros(years + 1)
    annual_food_opex = np.zeros(years + 1)
    annual_comp_opex = np.zeros(years + 1)
    annual_recovery = np.zeros(years + 1)

    for i in range(1, years + 1):
        units = occupied[i]
        new_units = max(0.0, cumulative_units[i] - cumulative_units[i - 1])

        # capex
        annual_capex[i] = new_units * C_avg * sm["wrapper_capex"] * capex_efficiency

        # recovery (conversion only)
        annual_recovery[i] = new_units * R_conv_avg

        # per-unit benefits
        energy_save = baseline_energy_cost * f_energy * sm["eff_savings"]
        water_save  = baseline_water_cost  * f_water  * sm["eff_savings"]
        health_save = H_save * persons_per_unit

        if include_food:
            food_benefit = (
                annual_food_cost_per_person * persons_per_unit * food_offset
                + baseline_fertilizer_cost_per_person * persons_per_unit * nutrient_recovery * fert_offset
            )
            annual_food_opex[i] = units * food_opex_p * persons_per_unit
        else:
            food_benefit = 0.0

        if include_comp:
            comp_benefit = (energy_save + water_save) * comp_offset * sm["eff_savings"]
            annual_comp_opex[i] = units * comp_opex_p * persons_per_unit
        else:
            comp_benefit = 0.0

        per_unit_total = (S_hard * sm["hard_savings"]) + energy_save + water_save + health_save + food_benefit + comp_benefit
        annual_benefit[i] = units * per_unit_total

        # maintenance: intentionally punitive compounding stressor; candidate for calibration/capping
        maint_base = baseline_maintenance * maint_factor[i]
        maint_with_deg = maint_base * ((1.0 + effective_deg[i]) ** i)
        annual_maint[i] = units * maint_with_deg * overhead_maintenance

    net_cf = annual_benefit - annual_capex - annual_maint - annual_food_opex - annual_comp_opex + annual_recovery
    npv = float(np.sum(net_cf * discount_factors()))

    terminal_units = occupied[-1]
    terminal_energy_save = terminal_units * (baseline_energy_cost / 0.12) * f_energy * sm["eff_savings"]  # kWh/year (using original implied conversion)
    terminal_water_save  = terminal_units * (baseline_water_cost / 1.5) * f_water * sm["eff_savings"]    # m3/year  (using original implied conversion)

    return {
        "npv_usd": npv,
        "terminal_units": terminal_units,
        "terminal_energy_kwh_per_year": terminal_energy_save,
        "terminal_water_m3_per_year": terminal_water_save,
        "material_recovery_usd_total": float(np.sum(annual_recovery)),
        "food_self_provision_percent": float(food_offset * 100.0) if include_food else 0.0,
    }

# ----------------------------
def simulate_node(node_pop, scenario, trust, S_hard, n_sims=200, seed=42, **kwargs):
    rng = np.random.default_rng(seed)
    npvs = []
    water = []
    energy = []
    recovery = []
    food = []
    for _ in range(n_sims):
        out = simulate_node_once(node_pop, scenario, trust, S_hard, rng, **kwargs)
        npvs.append(out["npv_usd"])
        water.append(out["terminal_water_m3_per_year"])
        energy.append(out["terminal_energy_kwh_per_year"])
        recovery.append(out["material_recovery_usd_total"])
        food.append(out["food_self_provision_percent"])

    npvs = np.array(npvs)
    return {
        "npv_median_MUSD": np.median(npvs) / 1e6,
        "npv_p5_MUSD": np.percentile(npvs, 5) / 1e6,
        "npv_p95_MUSD": np.percentile(npvs, 95) / 1e6,
        "prob_positive": float(np.mean(npvs > 0.0)),
        "terminal_water_Mm3_per_year_median": np.median(water) / 1e6,
        "terminal_energy_TWh_per_year_median": (np.median(energy) / 1e9),
        "material_recovery_MUSD_median": np.median(recovery) / 1e6,
        "food_self_provision_percent_median": float(np.median(food)),
    }

# ----------------------------
def simulate_subcluster_distributionally_correct(scenario, trust, S_hard,
                                                n_sims=200, seed=123,
                                                overhead_policy=1.1, overhead_maintenance=1.1, capex_efficiency=0.95):
    """
    For each MC draw: simulate 5 independent 20k nodes and sum NPVs within the draw.
    This yields a correct distribution for the 5x20k system.
    """
    rng = np.random.default_rng(seed)
    npvs = []
    water = []
    energy = []
    recovery = []
    food = []

    for _ in range(n_sims):
        npv_sum = 0.0
        w_sum = 0.0
        e_sum = 0.0
        r_sum = 0.0
        food_vals = []

        for __ in range(5):
            out = simulate_node_once(
                20000, scenario, trust, S_hard, rng,
                overhead_policy_lag=overhead_policy,
                overhead_maintenance=overhead_maintenance,
                capex_efficiency=capex_efficiency,
            )
            npv_sum += out["npv_usd"]
            w_sum += out["terminal_water_m3_per_year"]
            e_sum += out["terminal_energy_kwh_per_year"]
            r_sum += out["material_recovery_usd_total"]
            food_vals.append(out["food_self_provision_percent"])

        npvs.append(npv_sum)
        water.append(w_sum)
        energy.append(e_sum)
        recovery.append(r_sum)
        food.append(float(np.mean(food_vals)) if len(food_vals) else 0.0)

    npvs = np.array(npvs)
    return {
        "npv_median_MUSD": np.median(npvs) / 1e6,
        "npv_p5_MUSD": np.percentile(npvs, 5) / 1e6,
        "npv_p95_MUSD": np.percentile(npvs, 95) / 1e6,
        "prob_positive": float(np.mean(npvs > 0.0)),
        "terminal_water_Mm3_per_year_median": np.median(water) / 1e6,
        "terminal_energy_TWh_per_year_median": (np.median(energy) / 1e9),
        "material_recovery_MUSD_median": np.median(recovery) / 1e6,
        "food_self_provision_percent_median": float(np.median(food)),
    }

# ----------------------------
def find_threshold_S_hard(node_pop, scenario, trust, S_grid, n_sims=80, seed=7):
    """
    Find smallest S_hard where median NPV crosses >= 0 (linear interpolation with guard).
    """
    med_npvs = []
    for S in S_grid:
        res = simulate_node(node_pop, scenario, trust, S, n_sims=n_sims, seed=seed)
        med_npvs.append(res["npv_median_MUSD"])

    crossing = np.nan
    for i in range(len(S_grid) - 1):
        npv1, npv2 = med_npvs[i], med_npvs[i + 1]
        if npv1 <= 0.0 and npv2 >= 0.0:
            S1, S2 = float(S_grid[i]), float(S_grid[i + 1])
            if npv2 == npv1:
                crossing = S2  # degenerate; pick upper grid value
            else:
                crossing = S1 - npv1 * (S2 - S1) / (npv2 - npv1)
            break

    return float(crossing), med_npvs

# ----------------------------
if __name__ == "__main__":
    node_sizes = [5000, 10000, 50000, 100000, 250000, 1000000]
    scenarios = ["A", "B", "C"]
    trusts = ["high", "low"]

    S_grid = np.arange(0, 8500, 500)

    rows = []
    thr_rows = []

    for pop in node_sizes:
        for sc in scenarios:
            for tr in trusts:
                thr, _ = find_threshold_S_hard(pop, sc, tr, S_grid, n_sims=50)
                thr_rows.append({"node_pop": pop, "scenario": sc, "trust": tr, "min_S_hard_USD": thr})

                base = simulate_node(pop, sc, tr, S_hard=3500, n_sims=200, seed=42)
                base.update({"node_pop": pop, "scenario": sc, "trust": tr})
                rows.append(base)

    # Subcluster (5x20k) as distributionally-correct system
    for sc in scenarios:
        for tr in trusts:
            base = simulate_subcluster_distributionally_correct(sc, tr, S_hard=3500, n_sims=200, seed=123)
            base.update({"node_pop": "100k_subcluster (5x20k)", "scenario": sc, "trust": tr})
            rows.append(base)

    df = pd.DataFrame(rows)
    thr_df = pd.DataFrame(thr_rows)

    print("\n=== SNRS v1.3.1 rewrite — baseline S_hard=$3500 ===\n")
    print(df.round(3).to_string(index=False))

    print("\n=== Thresholds (rewrite) — min S_hard for median NPV >= 0 ===\n")
    print(thr_df.round(2).to_string(index=False))