import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from ydata_profiling import ProfileReport

# Page Configuration
st.set_page_config(page_title="InsightGrid Pro", page_icon="📊", layout="wide")

st.title("InsightGrid Pro")
st.markdown("Automated EDA, Interactive Analytics, and Data Cleaning Workspace")

uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file is not None:
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv(uploaded_file)
        
    current_df = st.session_state.df
    
    tab1, tab2, tab3 = st.tabs(["📊 Quick Dashboard", "🔍 Deep Profiling", "🧹 Data Cleaning"])
    
    with tab1:
        st.subheader("Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", current_df.shape[0])
        col2.metric("Columns", current_df.shape[1])
        col3.metric("Missing Values", current_df.isna().sum().sum())
        col4.metric("Duplicates", current_df.duplicated().sum())
        
        st.dataframe(current_df.head(), use_container_width=True)
        
        st.subheader("Distribution Analysis")
        numeric_cols = current_df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Select metric to visualize:", numeric_cols)
            fig = px.histogram(current_df, x=selected_col, marginal="box", color_discrete_sequence=["#1A73E8"])
            st.plotly_chart(fig, use_container_width=True)
            
    with tab2:
        st.subheader("Automated Statistical Report")
        if st.button("Generate Deep Profile"):
            with st.spinner("Analyzing dataset..."):
                # Generate report and render as HTML
                profile = ProfileReport(current_df, explorative=True, minimal=True)
                profile_html = profile.to_html()
                components.html(profile_html, height=800, scrolling=True)
                
    with tab3:
        st.subheader("Data Cleaning Operations")
        clean_col1, clean_col2 = st.columns(2)
        
        with clean_col1:
            if st.button("Drop Missing Values (NA)"):
                st.session_state.df = current_df.dropna()
                st.success("Missing values removed.")
                st.rerun()
                
        with clean_col2:
            if st.button("Drop Duplicates"):
                st.session_state.df = current_df.drop_duplicates()
                st.success("Duplicates removed.")
                st.rerun()
                
        st.download_button("Download Cleaned Dataset", data=st.session_state.df.to_csv(index=False).encode('utf-8'), file_name="cleaned_data.csv", mime="text/csv")
else:
    st.info("Please upload a CSV file to begin.")