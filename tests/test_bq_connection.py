import os
from google.cloud import bigquery
from dotenv import load_dotenv

# 1. Cargar configuración
load_dotenv()

# Variables basadas en tu estructura actual
project_id = 'mlopsmarketingproject'
dataset_id = 'olist_marketing_qualified_leads_dataset' # Tu "carpeta"
location = 'northamerica-northeast1' # Ubicación detectada en detalles

client = bigquery.Client(project=project_id)

# 2. SQL con referencia de 3 niveles
# Nota: La tabla se llama igual que el dataset, por eso se repite el nombre
# El SQL corregido según tu imagen Schema.png
sql_query = """
SELECT 
    mql.origin, 
    COUNT(mql.mql_id) as total_leads,
    COUNT(cd.mql_id) as deals_won
FROM `mlopsmarketingproject.olist_marketing_qualified_leads_dataset.olist_marketing_qualified_leads_dataset` AS mql
LEFT JOIN `mlopsmarketingproject.olist_marketing_qualified_leads_dataset.olist_closed_deals_dataset` AS cd 
    ON mql.mql_id = cd.mql_id
GROUP BY 1
ORDER BY total_leads DESC
LIMIT 5
"""

try:
    print(f"⏳ Consultando en: {project_id}.{dataset_id}...")
    # Ejecución especificando la ubicación que viste en los detalles
    df = client.query(sql_query, location='northamerica-northeast1').to_dataframe()
    
    print("✅ ¡Conexión exitosa! Los datos están fluyendo desde Montreal (northeast1).")
    print(df)

except Exception as e:
    print(f"❌ Error de acceso: {e}")
    print("\n💡 Senior Tip: Verifica en la consola de GCP que las tablas (closed_deals, etc.) ")
    print(f"realmente vivan DENTRO del dataset '{dataset_id}'.")