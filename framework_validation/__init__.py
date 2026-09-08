"""Website Director framework self-validation and bounded execution package."""

from .validator import validate_repository

_CLEAN_ROOM_EXPORTS = {
    "CleanRoomExecutionAdapters",
    "CleanRoomExecutionRequest",
    "CleanRoomManifest",
    "execute_clean_room_workflow",
    "prepare_clean_room_concept_run",
    "run_clean_room_creative_mode",
    "validate_owner_concept_selection",
    "validate_pre_generation_scope",
}

__all__ = [
    "CleanRoomExecutionAdapters",
    "CleanRoomExecutionRequest",
    "CleanRoomManifest",
    "execute_clean_room_workflow",
    "prepare_clean_room_concept_run",
    "run_clean_room_creative_mode",
    "validate_owner_concept_selection",
    "validate_pre_generation_scope",
    "validate_repository",
]


def __getattr__(name: str):
    if name in _CLEAN_ROOM_EXPORTS:
        from . import clean_room

        return getattr(clean_room, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
