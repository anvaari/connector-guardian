from configs.configs import BackOffConfs


def validate_backoff_configs() -> None:
    if BackOffConfs.exponential_ratio < 1:
        raise ValueError("`EXPONENTIAL_RATIO` must integer greater than 0, "
                         f"but {BackOffConfs.exponential_ratio} given.")
    if BackOffConfs.max_restart < 1:
        raise ValueError("`MAX_RESTART` must integer greater than 0, "
                         f"but {BackOffConfs.max_restart} given.")
