from src.cloud_data_engineering import execute_query_task
from src.eda import eda

def main():
    print("🚀 Starting the data engineering task...")
    execute_query_task()
    print("✅ Data engineering task completed successfully!")

    print("🔍 Starting Exploratory Data Analysis (EDA)...")
    eda()
    print("✅ EDA completed successfully! Visualization-ready data is saved.")
    
if __name__ == "__main__":
    main()