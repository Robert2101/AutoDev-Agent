"""
Gemini AI Agent - The brain of the AutoDev Agent.

This module uses Google's Gemini 1.5 Pro API to analyze code and generate fixes.
"""
import google.generativeai as genai
import time
from typing import List, Dict, Optional
from app.core.config import settings
from app.models import IssueType, IssueSeverity
import logging
import json

logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiAgent:
    """
    AI Agent powered by Google Gemini 1.5 Pro.
    
    Implements Chain of Thought prompting for:
    - Bug detection
    - Security vulnerability scanning
    - Code smell identification
    - Automated fix generation
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Gemini AI model."""
        self._api_key = api_key or settings.GEMINI_API_KEY
        genai.configure(api_key=self._api_key)
            
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # System prompt with Chain of Thought structure
        self.system_prompt = """You are a Senior Software Engineer with expertise in:
- Code review and bug detection
- Security vulnerability analysis
- Performance optimization
- Best practices and code quality

Your task is to analyze code files and identify issues. Follow this process:

1. **Analyze the code** for:
   - Syntax errors
   - Logic errors and race conditions
   - Security vulnerabilities (SQL injection, XSS, exposed secrets)
   - Code smells and anti-patterns
   - Performance issues

2. **For each issue found**:
   - Provide a clear, concise description
   - Specify the exact line number (if applicable)
   - Categorize the issue type and severity
   - Explain WHY it's a problem
   - Provide the corrected code block

3. **Guidelines**:
   - Do NOT remove comments unless necessary
   - Maintain the original code style and formatting
   - Provide complete, working code fixes
   - Be specific and actionable
   - If no issues are found, say "No issues detected"

**Output Format**:
For each issue, respond with a JSON object:
```json
{
  "issues": [
    {
      "file_path": "path/to/file.js",
      "line_number": 42,
      "issue_type": "security_vulnerability",
      "severity": "high",
      "description": "SQL injection vulnerability",
      "explanation": "User input is directly concatenated into SQL query without sanitization",
      "original_code": "SELECT * FROM users WHERE id = ' + userId + '",
      "fixed_code": "SELECT * FROM users WHERE id = $1",
      "fix_explanation": "Use parameterized queries to prevent SQL injection"
    }
  ]
}
```

Issue types: syntax_error, logic_error, security_vulnerability, code_smell, performance_issue, secret_exposure
Severity levels: low, medium, high, critical
"""
    
    def analyze_file(self, file_path: str, file_content: str, language: str, audit=None, db=None) -> List[Dict]:
        """
        Analyze a single file and detect issues.
        """
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Ensure the correct key is configured before every call
                genai.configure(api_key=self._api_key)
                
                prompt = f"""{self.system_prompt}

**File to Analyze**: {file_path}
**Language**: {language}
**Code**:
```{language}
{file_content}
```

Analyze this file and return ONLY a valid JSON object with detected issues.
If no issues are found, return: {{"issues": []}}
"""
                
                response = self.model.generate_content(prompt)
                result_text = response.text.strip()
                
                # Extract JSON from markdown code blocks if present
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0].strip()
                
                # Parse JSON response
                result = json.loads(result_text)
                
                issues = result.get("issues", [])
                
                # Add file_path to each issue if not present
                for issue in issues:
                    if "file_path" not in issue:
                        issue["file_path"] = file_path
                
                logger.info(f"Analyzed {file_path}: Found {len(issues)} issues")
                return issues
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Gemini response for {file_path}: {e}")
                logger.error(f"Response text: {result_text[:500]}")
                return []
            except Exception as e:
                err_str = str(e).lower()
                
                # Fingerprint the key for debugging
                current_key = f"{self._api_key[:4]}...{self._api_key[-4:]}" if self._api_key and len(self._api_key) > 8 else "Unknown"

                # 429 Handling
                if "429" in err_str:
                    msg = f"Rate Limit/Quota hit (429) using key: {current_key}"
                    logger.warning(msg)
                    
                    if audit and db:
                        from worker.tasks.audit_task import append_log
                        append_log(audit, db, 'WARNING', f'⏳ {msg}. Retrying...')

                    if ("billing" in err_str or "plan" in err_str) and attempt > 0:
                        logger.error(f"AI Quota Exceeded (Hard Limit): {e}")
                        raise e

                    if attempt < max_retries - 1:
                        wait_time = 60 if "quota" in err_str else 30
                        logger.warning(f"Retrying in {wait_time}s (Attempt {attempt + 1}/{max_retries})...")
                        time.sleep(wait_time)
                        continue
                
                logger.error(f"Error analyzing {file_path}: {e}")
                if attempt == max_retries - 1:
                    raise e
        return []
        return []
    
    def scan_for_secrets(self, file_content: str) -> List[Dict]:
        """
        Specialized scan for exposed secrets and credentials.
        
        Args:
            file_content: Content to scan
            
        Returns:
            List of detected secret exposures
        """
        prompt = f"""You are a security expert. Scan the following code for exposed secrets and credentials.

Look for:
- API keys (AWS, Google, Azure, OpenAI, etc.)
- Database passwords
- Private keys
- OAuth tokens
- Hardcoded credentials

**Code**:
```
{file_content}
```

Return ONLY a valid JSON object:
{{
  "secrets": [
    {{
      "type": "api_key",
      "description": "AWS API key exposed",
      "line": 15,
      "severity": "critical"
    }}
  ]
}}

If no secrets found, return: {{"secrets": []}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(result_text)
            return result.get("secrets", [])
            
        except Exception as e:
            logger.error(f"Error scanning for secrets: {e}")
            return []
    
    def validate_fix(self, original_code: str, fixed_code: str, language: str) -> bool:
        """
        Validate that a fix is syntactically correct.
        
        Args:
            original_code: Original code
            fixed_code: Fixed code
            language: Programming language
            
        Returns:
            True if fix appears valid
        """
        prompt = f"""Validate if this code fix is syntactically correct and maintains the same functionality.

**Original Code** ({language}):
```{language}
{original_code}
```

**Fixed Code** ({language}):
```{language}
{fixed_code}
```

Respond with ONLY: {{"valid": true}} or {{"valid": false}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            
            result = json.loads(result_text)
            return result.get("valid", False)
            
        except Exception:
            # If validation fails, assume it's invalid
            return False


# Create a global instance
gemini_agent = GeminiAgent()
