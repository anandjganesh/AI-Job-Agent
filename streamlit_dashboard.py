import sqlite3
import pandas as pd
import streamlit as st

# Page config
st.set_page_config(
    page_title="AI Job Agent",
    layout="wide"
)

st.title("🚀 AI Job Agent")

# Load data
conn = sqlite3.connect("jobs.db")

df = pd.read_sql(
    "SELECT * FROM jobs",
    conn
)

conn.close()

# Check if data exists
if df.empty:
    st.warning("No jobs found in the database.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

min_score = st.sidebar.slider(
    "Minimum Score",
    0,
    100,
    50
)

roles = ["All"] + sorted(
    df["role"].dropna().unique().tolist()
)

selected_role = st.sidebar.selectbox(
    "Role",
    roles
)

# Apply filters
filtered_df = df[
    df["score"] >= min_score
]

if selected_role != "All":
    filtered_df = filtered_df[
        filtered_df["role"] == selected_role
    ]

# Metrics
st.metric(
    "Total Jobs",
    len(filtered_df)
)

st.divider()

# Display jobs
for _, job in filtered_df.iterrows():

    with st.container():

        col1, col2 = st.columns([4, 1])

        with col1:
            st.subheader(job.get("title", "Unknown Title"))

            st.write(
                f"🏢 **Company:** {job.get('company', 'N/A')}"
            )

            st.write(
                f"🎯 **Role:** {job.get('role', 'N/A')}"
            )

            st.write(
                f"📌 **Status:** {job.get('status', 'N/A')}"
            )

            # Show clickable URL if available
            if "url" in df.columns and pd.notna(job["url"]):
                st.markdown(
                    f"🔗 [View Job Posting]({job['url']})"
                )

        with col2:
            st.metric(
                "Match Score",
                f"{int(job.get('score', 0))}%"
            )

        st.divider()

# Optional table view
with st.expander("View Raw Data"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )