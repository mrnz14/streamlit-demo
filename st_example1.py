import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Interactive EDA App", layout="wide")

st.title("Interactive EDA Dashboard")
st.write("Upload your CSV dataset and explore it interactively.")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    # --- Dataset Overview ---
    st.subheader("Dataset Overview")
    st.write("Shape:", df.shape)
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    # ----------------------------
    # Bar Plot (Categorical)
    # ----------------------------
    if cat_cols:
        st.subheader("Bar Plot")
        col_x = st.selectbox("Choose a categorical column:", cat_cols, key="bar_x")
        col_y = st.selectbox("Choose a numeric column:", [None] + numeric_cols, key="bar_y")

        if col_y:
            categories = st.multiselect(f"Select categories from {col_x}:", df[col_x].unique(), default=df[col_x].unique())
            df_filtered = df[df[col_x].isin(categories)]
            fig = px.bar(df_filtered, x=col_x, y=col_y, title=f"Bar plot of {col_y} by {col_x}")
        else:
            counts = df[col_x].value_counts().reset_index()
            counts.columns = [col_x, "Count"]  # rename columns
            fig = px.bar(counts, x=col_x, y="Count", title=f"Count of {col_x}")
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # Distribution Plot (Histogram)
    # ----------------------------
    if numeric_cols:
        st.subheader("Distribution Plot")
        col_hist = st.selectbox("Choose a numeric column:", numeric_cols, key="hist")
        bins = st.slider("Number of bins:", min_value=5, max_value=100, value=30)

        color_col = st.selectbox("Group distribution by (optional):", [None] + cat_cols, key="hist_color")
        fig = px.histogram(df, x=col_hist, nbins=bins, color=color_col, marginal="box",
                           title=f"Distribution of {col_hist}")
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # Scatter Plot
    # ----------------------------
    if len(numeric_cols) >= 2:
        st.subheader("Scatter Plot")
        col_x = st.selectbox("X-axis:", numeric_cols, key="scatter_x")
        col_y = st.selectbox("Y-axis:", numeric_cols, key="scatter_y")
        color_col = st.selectbox("Color by (optional):", [None] + cat_cols, key="scatter_color")

        df_filtered = df.copy()
        if color_col:
            categories = st.multiselect(f"Select categories from {color_col}:", df[color_col].unique(), default=df[color_col].unique())
            df_filtered = df[df[color_col].isin(categories)]

        fig = px.scatter(df_filtered, x=col_x, y=col_y, color=color_col,
                         title=f"Scatter plot: {col_x} vs {col_y}")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Upload a CSV file to start.")
