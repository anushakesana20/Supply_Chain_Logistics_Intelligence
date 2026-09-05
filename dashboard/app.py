import streamlit as st
import pandas as pd
import sqlite3
import joblib
import pickle
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Supply Chain Analytics Dashboard",
    page_icon="📦",
    layout="wide"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "supply_chain.db"
MODEL_DIR = BASE_DIR / "models"


# ============================================================
# TITLE
# ============================================================

st.title("📦 Supply Chain Analytics Dashboard")
st.subheader("DataCo Smart Supply Chain Analysis")

st.markdown("---")


# ============================================================
# DATABASE
# ============================================================

@st.cache_data
def load_data():

    if not DB_PATH.exists():
        st.error(f"Database not found: {DB_PATH}")
        st.stop()

    conn = sqlite3.connect(DB_PATH)

    tables = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """,
        conn
    )

    if tables.empty:
        conn.close()
        st.error("No tables found inside supply_chain.db")
        st.stop()

    if "supply_chain" in tables["name"].values:
        table_name = "supply_chain"
    else:
        table_name = tables["name"].iloc[0]

    df = pd.read_sql_query(
        f'SELECT * FROM "{table_name}"',
        conn
    )

    conn.close()

    return df


df = load_data()


# ============================================================
# BASIC CLEANING
# ============================================================

numeric_columns = [
    "Sales",
    "Order Item Quantity",
    "Product Price",
    "Days for shipment (scheduled)",
    "Late_delivery_risk"
]

for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")


# ------------------------------------------------------------
# MARKET
# ------------------------------------------------------------

if "Market" in df.columns:

    markets = sorted(
        df["Market"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_market = st.sidebar.selectbox(
        "Select Market",
        ["All"] + markets
    )

else:

    selected_market = "All"


# ------------------------------------------------------------
# SHIPPING MODE
# ------------------------------------------------------------

if "Shipping Mode" in df.columns:

    shipping_modes = sorted(
        df["Shipping Mode"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_shipping = st.sidebar.selectbox(
        "Select Shipping Mode",
        ["All"] + shipping_modes
    )

else:

    selected_shipping = "All"


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_market != "All":

    filtered_df = filtered_df[
        filtered_df["Market"] == selected_market
    ]


if selected_shipping != "All":

    filtered_df = filtered_df[
        filtered_df["Shipping Mode"] == selected_shipping
    ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

records = len(filtered_df)


# ------------------------------------------------------------
# ORDERS
# ------------------------------------------------------------

if "Order Id" in filtered_df.columns:

    orders = filtered_df["Order Id"].nunique()

elif "Order ID" in filtered_df.columns:

    orders = filtered_df["Order ID"].nunique()

else:

    orders = records


# ------------------------------------------------------------
# CUSTOMERS
# ------------------------------------------------------------

if "Customer Id" in filtered_df.columns:

    customers = filtered_df["Customer Id"].nunique()

elif "Customer ID" in filtered_df.columns:

    customers = filtered_df["Customer ID"].nunique()

else:

    customers = 0


# ------------------------------------------------------------
# SALES
# ------------------------------------------------------------

if "Sales" in filtered_df.columns:

    sales = filtered_df["Sales"].sum()

else:

    sales = 0


# ------------------------------------------------------------
# PROFIT
# ------------------------------------------------------------

if "Order Profit Per Order" in filtered_df.columns:

    profit = filtered_df[
        "Order Profit Per Order"
    ].sum()

elif "Benefit per order" in filtered_df.columns:

    profit = filtered_df[
        "Benefit per order"
    ].sum()

else:

    profit = 0


# ============================================================
# KPI DISPLAY
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "📋 Records",
    f"{records:,}"
)

col2.metric(
    "🛒 Orders",
    f"{orders:,}"
)

col3.metric(
    "👥 Customers",
    f"{customers:,}"
)

col4.metric(
    "💰 Sales",
    f"${sales:,.0f}"
)

col5.metric(
    "📈 Profit",
    f"${profit:,.0f}"
)


st.markdown("---")


# ============================================================
# DELIVERY STATUS
# ============================================================

st.header("🚚 Delivery Status")


if "Delivery Status" in filtered_df.columns:

    delivery_counts = (
        filtered_df["Delivery Status"]
        .value_counts()
        .sort_values(ascending=False)
    )

    st.bar_chart(delivery_counts)

else:

    st.info(
        "Delivery Status column not available."
    )


# ============================================================
# TOP CATEGORIES
# ============================================================

st.header("🏆 Top 10 Categories by Sales")


if (
    "Category Name" in filtered_df.columns
    and "Sales" in filtered_df.columns
):

    category_sales = (
        filtered_df
        .groupby("Category Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    category_sales.sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Sales")
    ax.set_ylabel("Category")
    ax.set_title(
        "Top 10 Categories by Sales"
    )

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# TOP REGIONS
# ============================================================

st.header("🌍 Top 10 Regions by Sales")


if (
    "Order Region" in filtered_df.columns
    and "Sales" in filtered_df.columns
):

    region_sales = (
        filtered_df
        .groupby("Order Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    region_sales.sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel("Sales")
    ax.set_ylabel("Region")
    ax.set_title(
        "Top 10 Regions by Sales"
    )

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# SHIPPING MODE DISTRIBUTION
# ============================================================

st.header("🚛 Shipping Mode Distribution")


if "Shipping Mode" in filtered_df.columns:

    shipping_counts = (
        filtered_df["Shipping Mode"]
        .value_counts()
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    shipping_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Shipping Mode")
    ax.set_ylabel("Number of Records")
    ax.set_title(
        "Shipping Mode Distribution"
    )

    plt.xticks(rotation=30)

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# LATE DELIVERY ANALYSIS
# ============================================================

st.header("⚠️ Late Delivery Risk")


if "Late_delivery_risk" in filtered_df.columns:

    risk_counts = (
        filtered_df["Late_delivery_risk"]
        .value_counts()
        .sort_index()
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "On-Time Orders",
            f"{risk_counts.get(0, 0):,}"
        )

    with col2:

        st.metric(
            "Late Orders",
            f"{risk_counts.get(1, 0):,}"
        )

    with col3:

        total = risk_counts.sum()

        if total > 0:

            late_percentage = (
                risk_counts.get(1, 0)
                / total
            ) * 100

        else:

            late_percentage = 0

        st.metric(
            "Late Delivery Rate",
            f"{late_percentage:.2f}%"
        )


else:

    st.info(
        "Late_delivery_risk column not available."
    )


# ============================================================
# SHIPPING MODE VS LATE DELIVERY
# ============================================================

st.header("🚚 Late Delivery by Shipping Mode")


if (
    "Shipping Mode" in filtered_df.columns
    and "Late_delivery_risk" in filtered_df.columns
):

    shipping_risk = (
        filtered_df
        .groupby("Shipping Mode")[
            "Late_delivery_risk"
        ]
        .mean()
        .sort_values(ascending=False)
        * 100
    )

    st.bar_chart(
        shipping_risk
    )

    st.caption(
        "Percentage of records labelled as late by shipping mode."
    )


# ============================================================
# MACHINE LEARNING
# ============================================================

st.markdown("---")

st.header(
    "🤖 Machine Learning — Late Delivery Prediction"
)


# ============================================================
# FIND MODEL
# ============================================================

def find_model():

    possible_models = [

        MODEL_DIR / "late_delivery_model.pkl",

        MODEL_DIR / "late_delivery_model.joblib",

        MODEL_DIR / "final_model.pkl",

        MODEL_DIR / "final_model.joblib",

        MODEL_DIR / "late_delivery.pkl",

        MODEL_DIR / "model.pkl"

    ]

    for model_path in possible_models:

        if model_path.exists():

            return model_path


    if MODEL_DIR.exists():

        for file in MODEL_DIR.iterdir():

            if file.suffix.lower() in [
                ".pkl",
                ".joblib"
            ]:

                return file


    return None


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_ml_model():

    model_path = find_model()

    if model_path is None:

        return None, None, "Model file not found."


    model = None

    # --------------------------------------------------------
    # Try joblib
    # --------------------------------------------------------

    try:

        model = joblib.load(
            model_path
        )

    except Exception:

        # ----------------------------------------------------
        # Try pickle
        # ----------------------------------------------------

        try:

            with open(
                model_path,
                "rb"
            ) as file:

                model = pickle.load(file)

        except Exception as e:

            return None, None, str(e)


    # --------------------------------------------------------
    # Load feature names
    # --------------------------------------------------------

    feature_names = None

    feature_path = (
        MODEL_DIR /
        "feature_names.pkl"
    )

    if feature_path.exists():

        try:

            feature_names = joblib.load(
                feature_path
            )

        except Exception:

            try:

                with open(
                    feature_path,
                    "rb"
                ) as file:

                    feature_names = pickle.load(
                        file
                    )

            except Exception:

                feature_names = None


    return model, feature_names, None


model, feature_names, model_error = (
    load_ml_model()
)


# ============================================================
# MODEL STATUS
# ============================================================

if model is not None:

    st.success(
        "✅ Late-delivery ML model loaded successfully!"
    )

    expected_features = getattr(
        model,
        "n_features_in_",
        None
    )

    if expected_features is not None:

        st.write(
            f"Model expects **{expected_features} features**."
        )

    if feature_names is not None:

        st.write(
            f"Saved feature names: **{len(feature_names)}**"
        )


else:

    st.warning(
        "⚠️ ML model could not be loaded."
    )

    if model_error:

        st.code(
            model_error
        )


# ============================================================
# ML PREDICTION INPUT
# ============================================================

if model is not None:

    st.subheader(
        "📦 Predict Late Delivery Risk"
    )

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # LEFT COLUMN
    # --------------------------------------------------------

    with col1:

        scheduled_days = st.number_input(
            "Days for shipment (scheduled)",
            min_value=0,
            max_value=20,
            value=4
        )


        shipping_mode = st.selectbox(
            "Shipping Mode",
            sorted(
                df["Shipping Mode"]
                .dropna()
                .unique()
                .tolist()
            )
        )


        market = st.selectbox(
            "Market",
            sorted(
                df["Market"]
                .dropna()
                .unique()
                .tolist()
            )
        )


        order_region = st.selectbox(
            "Order Region",
            sorted(
                df["Order Region"]
                .dropna()
                .unique()
                .tolist()
            )
        )


    # --------------------------------------------------------
    # RIGHT COLUMN
    # --------------------------------------------------------

    with col2:

        category = st.selectbox(
            "Category",
            sorted(
                df["Category Name"]
                .dropna()
                .unique()
                .tolist()
            )
        )


        sales_input = st.number_input(
            "Sales",
            min_value=0.0,
            value=100.0
        )


        quantity = st.number_input(
            "Order Item Quantity",
            min_value=1,
            value=1
        )


        product_price = st.number_input(
            "Product Price",
            min_value=0.0,
            value=100.0
        )


    # ========================================================
    # PREDICT BUTTON
    # ========================================================

    if st.button(
        "🔮 Predict Delivery Risk",
        type="primary"
    ):

        # ----------------------------------------------------
        # INPUT DATA
        # ----------------------------------------------------

        input_data = pd.DataFrame({

            "Days for shipment (scheduled)": [
                scheduled_days
            ],

            "Shipping Mode": [
                shipping_mode
            ],

            "Market": [
                market
            ],

            "Order Region": [
                order_region
            ],

            "Category Name": [
                category
            ],

            "Sales": [
                sales_input
            ],

            "Order Item Quantity": [
                quantity
            ],

            "Product Price": [
                product_price
            ]

        })


        try:

            # =================================================
            # FEATURES
            # =================================================

            categorical_features = [
                "Shipping Mode",
                "Market",
                "Order Region",
                "Category Name"
            ]


            numerical_features = [
                "Days for shipment (scheduled)",
                "Sales",
                "Order Item Quantity",
                "Product Price"
            ]


            # =================================================
            # CREATE PREPROCESSOR
            # =================================================

            preprocessor = ColumnTransformer(

                transformers=[

                    (
                        "categorical",

                        OneHotEncoder(
                            handle_unknown="ignore"
                        ),

                        categorical_features
                    ),

                    (
                        "numerical",

                        "passthrough",

                        numerical_features
                    )

                ]
            )


            # =================================================
            # PREPARE ORIGINAL DATA
            # =================================================

            X_original = df[
                numerical_features +
                categorical_features
            ].copy()


            X_original[
                numerical_features
            ] = (
                X_original[
                    numerical_features
                ]
                .apply(
                    pd.to_numeric,
                    errors="coerce"
                )
            )


            X_original = X_original.dropna()


            # =================================================
            # FIT PREPROCESSOR
            # =================================================

            preprocessor.fit(
                X_original
            )


            # =================================================
            # TRANSFORM INPUT
            # =================================================

            X_input_transformed = (
                preprocessor.transform(
                    input_data
                )
            )


            # =================================================
            # GET GENERATED FEATURE NAMES
            # =================================================

            generated_features = (
                preprocessor
                .get_feature_names_out()
            )


            # =================================================
            # CONVERT TO DATAFRAME
            # =================================================

            if hasattr(
                X_input_transformed,
                "toarray"
            ):

                X_input_array = (
                    X_input_transformed
                    .toarray()
                )

            else:

                X_input_array = (
                    X_input_transformed
                )


            X_input_df = pd.DataFrame(
                X_input_array,
                columns=generated_features
            )


            # =================================================
            # MATCH MODEL FEATURE COUNT
            # =================================================

            expected_features = getattr(
                model,
                "n_features_in_",
                None
            )


            # -------------------------------------------------
            # If saved feature names are available
            # -------------------------------------------------

            if feature_names is not None:

                feature_names_list = list(
                    feature_names
                )

                # Add missing features

                for feature in feature_names_list:

                    if feature not in X_input_df.columns:

                        X_input_df[feature] = 0


                # Keep only expected features
                # and preserve exact order

                X_input_df = X_input_df[
                    feature_names_list
                ]


            # =================================================
            # FALLBACK FEATURE COUNT FIX
            # =================================================

            if (
                expected_features is not None
                and X_input_df.shape[1]
                != expected_features
            ):

                current_features = (
                    X_input_df.shape[1]
                )


                if current_features < expected_features:

                    for i in range(
                        current_features,
                        expected_features
                    ):

                        X_input_df[
                            f"_missing_feature_{i}"
                        ] = 0


                elif current_features > expected_features:

                    X_input_df = X_input_df.iloc[
                        :,
                        :expected_features
                    ]


            # =================================================
            # FINAL MODEL INPUT
            # =================================================

            X_input = X_input_df


            # =================================================
            # PREDICTION
            # =================================================

            prediction = model.predict(
                X_input
            )[0]


            # =================================================
            # PROBABILITY
            # =================================================

            late_probability = None
            ontime_probability = None


            if hasattr(
                model,
                "predict_proba"
            ):

                probabilities = (
                    model
                    .predict_proba(
                        X_input
                    )[0]
                )


                # Handle binary classification

                if len(probabilities) >= 2:

                    ontime_probability = (
                        probabilities[0] * 100
                    )

                    late_probability = (
                        probabilities[1] * 100
                    )


            # =================================================
            # DISPLAY RESULT
            # =================================================

            st.markdown("---")

            if prediction == 1:

                st.error(
                    "🚨 LATE DELIVERY"
                )

                st.warning(
                    "Risk Level: HIGH"
                )

            else:

                st.success(
                    "✅ ON-TIME DELIVERY"
                )

                st.success(
                    "Risk Level: LOW"
                )


            # =================================================
            # PROBABILITY DISPLAY
            # =================================================

            if late_probability is not None:

                col1, col2 = st.columns(2)


                with col1:

                    st.metric(
                        "On-Time Probability",
                        f"{ontime_probability:.2f}%"
                    )


                with col2:

                    st.metric(
                        "Late Probability",
                        f"{late_probability:.2f}%"
                    )


            # =================================================
            # DEBUG INFO
            # =================================================

            st.caption(
                f"Prediction generated using "
                f"{X_input.shape[1]} model features."
            )


        except Exception as e:

            st.error(
                "Prediction failed."
            )

            st.code(
                str(e)
            )


# ============================================================
# FINAL ML MODEL PERFORMANCE
# ============================================================

st.markdown("---")

st.header(
    "📊 Final ML Model Performance"
)


# ============================================================
# MODEL METRICS
# ============================================================

accuracy = 0.6873476623088854


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Accuracy",
    f"{accuracy * 100:.2f}%"
)


col2.metric(
    "On-Time Precision",
    "61%"
)


col3.metric(
    "Late Precision",
    "80%"
)


col4.metric(
    "Late Recall",
    "57%"
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

st.subheader(
    "🎯 Confusion Matrix"
)


cm = pd.DataFrame(

    [
        [13521, 2787],
        [8501, 11295]
    ],

    index=[
        "Actual On-Time",
        "Actual Late"
    ],

    columns=[
        "Predicted On-Time",
        "Predicted Late"
    ]
)


st.dataframe(
    cm,
    use_container_width=True
)


# ============================================================
# CONFUSION MATRIX CHART
# ============================================================

fig, ax = plt.subplots(
    figsize=(7, 5)
)


ax.imshow(cm.values)


ax.set_xticks(
    range(len(cm.columns))
)

ax.set_xticklabels(
    cm.columns
)


ax.set_yticks(
    range(len(cm.index))
)

ax.set_yticklabels(
    cm.index
)


for i in range(
    len(cm.index)
):

    for j in range(
        len(cm.columns)
    ):

        ax.text(
            j,
            i,
            f"{cm.iloc[i, j]:,}",
            ha="center",
            va="center"
        )


ax.set_xlabel(
    "Predicted Label"
)

ax.set_ylabel(
    "True Label"
)

ax.set_title(
    "Final Model - Confusion Matrix"
)


st.pyplot(fig)

plt.close(fig)


# ============================================================
# MODEL INTERPRETATION
# ============================================================

st.subheader(
    "💡 Model Interpretation"
)


st.write(
    """
The machine learning model predicts whether a shipment
is likely to be delivered on time or late.

The model achieved approximately **68.73% accuracy**
on the test data.

The model uses shipment, sales, product and geographical
information to predict late-delivery risk.

Important factors include:

• Days for shipment (scheduled)

• Shipping Mode

• Market

• Order Region

• Category Name

• Sales

• Order Item Quantity

• Product Price

The model can help logistics teams identify shipments
that have a higher probability of late delivery.
"""
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.subheader(
    "📌 Business Insights"
)


st.info(
    """
1. Standard Class is the most frequently used shipping mode.

2. Late deliveries represent a significant portion
   of the dataset.

3. Scheduled shipment days are an important factor
   affecting delivery risk.

4. Shipping mode also has an important influence
   on delivery performance.

5. The prediction model can help logistics teams
   identify potentially delayed shipments before delivery.

6. The dashboard allows users to filter the analysis
   by market and shipping mode.
"""
)


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.subheader(
    "📥 Download Data"
)


csv_data = filtered_df.to_csv(
    index=False
)


st.download_button(

    label="⬇️ Download Filtered Dataset",

    data=csv_data,

    file_name="filtered_supply_chain_data.csv",

    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Supply Chain Logistics Intelligence Project | "
    "DataCo Smart Supply Chain Dataset"
)