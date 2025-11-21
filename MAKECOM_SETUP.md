# Make.com (Free) Webhook Setup Guide

## Why Make.com?
- ✅ **FREE plan available** (1,000 operations/month)
- ✅ Easy to use
- ✅ Works with Slack, Gmail, Google Sheets, etc.
- ✅ Perfect for this project

## Step-by-Step Setup

### Step 1: Create Make.com Account
1. Go to **https://www.make.com**
2. Click **"Sign up"** (free)
3. Verify your email

### Step 2: Create a New Scenario
1. Click **"Create a new scenario"** (top right)
2. Name it: **"Customer Churn Alerts"**

### Step 3: Add Webhook Trigger
1. Click the **"+"** button
2. Search for **"Webhooks"**
3. Select **"Webhooks"** → **"Custom webhook"**
4. Click **"Save"**
5. **Copy the webhook URL** (looks like: `https://hook.us1.make.com/xxxxx/xxxxx`)
6. **Paste this URL in your Streamlit app sidebar**

### Step 4: Add Action (Choose One)

#### Option A: Send Slack Message
1. Click **"+"** after the webhook
2. Search for **"Slack"**
3. Select **"Slack"** → **"Create a Message"**
4. Connect your Slack account (if not connected)
5. Configure:
   - **Channel**: Choose your channel (e.g., #customer-alerts)
   - **Text**: 
     ```
     🚨 High-Risk Customer Alert!
     
     Customer: {{1.customer_name}}
     Churn Probability: {{1.churn_probability}}
     Risk Level: {{1.risk_level}}
     Email: {{1.email}}
     Tenure: {{1.tenure}} months
     Monthly Charges: ${{1.monthly_charges}}
     ```
6. Click **"OK"**

#### Option B: Send Gmail
1. Click **"+"** after the webhook
2. Search for **"Gmail"**
3. Select **"Gmail"** → **"Send an Email"**
4. Connect your Gmail account
5. Configure:
   - **To**: Your email
   - **Subject**: `🚨 High-Risk Customer: {{1.customer_name}}`
   - **Content Type**: HTML
   - **Content**:
     ```html
     <h2>Customer Churn Alert!</h2>
     <p><strong>Customer Name:</strong> {{1.customer_name}}</p>
     <p><strong>Churn Probability:</strong> {{1.churn_probability}}</p>
     <p><strong>Risk Level:</strong> {{1.risk_level}}</p>
     <p><strong>Email:</strong> {{1.email}}</p>
     <p><strong>Tenure:</strong> {{1.tenure}} months</p>
     <p><strong>Monthly Charges:</strong> ${{1.monthly_charges}}</p>
     ```
6. Click **"OK"**

#### Option C: Add to Google Sheets
1. Click **"+"** after the webhook
2. Search for **"Google Sheets"**
3. Select **"Google Sheets"** → **"Add a Row"**
4. Connect your Google account
5. Select or create a spreadsheet
6. Map the fields:
   - **Customer Name** → `{{1.customer_name}}`
   - **Churn Probability** → `{{1.churn_probability}}`
   - **Risk Level** → `{{1.risk_level}}`
   - **Email** → `{{1.email}}`
   - **Tenure** → `{{1.tenure}}`
   - **Monthly Charges** → `{{1.monthly_charges}}`
7. Click **"OK"**

### Step 5: Test Your Scenario
1. Click **"Run once"** button (bottom left)
2. Make.com will wait for a webhook call
3. In your Streamlit app:
   - Paste the webhook URL in the sidebar
   - Upload test data
   - Click "Send Alerts via Webhook"
4. Check if the action (Slack/Gmail/Sheets) received the data

### Step 6: Turn On Your Scenario
1. Click the toggle switch at the bottom to **"ON"** (green)
2. Your automation is now active!

## Testing in Streamlit

1. **Run your Streamlit app:**
   ```bash
   streamlit run churn_app.py
   ```

2. **In the sidebar:**
   - Paste your Make.com webhook URL
   - Adjust risk thresholds if needed

3. **Upload test data:**
   - Use `test_customers.csv`
   - Click "Predict Churn Probability"

4. **Send alerts:**
   - Scroll down to "Send Alerts via Webhook"
   - Click the green button
   - You should see: "✅ Successfully sent X alert(s) via webhook!"

5. **Verify:**
   - Check your Slack channel / Gmail / Google Sheets
   - You should see the alert with customer data

## Troubleshooting

**Webhook not receiving data?**
- Make sure the scenario is turned ON (green toggle)
- Check that you copied the full webhook URL
- Verify the webhook is in "Custom webhook" mode (not "Instant")

**Data not showing correctly?**
- In Make.com, click on the webhook module
- Check "Data structure" to see what fields are available
- Use those exact field names (e.g., `{{1.customer_name}}`)

**Action not working?**
- Make sure you connected your account (Slack/Gmail/Sheets)
- Test the action separately first
- Check Make.com's execution history for errors

## Free Plan Limits

- **1,000 operations/month** (plenty for testing and demos)
- Each alert = 1 operation
- If you need more, upgrade to paid plan or use multiple free accounts

## Alternative: n8n Setup

If you prefer n8n:

1. Go to **https://n8n.io**
2. Sign up (free cloud plan)
3. Create workflow
4. Add **"Webhook"** node
5. Copy webhook URL
6. Add action nodes (Slack, Gmail, etc.)
7. Use the same URL in Streamlit

---

**That's it!** Your free webhook integration is ready. 🎉

