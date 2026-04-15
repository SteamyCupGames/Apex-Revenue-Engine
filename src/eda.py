import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google.cloud import bigquery
from dotenv import load_dotenv

QUERY = """
    SELECT *
    FROM `mlopsmarketingproject.olist_marketing_qualified_leads_dataset.abt_marketing_leads`
    """

def aggregate_data(df):
    attribution_df = df.groupby('origin').agg({
        'mql_id': 'count',
        'converted': 'sum',
        'ltv_revenue': 'sum'
    }).rename(columns={'mql_id': 'total_leads', 'converted': 'deals_won'})

    # We calculate key metrics (Efficiency vs Value)
    attribution_df['conversion_rate'] = (attribution_df['deals_won'] / attribution_df['total_leads']) * 100
    attribution_df['avg_ltv_per_deal'] = attribution_df['ltv_revenue'] / attribution_df['deals_won']

    # Sort by volume for visualization
    attribution_df = attribution_df.sort_values('total_leads', ascending=False)

    return attribution_df

def eda():
    load_dotenv()

    client = bigquery.Client()

    # Execute the query and convert to DataFrame
    df = client.query(QUERY).to_dataframe()

    df_aggregated = aggregate_data(df)

    df_aggregated.to_parquet('Data\\Processed\\visualization_ready_data.parquet', index=False)