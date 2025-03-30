"""
Defines a base class for presenters.
SOLID/DRY: Encapsulates common presenter initialization and provides optional app/service references.
KISS: Simple base for presenters.
"""
from typing import TYPE_CHECKING, Optional, Any, TypeVar, Generic

# Use TypeVar for generic service type hint if needed
S = TypeVar('S')

if TYPE_CHECKING: # Import view/app types only for type checking to avoid circular deps
    from ..views.base_view import BaseView # Assume app.py is at the root level relative to src # This relative import might fail depending on execution context, direct import safer if possible
    try:
        from app import AutoClickApp
    except ImportError: # Fallback if direct import fails (e.g., running a script inside src)
        AutoClickApp = Any # type: ignore

class BasePresenter(Generic[S]):
    """Base class for presenters, optionally generic over primary service type."""
    def __init__(self, view: Optional['BaseView'] = None,
                app: Optional['AutoClickApp'] = None,
                service: Optional[S] = None, # Allow injecting primary service directly
                **kwargs): # Allow injecting other services via kwargs
        if view is None:
            raise ValueError(f"View must be provided for presenter {self.__class__.__name__}")
        self._view = view
        self._app = app
        self._service = service # Store primary service if provided
        self._other_services = kwargs # Store additional injected services
        
        # Link view back to presenter is now done by App after both are created
        # if self._view: self._view.set_presenter(self)
    
    @property
    def view(self) -> 'BaseView':
        """Provides type-hinted access to the view."""
        # Init ensures view is not None
        return self._view
    
    @property
    def app(self) -> Optional['AutoClickApp']:
        """Provides type-hinted access to the main application instance (optional)."""
        return self._app
    
    @property
    def service(self) -> S:
        """Provides type-hinted access to the primary service."""
        if self._service is None:
            raise AttributeError(f"Primary service not injected or missing for presenter {self.__class__.__name__}")
        return self._service
    
    def get_service(self, service_name: str, service_type: type = object) -> Optional[Any]:
        """Gets an injected service by name from kwargs, optionally type-hinted."""
        svc = self._other_services.get(service_name)
        if svc is None:
            # Check if the requested service is the primary one
            if service_name == 'service' and self._service:
                 svc = self._service
            else:
                 print(f"Warning: Service '{service_name}' not injected/found for presenter {self.__class__.__name__}")
                 return None
        
        if not isinstance(svc, service_type):
            print(f"Warning: Service '{service_name}' has type {type(svc)}, expected {service_type}.")
            return None # Safer to return None if type mismatch
        
        return svc
    
    def update_app_status(self, message: str):
        """Safely requests the main app to update the status bar."""
        if self.app and hasattr(self.app, 'update_status'):
             self.app.update_status(message)
        else: print(f"STATUS ({self.__class__.__name__}): {message}") # Fallback log
    
    def initialize_view(self):
        """Called by App after presenter is linked to view. Subclasses override."""
        print(f"Initializing view for {self.__class__.__name__}")
        pass
    
    def _handle_error(self, action_desc: str, error: Exception, is_validation: bool = False):
        """Consolidated error handling for presenters."""
        # Log full error for debugging
        import traceback
        print(f"--- ERROR Handling Action: {action_desc} ---")
        traceback.print_exc()
        print("--- End Error Traceback ---")
        
        self.update_app_status(f"Error during {action_desc}.") # Update status bar
        title = "Input Error" if is_validation else "Operation Error"
        # Show user-friendly message using view's method
        self.view.display_error(title, str(error))
