import pandas as pd
from sqlalchemy import create_engine

# Replace with your actual Railway password
PASSWORD = "WCuuOyBHXtBqtPKFqgLjbuYeCkXYuHaG"

engine = create_engine(
    f"mysql+pymysql://root:{PASSWORD}@reseau.proxy.rlwy.net:41342/railway"
)

providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")
food = pd.read_csv("food_listings_data.csv")
claims = pd.read_csv("claims_data.csv")

providers.to_sql(
    "providers",
    con=engine,
    if_exists="replace",
    index=False
)

receivers.to_sql(
    "receivers",
    con=engine,
    if_exists="replace",
    index=False
)

food.to_sql(
    "food_listings",
    con=engine,
    if_exists="replace",
    index=False
)

claims.to_sql(
    "claims",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data uploaded successfully!")