# ============================================
# FILE: utils/file_handlers.py (Enhanced)
# ============================================
import io

def convert_df_to_csv(df):
    """Convert DataFrame to CSV for download"""
    return df.to_csv(index=False).encode('utf-8')

def convert_df_to_excel(df):
    """Convert DataFrame to Excel for download"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    return output.getvalue()

def convert_df_to_json(df):
    """Convert DataFrame to JSON for download"""
    return df.to_json(orient='records', indent=2).encode('utf-8')