import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ----------------- Initialize -----------------
if "staff_list" not in st.session_state:
    st.session_state.staff_list = [
        "JOSEPHINE","JACOB","NYOKABI","NAOMI","CHARITY","KEVIN",
        "MIRIAM","KIGEN","FAITH","JAMES","GEOFFREY","SPENCER",
        "EVANS","KENYORU"
    ]

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Date", "Hospital", "Region", "Procedure", "Surgeon", "Staff", "Notes"
    ])

# ----------------- Sidebar -----------------
menu = ["Dashboard", "Add Procedure", "Monthly Report", "Region Report", "Forecast", "Manage Staff", "Generate Test Data"]
choice = st.sidebar.radio("📌 Menu", menu)

# ----------------- Dashboard -----------------
def dashboard():
    st.title("🦴 Ortho Tracker Dashboard")

    df = st.session_state.data
    if df.empty:
        st.info("No records yet. Add or generate data from the sidebar.")
        return

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📝 Procedures", len(df))
    col2.metric("🏥 Hospitals", df["Hospital"].nunique())
    col3.metric("🌍 Regions", df["Region"].nunique())
    col4.metric("👩‍⚕️ Staff", df["Staff"].nunique())

    st.markdown("---")

    # Growth over time
    st.subheader("📈 Monthly Growth")
    monthly = df.groupby(df["Date"].dt.to_period("M")).size()
    st.line_chart(monthly)

    # Regional performance
    st.subheader("🌍 Regional Distribution")
    region_counts = df["Region"].value_counts()
    st.bar_chart(region_counts)

    # Staff participation
    st.subheader("👩‍⚕️ Staff Participation")
    staff_counts = df["Staff"].value_counts().head(10)
    st.bar_chart(staff_counts)


# ----------------- Add Procedure -----------------
if choice == "Add Procedure":
    st.subheader("➕ Add Procedure")
    with st.form("form"):
        date = st.date_input("Date")
        hospital = st.text_input("Hospital")
        region = st.text_input("Region")
        procedure = st.text_input("Procedure")
        surgeon = st.text_input("Surgeon")
        staff = st.selectbox("Staff", st.session_state.staff_list)
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Save")

        if submit:
            new = {
                "Date": pd.to_datetime(date),
                "Hospital": hospital,
                "Region": region,
                "Procedure": procedure,
                "Surgeon": surgeon,
                "Staff": staff,
                "Notes": notes
            }
            st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new])], ignore_index=True)
            st.success("✅ Procedure added!")


# ----------------- Monthly Report -----------------
elif choice == "Monthly Report":
    st.subheader("📑 Monthly Report")
    if st.session_state.data.empty:
        st.warning("No data")
    else:
        monthly_report = (
            st.session_state.data.groupby([st.session_state.data["Date"].dt.to_period("M"), "Region"])
            .size()
            .reset_index(name="Procedure Count")
        )
        st.dataframe(monthly_report)


# ----------------- Region Report -----------------
elif choice == "Region Report":
    st.subheader("📍 Region Report")
    df = st.session_state.data
    if df.empty:
        st.warning("No data")
    else:
        region = st.selectbox("Choose region", df["Region"].unique())
        region_df = df[df["Region"] == region]
        st.dataframe(region_df)

        monthly = region_df.groupby(region_df["Date"].dt.to_period("M")).size()
        st.line_chart(monthly)


# ----------------- Forecast -----------------
elif choice == "Forecast":
    st.subheader("🔮 Forecast")
    df = st.session_state.data
    if df.empty:
        st.warning("No data")
    else:
        monthly = df.groupby(df["Date"].dt.to_period("M")).size()
        if len(monthly) >= 2:
            last_val = monthly.iloc[-1]
            future = pd.Series(
                [last_val + random.randint(-2, 5) for _ in range(3)],
                index=pd.date_range(monthly.index[-1].to_timestamp() + pd.offsets.MonthBegin(), periods=3, freq="MS")
            )
            st.line_chart(pd.concat([monthly, future]))
        else:
            st.warning("Not enough history to forecast")


# ----------------- Manage Staff -----------------
elif choice == "Manage Staff":
    st.subheader("👩‍⚕️ Manage Staff")
    st.write("Current staff:", st.session_state.staff_list)
    new_staff = st.text_input("Add new staff")
    if st.button("Add Staff"):
        if new_staff and new_staff not in st.session_state.staff_list:
            st.session_state.staff_list.append(new_staff.strip())
            st.success(f"{new_staff} added!")
        else:
            st.warning("Enter a unique name")


# ----------------- Generate Test Data -----------------
elif choice == "Generate Test Data":
    st.subheader("🧪 Generate Test Data (50 records)")
    if st.button("Generate"):
        hospitals = ["Nairobi Hosp", "Kijabe Hosp", "MTRH Eldoret", "Meru Hosp", "Mombasa Hosp", "Kisii Hosp"]
        regions = ["Nairobi/Kijabe", "Eldoret", "Meru", "Mombasa", "Kisii"]
        procedures = ["Arthroplasty", "Fracture Fixation", "Spinal Surgery", "Knee Replacement", "Hip Replacement"]
        surgeons = ["Dr. A", "Dr. B", "Dr. C", "Dr. D"]

        new_data = []
        for _ in range(50):
            new_data.append({
                "Date": datetime.today() - timedelta(days=random.randint(0, 365)),
                "Hospital": random.choice(hospitals),
                "Region": random.choice(regions),
                "Procedure": random.choice(procedures),
                "Surgeon": random.choice(surgeons),
                "Staff": random.choice(st.session_state.staff_list),
                "Notes": "Test record"
            })

        st.session_state.data = pd.DataFrame(new_data)
        st.success("✅ 50 test records generated!")


# ----------------- Default -----------------
else:
    dashboard()
