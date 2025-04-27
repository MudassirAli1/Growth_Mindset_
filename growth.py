import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }   
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📂DataSweeper Sterling Integrator By Mudassir Ali")
st.write("Convert your files between CSV and Excel formats with built-in data cleaning and visualization, creating a project for Quarter 3.")

# File uploader
upload_files = st.file_uploader("Upload your files (CSV or Excel formats supported):", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue

        st.write(f"🔎 **Preview of {file.name}:**")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader(f"⚙ Data Cleaning Options for {file.name}")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("☑ Duplicates Removed!")

            with col2:
                if st.button(f"Fill missing values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("☑ Missing Values Filled!")

        # Column Selection
        st.subheader(f"Select columns to keep from {file.name}")
        columns = st.multiselect(f"Select columns for {file.name}", df.columns, default=list(df.columns))
        df = df[columns]

        # Data Visualization
        st.subheader(f"📊 Data Visualization for {file.name}")
        if st.checkbox(f"Visualize data for {file.name}"):
            numeric_data = df.select_dtypes(include='number')
            if not numeric_data.empty:
                st.bar_chart(numeric_data.iloc[:, :2])
            else:
                st.warning("No numeric columns available for visualization.")

        # Conversion Options
        st.subheader(f"⚙ Conversion Options for {file.name}")
        conversion_type = st.radio(f"Convert {file.name} to:", ("CSV", "Excel"), key=file.name)

        if st.button(f"Convert {file.name}", key=file.name + "_convert"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                download_file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                download_file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {download_file_name}",
                data=buffer,
                file_name=download_file_name,
                mime=mime_type
            )
            st.success("✨ File Converted Successfully!")
