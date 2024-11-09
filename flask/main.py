from flask import Flask, request, jsonify
import pickle
import pandas as pd

# Load the saved model pipeline
with open('../model/network_ids_pipeline.pkl', 'rb') as file:
    model_pipeline = pickle.load(file)
# Load the saved LabelEncoder
with open('../model/label_encoder.pkl', 'rb') as le_file:
    label_encoder = pickle.load(le_file)
# Initialize Flask app
app = Flask(__name__)

# Define a basic route to check if API is live
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello, World!"})

# Define the prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Parse JSON request
        data = request.get_json()
        features = data.get("features")
        
        if not features:
            return jsonify({"error": "No features provided"}), 400
        
        # Convert the comma-separated string into a list
        input_values = features.split(',')
        
        # Define the column names in the order expected by the model
        columns = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
            'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
            'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
            'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
            'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
            'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
            'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
            'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
        ]

        # Create a DataFrame with a single row of input values and columns
        input_df = pd.DataFrame([input_values], columns=columns)

        # Predict using the model pipeline
        prediction_encoded = model_pipeline.predict(input_df)
        predicted_label = label_encoder.inverse_transform([prediction_encoded[0]])
        
        # Return the prediction
        return jsonify({"prediction": predicted_label[0]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
