import streamlit as st
import pandas as pd
from datetime import datetime
from en_api import authenticate

st.set_page_config(page_title="Engaging Networks API Export", layout="centered")

st.title("📊 Engaging Networks API Data Export")

token = st.secrets["en_api"]["token"]

start_date = st.date_input("Select start date", datetime.today())
end_date = st.date_input("Select end date", datetime.today())

start_str = start_date.strftime("%m%d%Y")
end_str = end_date.strftime("%m%d%Y")

if st.button("Fetch Data"):
    with st.spinner("Fetching data from Engaging Networks..."):
        try:
            rows = authenticate(token, start_str, end_str)


            df = pd.DataFrame(rows[1:], columns=rows[0])
            st.success(f"Data retrieved successfully! {len(df)} records found.")

            st.dataframe(df.head(20))

            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download CSV",
                data=csv_bytes,
                file_name=f"en_data_{start_str}_{end_str}.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"Error fetching data: {e}")
