from src.cloud_data_engineering import execute_query_task
from src.eda import eda
from src.lead_scoring import lead_scoring

def main():
    print("🚀 Starting the data engineering task...")
    execute_query_task()
    print("✅ Data engineering task completed successfully!")

    print("🔍 Starting Exploratory Data Analysis (EDA)...")
    eda()
    print("✅ EDA completed successfully! Visualization-ready data is saved.")

    print("📊 Starting Lead Scoring...")
    lead_scoring()
    print("✅ Lead scoring completed successfully!")
    
if __name__ == "__main__":
    main()