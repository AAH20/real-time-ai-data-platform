# Real-time revenue-at-risk predictive and prescriptive analytics

**Evidence:** `deterministic-synthetic-case-study`  
**Receipt:** `86c813261653d3a49387aac648209da083e2ff5dacec369232b5be85098707fd`  
**Automation:** `disabled`

## Executive decision scorecard

- Modeled net expected value: `$283,778.86`
- Modeled return per platform dollar: `35.47x`
- Recommended interventions: `7`
- Predictive precision: `100.00%`
- Predictive recall: `85.71%`
- Brier score: `0.0487`

## Prescriptive decisions

| Order | Customer | Risk | Band | Recommendation | Expected value |
|---|---|---:|---|---|---:|
| ORD-1001 | ACME-EU | 96.1% | critical | reroute-inventory | $32,854.00 |
| ORD-1002 | NOVA-US | 6.6% | low | observe | $0.00 |
| ORD-1003 | ORBIT-UK | 82.4% | critical | reroute-inventory | $46,966.00 |
| ORD-1004 | KINETIC-AE | 19.0% | low | observe | $0.00 |
| ORD-1005 | HELIX-DE | 98.7% | critical | reroute-inventory | $67,672.00 |
| ORD-1006 | SUMMIT-CA | 40.3% | medium | reroute-inventory | $20,533.26 |
| ORD-1007 | PULSE-AU | 5.3% | low | observe | $0.00 |
| ORD-1008 | VERTEX-FR | 86.2% | critical | reroute-inventory | $39,406.00 |
| ORD-1009 | LUMEN-NL | 16.2% | low | observe | $0.00 |
| ORD-1010 | ATLAS-US | 93.1% | critical | reroute-inventory | $56,416.00 |
| ORD-1011 | EMBER-SE | 8.0% | low | observe | $0.00 |
| ORD-1012 | QUANTUM-SG | 69.1% | high | reroute-inventory | $27,931.60 |

## Claim boundary

- All customers, orders, outcomes, prices and costs are synthetic scenario inputs
- Predictive performance on this small deterministic fixture is not evidence of production accuracy
- Expected value is modeled opportunity, not realized revenue or guaranteed savings
- No Microsoft Fabric, Databricks, Kafka cloud service or customer data was accessed
