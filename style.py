import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            /* ===== Global Clean Light Theme ===== */
            body {
                font-family: 'Segoe UI', sans-serif;
                background-color: #ffffff;
                color: #333333;
                line-height: 1.5;
            }

            /* ===== Sidebar - minimal feel ===== */
            section[data-testid="stSidebar"] {
                background-color: #fbfbfb;
                padding: 1rem 0.8rem;
                border-right: 1px solid #f0f0f0;
            }
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] p {
                color: #444;
                font-size: 14px;
                font-weight: 500;
            }

            /* ===== Main Heading ===== */
            h1 {
                color: #2b5797;
                font-weight: 600;
                margin-bottom: 1rem;
                letter-spacing: -0.5px;
            }
            .main-heading {
                padding-bottom: 0.5rem;
                border-bottom: 1px solid #f0f0f0;
                margin-bottom: 1.5rem;
            }

            /* ===== Search Input - free feel ===== */
            .stTextInput > div > div > input {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #fff;
                padding: 0.5rem 0.75rem;
                font-size: 14px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.02);
                transition: all 0.2s ease-in-out;
                color: #333;
            }
            .stTextInput > div > div > input:focus {
                border-color: #2b5797;
                box-shadow: 0 0 6px rgba(43,87,151,0.15);
                outline: none;
            }
                
            /* ===== File Uploader Label Black ===== */
            .stFileUploader label {
                color: #000 !important;
                font-weight: 600;
                font-size: 14px;
            }
                
            /* ===== Search Placeholder Text Black ===== */
            .stTextInput input::placeholder {
                color: #000 !important;
                opacity: 0.7; /* Thoda light feel ke liye */
                font-weight: 500;
            }

            /* ===== File Uploader ===== */
            .stFileUploader {
                background-color: #fff;
                border-radius: 8px;
                border: 1px dashed #ccc;
                padding: 0.8rem;
                text-align: center;
                box-shadow: 0 1px 2px rgba(0,0,0,0.02);
                transition: all 0.2s ease-in-out;
            }
                
            /* ===== File Uploader Label Black ===== */
            .stFileUploader label {
                color: #000 !important;
                font-weight: 600;
                font-size: 14px;
            }


            /* ===== Tabs ===== */
            div[data-baseweb="tab-list"] button {
                background-color: transparent !important;
                border-radius: 8px !important;
                padding: 0.4rem 1rem !important;
                margin-right: 6px;
                font-weight: 500;
                font-size: 14px;
                color: #555;
                border: none !important;
                transition: background-color 0.2s ease-in-out;
            }
            div[data-baseweb="tab-list"] button:hover {
                background-color: #f5f8ff !important;
            }
            div[data-baseweb="tab-list"] button[aria-selected="true"] {
                background-color: #2b5797 !important;
                color: white !important;
            }

            /* ===== Expanders ===== */
            .streamlit-expanderHeader {
                background-color: #fafafa !important;
                border-radius: 6px;
                font-weight: 600;
                color: #333 !important;
                padding: 0.4rem 0.6rem;
                border: none;
                box-shadow: 0 1px 2px rgba(0,0,0,0.02);
            }
            .streamlit-expanderContent {
                background-color: #fff !important;
                padding: 0.5rem 0.8rem;
                border-left: 3px solid #2b5797;
                border-radius: 0px 6px 6px 0px;
            }

            /* ===== Buttons ===== */
            .stButton>button {
                background-color: #2b5797;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0.45rem 1rem;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                transition: background-color 0.2s ease-in-out, transform 0.1s ease-in-out;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            }
            .stButton>button:hover {
                background-color: #24487a;
                transform: translateY(-1px);
            }

            /* ===== Graph Container ===== */
            .stGraphVizChart {
                border-radius: 10px;
                padding: 0.5rem;
                background-color: #fff;
                box-shadow: 0 2px 8px rgba(0,0,0,0.03);
                margin-top: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)


