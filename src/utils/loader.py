import logging
from typing import List, Optional

import pandas as pd

logger = logging.getLogger(__name__)

# Minimal schema we expect from the FB ads dataset.
# (If any of these are missing we fail fast with a clear error.)
EXPECTED_COLUMNS: List[str] = [
    "date",
    "spend",
    "impressions",
    "clicks",
    "revenue",
]


def validate_schema(
    df: pd.DataFrame,
    expected_columns: Optional[List[str]] = None,
) -> None:
    """
    Validate that the dataframe has the required columns.

    Raises:
        ValueError: if required columns are missing.
    """
    if expected_columns is None:
        expected_columns = EXPECTED_COLUMNS

    missing = [col for col in expected_columns if col not in df.columns]
    extra = [col for col in df.columns if col not in expected_columns]

    if missing:
        logger.error("Schema validation failed. Missing columns: %s", missing)
        raise ValueError(f"Missing required columns: {missing}")

    if extra:
        # Extra columns are not fatal, but we log them for debugging.
        logger.warning("Extra columns present in dataset: %s", extra)

    logger.info("Schema validation passed. All required columns are present.")


def load_csv(
    path: str,
    expected_columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Load a CSV with retries + schema validation.

    Args:
        path: Path to CSV file.
        expected_columns: Optional explicit schema to validate.

    Returns:
        Pandas DataFrame.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if schema validation fails.
        Exception: for repeated unexpected errors.
    """
    if expected_columns is None:
        expected_columns = EXPECTED_COLUMNS

    # Simple retry loop to handle transient read errors.
    max_attempts = 3
    last_error: Optional[Exception] = None

    for attempt in range(1, max_attempts + 1):
        try:
            logger.info("Loading CSV from %s (attempt %d/%d)", path, attempt, max_attempts)
            df = pd.read_csv(path, parse_dates=["date"], infer_datetime_format=True)
            logger.info("CSV loaded successfully: %d rows x %d columns", df.shape[0], df.shape[1])

            validate_schema(df, expected_columns)

            if df.empty:
                logger.error("Loaded CSV is empty after reading: %s", path)
                raise ValueError("Dataset is empty after loading")

            return df

        except FileNotFoundError:
            logger.error("Data file not found at path: %s", path)
            raise  # no point retrying

        except Exception as exc:  # noqa: BLE001
            last_error = exc
            logger.exception("Unexpected error while loading CSV (attempt %d)", attempt)

    # If we reach here, all attempts failed.
    assert last_error is not None
    logger.error("Failed to load CSV after %d attempts. Last error: %s", max_attempts, last_error)
    raise last_error
