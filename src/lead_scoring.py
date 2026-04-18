import pandas as pd
import pyarrow.parquet as pq
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import classification_report, roc_auc_score
import matplotlib.pyplot as plt

def feature_engineering(df_ml):
    high_value_list = ['watches', 'health_beauty', 'audio_video_electronics']
    df_ml['is_high_value_segment'] = df_ml['business_segment'].isin(high_value_list).astype(int)

    # Encode categorical variables and build the model matrix
    features = ['origin', 'lead_type', 'is_high_value_segment']
    X = pd.get_dummies(df_ml[features], drop_first=True)
    y = df_ml['converted']  # target column derived from won_date

    # Use stratified split so class balance is preserved in train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    return X_train, X_test, y_train, y_test


def model_training(X_train, y_train):
    # Use stratified K-Folds to validate model stability across splits
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        class_weight='balanced'  # important for imbalanced binary classification
    )

    scoring = ['accuracy', 'precision', 'recall', 'roc_auc']
    cv_results = cross_validate(model, X_train, y_train, cv=skf, scoring=scoring)

    print(f"✅ Mean ROC-AUC: {cv_results['test_roc_auc'].mean():.4f} (+/- {cv_results['test_roc_auc'].std():.4f})")
    print(f"✅ Mean Recall (positive class detection): {cv_results['test_recall'].mean():.4f}")

    # Train final model on the full training set after validation
    model.fit(X_train, y_train)

    model_filename = 'C:\\Users\\User\\Desktop\\Software y Clases\\BigData\\OList\\olist-project-sa\\Model\\lead_scoring_rf_model.joblib'
    feature_list_filename = 'C:\\Users\\User\\Desktop\\Software y Clases\\BigData\\OList\\olist-project-sa\\Model\\model_features.joblib'

    joblib.dump(model, model_filename)
    joblib.dump(X_train.columns.tolist(), feature_list_filename)

def lead_scoring():
    print("⏳ Loading the local Parquet backup...")
    table = pq.read_table('C:\\Users\\User\\Desktop\\Software y Clases\\BigData\\OList\\olist-project-sa\\Data\\Processed\\abt_marketing.parquet')

    # Remove Arrow/Pandas metadata that can cause conversion conflicts
    # This avoids issues with metadata fields such as 'dbdate' during DataFrame creation
    safe_table = table.replace_schema_metadata(None)

    df_ml = safe_table.to_pandas()
    X_train, X_test, y_train, y_test = feature_engineering(df_ml)
    model = model_training(X_train, y_train)