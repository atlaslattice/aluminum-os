from element145.contracts import (
    BudgetTier,
    ConsentDecision,
    EpistemicState,
    ExecutionPlan,
    RoutingDecision,
    SafetyState,
    SphereQuery,
)


def test_contract_roundtrip():
    query = SphereQuery(
        query_id="q1",
        trace_id="t1",
        raw_input={"action": "read"},
        source="test",
    )
    decision = RoutingDecision(
        trace_id="t1",
        query_id="q1",
        house=0,
        sphere=0,
        epistemic_state=EpistemicState.KNOWN,
        safety_state=SafetyState.SAFE,
        selected_path="fast",
        selected_providers=["local_stub"],
        provider_weights={"local_stub": 1.0},
        policy_checks=[],
        budget_tier=BudgetTier.T2_FAST_LOW_COST,
        requires_human_approval=False,
        routing_reason="test",
    )
    consent = ConsentDecision(
        trace_id="t1",
        action_type="read",
        destructive=False,
        allowed=True,
        reason="test",
    )
    plan = ExecutionPlan(
        trace_id="t1",
        route=decision,
        consent=consent,
        operations=[{"provider": "local_stub", "type": "read"}],
    )

    assert query.trace_id == "t1"
    assert plan.route.epistemic_state == EpistemicState.KNOWN
    assert plan.consent.allowed is True
