# verify_setup.py
print("Checking dependencies...")

try:
    import streamlit; print(f"✓ streamlit: {streamlit.__version__}")
except: print("✗ streamlit: MISSING")

try:
    import pandas; print(f"✓ pandas: {pandas.__version__}")
except: print("✗ pandas: MISSING")

try:
    import plotly; print(f"✓ plotly: {plotly.__version__}")
except: print("✗ plotly: MISSING")

try:
    import numpy; print(f"✓ numpy: {numpy.__version__}")
except: print("✗ numpy: MISSING")

try:
    import scipy; print(f"✓ scipy: {scipy.__version__}")
except: print("✗ scipy: MISSING - Run: pip install scipy")

try:
    import sklearn; print(f"✓ sklearn: {sklearn.__version__}")
except: print("✗ sklearn: MISSING - Run: pip install scikit-learn")

try:
    import openpyxl; print(f"✓ openpyxl: {openpyxl.__version__}")
except: print("✗ openpyxl: MISSING - Run: pip install openpyxl")

print("\nAll done!")