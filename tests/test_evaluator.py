from src.agents.evaluator import Evaluator

def test_evaluator_runs_basic_validation():
    """
    Basic smoke test:
    Ensures Evaluator.validate() can run on a minimum summary structure
    without throwing errors.
    """

    cfg = {
        "low_ctr_threshold": 0.01,
        "min_impressions_for_stat": 10
    }

    evaluator = Evaluator(cfg)

    # Minimal synthetic daily data for ROAS validation
    summary = {
        "daily": [
            {"roas": 1.0, "spend": 100, "impressions": 1000},
            {"roas": 0.9, "spend": 110, "impressions": 900},
            {"roas": 1.1, "spend": 90, "impressions": 1100},
            {"roas": 0.95, "spend": 120, "impressions": 950},
            {"roas": 0.85, "spend": 100, "impressions": 1050},
            {"roas": 0.75, "spend": 130, "impressions": 980},
            {"roas": 0.67, "spend": 140, "impressions": 970},
            {"roas": 0.55, "spend": 150, "impressions": 960},
            {"roas": 0.50, "spend": 155, "impressions": 950},
            {"roas": 0.40, "spend": 160, "impressions": 940},
            {"roas": 0.35, "spend": 165, "impressions": 930},
            {"roas": 0.30, "spend": 170, "impressions": 920},
            {"roas": 0.28, "spend": 175, "impressions": 910},
            {"roas": 0.25, "spend": 180, "impressions": 900},
        ],
        "campaign": [],
        "low_ctr_campaigns": [],
        "recent_summary": {}
    }

    hypotheses = [
        {"hypothesis_id": "h_roas_drop", "hypothesis": "ROAS dropped"}
    ]

    result = evaluator.validate(hypotheses, summary)

    assert isinstance(result, list)
    assert len(result) == 1
