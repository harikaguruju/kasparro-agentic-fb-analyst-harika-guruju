\# Kasparro Agentic Facebook Performance Analyst



This repository contains my solution for the Kasparro Applied AI Engineer Assignment — Agentic Facebook Performance Analyst.



The system is a multi-agent AI pipeline that analyzes Facebook Ads performance data, detects ROAS drops, generates insights, validates hypotheses, and suggests creative improvements.



---



\## 🚀 Key Features



\- Multi-agent architecture (Planner, Data Agent, Insight Agent, Evaluator, Creative Generator)

\- Automatic ROAS drop detection

\- Campaign-level low CTR detection

\- Hypothesis generation \& validation

\- Creative recommendation generation

\- Markdown + JSON reporting

\- Test-driven validation using Pytest



---



\## 🧠 System Workflow



1\. User enters a query (example: "Analyze ROAS drop in last 7 days")

2\. Planner agent breaks it into tasks

3\. Data Agent loads and summarizes the dataset

4\. Insight Agent generates performance hypotheses

5\. Evaluator validates hypotheses using metrics

6\. Creative Generator produces creative suggestions

7\. Final results are saved to the `reports/` folder



---



\## 📂 Project Structure





