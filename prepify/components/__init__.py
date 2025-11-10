# ============================================
# FILE: components/__init__.py (Update)
# ============================================
# Import all components
from .logo import display_logo
from .header import display_header
from .footer import display_footer
from .whats_new import show_whats_new, show_version_badge

__all__ = [
    'display_logo',
    'display_header', 
    'display_footer',
    'show_whats_new',
    'show_version_badge'
]