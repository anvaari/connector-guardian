from dataclasses import dataclass

@dataclass(frozen=True)
class BackOffConfs:
    max_restart : int = 7
    exponential_ratio : int = 1


