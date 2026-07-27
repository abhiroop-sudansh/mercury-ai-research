import argparse
import json
import sys
from datetime import date
from pathlib import Path


# Find the main project folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Build the path to the src folder.
SRC_PATH = PROJECT_ROOT / "src"

# Allow Python to import the mercury package from src.
sys.path.insert(0, str(SRC_PATH))


from mercury.models import EventAnalysisRequest
from mercury.service import analyze_market_event


def parse_arguments() -> argparse.Namespace:
    """Read the stock symbol, event date, and benchmark from Terminal."""

    parser = argparse.ArgumentParser(
        description="Analyze stock returns around a market event."
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Stock ticker, for example NVDA",
    )

    parser.add_argument(
        "--event-date",
        required=True,
        help="Event date in YYYY-MM-DD format",
    )

    parser.add_argument(
        "--benchmark",
        default="SPY",
        help="Benchmark ticker; defaults to SPY",
    )

    return parser.parse_args()


def main() -> None:
    """Validate the input, run the analysis, and print the result."""

    args = parse_arguments()

    try:
        request = EventAnalysisRequest(
            symbol=args.symbol,
            event_date=date.fromisoformat(args.event_date),
            benchmark=args.benchmark,
        )

        result = analyze_market_event(request)

        output = result.model_dump(mode="json")

        print(json.dumps(output, indent=2))

    except Exception as exc:
        error_output = {
            "status": "error",
            "error_type": type(exc).__name__,
            "message": str(exc),
        }

        print(json.dumps(error_output, indent=2))
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()