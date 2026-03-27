from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from packages.mlops_ml.config import Settings
from packages.mlops_ml.trainer import train_and_log


def main() -> None:
    settings = Settings()
    result = train_and_log(settings)
    print({"accuracy": result.accuracy, "model_path": result.model_path})


if __name__ == "__main__":
    main()
