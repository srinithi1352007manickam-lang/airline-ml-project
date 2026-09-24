"""
train_model.py - Standalone Training Script for Random Forest Model
Airline Customer Satisfaction Machine Learning Project
"""

import sys
import os
import time

# Ensure safe UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from utils.preprocessing import (
    find_dataset_path,
    load_dataset,
    inspect_dataset,
    identify_target_column,
    train_and_evaluate_model,
    save_model_bundle
)

def main():
    print("=" * 70)
    print(" [*] AIRLINE CUSTOMER SATISFACTION - RANDOM FOREST TRAINING PIPELINE ")
    print("=" * 70)

    # 1. Dataset Discovery
    try:
        data_path = find_dataset_path()
        print(f"\n[1/5] [+] Found Dataset: {data_path}")
    except FileNotFoundError as e:
        print(f"\n[-] Error: {e}")
        sys.exit(1)

    # 2. Data Loading & Inspection
    print("\n[2/5] [*] Loading & Inspecting Dataset...")
    df = load_dataset(data_path)
    info = inspect_dataset(df)

    print(f"      • Total Rows: {info['num_rows']:,}")
    print(f"      • Total Columns: {info['num_cols']}")
    print(f"      • Duplicate Rows: {info['duplicates']}")
    print(f"      • Missing Values: {info['missing_values'] if info['has_missing'] else 'None'}")
    print(f"      • Categorical Features ({len(info['categorical_columns'])}): {info['categorical_columns']}")
    print(f"      • Numerical Features ({len(info['numerical_columns'])}): {len(info['numerical_columns'])} columns")

    # 3. Identify Target Column
    target_col = identify_target_column(df)
    print(f"\n[3/5] [*] Identified Target Column: '{target_col}'")
    val_counts = df[target_col].value_counts().to_dict()
    print(f"      • Class Distribution: {val_counts}")

    # 4. Training Random Forest Model
    print("\n[4/5] [*] Building Preprocessing Pipeline & Training Random Forest...")
    print("      • Train/Test Split: 80% Train, 20% Test (Stratified)")
    print("      • Estimators: 100 Trees | Max Depth: 16 | Multiprocessing: All Cores")
    
    start_time = time.time()
    result = train_and_evaluate_model(
        df=df,
        target_col=target_col,
        test_size=0.2,
        n_estimators=100,
        max_depth=16,
        random_state=42
    )
    elapsed = time.time() - start_time
    print(f"      [+] Training & Evaluation completed in {elapsed:.2f} seconds!")

    # 5. Model Evaluation Metrics
    metrics = result["metrics"]
    print("\n" + "=" * 70)
    print(" [*] MODEL PERFORMANCE EVALUATION (TEST SET)")
    print("=" * 70)
    print(f"  • Accuracy:        {metrics['accuracy'] * 100:.2f}%")
    print(f"  • Precision:       {metrics['precision'] * 100:.2f}%")
    print(f"  • Recall:          {metrics['recall'] * 100:.2f}%")
    print(f"  • F1-Score:        {metrics['f1_score'] * 100:.2f}%")
    print(f"  • ROC-AUC Score:   {metrics['roc_auc']:.4f}")
    print(f"  • Test Samples:    {metrics['test_samples']:,}")
    print("\n  • Confusion Matrix:")
    cm = metrics["confusion_matrix"]
    print(f"    [[TN={cm[0][0]:,}, FP={cm[0][1]:,}],")
    print(f"     [FN={cm[1][0]:,}, TP={cm[1][1]:,}]]")

    print("\n  • Top 10 Most Important Features:")
    for i, item in enumerate(result["feature_importances"][:10], 1):
        print(f"    {i:2d}. {item['Feature']:<35} : {item['Importance'] * 100:.2f}%")

    # 6. Save Model Bundle
    output_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")
    save_model_bundle(result, output_model_path)
    print(f"\n[5/5] [+] Trained Pipeline Bundle Saved to: {output_model_path}")
    print("=" * 70)
    print(" [*] Project training completed successfully! You can now run 'streamlit run app.py'.")
    print("=" * 70)

if __name__ == "__main__":
    main()
