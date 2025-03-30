"""
Defines constants used throughout the UI.
SOLID/KISS: Centralizes magic numbers and strings.
DRY: Avoids repeating these values.
"""

# Colors

COLOR_PRIMARY = "#3498db"
COLOR_SECONDARY = "#2ecc71"
COLOR_ACCENT = "#9b59b6"
COLOR_WARNING = "#f39c12"
COLOR_ERROR = "#e74c3c"
COLOR_DISABLED = "#95a5a6"

# Dimensions

INITIAL_WIDTH = 1250
INITIAL_HEIGHT = 880
MIN_WIDTH = 1000
MIN_HEIGHT = 720

# Padding/Radius

PAD_X_OUTER = 10
PAD_Y_OUTER = 10
PAD_X_INNER = 5
PAD_Y_INNER = 5
CORNER_RADIUS = 8

# Fonts

FONT_FAMILY_PRIMARY = "Segoe UI"
FONT_FAMILY_MONO = "Consolas"
FONT_SIZE_BASE = 13
FONT_SIZE_SMALL = 11
FONT_SIZE_LARGE = 15
FONT_WEIGHT_BOLD = "bold"

# File paths

SETTINGS_FILE = "autoclick_settings.v5.json"
CREDENTIALS_FILE = "autoclick_credentials.v5.json"
VARIABLES_FILE = "autoclick_variables.v5.json"
ERRORS_FILE = "autoclick_errors.v5.json"
WORKFLOWS_DIR = "workflows"

# Treeview Column IDs

COL_ID_NAME = "name"
COL_ID_USERNAME = "username"
COL_ID_STATUS = "status"
COL_ID_LAST_USED = "last_used"
COL_ID_CATEGORY = "category"
COL_ID_TAGS = "tags"
COL_ID_TYPE = "type"
COL_ID_VALUE = "value"
COL_ID_SEVERITY = "severity"
COL_ID_ACTION = "action"
COL_ID_SCOPE = "#0"
COL_ID_DESCRIPTION = "description"

# Grid arguments

GRID_ARGS_LABEL = {'sticky': "w", 'padx': PAD_X_INNER, 'pady': PAD_Y_INNER}
GRID_ARGS_WIDGET = {'sticky': "ew", 'padx': PAD_X_INNER, 'pady': PAD_Y_INNER}
GRID_ARGS_FULL_SPAN_WIDGET = {'sticky': "ew", 'padx': PAD_X_INNER, 'pady': PAD_Y_INNER, 'columnspan': 2}
GRID_ARGS_TEXTBOX = {'sticky': "nsew", 'padx': PAD_X_INNER, 'pady': PAD_Y_INNER}
