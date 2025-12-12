# n8n Workflow Setup Guide

## Overview

This directory contains the n8n workflow for AI-powered English sentence validation using Google Gemini.

## Quick Setup

### 1. Get Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### 2. Configure Environment

Add your Gemini API key to `.env` file:

```bash
GEMINI_API_KEY=your_api_key_here
```

### 3. Import Workflow

1. Open n8n at http://localhost:5678
2. Login with credentials:
   - Username: `admin`
   - Password: `admin_password_456!`
3. Click "Add workflow" → "Import from file"
4. Select `n8n/workflows/validate-sentence.json`
5. Click "Import"

### 4. Configure Gemini Credentials

1. Click on the "Google Gemini" node
2. In the "Credentials" section, click "Create New"
3. Enter your Gemini API key
4. Click "Save"

### 5. Activate Workflow

1. Click the "Inactive" toggle (top right)
2. It should turn green and say "Active"
3. Copy the webhook URL (should be: `http://n8n:5678/webhook/validate-sentence`)

## Workflow Details

### Nodes

1. **Webhook** - Receives POST requests with sentence data
2. **Prepare Prompt** - Formats the prompt for Gemini
3. **Google Gemini** - Sends prompt to Gemini AI
4. **Parse Response** - Extracts validation results
5. **Respond to Webhook** - Returns results to backend

### Input Format

```json
{
  "word": "example",
  "definition": "a thing characteristic of its kind",
  "sentence": "This is an example sentence."
}
```

### Output Format

```json
{
  "score": 8.5,
  "cefr_level": "B2",
  "is_correct": true,
  "feedback": "Excellent sentence! Good use of the word...",
  "corrected_sentence": "This is an example sentence.",
  "original_word": "example",
  "original_sentence": "This is an example sentence."
}
```

## Testing

### Test with curl

```bash
curl -X POST http://localhost:5678/webhook/validate-sentence \
  -H "Content-Type: application/json" \
  -d '{
    "word": "example",
    "definition": "a thing characteristic of its kind",
    "sentence": "This is an example of good writing."
  }'
```

### Expected Response

```json
{
  "score": 9.0,
  "cefr_level": "B2",
  "is_correct": true,
  "feedback": "Excellent use of the word 'example'...",
  "corrected_sentence": "This is an example of good writing."
}
```

## Scoring Criteria

- **0-3**: Major grammar errors, word misused
- **4-5**: Multiple grammar errors, word used incorrectly
- **6-7**: Minor errors, word used acceptably
- **8-9**: Good sentence, minor improvements possible
- **10**: Perfect grammar, excellent word usage

## CEFR Levels

- **A1/A2**: Basic sentences, simple vocabulary
- **B1/B2**: Intermediate complexity, correct structure
- **C1/C2**: Advanced, sophisticated language

## Troubleshooting

### Workflow not responding

1. Check if workflow is Active (green toggle)
2. Verify Gemini credentials are configured
3. Check n8n logs: `docker-compose logs n8n`

### Invalid API key error

1. Verify GEMINI_API_KEY in .env
2. Check if API key is valid at [Google AI Studio](https://aistudio.google.com/app/apikey)
3. Restart n8n: `docker-compose restart n8n`

### Webhook URL not working

1. Ensure N8N_WEBHOOK_URL in .env matches the workflow webhook
2. Default: `http://n8n:5678/webhook/validate-sentence`
3. Restart backend: `docker-compose restart worddee_backend`

## Advanced Configuration

### Temperature Setting

Adjust creativity in the Gemini node:
- Low (0.1-0.3): More consistent, factual responses
- Medium (0.4-0.7): Balanced creativity
- High (0.8-1.0): More creative, varied responses

### Max Tokens

Control response length (default: 500)
- Increase for longer, more detailed feedback
- Decrease for concise responses

## Support

For issues or questions:
1. Check n8n documentation: https://docs.n8n.io
2. Review Gemini API docs: https://ai.google.dev/docs
3. Open an issue on GitHub
