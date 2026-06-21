import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine,text


engine = create_engine(
    f"mysql+pymysql://{st.secrets['MYSQLUSER']}:{st.secrets['MYSQLPASSWORD']}@{st.secrets['MYSQLHOST']}:{st.secrets['MYSQLPORT']}/{st.secrets['MYSQLDATABASE']}"
)


providers = pd.read_sql("SELECT * FROM providers", engine)
receivers = pd.read_sql("SELECT * FROM receivers", engine)
food = pd.read_sql("SELECT * FROM food_listings", engine)
claims = pd.read_sql("SELECT * FROM claims", engine)


import streamlit as st

st.set_page_config(
  page_title="Food Waste management",
  page_icon="🍽️",
  layout='wide'
 )
st.sidebar.title("Navigation")
page=st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Provider Analysis",
        "Receiver Analysis",
        "Food Analysis",
        "Claims Analysis",
        "SQL Insights",
        "CRUD Operations"
    ]
)

if page == "Dashboard":

    st.title("📊 Dashboard")

    # =========================
    # KPI CARDS
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Providers", len(providers))

    with col2:
        st.metric("Receivers", len(receivers))

    with col3:
        st.metric("Food Listings", len(food))

    with col4:
        st.metric("Claims", len(claims))

    st.markdown("---")

    # =========================
    # FOOD TYPE DISTRIBUTION
    # =========================

    st.subheader("🍞 Food Type Distribution")

    food_type = food["Food_Type"].value_counts()

    fig1 = px.pie(
        values=food_type.values,
        names=food_type.index,
        title="Food Type Distribution"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # =========================
    # MEAL TYPE DISTRIBUTION
    # =========================

    st.subheader("🍽 Meal Type Distribution")

    meal_type = food["Meal_Type"].value_counts()

    fig2 = px.bar(
        x=meal_type.index,
        y=meal_type.values,
        title="Meal Type Distribution",
        labels={
            "x": "Meal Type",
            "y": "Count"
        }
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # =========================
    # PROVIDER TYPE DISTRIBUTION
    # =========================

    st.subheader("🏪 Provider Type Distribution")

    provider_type = food["Provider_Type"].value_counts()

    fig3 = px.bar(
        x=provider_type.index,
        y=provider_type.values,
        title="Provider Type Distribution",
        color=provider_type.index
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # =========================
    # TOP 10 LOCATIONS
    # =========================

    st.subheader("📍 Top 10 Locations by Food Listings")

    location_count = food["Location"].value_counts().head(10)

    fig4 = px.bar(
        x=location_count.values,
        y=location_count.index,
        orientation="h",
        title="Top 10 Locations"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    # =========================
    # RECENT FOOD LISTINGS
    # =========================

    st.subheader("📋 Food Listings Preview")

    st.dataframe(food.head(20))
    
    


elif page=="Provider Analysis":
    st.title("🏪 Provider Analysis")
    st.subheader("Provider Type Distribution")
    provider_counts=providers["Type"].value_counts()
    fig1=px.pie(
        values=provider_counts.values,
        names=provider_counts.index,
        title="Provider Types"
    )
    st.plotly_chart(fig1,use_container_width=True)
    st.subheader("Top 10 cities by Providers")
    city_counts = providers["City"].value_counts().head(10)

    fig2=px.bar(
        x=city_counts.values,
        y=city_counts.index,
        orientation="h",
        title="Top Provider Cities"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Providers Data")

    st.dataframe(providers)
    
elif page == "Receiver Analysis":
    st.title("🏢 Receiver Analysis")
    receiver_type=receivers["Type"].value_counts()
    fig1=px.pie(
        values=receiver_type.values,
        names=receiver_type.index,
        title="Receiver Type"
    )
    st.plotly_chart(fig1,use_container_width=True)
    city_counts=receivers["City"].value_counts().head(10)
    fig2=px.bar(
        x=city_counts.values,
        y=city_counts.index,
        orientation="h",
        title="Top Receiver Cities"
    )
    st.plotly_chart(fig2,use_container_width=True)
    st.dataframe(receivers)
elif page == "Food Analysis":
    st.title("🍞 Food Analysis")
 

    st.subheader("Food Type Distribution")

    food_type = food["Food_Type"].value_counts()

    fig1 = px.pie(
        values=food_type.values,
        names=food_type.index,
        title="Food Type Distribution"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Meal Type Distribution")

    meal_type = food["Meal_Type"].value_counts()

    fig2 = px.bar(
        x=meal_type.index,
        y=meal_type.values,
        title="Meal Type Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Quantity by Food Type")

    qty_food = food.groupby("Food_Type")["Quantity"].sum()

    fig3 = px.bar(
        x=qty_food.index,
        y=qty_food.values,
        title="Quantity by Food Type"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.dataframe(food)

elif page == "Claims Analysis":
    st.title("📋 Claims Analysis")
    st.subheader("Claims Status Distribution")
    status_counts=claims["Status"].value_counts()
    fig1=px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Claims Status Distribution"
    )
    st.plotly_chart(fig1,use_container_width=True)
    st.subheader("Top receivers")
    top_receivers=claims["Receiver_ID"].value_counts().head(10)
    fig=px.bar(
        x=top_receivers.index.astype(str),
        y=top_receivers.values,
        title="Top Receivers"
    )
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(claims)

elif page == "SQL Insights":
    st.title("🗄️ SQL Insights")        
  

    query1 = """
    SELECT City,
    COUNT(*) AS Total_Providers
    FROM providers
    GROUP BY City
    ORDER BY Total_Providers DESC
    """

    result1 = pd.read_sql(query1, engine)

    st.subheader("Providers by City")

    st.dataframe(result1)

    fig = px.bar(
        result1,
        x="City",
        y="Total_Providers",
        title="Providers by City"
    )

    st.plotly_chart(fig, use_container_width=True)
elif page == "CRUD Operations":

    st.title("🛠 CRUD Operations")

    operation = st.selectbox(
        "Select Operation",
        [
            "Add Food",
            "Update Food Quantity",
            "Delete Food"
        ]
    )

    # CREATE
    if operation == "Add Food":

        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1)
        location = st.text_input("Location")
        food_type = st.text_input("Food Type")
        meal_type = st.text_input("Meal Type")
        provider_id = st.number_input("Provider ID", min_value=1)

        if st.button("Add Food"):

            query = f"""
            INSERT INTO food_listings
            (Food_Name, Quantity, Location, Food_Type, Meal_Type, Provider_ID)
            VALUES
            ('{food_name}', {quantity}, '{location}',
            '{food_type}', '{meal_type}', {provider_id})
            """

            with engine.begin() as conn:
                conn.execute(text(query))

            st.success("Food Added Successfully")
            st.subheader("Latest Food Records")
            food_check=pd.read_sql(
                "SELECT * FROM food_listings ORDER BY Food_ID DESC LIMIT 10",
                engine
            )
            st.dataframe(food_check)

    # UPDATE
    elif operation == "Update Food Quantity":

        food_id = st.number_input("Food ID", min_value=1)
        new_quantity = st.number_input("New Quantity", min_value=1)

        if st.button("Update"):

            query = f"""
            UPDATE food_listings
            SET Quantity = {new_quantity}
            WHERE Food_ID = {food_id}
            """

            with engine.begin() as conn:
                conn.execute(text(query))

            st.success("Quantity Updated Successfully")

    # DELETE
    elif operation == "Delete Food":

        food_id = st.number_input("Food ID", min_value=1)

        if st.button("Delete"):

            query = f"""
            DELETE FROM food_listings
            WHERE Food_ID = {food_id}
            """

            with engine.begin() as conn:
                conn.execute(text(query))

            st.success("Food Deleted Successfully")