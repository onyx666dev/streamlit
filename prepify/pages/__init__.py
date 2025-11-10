# ============================================
# FILE: pages/__init__.py (Update)
# ============================================
# Import all pages
from . import (
    data_explorer,
    data_cleaning,
    data_transformation,
    outlier_detection,
    data_insights,
    visualizations,
    advanced_analytics,
    time_series_analysis,
    changelog  # ← Add this
)

__all__ = [
    'data_explorer',
    'data_cleaning',
    'data_transformation',
    'outlier_detection',
    'data_insights',
    'visualizations',
    'advanced_analytics',
    'time_series_analysis',
    'changelog'  # ← Add this
]