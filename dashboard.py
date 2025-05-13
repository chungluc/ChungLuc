import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Load the cleaned project data
df = pd.read_excel("Project_List.xlsx", skiprows=2)
df.columns = ["Code", "Location", "Intervention", "Sector", "Proposer",
              "Cost <4M", "Cost <2M", "Cost <1M", "Cost <0.5M",
              "In Scope", "Rationale", "Comment"]
df = df.dropna(subset=["Code"])  # Drop empty rows

# Sidebar filters
st.sidebar.header("Filter Projects")

sector_filter = st.sidebar.multiselect("Select Sector", options=df["Sector"].dropna().unique())
location_filter = st.sidebar.multiselect("Select Location", options=df["Location"].dropna().unique())
proposer_filter = st.sidebar.multiselect("Select Proposer", options=df["Proposer"].dropna().unique())
scope_filter = st.sidebar.selectbox("In Scope?", options=["All", "Y", "N"])

cost_4m_filter = st.sidebar.selectbox("Cost < BZ$4M?", options=["All", "Y", "N"])
cost_2m_filter = st.sidebar.selectbox("Cost < BZ$2M?", options=["All", "Y", "N"])
cost_1m_filter = st.sidebar.selectbox("Cost < BZ$1M?", options=["All", "Y", "N"])
cost_0_5m_filter = st.sidebar.selectbox("Cost < BZ$0.5M?", options=["All", "Y", "N"])

# Filtering logic
filtered_df = df.copy()
if sector_filter:
    filtered_df = filtered_df[filtered_df["Sector"].isin(sector_filter)]
if location_filter:
    filtered_df = filtered_df[filtered_df["Location"].isin(location_filter)]
if proposer_filter:
    filtered_df = filtered_df[filtered_df["Proposer"].isin(proposer_filter)]
if scope_filter in ["Y", "N"]:
    filtered_df = filtered_df[filtered_df["In Scope"].str.strip() == scope_filter]
if cost_4m_filter in ["Y", "N"]:
    filtered_df = filtered_df[filtered_df["Cost <4M"].astype(str).str.strip() == cost_4m_filter]
if cost_2m_filter in ["Y", "N"]:
    filtered_df = filtered_df[filtered_df["Cost <2M"].astype(str).str.strip() == cost_2m_filter]
if cost_1m_filter in ["Y", "N"]:
    filtered_df = filtered_df[filtered_df["Cost <1M"].astype(str).str.strip() == cost_1m_filter]
if cost_0_5m_filter in ["Y", "N"]:
    filtered_df = filtered_df[filtered_df["Cost <0.5M"].astype(str).str.strip() == cost_0_5m_filter]

# Display
st.title("Infrastructure Projects Dashboard")
st.markdown("Use the sidebar to filter the projects.")
st.dataframe(filtered_df.reset_index(drop=True))

# Summary: In Scope vs Out of Scope
st.markdown("### Summary: In-Scope vs Out-of-Scope Projects")
summary_counts = filtered_df["In Scope"].str.strip().value_counts()
summary_percent = (summary_counts / summary_counts.sum() * 100).round(2)
summary_df = pd.DataFrame({"Count": summary_counts, "Percentage": summary_percent})
summary_df.index = summary_df.index.map({"Y": "In Scope", "N": "Out of Scope"})
st.table(summary_df)

# Charts
st.markdown("### Project Distribution by Sector")
sector_counts = filtered_df["Sector"].value_counts()
fig1, ax1 = plt.subplots()
sector_counts.plot(kind='bar', ax=ax1)
ax1.set_ylabel("Number of Projects")
ax1.set_xlabel("Sector")
st.pyplot(fig1)

st.markdown("### Project Distribution by Location")
location_counts = filtered_df["Location"].value_counts().head(10)
fig2, ax2 = plt.subplots()
location_counts.plot(kind='bar', ax=ax2)
ax2.set_ylabel("Number of Projects")
ax2.set_xlabel("Location")
st.pyplot(fig2)

# Cost Distribution Chart for < BZ$0.5M
st.markdown("### Distribution of Projects Costing Less Than BZ$0.5M")
cost_0_5_df = df[df["Cost <0.5M"].astype(str).str.strip() == "Y"]
cost_0_5_sector = cost_0_5_df["Sector"].value_counts()
fig3, ax3 = plt.subplots()
cost_0_5_sector.plot(kind='bar', ax=ax3)
ax3.set_title("Projects < BZ$0.5M by Sector")
ax3.set_ylabel("Number of Projects")
ax3.set_xlabel("Sector")
st.pyplot(fig3)

# Export option
st.markdown("### Export Filtered Data")
output = io.BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    filtered_df.to_excel(writer, index=False, sheet_name='Filtered Projects')
data = output.getvalue()

st.download_button(
    label="Download Excel File",
    data=data,
    file_name="filtered_projects.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
) 
