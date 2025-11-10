# ============================================
# FILE: utils/data_processing.py (Enhanced)
# ============================================
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

def remove_missing_values(df):
    """Remove all rows with missing values"""
    return df.dropna()

def fill_missing_values(df):
    """Fill missing values intelligently"""
    cleaned_df = df.copy()
    
    # Fill categorical columns with mode
    cat_cols = cleaned_df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if cleaned_df[col].isnull().sum() > 0:
            mode_value = cleaned_df[col].mode()
            if len(mode_value) > 0:
                cleaned_df[col].fillna(mode_value[0], inplace=True)
    
    # Interpolate numerical columns
    num_cols = cleaned_df.select_dtypes(include=['number']).columns
    for col in num_cols:
        if cleaned_df[col].isnull().sum() > 0:
            cleaned_df[col].interpolate(method='linear', inplace=True)
            cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
    
    return cleaned_df

def remove_duplicates(df):
    """Remove duplicate rows"""
    return df.drop_duplicates()

def clean_all(df):
    """Apply all cleaning operations"""
    cleaned_df = fill_missing_values(df)
    cleaned_df = remove_duplicates(cleaned_df)
    return cleaned_df

def encode_categorical(df, column, method):
    """Encode categorical variables"""
    encoded_df = df.copy()
    
    if method == "Label Encoding":
        le = LabelEncoder()
        encoded_df[column] = le.fit_transform(encoded_df[column].astype(str))
    elif method == "One-Hot Encoding":
        encoded_df = pd.get_dummies(encoded_df, columns=[column], prefix=column)
    
    return encoded_df

def normalize_data(df, columns):
    """Normalize numeric columns to 0-1 range"""
    normalized_df = df.copy()
    scaler = MinMaxScaler()
    
    normalized_df[columns] = scaler.fit_transform(normalized_df[columns])
    
    return normalized_df

def standardize_data(df, columns):
    """Standardize numeric columns (z-score)"""
    standardized_df = df.copy()
    scaler = StandardScaler()
    
    standardized_df[columns] = scaler.fit_transform(standardized_df[columns])
    
    return standardized_df

def convert_column_type(df, column, new_type):
    """Convert column to specified type"""
    converted_df = df.copy()
    
    if new_type == "int":
        converted_df[column] = pd.to_numeric(converted_df[column], errors='coerce').astype('Int64')
    elif new_type == "float":
        converted_df[column] = pd.to_numeric(converted_df[column], errors='coerce')
    elif new_type == "str":
        converted_df[column] = converted_df[column].astype(str)
    elif new_type == "datetime":
        converted_df[column] = pd.to_datetime(converted_df[column], errors='coerce')
    elif new_type == "category":
        converted_df[column] = converted_df[column].astype('category')
    
    return converted_df

def detect_outliers_zscore(df, column, threshold=3):
    """Detect outliers using Z-score method"""
    col_data = df[column].dropna()
    z_scores = np.abs((col_data - col_data.mean()) / col_data.std())
    outlier_indices = col_data[z_scores > threshold].index.tolist()
    return outlier_indices

def detect_outliers_iqr(df, column, multiplier=1.5):
    """Detect outliers using IQR method"""
    col_data = df[column].dropna()
    Q1 = col_data.quantile(0.25)
    Q3 = col_data.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    outlier_indices = col_data[(col_data < lower_bound) | (col_data > upper_bound)].index.tolist()
    return outlier_indices

def remove_outliers(df, column, method):
    """Remove outliers from dataframe"""
    if "Z-Score" in method:
        outlier_indices = detect_outliers_zscore(df, column)
    elif "IQR" in method:
        outlier_indices = detect_outliers_iqr(df, column)
    else:  # Both methods
        zscore_outliers = detect_outliers_zscore(df, column)
        iqr_outliers = detect_outliers_iqr(df, column)
        outlier_indices = list(set(zscore_outliers) | set(iqr_outliers))
    
    return df.drop(outlier_indices)