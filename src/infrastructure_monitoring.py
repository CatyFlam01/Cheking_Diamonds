from __future__ import annotations

import json

from src.monitoring import get_infrastructure_metrics


def main() -> None:
    print(json.dumps(get_infrastructure_metrics(), indent=2))


if __name__ == "__main__":
    main()
