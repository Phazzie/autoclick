# AUTOCLICK Test Analysis

This document analyzes which tests can be kept, which should be discarded, and which require further discussion.

## Tests to Keep

### test_error_config_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\test_error_config_serialization.py`

**Tests Components:**

- `src/core/models.py`

### test_variable_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\test_variable_serialization.py`

**Tests Components:**

- `src/core/models.py`

### test_workflow_connection_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\test_workflow_connection_serialization.py`

**Tests Components:**

- `src/core/models.py`

### test_workflow_node_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\test_workflow_node_serialization.py`

**Tests Components:**

- `src/core/models.py`

### test_error_config_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\models\test_error_config_serialization.py`

**Tests Components:**

- `src/core/models.py`
- `src/core/utils/serialization.py`

### test_variable_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\models\test_variable_serialization.py`

**Tests Components:**

- `src/core/models.py`
- `src/core/utils/serialization.py`

### test_workflow_connection_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\models\test_workflow_connection_serialization.py`

**Tests Components:**

- `src/core/models.py`
- `src/core/utils/serialization.py`

### test_workflow_node_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\models\test_workflow_node_serialization.py`

**Tests Components:**

- `src/core/models.py`
- `src/core/utils/serialization.py`

### test_workflow_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\models\test_workflow_serialization.py`

**Tests Components:**

- `src/core/models.py`
- `src/core/utils/serialization.py`

### test_workflow_engine_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_engine_new.py`

**Tests Components:**

- `src/core/workflow/exceptions.py`
- `src/core/workflow/workflow_engine_new.py`
- `src/core/workflow/execution_result.py`
- `src/core/workflow/interfaces.py`

### test_workflow_service.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_service.py`

**Tests Components:**

- `src/core/workflow/workflow_service.py`
- `src/core/models.py`
- `src/core/workflow/workflow_engine.py`
- `src/core/context/execution_context.py`

### test_workflow_engine.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\engine\test_workflow_engine.py`

**Tests Components:**

- `src/core/utils/logging.py`
- `src/core/workflow/exceptions.py`
- `src/core/utils/error_handling.py`
- `src/core/workflow/execution_result.py`
- `src/core/workflow/engine/workflow_engine.py`
- `src/core/workflow/interfaces.py`

### test_workflow_executor.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\engine\test_workflow_executor.py`

**Tests Components:**

- `src/core/utils/logging.py`
- `src/core/workflow/engine/workflow_executor.py`
- `src/core/workflow/exceptions.py`
- `src/core/utils/error_handling.py`
- `src/core/workflow/execution_result.py`
- `src/core/workflow/interfaces.py`

### test_workflow_validator.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\engine\test_workflow_validator.py`

**Tests Components:**

- `src/core/utils/logging.py`
- `src/core/utils/error_handling.py`
- `src/core/workflow/engine/workflow_validator.py`
- `src/core/workflow/interfaces.py`

### test_base_workflow_service.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\service\test_base_workflow_service.py`

**Tests Components:**

- `src/core/utils/service.py`
- `src/core/utils/logging.py`
- `src/core/workflow/service/base_workflow_service.py`
- `src/core/utils/error_handling.py`
- `src/core/workflow/service_interfaces.py`
- `src/core/workflow/interfaces.py`

### test_workflow_service.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\service\test_workflow_service.py`

**Tests Components:**

- `src/core/workflow/workflow_dto.py`
- `src/core/workflow/service/base_workflow_service.py`
- `src/core/workflow/exceptions.py`
- `src/core/workflow/service_interfaces.py`
- `src/core/workflow/service/workflow_service.py`
- `src/core/workflow/interfaces.py`

### test_credential_adapter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\test_credential_adapter.py`

**Tests Components:**

- `src/core/credentials/credential_manager.py`
- `src/core/models.py`
- `src/ui/adapters/credential_adapter.py`

### test_data_source_adapter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\test_data_source_adapter.py`

**Tests Components:**

- `src/core/models.py`
- `src/ui/adapters/data_source_adapter.py`

### test_error_adapter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\test_error_adapter.py`

**Tests Components:**

- `src/core/models.py`
- `src/ui/adapters/error_adapter.py`

### test_action_execution_presenter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\presenters\test_action_execution_presenter.py`

**Tests Components:**

- `src/core/models.py`
- `src/ui/presenters/action_execution_presenter.py`
- `src/ui/adapters/workflow_adapter.py`

### test_credential_presenter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\presenters\test_credential_presenter.py`

**Tests Components:**

- `src/core/models.py`
- `src/ui/presenters/credential_presenter.py`
- `src/ui/adapters/credential_adapter.py`

### test_data_source_presenter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\presenters\test_data_source_presenter.py`

**Tests Components:**

- `src/ui/adapters/data_source_adapter.py`
- `src/core/models.py`
- `src/ui/presenters/data_source_presenter.py`

### test_error_presenter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\presenters\test_error_presenter.py`

**Tests Components:**

- `src/core/models.py`
- `src/ui/presenters/error_presenter.py`
- `src/ui/adapters/error_adapter.py`

### test_variable_presenter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\presenters\test_variable_presenter.py`

**Tests Components:**

- `src/core/models.py`
- `src/ui/adapters/variable_adapter.py`
- `src/ui/presenters/variable_presenter.py`

### test_workflow_presenter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\presenters\test_workflow_presenter.py`

**Tests Components:**

- `src/core/models.py`
- `src/ui/presenters/workflow_presenter.py`
- `src/ui/adapters/workflow_adapter.py`

### test_action_execution_view.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\views\test_action_execution_view.py`

**Tests Components:**

- `src/core/models.py`
- `src/ui/views/action_execution_view.py`

### test_data_source_view.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\views\test_data_source_view.py`

**Tests Components:**

- `src/core/models.py`

### test_error_view.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\views\test_error_view.py`

**Tests Components:**

- `src/core/models.py`
- `src/ui/views/error_view.py`

### test_workflow_view.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\views\test_workflow_view.py`

**Tests Components:**

- `src/core/models.py`
- `src/ui/views/workflow_view.py`

## Tests to Discard

### test_utils.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\astroid\test_utils.py`

**Tests Components:**


### test_abc.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_abc.py`

**Tests Components:**


### test_check.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_check.py`

**Tests Components:**


### test_classdef.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_classdef.py`

**Tests Components:**


### test_dataclasses.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_dataclasses.py`

**Tests Components:**


### test_detect.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_detect.py`

**Tests Components:**


### test_dictviews.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_dictviews.py`

**Tests Components:**


### test_diff.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_diff.py`

**Tests Components:**


### test_extendpickle.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_extendpickle.py`

**Tests Components:**


### test_fglobals.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_fglobals.py`

**Tests Components:**


### test_file.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_file.py`

**Tests Components:**


### test_functions.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_functions.py`

**Tests Components:**


### test_functors.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_functors.py`

**Tests Components:**


### test_logger.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_logger.py`

**Tests Components:**


### test_mixins.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_mixins.py`

**Tests Components:**


### test_module.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_module.py`

**Tests Components:**


### test_moduledict.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_moduledict.py`

**Tests Components:**


### test_nested.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_nested.py`

**Tests Components:**


### test_objects.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_objects.py`

**Tests Components:**


### test_properties.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_properties.py`

**Tests Components:**


### test_pycapsule.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_pycapsule.py`

**Tests Components:**


### test_recursive.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_recursive.py`

**Tests Components:**


### test_registered.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_registered.py`

**Tests Components:**


### test_restricted.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_restricted.py`

**Tests Components:**


### test_selected.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_selected.py`

**Tests Components:**


### test_session.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_session.py`

**Tests Components:**


### test_source.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_source.py`

**Tests Components:**


### test_sources.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_sources.py`

**Tests Components:**


### test_temp.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_temp.py`

**Tests Components:**


### test_threads.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_threads.py`

**Tests Components:**


### test_weakref.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\dill\tests\test_weakref.py`

**Tests Components:**


### test_against_stdlib_http.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\h11\tests\test_against_stdlib_http.py`

**Tests Components:**


### test_connection.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\h11\tests\test_connection.py`

**Tests Components:**


### test_events.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\h11\tests\test_events.py`

**Tests Components:**


### test_headers.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\h11\tests\test_headers.py`

**Tests Components:**


### test_helpers.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\h11\tests\test_helpers.py`

**Tests Components:**


### test_io.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\h11\tests\test_io.py`

**Tests Components:**


### test_receivebuffer.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\h11\tests\test_receivebuffer.py`

**Tests Components:**


### test_state.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\h11\tests\test_state.py`

**Tests Components:**


### test_util.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\h11\tests\test_util.py`

**Tests Components:**


### test_find_sources.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypy\test\test_find_sources.py`

**Tests Components:**


### test_ref_info.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypy\test\test_ref_info.py`

**Tests Components:**


### test_parse_data.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypy\test\meta\test_parse_data.py`

**Tests Components:**


### test_update_data.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypy\test\meta\test_update_data.py`

**Tests Components:**


### test_alwaysdefined.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_alwaysdefined.py`

**Tests Components:**


### test_analysis.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_analysis.py`

**Tests Components:**


### test_cheader.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_cheader.py`

**Tests Components:**


### test_commandline.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_commandline.py`

**Tests Components:**


### test_emit.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_emit.py`

**Tests Components:**


### test_emitclass.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_emitclass.py`

**Tests Components:**


### test_emitfunc.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_emitfunc.py`

**Tests Components:**


### test_emitwrapper.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_emitwrapper.py`

**Tests Components:**


### test_exceptions.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_exceptions.py`

**Tests Components:**


### test_external.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_external.py`

**Tests Components:**


### test_irbuild.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_irbuild.py`

**Tests Components:**


### test_ircheck.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_ircheck.py`

**Tests Components:**


### test_literals.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_literals.py`

**Tests Components:**


### test_namegen.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_namegen.py`

**Tests Components:**


### test_pprint.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_pprint.py`

**Tests Components:**


### test_rarray.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_rarray.py`

**Tests Components:**


### test_refcount.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_refcount.py`

**Tests Components:**


### test_run.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_run.py`

**Tests Components:**


### test_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_serialization.py`

**Tests Components:**


### test_struct.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_struct.py`

**Tests Components:**


### test_tuplename.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_tuplename.py`

**Tests Components:**


### test_typeops.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\mypyc\test\test_typeops.py`

**Tests Components:**


### test_file.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\pylint\testutils\functional\test_file.py`

**Tests Components:**


### test_sniffio.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\sniffio\_tests\test_sniffio.py`

**Tests Components:**


### test_asyncgen.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_asyncgen.py`

**Tests Components:**


### test_exceptiongroup_gc.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_exceptiongroup_gc.py`

**Tests Components:**


### test_guest_mode.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_guest_mode.py`

**Tests Components:**


### test_instrumentation.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_instrumentation.py`

**Tests Components:**


### test_io.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_io.py`

**Tests Components:**


### test_ki.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_ki.py`

**Tests Components:**


### test_local.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_local.py`

**Tests Components:**


### test_mock_clock.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_mock_clock.py`

**Tests Components:**


### test_parking_lot.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_parking_lot.py`

**Tests Components:**


### test_run.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_run.py`

**Tests Components:**


### test_thread_cache.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_thread_cache.py`

**Tests Components:**


### test_tutil.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_tutil.py`

**Tests Components:**


### test_unbounded_queue.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_unbounded_queue.py`

**Tests Components:**


### test_windows.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_core\_tests\test_windows.py`

**Tests Components:**


### test_abc.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_abc.py`

**Tests Components:**


### test_channel.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_channel.py`

**Tests Components:**


### test_contextvars.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_contextvars.py`

**Tests Components:**


### test_deprecate.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_deprecate.py`

**Tests Components:**


### test_deprecate_strict_exception_groups_false.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_deprecate_strict_exception_groups_false.py`

**Tests Components:**


### test_dtls.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_dtls.py`

**Tests Components:**


### test_exports.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_exports.py`

**Tests Components:**


### test_fakenet.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_fakenet.py`

**Tests Components:**


### test_file_io.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_file_io.py`

**Tests Components:**


### test_highlevel_generic.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_highlevel_generic.py`

**Tests Components:**


### test_highlevel_open_tcp_listeners.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_highlevel_open_tcp_listeners.py`

**Tests Components:**


### test_highlevel_open_tcp_stream.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_highlevel_open_tcp_stream.py`

**Tests Components:**


### test_highlevel_open_unix_stream.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_highlevel_open_unix_stream.py`

**Tests Components:**


### test_highlevel_serve_listeners.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_highlevel_serve_listeners.py`

**Tests Components:**


### test_highlevel_socket.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_highlevel_socket.py`

**Tests Components:**


### test_highlevel_ssl_helpers.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_highlevel_ssl_helpers.py`

**Tests Components:**


### test_path.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_path.py`

**Tests Components:**


### test_repl.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_repl.py`

**Tests Components:**


### test_scheduler_determinism.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_scheduler_determinism.py`

**Tests Components:**


### test_signals.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_signals.py`

**Tests Components:**


### test_socket.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_socket.py`

**Tests Components:**


### test_ssl.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_ssl.py`

**Tests Components:**


### test_subprocess.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_subprocess.py`

**Tests Components:**


### test_sync.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_sync.py`

**Tests Components:**


### test_testing.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_testing.py`

**Tests Components:**


### test_testing_raisesgroup.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_testing_raisesgroup.py`

**Tests Components:**


### test_threads.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_threads.py`

**Tests Components:**


### test_timeouts.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_timeouts.py`

**Tests Components:**


### test_tracing.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_tracing.py`

**Tests Components:**


### test_trio.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_trio.py`

**Tests Components:**


### test_unix_pipes.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_unix_pipes.py`

**Tests Components:**


### test_util.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_util.py`

**Tests Components:**


### test_wait_for_object.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_wait_for_object.py`

**Tests Components:**


### test_windows_pipes.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\test_windows_pipes.py`

**Tests Components:**


### test_gen_exports.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\tools\test_gen_exports.py`

**Tests Components:**


### test_mypy_annotate.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\trio\_tests\tools\test_mypy_annotate.py`

**Tests Components:**


### test_abnf.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\websocket\tests\test_abnf.py`

**Tests Components:**


### test_app.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\websocket\tests\test_app.py`

**Tests Components:**


### test_cookiejar.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\websocket\tests\test_cookiejar.py`

**Tests Components:**


### test_http.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\websocket\tests\test_http.py`

**Tests Components:**


### test_url.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\websocket\tests\test_url.py`

**Tests Components:**


### test_websocket.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\.venv\Lib\site-packages\websocket\tests\test_websocket.py`

**Tests Components:**


### test_workflow_service_import.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\scripts\tests\test_workflow_service_import.py`

**Tests Components:**


### test_workflow_validation_error_import.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\scripts\tests\test_workflow_validation_error_import.py`

**Tests Components:**


### test_models_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\test_models_serialization.py`

**Tests Components:**


### test_variable_types.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\variables\test_variable_types.py`

**Tests Components:**


### test_workflow_view_canvas.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\views\test_workflow_view_canvas.py`

**Tests Components:**

- `src/ui/views/workflow_view.py`

### test_against_stdlib_http.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\h11\tests\test_against_stdlib_http.py`

**Tests Components:**


### test_connection.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\h11\tests\test_connection.py`

**Tests Components:**


### test_events.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\h11\tests\test_events.py`

**Tests Components:**


### test_headers.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\h11\tests\test_headers.py`

**Tests Components:**


### test_helpers.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\h11\tests\test_helpers.py`

**Tests Components:**


### test_io.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\h11\tests\test_io.py`

**Tests Components:**


### test_receivebuffer.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\h11\tests\test_receivebuffer.py`

**Tests Components:**


### test_state.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\h11\tests\test_state.py`

**Tests Components:**


### test_util.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\h11\tests\test_util.py`

**Tests Components:**


### test_sniffio.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\sniffio\_tests\test_sniffio.py`

**Tests Components:**


### test_asyncgen.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_asyncgen.py`

**Tests Components:**


### test_exceptiongroup_gc.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_exceptiongroup_gc.py`

**Tests Components:**


### test_guest_mode.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_guest_mode.py`

**Tests Components:**


### test_instrumentation.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_instrumentation.py`

**Tests Components:**


### test_io.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_io.py`

**Tests Components:**


### test_ki.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_ki.py`

**Tests Components:**


### test_local.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_local.py`

**Tests Components:**


### test_mock_clock.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_mock_clock.py`

**Tests Components:**


### test_parking_lot.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_parking_lot.py`

**Tests Components:**


### test_run.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_run.py`

**Tests Components:**


### test_thread_cache.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_thread_cache.py`

**Tests Components:**


### test_tutil.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_tutil.py`

**Tests Components:**


### test_unbounded_queue.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_unbounded_queue.py`

**Tests Components:**


### test_windows.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_core\_tests\test_windows.py`

**Tests Components:**


### test_abc.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_abc.py`

**Tests Components:**


### test_channel.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_channel.py`

**Tests Components:**


### test_contextvars.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_contextvars.py`

**Tests Components:**


### test_deprecate.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_deprecate.py`

**Tests Components:**


### test_deprecate_strict_exception_groups_false.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_deprecate_strict_exception_groups_false.py`

**Tests Components:**


### test_dtls.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_dtls.py`

**Tests Components:**


### test_exports.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_exports.py`

**Tests Components:**


### test_fakenet.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_fakenet.py`

**Tests Components:**


### test_file_io.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_file_io.py`

**Tests Components:**


### test_highlevel_generic.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_highlevel_generic.py`

**Tests Components:**


### test_highlevel_open_tcp_listeners.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_highlevel_open_tcp_listeners.py`

**Tests Components:**


### test_highlevel_open_tcp_stream.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_highlevel_open_tcp_stream.py`

**Tests Components:**


### test_highlevel_open_unix_stream.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_highlevel_open_unix_stream.py`

**Tests Components:**


### test_highlevel_serve_listeners.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_highlevel_serve_listeners.py`

**Tests Components:**


### test_highlevel_socket.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_highlevel_socket.py`

**Tests Components:**


### test_highlevel_ssl_helpers.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_highlevel_ssl_helpers.py`

**Tests Components:**


### test_path.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_path.py`

**Tests Components:**


### test_repl.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_repl.py`

**Tests Components:**


### test_scheduler_determinism.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_scheduler_determinism.py`

**Tests Components:**


### test_signals.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_signals.py`

**Tests Components:**


### test_socket.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_socket.py`

**Tests Components:**


### test_ssl.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_ssl.py`

**Tests Components:**


### test_subprocess.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_subprocess.py`

**Tests Components:**


### test_sync.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_sync.py`

**Tests Components:**


### test_testing.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_testing.py`

**Tests Components:**


### test_testing_raisesgroup.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_testing_raisesgroup.py`

**Tests Components:**


### test_threads.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_threads.py`

**Tests Components:**


### test_timeouts.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_timeouts.py`

**Tests Components:**


### test_tracing.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_tracing.py`

**Tests Components:**


### test_trio.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_trio.py`

**Tests Components:**


### test_unix_pipes.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_unix_pipes.py`

**Tests Components:**


### test_util.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_util.py`

**Tests Components:**


### test_wait_for_object.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_wait_for_object.py`

**Tests Components:**


### test_windows_pipes.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\test_windows_pipes.py`

**Tests Components:**


### test_gen_exports.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\tools\test_gen_exports.py`

**Tests Components:**


### test_mypy_annotate.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\trio\_tests\tools\test_mypy_annotate.py`

**Tests Components:**


### test_abnf.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\websocket\tests\test_abnf.py`

**Tests Components:**


### test_app.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\websocket\tests\test_app.py`

**Tests Components:**


### test_cookiejar.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\websocket\tests\test_cookiejar.py`

**Tests Components:**


### test_http.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\websocket\tests\test_http.py`

**Tests Components:**


### test_url.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\websocket\tests\test_url.py`

**Tests Components:**


### test_websocket.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\venv\Lib\site-packages\websocket\tests\test_websocket.py`

**Tests Components:**


## Tests for Discussion

### test_implementation.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\test_implementation.py`

**Tests Components:**

- `src/ui/adapters/interfaces/workflow_interfaces.py`

### test_action_adapter_integration.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\scripts\tests\test_action_adapter_integration.py`

**Tests Components:**

- `src/ui/adapters/impl/action_adapter.py`
- `src/domain/actions/impl/action_service.py`

### test_action_factory_methods.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\scripts\tests\test_action_factory_methods.py`

**Tests Components:**

- `src/core/actions/action_factory.py`

### test_di_circular_import.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\scripts\tests\test_di_circular_import.py`

**Tests Components:**

- `src/infrastructure/di/container.py`
- `src/infrastructure/di/config.py`

### test_ui_components_integration.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\scripts\tests\test_ui_components_integration.py`

**Tests Components:**

- `src/ui/presenters/workflow_presenter.py`
- `src/ui/presenters/action_execution_presenter.py`
- `src/ui/presenters/credential_presenter.py`

### test_create_workflow_command.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\application\workflows\commands\test_create_workflow_command.py`

**Tests Components:**

- `src/domain/workflows/interfaces.py`
- `src/application/workflows/commands/create_workflow_command.py`

### test_action_factory.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\actions\test_action_factory.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/actions/base_action.py`
- `src/core/actions/action_factory.py`

### test_action_factory_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\actions\test_action_factory_new.py`

**Tests Components:**

- `src/core/actions/exceptions.py`
- `src/core/actions/action_factory_new.py`
- `src/core/actions/interfaces.py`

### test_action_interface.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\actions\test_action_interface.py`

**Tests Components:**

- `src/core/actions/action_interface.py`

### test_base_action.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\actions\test_base_action.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/actions/base_action.py`

### test_click_action.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\actions\test_click_action.py`

**Tests Components:**

- `src/core/actions/action_factory.py`
- `src/core/actions/click_action.py`

### test_credential_filter_action.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\actions\test_credential_filter_action.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/credentials/credential_manager.py`
- `src/core/actions/credential_filter_action.py`

### test_data_driven_action.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\actions\test_data_driven_action.py`

**Tests Components:**

- `src/core/data/mapping/mapper.py`
- `src/core/actions/action_interface.py`
- `src/core/data/iteration/context.py`
- `src/core/data/sources/base.py`
- `src/core/actions/base_action.py`
- `src/core/actions/data_driven_action.py`
- `src/core/actions/action_factory.py`

### test_if_then_else_action.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\actions\test_if_then_else_action.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/actions/if_then_else_action.py`
- `src/core/conditions/condition_interface.py`
- `src/core/actions/base_action.py`
- `src/core/conditions/base_condition.py`

### test_screenshot_action.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\actions\test_screenshot_action.py`

**Tests Components:**

- `src/core/utils/screenshot_capture.py`
- `src/core/actions/screenshot_action.py`

### test_switch_case_action.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\actions\test_switch_case_action.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/actions/switch_case_action.py`
- `src/core/conditions/condition_interface.py`
- `src/core/actions/base_action.py`
- `src/core/actions/action_factory.py`

### test_base_condition.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\conditions\test_base_condition.py`

**Tests Components:**

- `src/core/conditions/condition_interface.py`
- `src/core/conditions/base_condition.py`

### test_base_condition_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\conditions\test_base_condition_new.py`

**Tests Components:**

- `src/core/conditions/exceptions.py`
- `src/core/conditions/base_condition_new.py`

### test_comparison_condition.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\conditions\test_comparison_condition.py`

**Tests Components:**

- `src/core/conditions/comparison_condition.py`

### test_composite_conditions.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\conditions\test_composite_conditions.py`

**Tests Components:**

- `src/core/conditions/condition_interface.py`
- `src/core/conditions/base_condition.py`
- `src/core/conditions/composite_conditions.py`

### test_compound_conditions.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\conditions\test_compound_conditions.py`

**Tests Components:**

- `src/core/conditions/exceptions.py`
- `src/core/conditions/compound_condition_base.py`
- `src/core/conditions/compound_conditions.py`

### test_condition_factory.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\conditions\test_condition_factory.py`

**Tests Components:**

- `src/core/conditions/condition_factory.py`
- `src/core/conditions/condition_interface.py`
- `src/core/conditions/base_condition.py`

### test_condition_factory_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\conditions\test_condition_factory_new.py`

**Tests Components:**

- `src/core/conditions/exceptions.py`
- `src/core/conditions/condition_factory_new.py`

### test_condition_interface.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\conditions\test_condition_interface.py`

**Tests Components:**

- `src/core/conditions/condition_interface.py`

### test_element_exists_condition.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\conditions\test_element_exists_condition.py`

**Tests Components:**

- `src/core/conditions/element_exists_condition.py`

### test_text_contains_condition.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\conditions\test_text_contains_condition.py`

**Tests Components:**

- `src/core/conditions/text_contains_condition.py`

### test_context_builder.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\context\test_context_builder.py`

**Tests Components:**

- `src/core/context/context_builder.py`
- `src/core/context/execution_context_new.py`
- `src/core/context/exceptions.py`

### test_context_factory.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\context\test_context_factory.py`

**Tests Components:**

- `src/core/context/context_snapshot.py`
- `src/core/context/context_factory.py`
- `src/core/context/execution_context_new.py`

### test_context_options.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\context\test_context_options.py`

**Tests Components:**

- `src/core/context/context_options.py`

### test_context_snapshot.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\context\test_context_snapshot.py`

**Tests Components:**

- `src/core/context/context_snapshot.py`

### test_execution_context.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\context\test_execution_context.py`

**Tests Components:**

- `src/core/context/variable_storage.py`
- `src/core/context/context_options.py`
- `src/core/context/execution_state.py`
- `src/core/context/execution_context.py`

### test_execution_context_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\context\test_execution_context_new.py`

**Tests Components:**

- `src/core/context/context_snapshot.py`
- `src/core/context/execution_context_new.py`

### test_execution_state.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\context\test_execution_state.py`

**Tests Components:**

- `src/core/context/execution_state.py`

### test_variable_accessor.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\context\test_variable_accessor.py`

**Tests Components:**

- `src/core/context/variable_accessor.py`
- `src/core/context/exceptions.py`

### test_variable_storage.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\context\test_variable_storage.py`

**Tests Components:**

- `src/core/context/variable_storage.py`

### test_variable_storage_v2.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\context\test_variable_storage_v2.py`

**Tests Components:**

- `src/core/variables/variable.py`
- `src/core/context/variable_storage.py`
- `src/core/context/variable_storage_v2.py`
- `src/core/variables/variable_interface.py`
- `src/core/variables/typed_variables.py`

### test_iteration.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\data\iteration\test_iteration.py`

**Tests Components:**

- `src/core/data/iteration/iterator.py`
- `src/core/data/iteration/context.py`

### test_mapping.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\data\mapping\test_mapping.py`

**Tests Components:**

- `src/core/data/mapping/mapper.py`
- `src/core/data/mapping/variable_mapper.py`

### test_base_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\data\sources\test_base_new.py`

**Tests Components:**

- `src/core/data/sources/field.py`
- `src/core/data/sources/exceptions.py`
- `src/core/data/sources/base_new.py`
- `src/core/data/sources/record.py`

### test_data_sources.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\data\sources\test_data_sources.py`

**Tests Components:**

- `src/core/data/sources/json_source.py`
- `src/core/data/sources/base.py`
- `src/core/data/sources/csv_source.py`
- `src/core/data/sources/memory_source.py`

### test_field.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\data\sources\test_field.py`

**Tests Components:**

- `src/core/data/sources/field.py`
- `src/core/data/sources/exceptions.py`

### test_pagination.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\data\sources\test_pagination.py`

**Tests Components:**

- `src/core/data/sources/exceptions.py`
- `src/core/data/sources/pagination.py`

### test_query.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\data\sources\test_query.py`

**Tests Components:**

- `src/core/data/sources/query.py`
- `src/core/data/sources/exceptions.py`
- `src/core/data/sources/record.py`

### test_record.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\data\sources\test_record.py`

**Tests Components:**

- `src/core/data/sources/field.py`
- `src/core/data/sources/exceptions.py`
- `src/core/data/sources/record.py`

### test_error_factory.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\errors\test_error_factory.py`

**Tests Components:**

- `src/core/errors/recovery_strategies.py`
- `src/core/errors/error_manager.py`
- `src/core/errors/recovery_strategy.py`
- `src/core/errors/error_factory.py`

### test_error_listener.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\errors\test_error_listener.py`

**Tests Components:**

- `src/core/errors/logging_listener.py`
- `src/core/errors/error_listener.py`
- `src/core/errors/error_types.py`

### test_error_manager.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\errors\test_error_manager.py`

**Tests Components:**

- `src/core/errors/error_listener.py`
- `src/core/errors/error_types.py`
- `src/core/errors/error_manager.py`
- `src/core/errors/recovery_strategy.py`

### test_error_types.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\errors\test_error_types.py`

**Tests Components:**

- `src/core/errors/error_types.py`

### test_recovery_strategy.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\errors\test_recovery_strategy.py`

**Tests Components:**

- `src/core/errors/recovery_strategies.py`
- `src/core/errors/error_types.py`
- `src/core/errors/recovery_strategy.py`

### test_specific_errors.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\errors\test_specific_errors.py`

**Tests Components:**

- `src/core/errors/timeout_errors.py`
- `src/core/errors/element_errors.py`
- `src/core/errors/error_types.py`
- `src/core/errors/workflow_errors.py`

### test_specific_recovery_strategies.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\errors\test_specific_recovery_strategies.py`

**Tests Components:**

- `src/core/errors/recovery_strategies.py`
- `src/core/errors/error_types.py`

### test_expression_parser.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\expressions\test_expression_parser.py`

**Tests Components:**

- `src/core/expressions/expression_parser.py`

### test_error_handling.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\utils\test_error_handling.py`

**Tests Components:**

- `src/core/utils/error_handling.py`

### test_logging.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\utils\test_logging.py`

**Tests Components:**

- `src/core/utils/logging.py`

### test_screenshot_capture.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\utils\test_screenshot_capture.py`

**Tests Components:**

- `src/core/utils/screenshot_capture.py`

### test_screenshot_cleaner.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\utils\test_screenshot_cleaner.py`

**Tests Components:**

- `src/core/utils/screenshot_cleaner.py`

### test_screenshot_manager.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\utils\test_screenshot_manager.py`

**Tests Components:**

- `src/core/utils/screenshot_capture.py`
- `src/core/utils/screenshot_storage.py`
- `src/core/utils/screenshot_manager.py`
- `src/core/utils/screenshot_cleaner.py`

### test_screenshot_storage.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\utils\test_screenshot_storage.py`

**Tests Components:**

- `src/core/utils/screenshot_storage.py`

### test_serialization.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\utils\test_serialization.py`

**Tests Components:**

- `src/core/utils/serialization.py`

### test_service.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\utils\test_service.py`

**Tests Components:**

- `src/core/utils/service.py`

### test_variable_interface.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\variables\test_variable_interface.py`

**Tests Components:**

- `src/core/variables/variable.py`
- `src/core/context/variable_storage.py`
- `src/core/variables/variable_interface.py`

### test_variable_reference.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\variables\test_variable_reference.py`

**Tests Components:**

- `src/core/variables/exceptions.py`
- `src/core/variables/variable_reference.py`

### test_variable_resolver.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\variables\test_variable_resolver.py`

**Tests Components:**

- `src/core/variables/variable_resolver.py`
- `src/core/variables/exceptions.py`
- `src/core/variables/variable_reference.py`

### test_variable_storage.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\variables\test_variable_storage.py`

**Tests Components:**

- `src/core/variables/variable_storage.py`
- `src/core/variables/exceptions.py`
- `src/core/variables/variable_reference.py`

### test_workflow_dto.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_dto.py`

**Tests Components:**

- `src/core/workflow/workflow_dto.py`

### test_workflow_engine.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_engine.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/workflow/workflow_engine.py`
- `src/core/context/execution_state.py`
- `src/core/actions/base_action.py`
- `src/core/workflow/workflow_event.py`
- `src/core/context/execution_context.py`

### test_workflow_engine_interface.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_engine_interface.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/workflow/workflow_statistics.py`
- `src/core/workflow/workflow_engine_interface.py`
- `src/core/actions/base_action.py`
- `src/core/workflow/workflow_event.py`
- `src/core/context/execution_context.py`

### test_workflow_events.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_events.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/workflow/workflow_event.py`
- `src/core/actions/base_action.py`

### test_workflow_query.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_query.py`

**Tests Components:**

- `src/core/workflow/workflow_query.py`
- `src/core/workflow/service_exceptions.py`

### test_workflow_repository.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_repository.py`

**Tests Components:**

- `src/core/workflow/service_exceptions.py`
- `src/core/workflow/workflow_repository.py`

### test_workflow_serializer.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_serializer.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/workflow/workflow_serializer.py`
- `src/core/actions/base_action.py`
- `src/core/actions/action_factory.py`

### test_workflow_serializer_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_serializer_new.py`

**Tests Components:**

- `src/core/workflow/service_exceptions.py`
- `src/core/workflow/workflow_serializer_new.py`

### test_workflow_service_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_service_new.py`

**Tests Components:**

- `src/core/workflow/workflow_service_new.py`
- `src/core/workflow/service_exceptions.py`

### test_workflow_service_new_fixed.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_service_new_fixed.py`

**Tests Components:**

- `src/core/workflow/workflow_service_new.py`
- `src/core/workflow/service_exceptions.py`

### test_workflow_statistics.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\core\workflow\test_workflow_statistics.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/workflow/workflow_statistics.py`
- `src/core/workflow/workflow_event.py`
- `src/core/actions/base_action.py`

### test_action_metadata.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\actions\test_action_metadata.py`

**Tests Components:**

- `src/domain/actions/metadata.py`

### test_action_schemas.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\actions\test_action_schemas.py`

**Tests Components:**

- `src/domain/actions/schemas.py`

### test_action_service.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\actions\test_action_service.py`

**Tests Components:**

- `src/domain/exceptions/domain_exceptions.py`
- `src/domain/actions/impl/action_service.py`

### test_action_store.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\actions\test_action_store.py`

**Tests Components:**

- `src/domain/actions/impl/action_service.py`

### test_action_type_registry.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\actions\test_action_type_registry.py`

**Tests Components:**

- `src/domain/actions/action_type_registry.py`

### test_action_validator.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\actions\test_action_validator.py`

**Tests Components:**

- `src/domain/actions/impl/action_validator.py`

### test_error_handler.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\common\test_error_handler.py`

**Tests Components:**

- `src/domain/common/error_handler.py`
- `src/domain/exceptions/domain_exceptions.py`

### test_credential_formatter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\credentials\test_credential_formatter.py`

**Tests Components:**

- `src/core/credentials/credential_manager.py`
- `src/domain/credentials/impl/credential_formatter.py`

### test_credential_service.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\credentials\test_credential_service.py`

**Tests Components:**

- `src/core/credentials/credential_manager.py`
- `src/domain/credentials/impl/credential_service.py`
- `src/domain/exceptions/domain_exceptions.py`

### test_credential_utils.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\credentials\test_credential_utils.py`

**Tests Components:**

- `src/core/credentials/credential_manager.py`
- `src/domain/credentials/utils.py`

### test_credential_validator.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\domain\credentials\test_credential_validator.py`

**Tests Components:**

- `src/domain/credentials/impl/credential_validator.py`

### test_workflow_repository.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\infrastructure\repositories\test_workflow_repository.py`

**Tests Components:**

- `src/domain/workflows/models.py`
- `src/infrastructure/repositories/workflow_repository.py`

### test_workflow_serializer.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\infrastructure\serialization\test_workflow_serializer.py`

**Tests Components:**

- `src/domain/workflows/models.py`
- `src/infrastructure/serialization/workflow_serializer.py`

### test_credential_adapter_integration.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\integration\test_credential_adapter_integration.py`

**Tests Components:**

- `src/domain/credentials/impl/credential_service.py`
- `src/ui/adapters/impl/credential_adapter.py`
- `src/ui/presenters/credential_presenter.py`
- `src/ui/views/credential_view.py`

### test_credential_filter_integration.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\integration\test_credential_filter_integration.py`

**Tests Components:**

- `src/core/actions/action_interface.py`
- `src/core/credentials/credential_manager.py`
- `src/core/actions/credential_filter_action.py`
- `src/core/context/variable_storage.py`
- `src/core/workflow/workflow_engine.py`
- `src/core/actions/base_action.py`

### test_workflow_integration.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\integration\test_workflow_integration.py`

**Tests Components:**

- `src/ui/adapters/interfaces/workflow_interfaces.py`

### test_adapter_factory.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\test_adapter_factory.py`

**Tests Components:**

- `src/core/credentials/credential_manager.py`
- `src/core/data/data_source_manager.py`
- `src/core/loops/loop_factory.py`
- `src/ui/adapters/impl/variable_adapter.py`
- `src/ui/adapters/impl/workflow_adapter.py`
- `src/ui/adapters/impl/condition_adapter.py`
- `src/core/variables/variable_storage.py`
- `src/core/workflow/workflow_service_new.py`
- `src/ui/adapters/impl/data_source_adapter.py`
- `src/ui/adapters/impl/error_adapter.py`
- `src/ui/adapters/impl/credential_adapter.py`
- `src/core/errors/error_manager.py`
- `src/ui/adapters/impl/loop_adapter.py`
- `src/core/reporting/reporting_service.py`
- `src/ui/adapters/impl/reporting_adapter.py`
- `src/ui/adapters/factory/adapter_factory.py`
- `src/core/conditions/condition_factory_new.py`

### test_condition_adapter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\test_condition_adapter.py`

**Tests Components:**

- `src/ui/adapters/condition_adapter.py`
- `src/core/conditions/condition_factory.py`
- `src/core/conditions/text_contains_condition.py`
- `src/core/conditions/comparison_condition.py`
- `src/core/conditions/composite_conditions.py`
- `src/core/conditions/element_exists_condition.py`

### test_loop_adapter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\test_loop_adapter.py`

**Tests Components:**

- `src/core/conditions/condition_factory.py`
- `src/core/actions/while_loop_action.py`
- `src/core/actions/for_each_action.py`
- `src/ui/adapters/loop_adapter.py`
- `src/core/actions/action_factory.py`

### test_reporting_adapter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\test_reporting_adapter.py`

**Tests Components:**

- `src/core/reporting/reporting_service.py`
- `src/ui/adapters/impl/reporting_adapter.py`

### test_variable_adapter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\test_variable_adapter.py`

**Tests Components:**

- `src/core/variables/variable_storage.py`
- `src/core/variables/variable_type.py`
- `src/ui/adapters/impl/variable_adapter.py`

### test_workflow_adapter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\test_workflow_adapter.py`

**Tests Components:**

- `src/ui/adapters/impl/workflow_adapter.py`
- `src/ui/adapters/interfaces/workflow_interfaces.py`

### test_action_adapter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\impl\test_action_adapter.py`

**Tests Components:**

- `src/ui/adapters/impl/action_adapter.py`
- `src/domain/actions/interfaces.py`

### test_condition_adapter_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\impl\test_condition_adapter_new.py`

**Tests Components:**

- `src/ui/adapters/impl/condition_adapter.py`
- `src/domain/conditions/interfaces.py`

### test_credential_adapter_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\impl\test_credential_adapter_new.py`

**Tests Components:**

- `src/core/credentials/credential_manager.py`
- `src/domain/credentials/interfaces.py`
- `src/ui/adapters/impl/credential_adapter.py`

### test_data_source_adapter_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\impl\test_data_source_adapter_new.py`

**Tests Components:**

- `src/ui/adapters/impl/data_source_adapter.py`
- `src/domain/datasources/interfaces.py`

### test_error_adapter_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\impl\test_error_adapter_new.py`

**Tests Components:**

- `src/ui/adapters/impl/error_adapter.py`
- `src/domain/errors/interfaces.py`

### test_loop_adapter_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\impl\test_loop_adapter_new.py`

**Tests Components:**

- `src/ui/adapters/impl/loop_adapter.py`
- `src/domain/loops/interfaces.py`

### test_reporting_adapter_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\impl\test_reporting_adapter_new.py`

**Tests Components:**

- `src/ui/adapters/impl/reporting_adapter.py`
- `src/domain/reporting/interfaces.py`

### test_variable_adapter_new.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\impl\test_variable_adapter_new.py`

**Tests Components:**

- `src/domain/variables/interfaces.py`
- `src/ui/adapters/impl/variable_adapter.py`

### test_workflow_command_adapter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\adapters\impl\test_workflow_command_adapter.py`

**Tests Components:**

- `src/ui/adapters/impl/workflow_command_adapter.py`

### test_context_menu.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\components\test_context_menu.py`

**Tests Components:**

- `src/ui/components/context_menu.py`

### test_batch_operations_dialog.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\dialogs\test_batch_operations_dialog.py`

**Tests Components:**

- `src/ui/dialogs/batch_operations_dialog.py`

### test_base_presenter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\presenters\test_base_presenter.py`

**Tests Components:**

- `src/ui/presenters/base_presenter.py`

### test_condition_presenter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\presenters\test_condition_presenter.py`

**Tests Components:**

- `src/ui/adapters/condition_adapter.py`
- `src/ui/presenters/condition_presenter.py`

### test_loop_presenter.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\presenters\test_loop_presenter.py`

**Tests Components:**

- `src/ui/presenters/loop_presenter.py`
- `src/ui/adapters/loop_adapter.py`

### test_condition_view.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\views\test_condition_view.py`

**Tests Components:**

- `src/ui/views/condition_view.py`

### test_credential_view.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\views\test_credential_view.py`

**Tests Components:**

- `src/ui/views/credential_view.py`

### test_loop_view.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\views\test_loop_view.py`

**Tests Components:**

- `src/ui/views/loop_view.py`

### test_variable_view.py

**Path:** `C:\Users\thump\OneDrive\Desktop\AUTOCLICK\tests\ui\views\test_variable_view.py`

**Tests Components:**

- `src/ui/views/variable_view.py`

