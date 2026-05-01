import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="AI Support Triage",
    layout="wide",
    initial_sidebar_state="expanded"
)


df = pd.read_csv("output.csv")

st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
h1, h2, h3, h4 {
    color: #e2e8f0;
}
.stDataFrame {
    border-radius: 10px;
}
.metric-box {
    padding: 15px;
    border-radius: 12px;
    background: linear-gradient(135deg, #1e293b, #334155);
    color: white;
}
</style>
""", unsafe_allow_html=True)


st.title("🧠 AI Support Triage System")
st.caption("Smart classification • Risk detection • Safe responses")


st.sidebar.header("⚙️ Controls")

status_filter = st.sidebar.selectbox(
    "Filter by Status",
    ["All"] + list(df["status"].unique())
)

type_filter = st.sidebar.selectbox(
    "Filter by Request Type",
    ["All"] + list(df["request_type"].unique())
)

search = st.sidebar.text_input("🔍 Search issue")


filtered_df = df.copy()

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]

if type_filter != "All":
    filtered_df = filtered_df[filtered_df["request_type"] == type_filter]

if search:
    filtered_df = filtered_df[
    filtered_df.apply(
        lambda row: search.lower() in str(row.get("issue", "")).lower()
        or search.lower() in str(row["response"]).lower()
        or search.lower() in str(row["product_area"]).lower(),
        axis=1
    )
]


col1, col2, col3 = st.columns(3)

col1.metric("📄 Total Tickets", len(df))
col2.metric("🚨 Escalated", len(df[df["status"] == "escalated"]))
col3.metric("✅ Replied", len(df[df["status"] == "replied"]))


st.subheader("📋 Triage Results")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)


st.subheader("🔍 Inspect Ticket")

if len(filtered_df) > 0:
    index = st.number_input(
        "Select row index",
        min_value=0,
        max_value=len(filtered_df)-1,
        step=1
    )

    row = filtered_df.iloc[index]

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### 🧾 Response")
        st.write(row["response"])

    with colB:
        st.markdown("### 🧠 Justification")
        st.write(row["justification"])

    st.markdown("### 🏷️ Metadata")
    st.json({
        "status": row["status"],
        "product_area": row["product_area"],
        "request_type": row["request_type"]
    })

else:
    st.warning("No results match your filters.")


st.markdown("---")
st.caption("AI Decision System • Safe Triage")