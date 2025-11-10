# ============================================
# FILE: config/settings.py (Enhanced with version)
# ============================================
# Configuration settings for the application

# Version Information
APP_VERSION = "2.0.0"
APP_VERSION_NAME = "Enhanced Edition"
RELEASE_DATE = "2024-11-06"

# Previous versions
VERSION_HISTORY = {
    "2.0.0": {
        "name": "Enhanced Edition",
        "date": "2024-11-06",
        "features": 40,
        "type": "major"
    },
    "1.0.0": {
        "name": "Initial Release",
        "date": "2024-10-15",
        "features": 15,
        "type": "major"
    }
}

# App Configuration
APP_TITLE = "PrePify Pro Dashboard"
APP_ICON = "📊"
LAYOUT = "wide"

# Project Information
PROJECT_INFO = {
    "type": "1st Streamlit Application",
    "trainer": "Yash Sharma",
    "course": "AI & Machine Learning Training",
    "institution": "Nexpert Academy",
    "developer": "ONYXCODE"
}

# File upload settings
ALLOWED_FILE_TYPES = ['csv', 'xlsx', 'xls', 'json']
MAX_FILE_SIZE_MB = 200

# Visualization settings
DEFAULT_COLOR_SCHEME = 'Plotly'
CHART_HEIGHT = 550

# Data cleaning settings
INTERPOLATION_METHOD = 'linear'

# Feature flags
ENABLE_WHATS_NEW = True
ENABLE_VERSION_BADGE = True
ENABLE_CHANGELOG_TAB = True