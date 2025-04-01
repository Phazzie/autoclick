"""Workflow module for defining and executing workflows.

This module provides components for defining, validating, and executing workflows.
"""
# Import original components for backward compatibility
from src.core.workflow.workflow_engine_interface import WorkflowEngineInterface
from src.core.workflow.workflow_engine import WorkflowEngine as LegacyWorkflowEngine, WorkflowStatus
from src.core.workflow.workflow_event import (
    WorkflowEventType, WorkflowEvent as LegacyWorkflowEvent,
    WorkflowStateEvent, ActionEvent, EventDispatcher
)
from src.core.workflow.workflow_statistics import WorkflowStatistics
from src.core.workflow.workflow_service import WorkflowService as LegacyWorkflowService

# Import new components
from .interfaces import (
    WorkflowDefinition, ExecutionResult,
    IWorkflowValidator, IWorkflowExecutor, IWorkflowEngine, IEventBus,
    IWorkflow, IWorkflowStep, IWorkflowEventBus, IWorkflowEventListener
)
from .exceptions import (
    WorkflowError, WorkflowValidationError, WorkflowExecutionError,
    ActionExecutionError, WorkflowNotFoundError, InvalidWorkflowDefinitionError,
    CyclicDependencyError, MissingActionError, InvalidConnectionError
)
from .execution_result import ExecutionResult, ActionResult
from .workflow_validator import WorkflowValidator
from .workflow_executor import WorkflowExecutor
from .workflow_engine_new import WorkflowEngine
from ..events.workflow_events import (
    WorkflowEvent, WorkflowStartedEvent, WorkflowCompletedEvent, WorkflowFailedEvent,
    ActionStartedEvent, ActionCompletedEvent, ActionFailedEvent, VariableUpdatedEvent,
    ValidationEvent, EVENT_WORKFLOW_STARTED, EVENT_WORKFLOW_COMPLETED,
    EVENT_WORKFLOW_FAILED, EVENT_ACTION_STARTED, EVENT_ACTION_COMPLETED,
    EVENT_ACTION_FAILED, EVENT_VARIABLE_UPDATED, EVENT_VALIDATION_COMPLETED
)
from ..events.event_bus import EventBus

# Import service components
from .service_interfaces import (
    IWorkflowQuery, IWorkflowDTO, IWorkflowStepDTO,
    IWorkflowSerializer, IWorkflowRepository, IWorkflowService
)
from .service_exceptions import (
    WorkflowServiceError, WorkflowNotFoundError as ServiceWorkflowNotFoundError,
    WorkflowStepNotFoundError, WorkflowValidationError as ServiceWorkflowValidationError,
    WorkflowExecutionError as ServiceWorkflowExecutionError, WorkflowAlreadyExistsError,
    WorkflowRepositoryError, WorkflowSerializationError, WorkflowDeserializationError,
    WorkflowQueryError
)
from .workflow_dto import WorkflowDTO, WorkflowStepDTO
from .workflow_query import (
    WorkflowQuery, PropertyQuery, AndQuery, OrQuery, NotQuery,
    AllQuery, NoneQuery, WorkflowQueryBuilder
)
from .workflow_serializer_new import WorkflowSerializer
from .workflow_repository import FileSystemWorkflowRepository, InMemoryWorkflowRepository
from .workflow_service_new import WorkflowService

__all__ = [
    # Legacy components
    'WorkflowEngineInterface',
    'LegacyWorkflowEngine',
    'WorkflowStatus',
    'WorkflowEventType',
    'LegacyWorkflowEvent',
    'WorkflowStateEvent',
    'ActionEvent',
    'EventDispatcher',
    'WorkflowStatistics',
    'LegacyWorkflowService',

    # New interfaces
    'WorkflowDefinition', 'ExecutionResult',
    'IWorkflowValidator', 'IWorkflowExecutor', 'IWorkflowEngine', 'IEventBus',
    'IWorkflow', 'IWorkflowStep', 'IWorkflowEventBus', 'IWorkflowEventListener',

    # New exceptions
    'WorkflowError', 'WorkflowValidationError', 'WorkflowExecutionError',
    'ActionExecutionError', 'WorkflowNotFoundError', 'InvalidWorkflowDefinitionError',
    'CyclicDependencyError', 'MissingActionError', 'InvalidConnectionError',

    # New value objects
    'ExecutionResult', 'ActionResult',

    # New implementations
    'WorkflowValidator', 'WorkflowExecutor', 'WorkflowEngine',

    # New events
    'WorkflowEvent', 'WorkflowStartedEvent', 'WorkflowCompletedEvent', 'WorkflowFailedEvent',
    'ActionStartedEvent', 'ActionCompletedEvent', 'ActionFailedEvent', 'VariableUpdatedEvent',
    'ValidationEvent', 'EVENT_WORKFLOW_STARTED', 'EVENT_WORKFLOW_COMPLETED',
    'EVENT_WORKFLOW_FAILED', 'EVENT_ACTION_STARTED', 'EVENT_ACTION_COMPLETED',
    'EVENT_ACTION_FAILED', 'EVENT_VARIABLE_UPDATED', 'EVENT_VALIDATION_COMPLETED',

    # Event bus
    'EventBus',

    # Service interfaces
    'IWorkflowQuery', 'IWorkflowDTO', 'IWorkflowStepDTO',
    'IWorkflowSerializer', 'IWorkflowRepository', 'IWorkflowService',

    # Service exceptions
    'WorkflowServiceError', 'ServiceWorkflowNotFoundError',
    'WorkflowStepNotFoundError', 'ServiceWorkflowValidationError',
    'ServiceWorkflowExecutionError', 'WorkflowAlreadyExistsError',
    'WorkflowRepositoryError', 'WorkflowSerializationError',
    'WorkflowDeserializationError', 'WorkflowQueryError',

    # Service implementations
    'WorkflowDTO', 'WorkflowStepDTO',
    'WorkflowQuery', 'PropertyQuery', 'AndQuery', 'OrQuery', 'NotQuery',
    'AllQuery', 'NoneQuery', 'WorkflowQueryBuilder',
    'WorkflowSerializer',
    'FileSystemWorkflowRepository', 'InMemoryWorkflowRepository',
    'WorkflowService'
]
