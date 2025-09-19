import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# --- Custom CSS ---
st.markdown("""
<style>
    .stApp { background-color: #f0f8ff; }
    h1, h2, h3 { color: #004d4d; }
    .stMetric { background: #e0ffff; border-radius: 10px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- Fun facts ---
facts = [
    "🦴 Orthopedic implants can last 15–20 years depending on activity.",
    "🏃 Hip replacements are one of the most successful surgeries.",
    "🧬 Bone can regenerate without scarring.",
    "🦵 Knee replacement is one of the most common procedures."
]

# --- Staff ---
default_staff = ["JOSEPHINE","JACOB","NYOKABI","NAOMI","CHARITY","KEVIN",
                 "MIRIAM","KIGEN","FAITH","JAMES","GEOFFREY","SPENCER",
                 "EVANS","KENYORU"]

if "staff_list" not in st.session_state:
    st.session_state.staff_list = default_staff.copy()

# --- Data initialization ---
if "data" not in st.session_state:
    hospitals = ["Nairobi Hosp", "Kijabe Hosp", "MTRH Eldoret", "Meru Hosp", "Mombasa Hosp", "Kisii Hosp"]
    regions = ["Nairobi/Kijabe", "Eldoret", "Meru", "Mombasa", "Kisii"]
    procedures = ["Arthroplasty", "Fracture Fixation", "Spinal Surgery", "Knee Replacement", "Hip Replacement"]
    surgeons = ["Dr. A", "Dr. B", "Dr. C", "Dr. D"]
    
    data = []
    for _ in range(50):
        data.append({
            "Date": datetime.today() - timedelta(days=random.randint(0, 365)),
            "Hospital": random.choice(hospitals),
            "Region": random.choice(regions),
            "Procedure": random.choice(procedures),
            "Surgeon": random.choice(surgeons),
            "Staff": random.choice(st.session_state.staff_list),
            "Notes": "Auto-generated"
        })
    st.session_state.data = pd.DataFrame(data)

# --- Sidebar ---
menu = ["Dashboard", "Add Procedure", "Monthly Report", "Region Report", "Manage Staff"]
choice = st.sidebar.selectbox("Menu", menu)

# ----------------- Dashboard -----------------
if choice == "Dashboard":
    st.title("🦴 Ortho Tracker Dashboard")
    df = st.session_state.data
    if df.empty:
        st.info("No procedure records yet.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Procedures", len(df))
        col2.metric("Hospitals", df["Hospital"].nunique())
        col3.metric("Regions", df["Region"].nunique())
        col4.metric("Active Staff", df["Staff"].nunique())
        
        st.markdown("---")
        st.subheader("Monthly Procedure Growth")
        monthly = df.groupby(df["Date"].dt.to_period("M")).size()
        st.line_chart(monthly)
        
        st.subheader("Procedures by Region")
        region_counts = df["Region"].value_counts()
        st.bar_chart(region_counts)
        
        st.subheader("Top Staff Participation")
        staff_counts = df["Staff"].value_counts().head(10)
        st.bar_chart(staff_counts)
        
        st.success(random.choice(facts))

# ----------------- Add Procedure -----------------
elif choice == "Add Procedure":
    st.subheader("Add Procedure Record")
    with st.form("form"):
        date = st.date_input("Date")
        hospital = st.text_input("Hospital")
        region = st.text_input("Region")
        procedure = st.text_input("Procedure")
        surgeon = st.text_input("Surgeon")
        staff = st.selectbox("Staff", st.session_state.staff_list)
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Add")
        if submit:
            new_row = {
                "Date": pd.to_datetime(date),
                "Hospital": hospital,
                "Region": region,
                "Procedure": procedure,
                "Surgeon": surgeon,
                "Staff": staff,
                "Notes": notes
            }
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
            st.success("Procedure added!")

# ----------------- Monthly Report -----------------
elif choice == "Monthly Report":
    st.subheader("Monthly Report")
    df = st.session_state.data
    if df.empty:
        st.warning("No data available")
    else:
        report = df.groupby([df["Date"].dt.to_period("M"), "Region"])["Procedure"].count().reset_index()
        report.columns = ["Month", "Region", "Count"]
        st.dataframe(report)

# ----------------- Region Report -----------------
elif choice == "Region Report":
    st.subheader("Region Report")
    df = st.session_state.data
    if df.empty:
        st.warning("No data available")
    else:
        regions = df["Region"].unique()
        selected = st.selectbox("Select Region", regions)
        region_data = df[df["Region"]==selected]
        st.dataframe(region_data)

# ----------------- Manage Staff -----------------
elif choice == "Manage Staff":
    st.subheader("Manage Staff")
    st.write(st.session_state.staff_list)
    new_staff = st.text_input("Add Staff Name")
    if st.button("Add Staff"):
        if new_staff and new_staff not in st.session_state.staff_list:
            st.session_state.staff_list.append(new_staff.strip())
            st.success(f"{new_staff} added!")
        else:
            st.warning("Invalid or duplicate name")
