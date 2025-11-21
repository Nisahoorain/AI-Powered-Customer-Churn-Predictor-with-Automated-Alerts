import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle
import requests
from sklearn.preprocessing import LabelEncoder

# Page configuration
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 1.2rem;
        font-weight: bold;
        background-color: #28a745;
        color: white;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #218838;
    }
    .high-risk {
        background-color: #ffcccc !important;
    }
    .medium-risk {
        background-color: #fff4cc !important;
    }
    .low-risk {
        background-color: #ccffcc !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Load model and preprocessing data
@st.cache_resource
def load_model():
    try:
        model = joblib.load('churn_model.pkl')
        with open('preprocessing.pkl', 'rb') as f:
            preprocessing = pickle.load(f)
        return model, preprocessing
    except FileNotFoundError:
        st.error("⚠️ Model files not found! Please run the training notebook first to generate churn_model.pkl and preprocessing.pkl")
        return None, None

# Function to generate retention recommendations
def get_retention_recommendation(row):
    """Generate personalized retention recommendations based on customer features"""
    recommendations = []
    
    tenure = row.get('tenure', 0)
    contract = str(row.get('Contract', '')).lower()
    monthly_charges = row.get('MonthlyCharges', 0)
    online_security = str(row.get('OnlineSecurity', '')).lower()
    tech_support = str(row.get('TechSupport', '')).lower()
    payment_method = str(row.get('PaymentMethod', '')).lower()
    
    # Low tenure + month-to-month contract
    if tenure < 12 and 'month-to-month' in contract:
        recommendations.append("🎯 Offer 6-month discount contract to increase commitment")
    
    # High monthly charges + no security
    if monthly_charges > 80 and ('no' in online_security or 'no internet' in online_security):
        recommendations.append("🔒 Bundle online security for free to increase value perception")
    
    # No tech support + high charges
    if monthly_charges > 70 and ('no' in tech_support or 'no internet' in tech_support):
        recommendations.append("🛠️ Offer free tech support trial to improve satisfaction")
    
    # Electronic check payment (higher churn risk)
    if 'electronic check' in payment_method:
        recommendations.append("💳 Offer discount for switching to automatic payment")
    
    # Long tenure but high risk
    if tenure > 24 and len(recommendations) == 0:
        recommendations.append("⭐ Loyalty reward program - special offer for long-term customers")
    
    # Default recommendation
    if len(recommendations) == 0:
        recommendations.append("📞 Personal outreach from customer success team")
    
    return " | ".join(recommendations) if recommendations else "📞 Contact customer success team"

# Initialize session state
if 'predictions_made' not in st.session_state:
    st.session_state.predictions_made = False
if 'predictions_df' not in st.session_state:
    st.session_state.predictions_df = None

# Load model
model, preprocessing = load_model()

# Header
st.markdown('<h1 class="main-header">📊 Customer Churn Predictor</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Webhook URL input (supports Zapier, Make.com, n8n, etc.)
    st.subheader("🔗 Webhook Integration")
    st.caption("💡 Free options: Make.com, n8n, or IFTTT")
    zapier_webhook = st.text_input(
        "Webhook URL",
        placeholder="https://hooks.zapier.com/... or https://hook.us1.make.com/...",
        help="Get this URL from Make.com (free), Zapier, n8n, or IFTTT"
    )
    
    # Probability threshold for churn prediction (business trade-off)
    st.subheader("🎯 Prediction Threshold")
    st.caption("Adjust sensitivity: Lower = catch more churners (higher recall), Higher = fewer false positives")
    prediction_threshold = st.slider(
        "Churn Probability Threshold",
        min_value=0.20,
        max_value=0.70,
        value=0.35,
        step=0.05,
        format="%.2f",
        help="Probability threshold for predicting churn. Lower values catch more churners but may have more false positives."
    )
    st.caption(f"Current: {prediction_threshold*100:.0f}% - {'Very Sensitive' if prediction_threshold < 0.3 else 'Balanced' if prediction_threshold < 0.5 else 'Strict'}")
    
    # Risk threshold
    st.subheader("Risk Thresholds")
    high_risk_threshold = st.slider(
        "High Risk Threshold (%)",
        min_value=50,
        max_value=90,
        value=70,
        help="Customers with churn probability above this will be marked as high risk"
    )
    
    medium_risk_threshold = st.slider(
        "Medium Risk Threshold (%)",
        min_value=30,
        max_value=70,
        value=50,
        help="Customers with churn probability above this will be marked as medium risk"
    )
    
    st.markdown("---")
    st.info("💡 **Tip:** Upload a CSV/Excel file with customer data to get churn predictions!")

# Main content
st.header("📁 Upload Customer Data")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=['csv', 'xlsx', 'xls'],
    help="Upload a file with customer information. Required columns may vary, but should include features like tenure, MonthlyCharges, TotalCharges, Contract, etc."
)

if uploaded_file is not None:
    # Read the file
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ File uploaded successfully! ({len(df)} rows)")
        
        # Display uploaded data preview
        with st.expander("📋 Preview Uploaded Data", expanded=False):
            st.dataframe(df.head(10))
            st.caption(f"Total rows: {len(df)}")
        
        # Preprocess and predict
        if model is not None and preprocessing is not None:
            if st.button("🔮 Predict Churn Probability", type="primary"):
                try:
                    # Preprocess the data
                    df_processed = df.copy()
                    
                    # Handle missing values and data types
                    # Convert TotalCharges if it exists
                    if 'TotalCharges' in df_processed.columns:
                        df_processed['TotalCharges'] = pd.to_numeric(df_processed['TotalCharges'], errors='coerce')
                        df_processed['TotalCharges'].fillna(df_processed['TotalCharges'].median(), inplace=True)
                    
                    # Encode categorical variables using saved encoders
                    label_encoders = preprocessing['label_encoders']
                    feature_names = preprocessing['feature_names']
                    
                    # Prepare features - try to match with model's expected features
                    # If customerID exists, drop it
                    if 'customerID' in df_processed.columns:
                        df_processed = df_processed.drop('customerID', axis=1)
                    
                    # Encode categorical columns
                    for col in label_encoders.keys():
                        if col in df_processed.columns:
                            le = label_encoders[col]
                            # Handle unseen categories
                            df_processed[col] = df_processed[col].astype(str)
                            unique_values = set(df_processed[col].unique())
                            known_classes = set(le.classes_)
                            unknown = unique_values - known_classes
                            
                            if unknown:
                                st.warning(f"⚠️ Unknown values in {col}: {unknown}. These will be encoded as 0.")
                                # Map unknown to a default value
                                df_processed[col] = df_processed[col].apply(
                                    lambda x: le.transform([x])[0] if x in known_classes else 0
                                )
                            else:
                                df_processed[col] = le.transform(df_processed[col])
                    
                    # Ensure all required features are present
                    missing_features = set(feature_names) - set(df_processed.columns)
                    if missing_features:
                        st.error(f"❌ Missing required features: {missing_features}")
                        st.info("Please ensure your CSV includes all necessary columns. Refer to the original dataset structure.")
                    else:
                        # Select only the features the model expects
                        X = df_processed[feature_names]
                        
                        # Make predictions using custom threshold
                        predictions_proba = model.predict_proba(X)[:, 1]  # Probability of churn
                        # Use custom threshold instead of default 0.5
                        predictions = (predictions_proba >= prediction_threshold).astype(int)
                        
                        # Create results dataframe
                        results_df = df.copy()
                        results_df['Churn_Probability'] = (predictions_proba * 100).round(2)
                        results_df['Predicted_Churn'] = ['Yes' if p == 1 else 'No' for p in predictions]
                        
                        # Add retention recommendations
                        results_df['Retention_Recommendation'] = results_df.apply(get_retention_recommendation, axis=1)
                        
                        # Add risk level
                        results_df['Risk_Level'] = results_df['Churn_Probability'].apply(
                            lambda x: 'High Risk' if x >= high_risk_threshold 
                            else 'Medium Risk' if x >= medium_risk_threshold 
                            else 'Low Risk'
                        )
                        
                        # Store in session state
                        st.session_state.predictions_made = True
                        st.session_state.predictions_df = results_df
                        
                        st.success(f"✅ Predictions completed for {len(results_df)} customers!")
                        
                except Exception as e:
                    st.error(f"❌ Error during prediction: {str(e)}")
                    st.info("Please ensure your data format matches the expected structure. Check the notebook for required columns.")
        
        # Display predictions if available
        if st.session_state.predictions_made and st.session_state.predictions_df is not None:
            st.markdown("---")
            st.header("📊 Churn Predictions")
            
            results_df = st.session_state.predictions_df
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Customers", len(results_df))
            with col2:
                high_risk_count = len(results_df[results_df['Risk_Level'] == 'High Risk'])
                st.metric("High Risk Customers", high_risk_count, delta=f"{high_risk_count/len(results_df)*100:.1f}%")
            with col3:
                predicted_churn = len(results_df[results_df['Predicted_Churn'] == 'Yes'])
                st.metric("Predicted to Churn", predicted_churn, delta=f"{predicted_churn/len(results_df)*100:.1f}%")
            with col4:
                avg_prob = results_df['Churn_Probability'].mean()
                st.metric("Average Churn Probability", f"{avg_prob:.1f}%")
            
            # Feature Importance Visualization
            if model is not None and hasattr(model, 'feature_importances_'):
                st.markdown("---")
                st.subheader("📈 Feature Importance")
                st.caption("Top features driving churn predictions")
                
                feature_importance_df = pd.DataFrame({
                    'Feature': preprocessing['feature_names'],
                    'Importance': model.feature_importances_
                }).sort_values('Importance', ascending=False).head(10)
                
                st.bar_chart(feature_importance_df.set_index('Feature')['Importance'])
                
                with st.expander("View all feature importances"):
                    st.dataframe(feature_importance_df, use_container_width=True)
            
            # Display results table with styling
            st.markdown("---")
            st.subheader("📋 Detailed Predictions with Retention Recommendations")
            
            # Color code the dataframe
            def highlight_risk(row):
                if row['Risk_Level'] == 'High Risk':
                    return ['background-color: #ffcccc'] * len(row)
                elif row['Risk_Level'] == 'Medium Risk':
                    return ['background-color: #fff4cc'] * len(row)
                else:
                    return ['background-color: #ccffcc'] * len(row)
            
            # Select columns to display
            display_cols = ['Churn_Probability', 'Predicted_Churn', 'Risk_Level']
            # Add original columns if they exist (prioritize common ones)
            original_cols = ['customerID', 'Name', 'Email', 'tenure', 'MonthlyCharges', 'TotalCharges', 'Contract']
            for col in original_cols:
                if col in results_df.columns and col not in display_cols:
                    display_cols.insert(0, col)
            
            # Add any remaining columns
            for col in results_df.columns:
                if col not in display_cols:
                    display_cols.append(col)
            
            styled_df = results_df[display_cols].style.apply(highlight_risk, axis=1)
            st.dataframe(styled_df, use_container_width=True, height=400)
            
            # Download button for results
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Predictions as CSV",
                data=csv,
                file_name="churn_predictions.csv",
                mime="text/csv"
            )
            
            # Webhook integration button
            st.markdown("---")
            st.header("🚨 Send Alerts via Webhook")
            
            if zapier_webhook:
                if st.button("🟢 Send Alerts via Webhook", type="primary", use_container_width=True):
                    try:
                        # Filter high-risk customers
                        high_risk_customers = results_df[results_df['Risk_Level'] == 'High Risk']
                        
                        if len(high_risk_customers) == 0:
                            st.warning("⚠️ No high-risk customers to send alerts for.")
                        else:
                            # Prepare data for Zapier
                            alerts_sent = 0
                            for idx, row in high_risk_customers.iterrows():
                                # Create payload
                                payload = {
                                    'customer_name': str(row.get('Name', row.get('customerID', 'Unknown'))),
                                    'churn_probability': f"{row['Churn_Probability']:.2f}%",
                                    'risk_level': row['Risk_Level'],
                                    'predicted_churn': row['Predicted_Churn'],
                                    'email': str(row.get('Email', 'N/A')),
                                    'tenure': str(row.get('tenure', 'N/A')),
                                    'monthly_charges': str(row.get('MonthlyCharges', 'N/A')),
                                }
                                
                                # Send to webhook (works with Make.com, Zapier, n8n, etc.)
                                response = requests.post(zapier_webhook, json=payload, timeout=10)
                                
                                if response.status_code in [200, 201, 202]:
                                    alerts_sent += 1
                                else:
                                    st.warning(f"⚠️ Failed to send alert for customer {idx}: {response.status_code}")
                            
                            if alerts_sent > 0:
                                st.success(f"✅ Successfully sent {alerts_sent} alert(s) via webhook!")
                                st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error sending alerts: {str(e)}")
                        st.info("Please check your webhook URL and ensure your automation is active.")
            else:
                st.warning("⚠️ Please enter your Webhook URL in the sidebar to enable alerts.")
                st.info("""
                **💡 Free Webhook Options:**
                
                **Option 1: Make.com (Recommended - FREE)**
                1. Go to https://www.make.com and sign up (free plan available)
                2. Create a new scenario
                3. Add "Webhooks" → "Custom webhook"
                4. Copy the webhook URL and paste it here
                5. Add actions (Slack, Gmail, Google Sheets, etc.)
                
                **Option 2: n8n (FREE)**
                1. Go to https://n8n.io and sign up (free cloud plan)
                2. Create a workflow
                3. Add "Webhook" node
                4. Copy the webhook URL
                
                **Option 3: IFTTT (FREE)**
                1. Go to https://ifttt.com
                2. Create applet with "Webhooks" trigger
                3. Get your webhook URL
                """)
    
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        st.info("Please ensure your file is a valid CSV or Excel file.")

else:
    # Show instructions when no file is uploaded
    st.info("👆 Please upload a CSV or Excel file to get started!")
    
    st.markdown("---")
    st.subheader("📖 Instructions")
    st.markdown("""
    1. **Prepare your data**: Ensure your CSV/Excel file contains customer information
    2. **Upload**: Use the file uploader above to select your file
    3. **Predict**: Click the "Predict Churn Probability" button
    4. **Review**: Check the predictions table with color-coded risk levels
    5. **Alert**: Configure webhook (Make.com/Zapier/n8n) in the sidebar and send alerts for high-risk customers
    
    **Required columns** (based on Telco dataset):
    - `tenure`: Number of months the customer has been with the company
    - `MonthlyCharges`: Monthly charges amount
    - `TotalCharges`: Total charges amount
    - `Contract`: Contract type (Month-to-month, One year, Two year)
    - Other service-related columns (PhoneService, InternetService, etc.)
    """)

# Footer
st.markdown("---")
st.caption("💡 Built with Streamlit | Powered by Machine Learning | Integrated with Webhooks (Make.com/Zapier/n8n)")

