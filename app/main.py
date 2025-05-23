import streamlit as st
import pandas as pd

st.set_page_config(page_title="FieldVerify AI Toolkit", layout="centered")

st.title("FieldVerify AI Toolkit 🛠️")
st.sidebar.title("Choose a Module")

page = st.sidebar.selectbox("Module", ["Home", "Invoice Verifier"])

if page == "Home":
    st.subheader("Welcome!")
    st.write("""
        This toolkit helps field verification teams work smarter using AI.
        Choose a module from the sidebar to get started.
    """)

elif page == "Invoice Verifier":
    st.subheader("Upload Agent Report (CSV or Excel)")

    uploaded_file = st.file_uploader("Upload agent verification report", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            # Read the uploaded file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # Normalize column names
            df.columns = df.columns.str.strip().str.lower()

            # Show success and column info
            st.success("File uploaded successfully!")
            st.write("📋 Column names:", df.columns.tolist())
            st.write("🔍 Preview:", df.head())

            # Check for job_id column
            if 'job_id' not in df.columns:
                st.error("❌ Missing 'job_id' column. Cannot proceed.")
            else:
                total_jobs = len(df)
                duplicate_jobs = df[df.duplicated('job_id', keep=False)]

                st.write(f"✅ Total Records: {total_jobs}")
                st.write(f"⚠️ Duplicates Found: {len(duplicate_jobs)}")

                if not duplicate_jobs.empty:
                    st.subheader("🚨 Duplicate Entries:")
                    st.dataframe(duplicate_jobs)

        except Exception as e:
            st.error(f"Error processing file: {e}")

