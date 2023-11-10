from dataclasses import dataclass
from os import getenv

@dataclass(frozen=True)
class BackOffConfs:
    max_restart : int = int(getenv("MAX_RESTART",7))
    exponential_ratio : int = int(getenv("EXPONENTIAL_RATIO",2))
    is_enabled : bool = bool(int(getenv("ENABLE_BACKOFF",1)))


