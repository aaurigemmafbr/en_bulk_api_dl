import streamlit as st
import pandas as pd
from datetime import datetime
from en_api import authenticate

def check_password():
    """Simple password check stored in Streamlit secrets"""
    def password_entered():
        if st.session_state["password"] == st.secrets["app"]["password"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        return True

if check_password():
    st.set_page_config(page_title="Engaging Networks Export", layout="centered")

    st.title("📊 Engaging Networks Data Export")

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

                start_fmt = start_date.strftime("%m.%d.%y")
                end_fmt = end_date.strftime("%m.%d.%y")
                download_name = f"{start_fmt} to {end_fmt} EN Bulk API.csv"

                csv_bytes = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_bytes,
                    file_name=download_name,
                    mime="text/csv",
                )

            except Exception as e:
                st.error(f"Error fetching data: {e}")
