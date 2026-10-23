

import streamlit as st
import json
import hashlib
from pathlib import Path

st.set_page_config(page_title="UniFind AI", page_icon="🎓")

USERS_FILE = Path("users.json")
REPORTS_FILE = Path("reports.json")

# Demo admin account
ADMIN_EMAIL = "admin@unifind.com"
ADMIN_PASSWORD = "Admin@123"

def load_data(file):
    if file.exists():
        try:
            return json.loads(file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}

def save_data(file, data):
    file.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🎓 UniFind AI")
st.subheader("Campus Lost and Found Assistant")

# Logged-in page
if st.session_state.user:
    user = st.session_state.user
    st.success(f"Welcome, {user['email']}!")

    if user["role"] == "admin":
        st.header("🛠️ Admin Dashboard")
        reports = load_data(REPORTS_FILE)
        if isinstance(reports, list) and reports:
            st.write(f"Total reports: {len(reports)}")
            st.dataframe(reports)
        else:
            st.info("No reports available yet.")
    else:
        st.header("📦 Report Lost or Found Item")
        item = st.text_input("Enter item name", key="item_name")
        location = st.text_input("Enter the location", key="item_location")
        item_type = st.selectbox(
    "Select type",
    ["Lost", "Found"],
    key="item_type"
)
        if st.button("Submit Report"):
            if item.strip() and location.strip():
                reports = load_data(REPORTS_FILE)
                if not isinstance(reports, list):
                    reports = []
                reports.append({
                    "item": item.strip(),
                    "location": location.strip(),
                    "type": item_type,
                    "reported_by": user["email"]
                })
                save_data(REPORTS_FILE, reports)
                st.success("Report submitted successfully!")
            else:
                st.warning("Enter item name and location.")

        st.header("View All Reports")
        reports = load_data(REPORTS_FILE)
        if isinstance(reports, list) and reports:
            for i, report in enumerate(reports, 1):
                st.write(f"**Report {i}**")
                st.write("Item:", report["item"])
                st.write("Location:", report["location"])
                st.write("Type:", report["type"])
                st.divider()
        else:
            st.info("No reports yet.")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

else:
    signup_tab, login_tab, admin_tab = st.tabs(
        ["Sign Up", "Login", "Admin Login"]
    )

    with signup_tab:
        st.header("Create Account")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input(
            "Password", type="password", key="signup_password"
        )
        confirm = st.text_input(
            "Confirm Password", type="password", key="signup_confirm"
        )

        if st.button("Sign Up"):
            if not email.strip() or not password:
                st.warning("Enter email and password.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                users = load_data(USERS_FILE)
                if email.strip().lower() == ADMIN_EMAIL:
                    st.error("This email is reserved for admin.")
                elif email.strip().lower() in users:
                    st.error("Account already exists. Please log in.")
                else:
                    users[email.strip().lower()] = {
                        "password": hash_password(password),
                        "role": "user"
                    }
                    save_data(USERS_FILE, users)
                    st.success("Account created! Now open the Login tab.")

    with login_tab:
        st.header("User Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input(
            "Password", type="password", key="login_password"
        )

        if st.button("Login"):
            users = load_data(USERS_FILE)
            account = users.get(email.strip().lower())

            if account and account["password"] == hash_password(password):
                st.session_state.user = {
                    "email": email.strip().lower(),
                    "role": "user"
                }
                st.rerun()
            else:
                st.error("Incorrect email or password.")

    with admin_tab:
        st.header("Admin Login")
        admin_email = st.text_input("Admin Email", key="admin_email")
        admin_password = st.text_input(
            "Admin Password", type="password", key="admin_password"
        )

        if st.button("Admin Login"):
            if (admin_email.strip().lower() == ADMIN_EMAIL
                    and admin_password == ADMIN_PASSWORD):
                st.session_state.user = {
                    "email": ADMIN_EMAIL,
                    "role": "admin"
                }
                st.rerun()
            else:
                st.error("Invalid admin credentials.")

import streamlit as st
import json
from pathlib import Path

st.title("UniFind AI")
st.subheader("Campus Lost and Found")
st.write("Welcome")

REPORTS_FILE = Path("reports.json")

def load_reports():
    if REPORTS_FILE.exists():
        try:
            return json.loads(
                REPORTS_FILE.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError:
            return []
    return []

def save_reports(reports):
    REPORTS_FILE.write_text(
        json.dumps(reports, indent=2),
        encoding="utf-8"
    )

item_name = st.text_input("Enter item name")
location = st.text_input("Where was it lost or found?")

item_type = st.selectbox(
    "Select type",
    ["Lost", "Found"]
)

if st.button("Submit Report"):
    if item_name.strip() and location.strip():
        reports = load_reports()

        reports.append({
            "item": item_name.strip(),
            "location": location.strip(),
            "type": item_type
        })

        save_reports(reports)
        st.success("Report submitted successfully!")
    else:
        st.warning("Please enter item name and location.")

st.divider()
st.header("View All Reports")

reports = load_reports()

if reports:
    for index, report in enumerate(reports, start=1):
        with st.container(border=True):
            st.write(f"Report {index}")
            st.write("Item:", report["item"])
            st.write("Location:", report["location"])
            st.write("Type:", report["type"])
else:
    st.info("No reports available.")

    # UniFind AI Chat Box

st.subheader("💬 UniFind AI Chat Assistant")
st.write("Ask me about lost and found items!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_message = st.chat_input("Type your message here...")

if user_message:
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_message
    })

    reports = load_reports()
    query = user_message.lower()
    matches = []

    if isinstance(reports, list):
        for report in reports:
            if isinstance(report, dict):
                searchable_text = " ".join(
                    str(value) for value in report.values()
                ).lower()

                if any(word in searchable_text for word in query.split()):
                    matches.append(report)

    if matches:
        reply = "I found these possible matching reports:\n\n"
        for report in matches[:5]:
            reply += str(report) + "\n\n"
    else:
        reply = (
            "I couldn't find a matching report yet. "
            "Try describing the item, its colour, or where you lost it."
        )

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()