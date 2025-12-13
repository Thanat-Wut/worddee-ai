# n8n Workflow Setup Guide - Complete Instructions

## 🎯 Overview

This guide will help you set up the n8n workflow for AI-powered sentence validation using Google Gemini.

## 📋 Prerequisites

1. ✅ Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. ✅ n8n running on http://localhost:5678
3. ✅ Backend running on http://localhost:8000

## 🚀 Setup Steps

### Step 1: Access n8n

```bash
open http://localhost:5678


Username: admin
Password: admin_password_456!
```

### Step 2: Import Workflow

1. Click **"Workflows"** (left sidebar)
2. Click **"Add workflow"** → **"Import from file"**
3. Select: `n8n/workflows/validate-sentence-v2.json`
4. Click **"Import"**

### Step 3: Configure AI Agent Node

**Important: This is the most critical step!**

1. Click on the **"AI Agent"** node (second node)
2. In the right panel, find **"Chat Model"** section
3. Click **"Add Chat Model"**
4. Select **"Google Gemini Chat Model"**

**Configure Gemini:**

5. **Model:** Select `gemini-1.5-flash`
6. **Credential:** Click "Create New Credential"
   - Paste your Gemini API Key
   - Click "Save"
7. **System Message:** Paste this prompt:

```
You are an expert English teacher evaluating student sentences.

Analyze the sentence and return a JSON object with these exact fields:
- score: number 0-10 (0=terrible, 10=perfect)
- cefr_level: string (A1, A2, B1, B2, C1, or C2) - single level only
- is_correct: boolean (true if sentence is grammatically correct)
- feedback: string (constructive feedback for the student)
- corrected_sentence: string (corrected version or original if perfect)

Scoring criteria:
0-3: Major grammar errors, word misused completely
4-5: Multiple errors, word used incorrectly
6-7: Minor errors, word used acceptably
8-9: Good sentence, small improvements possible
10: Perfect grammar and word usage

CEFR levels:
A1: Very basic sentences
A2: Simple sentences with common words
B1: Everyday situations, correct basic grammar
B2: Complex ideas, good control of grammar
C1: Sophisticated language, rare errors
C2: Native-like proficiency

IMPORTANT: Return ONLY valid JSON, no other text.
```

8. **Options:**
   - Temperature: `0.3` (for consistency)
   - Max Tokens: `500`

9. **Prompt:** Set to:
```
Word to practice: {{ $json.body.word }}
Definition: {{ $json.body.definition }}
Student's sentence: {{ $json.body.sentence }}

Analyze this sentence and return JSON.
```

10. Click **"Back to canvas"**

### Step 4: Save & Activate

1. Click **"Save"** (top right)
2. Toggle **"Inactive"** → **"Active"** (should turn green)
3. Verify you see: **"Workflow activated successfully"**

### Step 5: Test Webhook

```bash

curl -X POST http://localhost:5678/webhook/validate-sentence \
  -H "Content-Type: application/json" \
  -d '{
    "word": "practice",
    "definition": "repeated exercise in learning",
    "sentence": "I practice English every day to improve my skills."
  }'


{
  "score": 8,
  "cefr_level": "B2",
  "is_correct": true,
  "feedback": "Excellent sentence! You've used 'practice' correctly...",
  "corrected_sentence": "I practice English every day to improve my skills.",
  "original_word": "practice",
  "original_sentence": "I practice English every day to improve my skills."
}
```

## 🐛 Troubleshooting

### Error: "The requested webhook is not registered"

**Solution:**
1. Make sure workflow is **Active** (green toggle)
2. Click on Webhook node → verify path is `validate-sentence`
3. Restart n8n: `docker-compose restart n8n`
4. Wait 10 seconds, try again

### Error: "Model output doesn't fit required format"

**Solution:**
1. AI Agent node → Chat Model → check System Message is correct
2. Make sure Temperature = 0.3 (lower = more consistent)
3. Verify Gemini API key is valid

### Error: Frontend still shows mock results

**Solution:**

```bash

docker-compose logs worddee_backend | grep "Error validating"



# Check .env has correct webhook URL
cat .env | grep N8N_WEBHOOK_URL
# Should be: N8N_WEBHOOK_URL=http://n8n:5678/webhook/validate-sentence


docker-compose restart worddee_backend
```

### Error: "Connection refused" or "Timeout"

**Solution:**
```bash

docker-compose ps


docker-compose up -d n8n
```

## ✅ Verification Checklist

- [ ] n8n accessible at http://localhost:5678
- [ ] Workflow "Validate Sentence v2" imported
- [ ] AI Agent configured with Gemini API key
- [ ] System message pasted correctly
- [ ] Workflow is **Active** (green toggle)
- [ ] Test curl command returns JSON (not error)
- [ ] Frontend shows real scores (not mock 7.0)

## 🎓 Understanding the Workflow

```
[Webhook] → Receives { word, definition, sentence }
    ↓
[AI Agent] → Sends to Gemini with system prompt
    ↓
[Extract Output] → Gets Gemini's response
    ↓
[Format Response] → Converts to backend format
    ↓
[Respond] → Returns JSON to backend
```

## 📝 Field Mapping

| Gemini Output | Backend Field | Type |
|---------------|---------------|------|
| score | score | number |
| cefr_level | cefr_level | string |
| is_correct | is_correct | boolean |
| feedback | feedback | string |
| corrected_sentence | corrected_sentence | string |

## 🔗 Related Files

- Backend: `backend/services/ai_service.py`
- Frontend: `frontend/lib/api.ts`
- Environment: `.env` (N8N_WEBHOOK_URL)

## 🆘 Still Need Help?

1. Check n8n logs: `docker-compose logs -f n8n`
2. Check backend logs: `docker-compose logs -f worddee_backend`
3. Verify Gemini API key at https://aistudio.google.com/app/apikey
4. Make sure you have API quota remaining

## ⚡ Quick Test Commands

```bash

curl http://localhost:5678


curl -X POST http://localhost:5678/webhook/validate-sentence \
  -H "Content-Type: application/json" \
  -d '{"word":"test","definition":"trial","sentence":"This is a test."}'


curl http://localhost:8000/health


open http://localhost:3000
```
