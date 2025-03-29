"""Error handling module for the automation system"""
from src.core.errors.error_types import ErrorType, Error
from src.core.errors.error_listener import ErrorListener, ErrorEvent
from src.core.errors.recovery_strategy import RecoveryStrategy, RecoveryResult
from src.core.errors.error_manager import ErrorManager
