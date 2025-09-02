"""
Public API: Only expose MusicQueryController.
"""
from .application.music_query_controller import MusicQueryController

__all__ = ["MusicQueryController"]
