# Planner Agent Prompt

**Goal:** Given a user instruction (e.g., "Analyze ROAS drop in last 7 days"), decompose into a clear, ordered set of subtasks for the Data Agent, Insight Agent, Evaluator, and Creative Generator.

**Input:** short natural-language user query + high-level config (thresholds).

**Constraints:**
- Use summaries (aggregates) produced by Data Agent — do NOT expect full CSV.
- Produce tasks that are actionable and include expected outputs and confidence requirements.
- Provide retry/reflection logic: if an agent returns low-confidence, the planner should add a "re-run with adjusted params" task.

**Output (JSON):**
```json
{
  "tasks": [
    {
      "id": "load_summary",
      "agent": "data_agent",
      "desc": "Load dataset and produce daily/campaign summaries",
      "expected_output": "summary dict"
    },
    {
      "id": "detect_drop_periods",
      "agent": "data_agent",
      "desc": "Identify date windows with ROAS drops",
      "expected_output": "list of windows with metrics"
    },
    {
      "id": "generate_hypotheses",
      "agent": "insight_agent",
      "desc": "Produce candidate hypotheses with expected signals and confidence"
    },
    {
      "id": "validate_hypotheses",
      "agent": "evaluator",
      "desc": "Run quantitative tests and return validation records"
    },
    {
      "id": "creative_recommendations",
      "agent": "creative_generator",
      "desc": "Produce new creative messages for low-CTR campaigns"
    }
  ]
}
