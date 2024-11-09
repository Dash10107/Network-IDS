import streamlit as st
import pickle
import pandas as pd

# Load the model pipeline and label encoder
with open('../model/network_ids_pipeline.pkl', 'rb') as file:
    model_pipeline = pickle.load(file)

with open('../model/label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)

# Define the Streamlit app
st.set_page_config(page_title="Network Intrusion Detection", layout="wide")
st.title("Network Intrusion Detection System")

st.markdown("""
This application predicts network traffic sessions as **Normal** or **Intrusive** based on various features.
You can either input custom values or test using sample packets.
""")

# Sidebar for sample packets
st.sidebar.header("Sample Packet Testing")
# Expanded sample packets with all columns
sample_packets = {
    "Normal Packet": {
        "duration": 0, "protocol_type": "udp", "service": "private", "flag": "SF", "src_bytes": 45, "dst_bytes": 44,
        "land": 0, "wrong_fragment": 0, "urgent": 0, "hot": 0, "num_failed_logins": 0, "logged_in": 0,
        "num_compromised": 0, "root_shell": 0, "su_attempted": 0, "num_root": 0, "num_file_creations": 0,
        "num_shells": 0, "num_access_files": 0, "num_outbound_cmds": 0, "is_host_login": 0, "is_guest_login": 0,
        "count": 505, "srv_count": 505, "serror_rate": 0.00, "srv_serror_rate": 0.00, "rerror_rate": 0.00,
        "srv_rerror_rate": 0.00, "same_srv_rate": 1.00, "diff_srv_rate": 0.00, "srv_diff_host_rate": 0.00,
        "dst_host_count": 255, "dst_host_srv_count": 255, "dst_host_same_srv_rate": 1.00, "dst_host_diff_srv_rate": 0.00,
        "dst_host_same_src_port_rate": 1.00, "dst_host_srv_diff_host_rate": 0.00, "dst_host_serror_rate": 0.00,
        "dst_host_srv_serror_rate": 0.00, "dst_host_rerror_rate": 0.00, "dst_host_srv_rerror_rate": 0.00
    },
    "Intrusive Packet": {
        "duration": 0, "protocol_type": "tcp", "service": "ldap", "flag": "REJ", "src_bytes": 0, "dst_bytes": 0,
        "land": 0, "wrong_fragment": 0, "urgent": 0, "hot": 0, "num_failed_logins": 0, "logged_in": 0,
        "num_compromised": 0, "root_shell": 0, "su_attempted": 0, "num_root": 0, "num_file_creations": 0,
        "num_shells": 0, "num_access_files": 0, "num_outbound_cmds": 0, "is_host_login": 0, "is_guest_login": 0,
        "count": 118, "srv_count": 19, "serror_rate": 0.00, "srv_serror_rate": 0.00, "rerror_rate": 1.00,
        "srv_rerror_rate": 1.00, "same_srv_rate": 0.16, "diff_srv_rate": 0.05, "srv_diff_host_rate": 0.00,
        "dst_host_count": 255, "dst_host_srv_count": 19, "dst_host_same_srv_rate": 0.07, "dst_host_diff_srv_rate": 0.05,
        "dst_host_same_src_port_rate": 0.00, "dst_host_srv_diff_host_rate": 0.00, "dst_host_serror_rate": 0.00,
        "dst_host_srv_serror_rate": 0.00, "dst_host_rerror_rate": 1.00, "dst_host_srv_rerror_rate": 1.00
    }
}


sample_choice = st.sidebar.selectbox("Choose a sample packet:", options=list(sample_packets.keys()))

if st.sidebar.button("Predict Sample Packet"):
    # Convert selected packet to DataFrame
    input_df = pd.DataFrame([sample_packets[sample_choice]])
    prediction_encoded = model_pipeline.predict(input_df)
    predicted_label = label_encoder.inverse_transform([prediction_encoded[0]])
    if predicted_label == "normal":
        st.sidebar.success(f"Prediction for {sample_choice}: {predicted_label[0]}")
    else:
        st.sidebar.error(f"Prediction for {sample_choice}: {predicted_label[0]}")    


# Custom input form
st.header("Custom Packet Input")
st.write("Enter the details for a custom packet below or use the **Sample Packet Testing** in the sidebar.")

# Modal simulation with conditional display
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = False

if st.button("Open Input Modal"):
    st.session_state.show_modal = not st.session_state.show_modal

if st.session_state.show_modal:
    with st.expander("Custom Packet Input", expanded=True):
        duration = st.number_input("Duration", min_value=0, max_value=1_000_000, value=0)
        protocol_type = st.selectbox("Protocol Type", options=["tcp", "udp", "icmp"])
        service = st.selectbox("Service", options=["http", "smtp", "ftp","private", "dns", "other"])
        flag = st.selectbox("Flag", options=["SF", "S1", "REJ", "RSTR", "RSTO"])
        src_bytes = st.number_input("Source Bytes", min_value=0, max_value=1_000_000, value=0)
        dst_bytes = st.number_input("Destination Bytes", min_value=0, max_value=1_000_000, value=0)

        # Collect remaining fields and predict
        if st.button("Predict Custom Input"):
            features = {
                "duration": duration, "protocol_type": protocol_type, "service": service, "flag": flag,
                "src_bytes": src_bytes, "dst_bytes": dst_bytes, "land": 0, "wrong_fragment": 0,
                "urgent": 0, "hot": 0, "num_failed_logins": 0, "logged_in": 0, "num_compromised": 0,
                "root_shell": 0, "su_attempted": 0, "num_root": 0, "num_file_creations": 0,
                "num_shells": 0, "num_access_files": 0, "num_outbound_cmds": 0, "is_host_login": 0,
                "is_guest_login": 0, "count": 0, "srv_count": 0, "serror_rate": 0.0,
                "srv_serror_rate": 0.0, "rerror_rate": 0.0, "srv_rerror_rate": 0.0,
                "same_srv_rate": 0.0, "diff_srv_rate": 0.0, "srv_diff_host_rate": 0.0,
                "dst_host_count": 0, "dst_host_srv_count": 0, "dst_host_same_srv_rate": 0.0,
                "dst_host_diff_srv_rate": 0.0, "dst_host_same_src_port_rate": 0.0,
                "dst_host_srv_diff_host_rate": 0.0, "dst_host_serror_rate": 0.0,
                "dst_host_srv_serror_rate": 0.0, "dst_host_rerror_rate": 0.0,
                "dst_host_srv_rerror_rate": 0.0
            }

            # Convert to DataFrame and predict
            input_df = pd.DataFrame([features])
            prediction_encoded = model_pipeline.predict(input_df)
            predicted_label = label_encoder.inverse_transform([prediction_encoded[0]])
            if predicted_label == "normal":
                st.success(f"Prediction for Custom Input: {predicted_label[0]}")
            else:
                st.error(f"Prediction for Custom Input: {predicted_label[0]}")
