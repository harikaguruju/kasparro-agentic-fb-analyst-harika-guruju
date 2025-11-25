#!/usr/bin/env python3
import os
import json
import argparse
import yaml
from src.agents.planner import Planner
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import Evaluator
from src.agents.creative_generator import CreativeGenerator

CONFIG_PATH = "config/config.yaml"

def load_config(path=CONFIG_PATH):
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="User query, e.g. 'Analyze ROAS drop'")
    args = parser.parse_args()

    cfg = load_config()

    planner = Planner(cfg)
    data_agent = DataAgent(cfg)
    insight_agent = InsightAgent(cfg)
    evaluator = Evaluator(cfg)
    creative = CreativeGenerator(cfg)

    # 1. Planner decomposes the query into tasks
    tasks = planner.plan(args.query)

    # 2. Data agent loads and summarizes the dataset
    summary = data_agent.load_and_summarize()

    # 3. Insight agent generates hypotheses
    hypotheses = insight_agent.generate_hypotheses(summary)

    # 4. Evaluator validates hypotheses
    validations = evaluator.validate(hypotheses, summary)

    # 5. Creative generator produces new ideas for low-CTR campaigns
    creatives = creative.generate(summary)

    # Save outputs
    os.makedirs("reports", exist_ok=True)

    with open("reports/insights.json", "w") as f:
        json.dump(hypotheses, f, indent=2)

    with open("reports/validations.json", "w") as f:
        json.dump(validations, f, indent=2)

    with open("reports/creatives.json", "w") as f:
        json.dump(creatives, f, indent=2)

    # Create report.md
    report_lines = []
    report_lines.append("# Final Report\n")
    report_lines.append("## Hypotheses\n")
    for h in hypotheses:
        report_lines.append(f"- **{h.get('hypothesis_id')}**: {h.get('hypothesis')} (confidence={h.get('confidence')})")

    report_lines.append("\n## Validations\n")
    for v in validations:
        report_lines.append(f"- **{v.get('hypothesis_id')}** → validated: {v.get('validated')}, evidence: {v.get('evidence')}")

    report_lines.append("\n## Creative Suggestions Generated\n")
    report_lines.append("See `creatives.json` for full outputs.")

    with open("reports/report.md", "w") as f:
        f.write("\n".join(report_lines))

    print("Done! Outputs saved in reports/ folder.")

if __name__ == "__main__":
    main()
