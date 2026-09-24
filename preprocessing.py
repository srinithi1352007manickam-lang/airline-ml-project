"""
preprocessing.py - Data Preprocessing & Machine Learning Pipeline Utilities
Airline Customer Satisfaction Project
"""

import os
import glob
import joblib
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, List, Optional
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

def find_dataset_path(base_dir: Optional[str] = None) -> str:
    """
    Automatically detects and locates the dataset file in the project folder.
    Checks the dataset/ subdirectory first, then the root directory.
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Preferred direct candidate paths
    candidates = [
        os.path.join(base_dir, "dataset", "Airline_customer_satisfaction.csv"),
        os.path.join(base_dir, "Airline_customer_satisfaction.csv"),
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    # Scan dataset subfolder for any CSV file
    dataset_folder = os.path.join(base_dir, "dataset")
    if os.path.isdir(dataset_folder):
        csv_files = glob.glob(os.path.join(dataset_folder, "*.csv"))
        if csv_files:
            return csv_files[0]

    # Scan project root for any CSV file
    csv_files = glob.glob(os.path.join(base_dir, "*.csv"))
    if csv_files:
        return csv_files[0]

    raise FileNotFoundError("Could not find any CSV dataset in the project directory or dataset/ folder.")


def load_dataset(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Loads dataset from disk with error handling.
    """
    if file_path is None or not os.path.exists(file_path):
        file_path = find_dataset_path()
    
    df = pd.read_csv(file_path)
    return df


def inspect_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs comprehensive structural inspection of the dataset.
    """
    missing = df.isnull().sum()
    missing_dict = missing[missing > 0].to_dict()
    duplicates_count = int(df.duplicated().sum())

    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    return {
        "num_rows": len(df),
        "num_cols": len(df.columns),
        "columns": list(df.columns),
        "numerical_columns": num_cols,
        "categorical_columns": cat_cols,
        "missing_values": missing_dict,
        "has_missing": len(missing_dict) > 0,
        "duplicates": duplicates_count,
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }


def identify_target_column(df: pd.DataFrame) -> str:
    """
    Automatically detects the target column from the dataset.
    Prioritizes columns named 'satisfaction', 'target', 'label', 'class', 
    or binary categorical columns.
    """
    # 1. Exact match on satisfaction
    for col in df.columns:
        if col.strip().lower() == "satisfaction":
            return col

    # 2. Key word match
    for col in df.columns:
        col_lower = col.strip().lower()
        if any(term in col_lower for term in ["target", "label", "outcome", "class", "satisfaction"]):
            return col

    # 3. Fallback: Find first binary categorical column
    for col in df.columns:
        if df[col].dtype == object and df[col].nunique() == 2:
            return col

    # Default to first column or last column
    return df.columns[0]


def get_feature_types(df: pd.DataFrame, target_col: str) -> Tuple[List[str], List[str]]:
    """
    Returns lists of categorical and numerical feature column names, excluding target.
    """
    feature_df = df.drop(columns=[target_col], errors="ignore")
    cat_cols = feature_df.select_dtypes(include=["object", "category"]).columns.tolist()
    num_cols = feature_df.select_dtypes(include=[np.number]).columns.tolist()
    return cat_cols, num_cols


def build_preprocessor(categorical_cols: List[str], numerical_cols: List[str]) -> ColumnTransformer:
    """
    Constructs a reusable ColumnTransformer for data preprocessing.
    - Numerical features: Median Imputation
    - Categorical features: Most Frequent Imputation + OneHotEncoding (handles unseen classes)
    """
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_cols),
            ("cat", cat_pipeline, categorical_cols)
        ],
        remainder="drop"
    )

    return preprocessor


def create_ml_pipeline(
    categorical_cols: List[str],
    numerical_cols: List[str],
    n_estimators: int = 100,
    max_depth: Optional[int] = 16,
    random_state: int = 42
) -> Pipeline:
    """
    Creates an end-to-end Scikit-Learn Pipeline combining the preprocessor
    and the RandomForestClassifier.
    """
    preprocessor = build_preprocessor(categorical_cols, numerical_cols)
    
    rf_classifier = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        n_jobs=-1
    )

    full_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", rf_classifier)
    ])

    return full_pipeline


def train_and_evaluate_model(
    df: pd.DataFrame,
    target_col: str = "satisfaction",
    test_size: float = 0.2,
    n_estimators: int = 100,
    max_depth: Optional[int] = 16,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Preprocesses data, fits Random Forest, evaluates metrics, and extracts feature importances.
    Prevents data leakage by fitting preprocessing strictly on training data.
    """
    # 1. Clean duplicates if any
    clean_df = df.drop_duplicates().copy()

    # 2. Extract features and target
    X = clean_df.drop(columns=[target_col])
    y_raw = clean_df[target_col]

    # Map target to 1 (satisfied) and 0 (dissatisfied)
    target_mapping = {"satisfied": 1, "dissatisfied": 0}
    if set(y_raw.unique()).issubset({"satisfied", "dissatisfied"}):
        y = y_raw.map(target_mapping).values
        class_labels = ["dissatisfied", "satisfied"]
    else:
        # Generic factorize
        y, uniques = pd.factorize(y_raw)
        class_labels = [str(u) for u in uniques]

    cat_cols, num_cols = get_feature_types(clean_df, target_col)

    # 3. Train-Test Split (Stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # 4. Create and train pipeline
    pipeline = create_ml_pipeline(
        categorical_cols=cat_cols,
        numerical_cols=num_cols,
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )

    pipeline.fit(X_train, y_train)

    # 5. Evaluate on test set
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else None

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_proba)) if y_proba is not None else 0.0
    cm = confusion_matrix(y_test, y_pred).tolist()
    clf_report = classification_report(y_test, y_pred, target_names=class_labels, output_dict=True)

    # 6. Extract Feature Importances
    preprocessor = pipeline.named_steps["preprocessor"]
    rf = pipeline.named_steps["classifier"]

    # Retrieve transformed feature names
    cat_encoder = preprocessor.named_transformers_["cat"].named_steps["onehot"]
    cat_feature_names = cat_encoder.get_feature_names_out(cat_cols).tolist()
    all_feature_names = num_cols + cat_feature_names

    importances = rf.feature_importances_
    feat_imp_df = pd.DataFrame({
        "Feature": all_feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False).reset_index(drop=True)

    return {
        "pipeline": pipeline,
        "metrics": {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "roc_auc": roc_auc,
            "confusion_matrix": cm,
            "classification_report": clf_report,
            "test_samples": len(y_test),
            "train_samples": len(y_train)
        },
        "feature_importances": feat_imp_df.to_dict(orient="records"),
        "categorical_cols": cat_cols,
        "numerical_cols": num_cols,
        "class_labels": class_labels,
        "target_col": target_col,
        "hyperparameters": {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "test_size": test_size,
            "random_state": random_state
        }
    }


def save_model_bundle(bundle_data: Dict[str, Any], filepath: str = "model.pkl") -> str:
    """
    Saves the entire trained pipeline, metadata, and evaluation results to disk.
    """
    joblib.dump(bundle_data, filepath)
    return filepath


def load_model_bundle(filepath: str = "model.pkl") -> Optional[Dict[str, Any]]:
    """
    Loads saved model bundle if it exists.
    """
    if os.path.exists(filepath):
        try:
            return joblib.load(filepath)
        except Exception as e:
            print(f"Error loading model bundle: {e}")
            return None
    return None
