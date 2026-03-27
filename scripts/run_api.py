from pathlib import Path
import sys

import uvicorn

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def main() -> None:
    uvicorn.run(
        "mlops_api.main:app",
        host="0.0.0.0",
        port=8000,
        app_dir=str(ROOT_DIR / "apps" / "api"),
    )


if __name__ == "__main__":
    main()
