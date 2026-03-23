-- Royalty Runtime: Execution Events Ledger
-- v0.1 Schema — "Store first, verify clearly, interpret later"

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE execution_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL,
    primary_package TEXT NOT NULL,
    lineage_hash TEXT NOT NULL,
    lineage_payload_version TEXT NOT NULL,
    runtime_name TEXT NOT NULL,
    runtime_version TEXT NOT NULL,
    event_timestamp BIGINT NOT NULL,
    sdk_version TEXT,
    premium_path_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    lease_id TEXT,
    payload_json JSONB NOT NULL,
    hash_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verification_error TEXT,
    received_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_execution_events_session_id ON execution_events (session_id);
CREATE INDEX idx_execution_events_primary_package ON execution_events (primary_package);
CREATE INDEX idx_execution_events_lineage_hash ON execution_events (lineage_hash);
CREATE INDEX idx_execution_events_received_at ON execution_events (received_at DESC);
CREATE INDEX idx_execution_events_event_timestamp ON execution_events (event_timestamp DESC);
CREATE INDEX idx_execution_events_payload_json_gin ON execution_events USING GIN (payload_json);
CREATE INDEX idx_execution_events_lease_id ON execution_events (lease_id) WHERE lease_id IS NOT NULL;
CREATE INDEX idx_execution_events_premium ON execution_events (premium_path_enabled) WHERE premium_path_enabled = TRUE;