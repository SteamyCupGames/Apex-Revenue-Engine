import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv


project_id = 'mlopsmarketingproject'
dataset_id = 'olist_marketing_qualified_leads_dataset'
location = 'northamerica-northeast1'

QUERY = f"""
        WITH seller_performance AS (
            SELECT 
                seller_id, 
                SUM(price) as total_revenue,
                COUNT(order_id) as total_orders
            FROM `{project_id}.{dataset_id}.olist_order_items_dataset`
            GROUP BY 1
        )
        SELECT 
            mql.mql_id,
            mql.first_contact_date,
            mql.landing_page_id,
            mql.origin,
            cd.business_segment,
            cd.lead_type,
            cd.lead_behaviour_profile, -- Key profiles: cat, wolf, shark, eagle [5]
            cd.won_date,
            IF(cd.won_date IS NOT NULL, 1, 0) as converted,
            COALESCE(sp.total_revenue, 0) as ltv_revenue,
            COALESCE(sp.total_orders, 0) as orders_count
        FROM `{project_id}.{dataset_id}.olist_marketing_qualified_leads_dataset` mql
        LEFT JOIN `{project_id}.{dataset_id}.olist_closed_deals_dataset` cd 
            ON mql.mql_id = cd.mql_id
        LEFT JOIN seller_performance sp 
            ON cd.seller_id = sp.seller_id
        """

def execute_query_task():
    load_dotenv()
    client = bigquery.Client(project=project_id)
    df_abt = client.query(QUERY, location=location).to_dataframe()

    df_abt['converted'] = df_abt['won_date'].notna().astype(int)

    qualification_cols = ['lead_type', 'lead_behaviour_profile', 'business_segment']
    df_abt[qualification_cols] = df_abt[qualification_cols].fillna('not_qualified')

    destination_table = f"{project_id}.{dataset_id}.abt_marketing_leads"

    df_abt.to_gbq(
        destination_table=destination_table,
        project_id=project_id,
        if_exists='replace', # Or 'append' if it were a daily process
        location=location
    )

    df_abt.to_parquet('Data\\Processed\\abt_marketing.parquet', index=False)