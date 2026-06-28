# Supply Chain & Logistics

Agents optimizing routes, forecasting demand, coordinating suppliers, and managing inventory face critical failures around data freshness, coordination, and demand-supply mismatches.

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Demand Forecasting](goals/demand-forecasting/) | Forecast accuracy, seasonality, bullwhip effect | In progress |
| [Route Optimization](goals/route-optimization/) | Route divergence, real-time conditions, constraint violations | In progress |
| [Supplier Coordination](goals/supplier-coordination/) | SLA tracking, lead time accuracy, diversification | In progress |
| [Inventory Control](goals/inventory-control/) | Stock-outs, safety stock, perishable goods | In progress |

**Status**: ~40 patterns planned

## Key Challenges

1. **Bullwhip Amplification**: Small demand variance cascades upstream
2. **Data Staleness**: Routes assume conditions that changed; traffic data old
3. **Supplier Reliability**: SLAs optimistic; real performance lagging
4. **Perishable Spoilage**: Shelf life not tracked per batch
5. **Multi-Warehouse Sync**: Global inventory visibility missing
