# n8n Workflow - AI Sentence Validation

## 🎯 Overview

This workflow uses Google Gemini AI to validate English sentences and provide detailed feedback.

## 📋 Setup Instructions

### Step 1: Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. Copy your API key (starts with `AIzaSy...`)

### Step 2: Configure Environment

1. Open `worddee-ai/.env` file
2. Add your Gemini API key:
   ```bash
   GEMINI_API_KEY=AIzaSyD_your_actual_key_here
   ```
3. Save the file

### Step 3: Access n8n Interface

1. Make sure Docker is running:
   ```bash
   cd /path/to/worddee-ai
   docker-compose up -d
   ```

2. Open n8n in browser:
   ```
   http://localhost:5678
   ```

3. Login with credentials from `.env`:
   - **Username**: `admin`
   - **Password**: `admin_password_456!`

### Step 4: Import Workflow

1. In n8n interface, click **"Workflows"** in left sidebar
2. Click **"Add Workflow"** (+ button)
3. Click **"⋮"** menu (top right) → **"Import from File"**
4. Select `n8n/workflows/validate-sentence.json`
5. Click **"Import"**

### Step 5: Configure Gemini Credentials

1. Open the imported workflow
2. Click on **"Google Gemini Chat Model"** node
3. In the **Credential** dropdown:
   - If no credential exists:
     - Click **"Create New"**
     - Name: `Google Gemini API`
     - API Key: Paste your Gemini API key
     - Click **"Save"**
   - If credential exists:
     - Select existing credential
     - Verify API key is correct

### Step 6: Activate Workflow

1. Click **"Inactive"** toggle (top right)
2. It should turn to **"Active"** (green)
3. Workflow is now ready to receive requests!

## 🧪 Testing the Workflow

### Test via n8n Interface

1. In the workflow editor, click **"Webhook"** node
2. Click **"Listen for Test Event"**
3. In another terminal, send a test request:
   ```bash
   curl -X POST http://localhost:5678/webhook/validate-sentence \
     -H "Content-Type: application/json" \
     -d '{
       "word": "apple",
       "sentence": "I eat an apple every day."
     }'
   ```

4. Check the response:
   ```json
   {
     "score": 9.0,
     "cefr_level": "A2",
     "feedback": "Excellent! Your sentence correctly uses 'apple' with proper grammar.",
     "corrected_sentence": "I eat an apple every day."
   }
   ```

### Test via Worddee.ai App

1. Open frontend: `http://localhost:3000`
2. Click **"Get Random Word"**
3. Type a practice sentence
4. Click **"Submit"**
5. You should see real AI feedback instead of mock data!

## 📊 Workflow Nodes Explained

### 1. Webhook (Trigger)
- **Type**: POST endpoint
- **URL**: `/webhook/validate-sentence`
- **Input**: `{ "word": "...", "sentence": "..." }`
- **Purpose**: Receives sentence validation requests from backend

### 2. Google Gemini Chat Model
- **Model**: `gemini-1.5-flash`
- **Temperature**: 0.3 (focused, consistent responses)
- **System Prompt**: Acts as English teacher evaluating sentences
- **Purpose**: Validates sentence using AI

### 3. Format Response (Code Node)
- **Language**: JavaScript
- **Purpose**: 
  - Parse JSON from AI response
  - Validate score (0-10 range)
  - Ensure all required fields exist
  - Handle errors gracefully

### 4. Respond to Webhook
- **Type**: JSON response
- **Purpose**: Send formatted result back to backend

## 🔧 Troubleshooting

### Workflow Not Receiving Requests

**Problem**: Backend shows "n8n validation failed, using mock"

**Solutions**:
1. Check workflow is **Active** (green toggle)
2. Verify webhook path: `/webhook/validate-sentence`
3. Check n8n container is running:
   ```bash
   docker ps | grep n8n
   ```
4. Test webhook directly:
   ```bash
   curl -X POST http://localhost:5678/webhook/validate-sentence \
     -H "Content-Type: application/json" \
     -d '{"word":"test","sentence":"This is a test."}'
   ```

### Gemini API Errors

**Problem**: `401 Unauthorized` or `Invalid API Key`

**Solutions**:
1. Verify API key in n8n credentials
2. Check API key is active at [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Ensure no extra spaces in API key
4. Try regenerating API key

**Problem**: `429 Too Many Requests`

**Solutions**:
1. You've exceeded free tier quota
2. Wait a few minutes and try again
3. Consider upgrading to paid plan

### Workflow Execution Errors

**Problem**: Workflow fails at Format Response node

**Solutions**:
1. Check AI response format in execution logs
2. Verify JSON parsing logic in Code node
3. Test with simple sentences first

## 📝 Customization

### Adjust Scoring Strictness

Edit the system prompt in **Google Gemini Chat Model** node:

```
For stricter grading:
"Be strict with grammar errors. Deduct 2 points for each mistake."

For more lenient grading:
"Focus on communication effectiveness over perfect grammar."
```

### Change CEFR Level Criteria

```
"Assign CEFR levels based on:
- A1/A2: Simple sentences, basic vocabulary
- B1/B2: Complex sentences, varied vocabulary
- C1/C2: Advanced structures, idiomatic expressions"
```

### Add More Feedback Details

```
Respond with this JSON format:
{
  "score": 0-10,
  "cefr_level": "A1-C2",
  "feedback": "detailed explanation",
  "corrected_sentence": "improved version",
  "grammar_errors": ["list of specific errors"],
  "vocabulary_usage": "assessment of word usage",
  "suggestions": ["improvement tips"]
}
```

## 🔗 Integration with Backend

The backend (`backend/services/ai_service.py`) automatically:

1. Sends validation requests to n8n webhook
2. Receives AI response
3. Falls back to mock if n8n unavailable
4. Saves results to database

No code changes needed once workflow is active!

## 📚 Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Worddee.ai Backend Code](../backend/services/ai_service.py)
- [Webhook Testing Tool](https://webhook.site/)

## ✅ Verification Checklist

- [ ] Gemini API key obtained
- [ ] API key added to `.env`
- [ ] n8n accessible at `http://localhost:5678`
- [ ] Workflow imported successfully
- [ ] Gemini credentials configured
- [ ] Workflow activated (green toggle)
- [ ] Test request successful
- [ ] Frontend shows real AI feedback

---

🎉 **Congratulations!** Your AI sentence validation is now fully functional!
