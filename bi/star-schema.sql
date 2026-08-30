CREATE TABLE dim_customer (
    customer_key BIGINT PRIMARY KEY,
    customer_id VARCHAR(64) UNIQUE NOT NULL,
    customer_tier VARCHAR(32) NOT NULL,
    region VARCHAR(32) NOT NULL,
    effective_from TIMESTAMP NOT NULL,
    effective_to TIMESTAMP,
    is_current BOOLEAN NOT NULL
);

CREATE TABLE dim_action (
    action_key INTEGER PRIMARY KEY,
    action_name VARCHAR(64) UNIQUE NOT NULL,
    action_category VARCHAR(32) NOT NULL
);

CREATE TABLE fact_revenue_risk_decision (
    decision_id VARCHAR(64) PRIMARY KEY,
    event_time TIMESTAMP NOT NULL,
    customer_key BIGINT NOT NULL REFERENCES dim_customer(customer_key),
    action_key INTEGER NOT NULL REFERENCES dim_action(action_key),
    order_id VARCHAR(64) NOT NULL,
    model_version VARCHAR(64) NOT NULL,
    predicted_delay_probability DECIMAL(8,6) NOT NULL,
    actual_delayed BOOLEAN,
    order_value_usd DECIMAL(18,2) NOT NULL,
    expected_loss_usd DECIMAL(18,2) NOT NULL,
    intervention_cost_usd DECIMAL(18,2) NOT NULL,
    expected_value_usd DECIMAL(18,2) NOT NULL,
    realized_value_usd DECIMAL(18,2),
    data_freshness_seconds INTEGER NOT NULL,
    evidence_receipt_sha256 CHAR(64) NOT NULL
);

CREATE INDEX ix_decision_event_time ON fact_revenue_risk_decision(event_time);
CREATE INDEX ix_decision_customer ON fact_revenue_risk_decision(customer_key, event_time);
