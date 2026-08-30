# Executive BI and decision-intelligence dashboard

## Page 1 — Revenue command center

- Modeled expected value, realized value and value-realization rate
- Revenue at risk by customer, geography and product
- Recommended interventions by urgency and owner
- Data freshness and pipeline health
- Drill-through from executive KPI to order, source events and receipt

## Page 2 — Predictive model performance

- Precision, recall, false-positive cost and false-negative exposure
- Calibration plot and Brier score
- Performance by customer tier, region and order-value band
- Prediction drift and feature-distribution drift
- Model-version comparison with promotion boundary

## Page 3 — Prescriptive action performance

- Expected versus realized value by action
- Intervention cost and acceptance rate
- Incremental value by treatment cohort
- Actions rejected by operators and recorded reasons
- Counterfactual baseline and confidence interval

## Page 4 — Data-platform unit economics

- Cost per million events and per successful intervention
- Streaming, storage, query and model-serving cost allocation
- Freshness SLO attainment
- Cost and value by tenant, workflow and cloud
- Azure managed-service versus OSS/hybrid comparison

## Semantic-model rules

- Currency measures use explicit USD normalization and retain source currency.
- Slowly changing customer attributes use a type-2 dimension.
- Predictions and outcomes remain separate to prevent label leakage.
- Expected value and realized value are never presented as interchangeable.
- Every executive metric can drill through to source lineage and the immutable decision receipt.
