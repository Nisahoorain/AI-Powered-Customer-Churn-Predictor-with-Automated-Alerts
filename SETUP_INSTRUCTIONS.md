# Setup Instructions

## Quick Start Guide

### Step 1: Download the Dataset

1. Go to [Kaggle Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
2. Download the dataset (you may need to create a free Kaggle account)
3. Extract `WA_Fn-UseC_-Telco-Customer-Churn.csv` and place it in the project root directory

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Train the Model

1. Open `1_Train_Model.ipynb` in Jupyter Notebook
2. Run all cells sequentially
3. This will generate:
   - `churn_model.pkl` - The trained model
   - `preprocessing.pkl` - Preprocessing encoders and metadata

**Expected Output:**
- Model accuracy should be ≥78% (typically 80-85%)
- Model file saved successfully

### Step 4: Run the Streamlit App Locally

```bash
streamlit run churn_app.py
```

The app will open in your browser at `http://localhost:8501`

### Step 5: Test with Sample Data

1. Use the provided `test_customers.csv` file
2. Upload it through the Streamlit interface
3. Click "Predict Churn Probability"
4. Review the predictions

### Step 6: Set Up Zapier Integration (Optional)

1. Go to [zapier.com](https://zapier.com) and create a free account
2. Create a new Zap:
   - **Trigger**: "Webhooks by Zapier" → "Catch Hook"
   - **Action**: Choose one:
     - Send Slack message
     - Send Gmail
     - Add row to Google Sheets
     - Create task in Trello/Notion
3. Copy the webhook URL from Zapier
4. Paste it in the Streamlit sidebar under "Zapier Webhook URL"
5. Test by uploading data and clicking "Send Alerts via Zapier"

## Deployment to Streamlit Cloud

1. Push your code to GitHub (make sure `churn_model.pkl` and `preprocessing.pkl` are committed)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and branch
6. Set main file to `churn_app.py`
7. Click "Deploy"

**Note:** Make sure your model files are in the repository. You may need to adjust `.gitignore` to allow `.pkl` files.

## Troubleshooting

### Model files not found
- Ensure you've run the training notebook first
- Check that `churn_model.pkl` and `preprocessing.pkl` are in the project root

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify your virtual environment is activated

### Zapier webhook not working
- Verify the webhook URL is correct
- Check that your Zap is turned on in Zapier
- Test the webhook manually using a tool like Postman

### Data format errors
- Ensure your CSV matches the expected column structure
- Check the original dataset format for reference
- Required columns: tenure, MonthlyCharges, TotalCharges, Contract, etc.

## Next Steps

- Customize the risk thresholds in the sidebar
- Add more visualizations to the dashboard
- Integrate with additional Zapier actions
- Deploy to production

