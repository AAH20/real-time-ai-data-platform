# Unit-economics contract

The platform separates infrastructure efficiency from business value.

## Infrastructure units

- Cost per million events ingested
- Cost per GB transformed
- Cost per TB stored and queried
- Cost per 1,000 predictions
- Cross-cloud egress cost per workflow

## Data-product units

- Cost per valid and fresh customer/order state
- Cost per query with complete lineage
- Cost per schema-breaking incident avoided
- Freshness-SLO attainment by data product

## Business-workflow units

- Cost per evaluated order
- Cost per recommended intervention
- Cost per accepted intervention
- Modeled expected value per intervention
- Realized incremental value per intervention
- Return per platform dollar

## Required causal boundary

Expected value is a decision-model output. Realized value must be measured later against an appropriate control or counterfactual. A dashboard must never relabel expected value as savings or revenue.

The included synthetic scenario processes 500 million modeled events at a configurable $16 per million, producing an $8,000 modeled platform cost. These are scenario assumptions rather than Azure, Microsoft Fabric or vendor quotations.
