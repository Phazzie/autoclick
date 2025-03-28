# CredentialFilterAction

The `CredentialFilterAction` is designed to identify failed login credentials and mark them as inactive rather than removing them from the credential list.

## Overview

When automating login processes, it's common to encounter failed login attempts due to invalid credentials, locked accounts, or other issues. The `CredentialFilterAction` provides a way to track these failed attempts and mark the corresponding credentials as inactive, allowing you to:

- Keep a record of all credentials, including those that have failed
- Avoid using credentials that have previously failed
- Customize how failed credentials are categorized (blacklisted, locked, expired, etc.)

## Usage

### Basic Usage

```python
from src.core.actions.credential_filter_action import CredentialFilterAction
from src.core.credentials.credential_manager import CredentialManager, CredentialStatus

# Create a credential manager
credential_manager = CredentialManager()

# Add some credentials
credential_manager.add_credential("user1", "pass1")
credential_manager.add_credential("user2", "pass2")

# Create the action
action = CredentialFilterAction(
    description="Filter failed credentials",
    credential_manager=credential_manager
)

# Execute the action with context containing login results
context = {
    "username": "user1",
    "success": False,
    "message": "Invalid password"
}

result = action.execute(context)
```

### Customizing Inactive Status

You can customize which status is used for inactive credentials:

```python
# Mark failed credentials as expired instead of blacklisted
action = CredentialFilterAction(
    description="Filter failed credentials",
    credential_manager=credential_manager,
    inactive_status=CredentialStatus.EXPIRED
)
```

### Integration with Workflow Engine

The `CredentialFilterAction` can be integrated into a workflow:

```python
from src.core.workflow.workflow_engine import WorkflowEngine

# Create a workflow
workflow = [
    # ... other actions ...
    CredentialFilterAction(
        description="Filter failed credentials",
        credential_manager=credential_manager
    ),
    # ... other actions ...
]

# Execute the workflow
engine = WorkflowEngine()
engine.run_workflow(workflow, context)
```

## Parameters

The `CredentialFilterAction` constructor accepts the following parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| description | str | (required) | Human-readable description of the action |
| credential_manager | CredentialManager | (required) | Credential manager to use |
| username_variable | str | "username" | Name of the variable containing the username |
| success_variable | str | "success" | Name of the variable containing the success flag |
| message_variable | str | "message" | Name of the variable containing the result message |
| inactive_status | CredentialStatus | CredentialStatus.BLACKLISTED | Status to set for inactive credentials |
| action_id | str | None | Optional unique identifier |

## Return Value

The `execute` method returns an `ActionResult` with the following data:

```python
{
    "updated_count": 1,  # Number of credentials marked as inactive
    "statistics": {      # Statistics from the credential manager
        "total": 10,
        "status_counts": {
            "UNUSED": 5,
            "SUCCESS": 3,
            "FAILURE": 0,
            "BLACKLISTED": 2,
            # ... other statuses ...
        },
        "success_rate": 0.6
    }
}
```

## Example

See the [credential_filter_example.py](../../examples/credential_filter_example.py) file for a complete example of how to use the `CredentialFilterAction`.
