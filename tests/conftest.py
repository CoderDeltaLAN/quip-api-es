import warnings

warnings.filterwarnings(
    "ignore",
    message=r".*on_event is deprecated.*",
    category=DeprecationWarning,
)
