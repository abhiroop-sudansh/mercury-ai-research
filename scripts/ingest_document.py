import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))


from mercury.documents.ingestion import ingest_document


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingest and standardize a financial document."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the raw JSON document.",
    )

    parser.add_argument(
        "--output-dir",
        default="data/processed/documents",
        help="Directory for standardized documents.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    try:
        input_path = Path(args.input)
        output_directory = Path(args.output_dir)

        output_path = ingest_document(
            input_path=input_path,
            output_directory=output_directory,
        )

        result = {
            "status": "success",
            "input_path": str(input_path),
            "output_path": str(output_path),
        }

        print(json.dumps(result, indent=2))

    except Exception as exc:
        error_result = {
            "status": "error",
            "error_type": type(exc).__name__,
            "message": str(exc),
        }

        print(json.dumps(error_result, indent=2))
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()