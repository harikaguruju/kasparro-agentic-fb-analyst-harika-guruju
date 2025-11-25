# Data Agent Prompt

**Goal:** Load the dataset, validate schema, clean metrics, compute summaries, and return structured aggregates for downstream agents.

**Required Behaviors:**
- Load CSV from path provided by config or environment variable.
- Validate presence of key columns:
  - campaign_name, adset_name, date, spend, impressions, clicks,
    purchases, revenue, roas, creative_type, creative_message,
    audience_type, platform, country
- Handle missing numeric values by coercing to 0.
- Compute:
  - CTR if missing: clicks / impressions
  - ROAS if missing: revenue / spend
- Produce:
  - Daily summary (date → impressions, clicks, spend, revenue, purchases, ctr, roas)
  - Campaign summary (campaign_name → same metrics)
  - Last 7-day performance summary
  - List of low-CTR campaigns (ctr < low_ctr_threshold from config)

**Output Format (JSON):**
```json
{
  "n_rows": 0,
  "date_range": ["YYYY-MM-DD", "YYYY-MM-DD"],
  "daily": [...],
  "campaign": [...],
  "recent_summary": {
    "impressions": 0,
    "clicks": 0,
    "spend": 0,
    "revenue": 0,
    "ctr": 0,
    "roas": 0
  },
  "low_ctr_campaigns": [...]
}
