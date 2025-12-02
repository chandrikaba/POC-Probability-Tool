# Gemini API Setup Guide

## Getting Your API Key

### Step 1: Visit Google AI Studio

Go to: https://makersuite.google.com/app/apikey

### Step 2: Sign In

- Sign in with your Google account
- Accept the terms of service if prompted

### Step 3: Create API Key

1. Click on "Create API Key" button
2. Select a Google Cloud project (or create a new one)
3. Copy the generated API key

### Step 4: Configure the Project

1. Open `config/settings.py` in your project
2. Find the line:
   ```python
   GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
   ```
3. Replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key:
   ```python
   GEMINI_API_KEY = "AIzaSyD..."  # Your actual key
   ```
4. Save the file

## API Key Security

### Important Security Notes

- ⚠️ **Never commit your API key to version control**
- ⚠️ **Never share your API key publicly**
- ⚠️ **Keep your API key confidential**

### Best Practices

1. **Use Environment Variables** (Advanced)
   ```python
   import os
   GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
   ```

2. **Add to .gitignore**
   The `config/settings.py` file is already in `.gitignore`

3. **Rotate Keys Regularly**
   Generate new API keys periodically for security

## API Models

### Available Models

1. **gemini-1.5-flash** (Default)
   - Faster responses
   - Lower cost
   - Good for most use cases

2. **gemini-1.5-pro**
   - Higher quality output
   - Better for complex tasks
   - More expensive

### Changing Models

Edit `config/settings.py`:
```python
GEMINI_MODEL = "gemini-1.5-pro"  # For better quality
```

## Rate Limits

### Free Tier Limits

- 60 requests per minute
- 1,500 requests per day

### Handling Rate Limits

The generator includes automatic delays between batches:
```python
API_DELAY_SECONDS = 2  # Adjust in config/settings.py
```

If you hit rate limits:
1. Reduce `BATCH_SIZE` (e.g., from 50 to 25)
2. Increase `API_DELAY_SECONDS` (e.g., from 2 to 5)

## Troubleshooting

### Error: Invalid API Key

```
google.api_core.exceptions.PermissionDenied: 403 API key not valid
```

**Solutions:**
- Verify you copied the entire API key
- Check for extra spaces or quotes
- Generate a new API key

### Error: Quota Exceeded

```
google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded
```

**Solutions:**
- Wait for quota to reset (usually 1 minute or 24 hours)
- Reduce batch size
- Increase delay between requests
- Consider upgrading to paid tier

### Error: Model Not Found

```
google.api_core.exceptions.NotFound: 404 Model not found
```

**Solutions:**
- Check model name spelling in `config/settings.py`
- Ensure you're using a supported model
- Update the google-generativeai package

## Cost Estimation

### Free Tier

- **gemini-1.5-flash**: Free up to rate limits
- **gemini-1.5-pro**: Limited free usage

### Paid Usage

For 1000 rows with default settings:
- Batch size: 50 rows
- Total batches: 20
- Estimated cost: $0.10 - $0.50 (varies by model)

## Additional Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [API Pricing](https://ai.google.dev/pricing)
- [Python SDK Documentation](https://ai.google.dev/tutorials/python_quickstart)

## Support

If you encounter issues:
1. Check the error message carefully
2. Review this guide
3. Consult the official documentation
4. Verify your API key is valid and active
