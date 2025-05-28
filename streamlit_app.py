import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Document Processing System", page_icon="📄", layout="centered")

# --- THEME ---
st.markdown(
    """
    <style>
    body, .stApp { background: #181818 !important; color: #f5f5f5 !important; }
    .stApp { font-family: 'Segoe UI', Arial, sans-serif; }
    h1, h2, h3, h4, h5, h6 { color: #ff9800 !important; }
    .css-1v0mbdj, .css-1d391kg, .css-1cpxqw2 { background: #232323 !important; border-radius: 12px !important; }
    .stButton>button { background: linear-gradient(90deg, #ff9800 0%, #ff5722 100%) !important; color: #fff !important; border: none !important; border-radius: 6px !important; font-weight: 600 !important; font-size: 18px !important; }
    .stButton>button:hover { background: linear-gradient(90deg, #ff5722 0%, #ff9800 100%) !important; }
    .stTextInput>div>input, .stTextArea>div>textarea, .stFileUploader>div>input { background: #181818 !important; color: #fff !important; border: 1px solid #444 !important; border-radius: 6px !important; }
    .stTabs [data-baseweb="tab"] { color: #ff9800 !important; background: #232323 !important; border-radius: 8px 8px 0 0 !important; }
    .stTabs [aria-selected="true"] { background: #181818 !important; color: #fff !important; border-bottom: 4px solid #ff9800 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Document Processing System")

TABS = ["File Upload", "JSON Data", "Email Content"]
tab1, tab2, tab3 = st.tabs(TABS)

API_URL = os.environ.get("MAS_API_URL", "http://localhost:8000/process")

with tab1:
    st.subheader("Upload Document (PDF, JSON, Email)")
    file = st.file_uploader("Choose a file", type=["pdf", "json", "eml"])
    st.markdown("""
    <span style='color:#ffd180;font-size:0.98em;'>
    <b>Sample files:</b> Try uploading <code>sample_invoice.pdf</code> or <code>sample_email.eml</code> from the <b>data/</b> folder.
    </span>
    """, unsafe_allow_html=True)
    if file and st.button("Process Document", key="file_btn"):
        with st.spinner("Processing..."):
            files = {"file": (file.name, file.getvalue())}
            response = requests.post(API_URL, files=files)
            if response.ok:
                st.success("Processed!")
                st.json(response.json())
            else:
                st.error(f"Error: {response.text}")

with tab2:
    st.subheader("Paste JSON Data")
    json_sample = '''{
  "invoice_number": "INV-2025-0012",
  "date": "2025-05-28",
  "due_date": "2025-06-27",
  "vendor": {"name": "Acme Corp", "email": "billing@acme.com"},
  "client": {"name": "Beta LLC", "email": "accounts@beta.com"},
  "items": [
    {"description": "Consulting", "quantity": 10, "unit_price": 200.0, "amount": 2000.0},
    {"description": "Support", "quantity": 5, "unit_price": 100.0, "amount": 500.0}
  ],
  "total": 2500.0,
  "payment_terms": "Net 30"
}'''
    json_data = st.text_area("Paste your JSON here", value=json_sample, height=250)
    st.markdown("""
    <span style='color:#ffd180;font-size:0.98em;'>
    <b>Example:</b> Paste a real invoice or structured data as JSON.<br>
    <span>See <code>data/sample_invoice.json</code> for a full example.</span>
    </span>
    """, unsafe_allow_html=True)
    if st.button("Process JSON", key="json_btn"):
        with st.spinner("Processing..."):
            response = requests.post(API_URL, data={"json_data": json_data})
            if response.ok:
                st.success("Processed!")
                st.json(response.json())
            else:
                st.error(f"Error: {response.text}")

with tab3:
    st.subheader("Paste Email Content")
    email_sample = '''From: jane.doe@company.com
To: support@service.com
Subject: Request for Quotation - Cloud Migration
Date: Wed, 28 May 2025 10:15:00 +0000

Hello,

We are interested in migrating our infrastructure to the cloud and would like a detailed quotation for the following services:
- Cloud architecture design
- Migration planning
- Ongoing support

Please include estimated timelines and pricing.

Best regards,
Jane Doe
IT Manager
Company Inc.'''
    email_data = st.text_area("Paste your email (headers + body)", value=email_sample, height=250)
    st.markdown("""
    <span style='color:#ffd180;font-size:0.98em;'>
    <b>Example:</b> Paste a real email (headers + body).<br>
    <span>See <code>data/sample_email.eml</code> for a full example.</span>
    </span>
    """, unsafe_allow_html=True)
    if st.button("Process Email", key="email_btn"):
        with st.spinner("Processing..."):
            response = requests.post(API_URL, data={"email_content": email_data})
            if response.ok:
                st.success("Processed!")
                st.json(response.json())
            else:
                st.error(f"Error: {response.text}")
