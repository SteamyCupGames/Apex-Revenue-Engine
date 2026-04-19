import pandas as pd
import joblib
import pyarrow.parquet as pq
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

def clean_and_train_dataset(df_rf):
    df_reg = df_rf[df_rf['converted'] == 1].copy()

    high_value_list = ['watches', 'health_beauty', 'audio_video_electronics']
    df_reg['is_high_value_segment'] = df_reg['business_segment'].isin(high_value_list).astype(int)

    features = ['origin', 'lead_type', 'is_high_value_segment']
    X = pd.get_dummies(df_reg[features], drop_first=True)
    y = df_reg['ltv_revenue']  # our economic target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

def regressor(X_train, X_test, y_train, y_test):
    regressor = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42)
    regressor.fit(X_train, y_train)

    # Evaluation
    y_pred = regressor.predict(X_test)
    print(f"📊 MAE (Mean Absolute Error): ${mean_absolute_error(y_test, y_pred):.2f}")
    print(f"📊 R2 score: {r2_score(y_test, y_pred):.4f}")

    # Save artifacts for Streamlit
    joblib.dump(regressor, r'C:\Users\User\Desktop\Software y Clases\BigData\OList\olist-project-sa\Model\ltv_regressor_model.joblib')
    joblib.dump(X_train.columns.tolist(), r'C:\Users\User\Desktop\Software y Clases\BigData\OList\olist-project-sa\Model\regressor_features.joblib')

def ltv_predictor():
    table = pq.read_table('C:\\Users\\User\\Desktop\\Software y Clases\\BigData\\OList\\olist-project-sa\\Data\\Processed\\abt_marketing.parquet')
    safe_table = table.replace_schema_metadata(None)
    df_rf = safe_table.to_pandas()
    X_train, X_test, y_train, y_test = clean_and_train_dataset(df_rf)
    regressor(X_train, X_test, y_train, y_test)
