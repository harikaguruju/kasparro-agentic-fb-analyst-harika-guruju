import logging
from dataclasses import dataclass
from typing import Dict, Any, List

import pandas as pd

from src.utils.loader import load_csv

logger = logging.getLogger(__name__)

# Columns we expect to exist in the dataset
REQUIRED_COLUMNS: List[str] = [
    "date",
    "campaign_name",
    "spend",
    "impressions",
    "clicks",
    "revenue",
]


@dataclass
class DataAgent:
    cfg: Dict[str, Any]

    def load_and_summarize(self) -> Dict[str, Any]:
        """
        Load the Facebook Ads dataset and compute a few high-level metrics.

        Returns a summary dict that at least contains:
          - df: the raw pandas DataFrame
          - totals: {spend, revenue, clicks, impressions}
          - overall: {ctr, roas}
        """
        data_path = self.cfg["data_csv"]
        logger.info("DataAgent: loading dataset from %s", data_path)

        df: pd.DataFrame = load_csv(
            data_path,
            required_columns=REQUIRED_COLUMNS,
        )

        logger.info(
            "DataAgent: dataset loaded with %d rows and %d columns",
            len(df),
            df.shape[1],
        )

        total_spend = float(df["spend"].sum())
        total_revenue = float(df["revenue"].sum())
        total_clicks = int(df["clicks"].sum())
        total_impressions = int(df["impressions"].sum())

        overall_ctr = (
            total_clicks / total_impressions if total_impressions > 0 else 0.0
        )
        overall_roas = (
            total_revenue / total_spend if total_spend > 0 else 0.0
        )

        logger.info(
            "DataAgent: totals – spend=%.2f, revenue=%.2f, clicks=%d, impressions=%d, CTR=%.4f, ROAS=%.2f",
            total_spend,
            total_revenue,
            total_clicks,
            total_impressions,
            overall_ctr,
            overall_roas,
        )

        summary: Dict[str, Any] = {
            "df": df,
            "totals": {
                "spend": total_spend,
                "revenue": total_revenue,
                "clicks": total_clicks,
                "impressions": total_impressions,
            },
            "overall": {
                "ctr": overall_ctr,
                "roas": overall_roas,
            },
        }

        return summary
