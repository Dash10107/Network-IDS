# app.py

import streamlit as st
import pickle
import pandas as pd

# Load the model pipeline
with open('model/network_ids_pipeline.pkl', 'rb') as file:
    model_pipeline = pickle.load(file)

# Load the label encoder
with open('model/label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)

# Define Streamlit app
st.title("Network Intrusion Detection System")

st.write("""
This app predicts whether a network traffic session is **Normal** or **Intrusive** based on input features.
""")

# Collect user input for all features, grouped for easier navigation
with st.form("input_form"):
    st.header("Basic Features")
    duration = st.number_input("Duration", min_value=0, max_value=1_000_000, value=0)
    protocol_type = st.selectbox("Protocol Type", options=["tcp", "udp", "icmp"])
    service = st.selectbox("Service", options=["http", "smtp", "ftp", "dns", "other"])
    flag = st.selectbox("Flag", options=["SF", "S1", "REJ", "RSTR", "RSTO"])

    st.header("Source and Destination Bytes")
    src_bytes = st.number_input("Source Bytes", min_value=0, max_value=1_000_000, value=0)
    dst_bytes = st.number_input("Destination Bytes", min_value=0, max_value=1_000_000, value=0)

    st.header("Login and Access Details")
    land = st.selectbox("Land", options=[0, 1])
    logged_in = st.selectbox("Logged In", options=[0, 1])
    is_host_login = st.selectbox("Is Host Login", options=[0, 1])
    is_guest_login = st.selectbox("Is Guest Login", options=[0, 1])

    st.header("Counts and Rates")
    count = st.number_input("Count", min_value=0, max_value=1_000_000, value=0)
    srv_count = st.number_input("Service Count", min_value=0, max_value=1_000_000, value=0)
    serror_rate = st.number_input("SError Rate", min_value=0.0, max_value=1.0, value=0.0)
    srv_serror_rate = st.number_input("Service SError Rate", min_value=0.0, max_value=1.0, value=0.0)
    rerror_rate = st.number_input("RError Rate", min_value=0.0, max_value=1.0, value=0.0)
    srv_rerror_rate = st.number_input("Service RError Rate", min_value=0.0, max_value=1.0, value=0.0)
    same_srv_rate = st.number_input("Same Service Rate", min_value=0.0, max_value=1.0, value=0.0)
    diff_srv_rate = st.number_input("Different Service Rate", min_value=0.0, max_value=1.0, value=0.0)
    srv_diff_host_rate = st.number_input("Service Different Host Rate", min_value=0.0, max_value=1.0, value=0.0)
    dst_host_count = st.number_input("Destination Host Count", min_value=0, max_value=1_000_000, value=0)
    dst_host_srv_count = st.number_input("Destination Host Service Count", min_value=0, max_value=1_000_000, value=0)
    dst_host_same_srv_rate = st.number_input("Destination Host Same Service Rate", min_value=0.0, max_value=1.0, value=0.0)
    dst_host_diff_srv_rate = st.number_input("Destination Host Different Service Rate", min_value=0.0, max_value=1.0, value=0.0)
    dst_host_same_src_port_rate = st.number_input("Destination Host Same Src Port Rate", min_value=0.0, max_value=1.0, value=0.0)
    dst_host_srv_diff_host_rate = st.number_input("Destination Host Service Different Host Rate", min_value=0.0, max_value=1.0, value=0.0)
    dst_host_serror_rate = st.number_input("Destination Host SError Rate", min_value=0.0, max_value=1.0, value=0.0)
    dst_host_srv_serror_rate = st.number_input("Destination Host Service SError Rate", min_value=0.0, max_value=1.0, value=0.0)
    dst_host_rerror_rate = st.number_input("Destination Host RError Rate", min_value=0.0, max_value=1.0, value=0.0)
    dst_host_srv_rerror_rate = st.number_input("Destination Host Service RError Rate", min_value=0.0, max_value=1.0, value=0.0)

    submit_button = st.form_submit_button(label="Predict")

# When the form is submitted, process input and make a prediction
if submit_button:
    try:
        # Collecting all input into a single dictionary
        features = {
            "duration": duration, "protocol_type": protocol_type, "service": service, "flag": flag,
            "src_bytes": src_bytes, "dst_bytes": dst_bytes, "land": land, "wrong_fragment": 0,
            "urgent": 0, "hot": 0, "num_failed_logins": 0, "logged_in": logged_in, "num_compromised": 0,
            "root_shell": 0, "su_attempted": 0, "num_root": 0, "num_file_creations": 0,
            "num_shells": 0, "num_access_files": 0, "num_outbound_cmds": 0, "is_host_login": is_host_login,
            "is_guest_login": is_guest_login, "count": count, "srv_count": srv_count, "serror_rate": serror_rate,
            "srv_serror_rate": srv_serror_rate, "rerror_rate": rerror_rate, "srv_rerror_rate": srv_rerror_rate,
            "same_srv_rate": same_srv_rate, "diff_srv_rate": diff_srv_rate, "srv_diff_host_rate": srv_diff_host_rate,
            "dst_host_count": dst_host_count, "dst_host_srv_count": dst_host_srv_count,
            "dst_host_same_srv_rate": dst_host_same_srv_rate, "dst_host_diff_srv_rate": dst_host_diff_srv_rate,
            "dst_host_same_src_port_rate": dst_host_same_src_port_rate, "dst_host_srv_diff_host_rate": dst_host_srv_diff_host_rate,
            "dst_host_serror_rate": dst_host_serror_rate, "dst_host_srv_serror_rate": dst_host_srv_serror_rate,
            "dst_host_rerror_rate": dst_host_rerror_rate, "dst_host_srv_rerror_rate": dst_host_srv_rerror_rate
        }

        # Convert input values to DataFrame
        input_df = pd.DataFrame([features])

        # Predict using the model pipeline
        prediction_encoded = model_pipeline.predict(input_df)
        predicted_label = label_encoder.inverse_transform([prediction_encoded[0]])

        # Display the result
        st.success(f"Prediction: {predicted_label[0]}")

    except Exception as e:
        st.error(f"Error: {e}")
