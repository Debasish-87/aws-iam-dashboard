import streamlit as st
import json
from pathlib import Path
from graphviz import Digraph
from style import apply_custom_css  # Custom CSS

# --------------------------
# Page Config
# --------------------------
st.set_page_config(
    page_title="AWS IAM Dashboard",
    layout="wide",
    page_icon="🔐"
)

# Apply custom styles
apply_custom_css()

# --------------------------
# Session State Init
# --------------------------
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# --------------------------
# Page Heading
# --------------------------
st.markdown("<h1 style='text-align:center; color:#2b5797;'>AWS IAM Graphical View</h1>", unsafe_allow_html=True)

# --------------------------
# Search + File Upload + Refresh Row
# --------------------------
# Swap col2 and col3 here
col1, col2, col3 = st.columns([2, 0.5, 1])

with col2:
    st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
    if st.button("🔄 Refresh"):
        st.session_state.search_query = ""  # Clear search text
        st.rerun()  # Updated here, use st.rerun instead of experimental_rerun
    st.markdown("</div>", unsafe_allow_html=True)

with col1:
    search_query = st.text_input(
        "🔍 Search IAM User",
        placeholder="Type a username...",
        key="search_query"
    )

with col3:
    uploaded_file = st.file_uploader("📂 Upload AWS IAM / Org JSON", type=["json"])

# --------------------------
# Load Data
# --------------------------
def load_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ Error loading JSON: {e}")
        return {}

if uploaded_file is None:
    st.caption("📄 No file uploaded — using sample file.")
    sample_path = Path("data/sample_iam.json")
    if sample_path.exists():
        data = load_json(sample_path)
    else:
        st.error("❌ Sample file not found.")
        st.stop()
else:
    try:
        data = json.load(uploaded_file)
        st.success("✅ File uploaded successfully!")
    except Exception as e:
        st.error(f"❌ Failed to parse uploaded JSON: {e}")
        st.stop()

# --------------------------
# Filter Data
# --------------------------
def filter_data_by_user(data, query):
    if not query:
        return data
    filtered_users = [
        u for u in data.get("users", [])
        if query.lower() in u["name"].lower()
    ]
    return {**data, "users": filtered_users}

data = filter_data_by_user(data, st.session_state.search_query)

# --------------------------
# IAM Graph
# --------------------------
def build_iam_graph(data):
    if not data.get("users"):
        return None
    dot = Digraph(comment="IAM Structure", format="svg")
    dot.attr(rankdir="LR", fontsize="10", fontname="Helvetica", nodesep="0.3", ranksep="0.4")
    colors = {
        "user": "#FDE68A",
        "role": "#93C5FD",
        "policy": "#86EFAC",
        "service": "#E5E7EB",
        "permission": "#FCA5A5"
    }
    created_nodes = set()
    for user in data.get("users", []):
        if user["name"] not in created_nodes:
            dot.node(user["name"], shape="ellipse", style="filled", fillcolor=colors["user"])
            created_nodes.add(user["name"])
        for role in user.get("roles", []):
            if role["name"] not in created_nodes:
                dot.node(role["name"], shape="box", style="filled", fillcolor=colors["role"])
                created_nodes.add(role["name"])
            dot.edge(user["name"], role["name"], label="assumes", fontsize="8")
            for policy in role.get("policies", []):
                if policy["name"] not in created_nodes:
                    dot.node(policy["name"], shape="hexagon", style="filled", fillcolor=colors["policy"])
                    created_nodes.add(policy["name"])
                dot.edge(role["name"], policy["name"], label="attached", fontsize="8")
                for service, perms in policy.get("services", {}).items():
                    service_node = f"{policy['name']}::{service}"
                    if service_node not in created_nodes:
                        dot.node(service_node, service, shape="component", style="filled", fillcolor=colors["service"])
                        created_nodes.add(service_node)
                    dot.edge(policy["name"], service_node)
                    for perm in perms:
                        perm_node = f"{service_node}::{perm}"
                        if perm_node not in created_nodes:
                            dot.node(perm_node, perm, shape="note", style="filled", fillcolor=colors["permission"])
                            created_nodes.add(perm_node)
                        dot.edge(service_node, perm_node)
    return dot

# --------------------------
# Organization Graph
# --------------------------
def build_org_graph(data):
    if "organization" not in data:
        return None
    dot = Digraph(comment="AWS Organization", format="svg")
    dot.attr(rankdir="TB", fontsize="10", fontname="Helvetica", nodesep="0.3", ranksep="0.4")
    dot.attr("node", shape="folder", style="filled", color="#F3F4F6")

    def add_unit(parent, unit):
        dot.node(unit["name"], shape="folder", color="#E5E7EB")
        if parent:
            dot.edge(parent, unit["name"])
        for account in unit.get("accounts", []):
            dot.node(account, shape="component", color="white")
            dot.edge(unit["name"], account)
        for child in unit.get("organizational_units", []):
            add_unit(unit["name"], child)

    add_unit(None, data["organization"])
    return dot

# --------------------------
# List View
# --------------------------
def render_iam_list(data):
    if not data.get("users"):
        st.info("No IAM users found.")
        return
    for user in data.get("users", []):
        with st.expander(f"👤 {user['name']}"):
            for role in user.get("roles", []):
                with st.expander(f"📦 Role: {role['name']}"):
                    for policy in role.get("policies", []):
                        with st.expander(f"📜 Policy: {policy['name']}"):
                            for service, perms in policy.get("services", {}).items():
                                with st.expander(f"🔧 Service: {service}"):
                                    for perm in perms:
                                        st.write(f"• `{perm}`")

# --------------------------
# Tabs
# --------------------------
tab1, tab2, tab3 = st.tabs(["👤 IAM Structure", "🏢 Organization Structure", "📋 List View"])

with tab1:
    st.subheader("IAM Users, Roles, Policies, Services, and Permissions")
    iam_graph = build_iam_graph(data)
    if iam_graph:
        st.graphviz_chart(iam_graph, use_container_width=True)
    else:
        st.info("No IAM data to display.")

with tab2:
    st.subheader("AWS Organization")
    org_graph = build_org_graph(data)
    if org_graph:
        st.graphviz_chart(org_graph, use_container_width=True)
    else:
        st.info("ℹ No organization data found in JSON.")

with tab3:
    st.subheader("Structured IAM List View")
    render_iam_list(data)
