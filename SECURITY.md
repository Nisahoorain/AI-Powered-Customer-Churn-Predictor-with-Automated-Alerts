# Security Best Practices

## 🔒 Protecting Sensitive Information

This project follows security best practices to protect sensitive data:

### ✅ What's Safe to Commit
- Source code
- Model files (`.pkl`)
- Sample/test data
- Configuration templates
- Documentation

### ❌ Never Commit
- API keys or secrets
- Webhook URLs with authentication tokens
- Database credentials
- Personal access tokens
- `.env` files with actual values
- Production credentials

### 🛡️ Current Security Measures

1. **Webhook URLs**: Entered by users in the Streamlit app (not hardcoded)
2. **Environment Variables**: Protected by `.gitignore`
3. **No Hardcoded Secrets**: All sensitive data is user-provided at runtime

### 📝 For Production Use

If deploying this for production:
- Use environment variables for all secrets
- Enable authentication on the Streamlit app
- Use secure webhook endpoints
- Implement rate limiting
- Add input validation
- Use HTTPS only
- Regular security audits

### 🔐 Environment Variables (if needed)

If you need to add environment variables, create a `.env` file (already in `.gitignore`):

```bash
# .env (DO NOT COMMIT THIS FILE)
WEBHOOK_URL=https://your-webhook-url.com
API_KEY=your-api-key-here
```

Then load them in your code:
```python
import os
from dotenv import load_dotenv

load_dotenv()
webhook_url = os.getenv('WEBHOOK_URL')
```

---

**Remember**: Always review your code before committing to ensure no secrets are exposed!

