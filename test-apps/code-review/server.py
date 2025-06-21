#!/usr/bin/env python3

"""App 3: Code Review System with AI Suggestions
Tests: Code analysis, pattern matching, suggestion generation.
"""

import ast
import os
import re
import sys

import torch
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from vector_search_adapter import VectorSearchAdapter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

torch.set_default_device("cpu")
app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
vector_db = VectorSearchAdapter(384)

# Pre-load code patterns and best practices
best_practices = [
    {
        "pattern": "except Exception:",
        "issue": "Catching generic Exception",
        "suggestion": "Use specific exception types for better error handling",
        "severity": "medium",
        "example": "except ValueError: or except (ValueError, TypeError):",
    },
    {
        "pattern": "TODO|FIXME|XXX",
        "issue": "Unfinished code marker",
        "suggestion": "Complete the implementation or create a ticket",
        "severity": "low",
        "example": "Implement the feature or remove the marker",
    },
    {
        "pattern": "password|secret|key|token",
        "issue": "Potential hardcoded secret",
        "suggestion": "Use environment variables or secure key management",
        "severity": "high",
        "example": "os.environ.get('API_KEY') or use a secrets manager",
    },
    {
        "pattern": "eval\\(|exec\\(",
        "issue": "Dangerous function usage",
        "suggestion": "Avoid eval/exec for security reasons",
        "severity": "high",
        "example": "Use ast.literal_eval() for safe evaluation",
    },
]

# Add patterns to vector DB
for practice in best_practices:
    desc = f"{practice['issue']}: {practice['suggestion']}"
    embedding = model.encode(desc)
    vector_db.add(embedding, practice)


class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
    filename: str = "untitled"


def analyze_code_quality(code: str, language: str):
    """Analyze code for quality issues."""
    issues = []
    lines = code.split("\n")

    # Pattern-based analysis
    for i, line in enumerate(lines, 1):
        for practice in best_practices:
            if re.search(practice["pattern"], line, re.IGNORECASE):
                issues.append(
                    {
                        "line": i,
                        "code": line.strip(),
                        "issue": practice["issue"],
                        "suggestion": practice["suggestion"],
                        "severity": practice["severity"],
                        "example": practice["example"],
                    }
                )

    # Python-specific analysis
    if language == "python":
        try:
            tree = ast.parse(code)

            # Check for missing docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if not ast.get_docstring(node):
                        line_no = node.lineno
                        issues.append(
                            {
                                "line": line_no,
                                "code": (
                                    f"def {node.name}..."
                                    if isinstance(node, ast.FunctionDef)
                                    else f"class {node.name}..."
                                ),
                                "issue": "Missing docstring",
                                "suggestion": "Add a docstring to document the purpose",
                                "severity": "low",
                                "example": '"""Description of function/class"""',
                            }
                        )

            # Check for long functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno
                    if func_lines > 50:
                        issues.append(
                            {
                                "line": node.lineno,
                                "code": f"def {node.name}... ({func_lines} lines)",
                                "issue": "Function too long",
                                "suggestion": "Consider breaking into smaller functions",
                                "severity": "medium",
                                "example": "Split into logical sub-functions",
                            }
                        )
        except Exception:
            pass

    return issues


def generate_ai_suggestions(code: str, issues: list):
    """Generate AI-powered suggestions based on code context."""
    suggestions = []

    # Get similar code patterns
    code_desc = f"Code with {len(issues)} issues"
    embedding = model.encode(code_desc)
    similar = vector_db.search(embedding, k=3)

    for score, meta in similar:
        if score > 0.5:
            suggestions.append(
                {
                    "type": "pattern",
                    "suggestion": meta["suggestion"],
                    "confidence": float(score),
                }
            )

    return suggestions


@app.post("/api/review")
async def review_code(request: CodeReviewRequest):
    """Perform code review with AI assistance."""
    issues = analyze_code_quality(request.code, request.language)
    ai_suggestions = generate_ai_suggestions(request.code, issues)

    # Calculate overall score
    score = 100
    for issue in issues:
        if issue["severity"] == "high":
            score -= 10
        elif issue["severity"] == "medium":
            score -= 5
        else:
            score -= 2

    score = max(0, score)

    return {
        "filename": request.filename,
        "language": request.language,
        "score": score,
        "issues": issues,
        "ai_suggestions": ai_suggestions,
        "summary": {
            "total_issues": len(issues),
            "high_severity": sum(1 for i in issues if i["severity"] == "high"),
            "medium_severity": sum(1 for i in issues if i["severity"] == "medium"),
            "low_severity": sum(1 for i in issues if i["severity"] == "low"),
        },
    }


@app.get("/")
async def read_index():
    return HTMLResponse(
        r"""
<!DOCTYPE html>
<html>
<head>
    <title>AI Code Review System</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.0/codemirror.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.0/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.0/mode/python/python.min.js"></script>
    <style>
        body { font-family: -apple-system, sans-serif; margin: 0; padding: 20px; background: #f0f2f5; }
        .container { max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .panel { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        h1 { text-align: center; color: #333; }
        h2 { color: #555; margin-top: 0; }
        .CodeMirror { height: 400px; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #4CAF50; color: white; border: none; padding: 12px 30px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #45a049; }
        .score { font-size: 48px; font-weight: bold; text-align: center; margin: 20px 0; }
        .score.good { color: #4CAF50; }
        .score.medium { color: #ff9800; }
        .score.bad { color: #f44336; }
        .issue { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .issue.high { background: #f8d7da; border-color: #dc3545; }
        .issue.medium { background: #fff3cd; border-color: #ffc107; }
        .issue.low { background: #d1ecf1; border-color: #17a2b8; }
        .suggestion { background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .line-number { color: #666; font-weight: bold; }
        .code-snippet { background: #f4f4f4; padding: 5px 10px; border-radius: 3px; font-family: monospace; margin: 5px 0; }
        .stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat { text-align: center; }
        .stat-number { font-size: 36px; font-weight: bold; }
        .stat-label { color: #666; }
    </style>
</head>
<body>
    <h1>🔍 AI-Powered Code Review</h1>

    <div class="container">
        <div class="panel">
            <h2>Code Input</h2>
            <textarea id="codeInput"></textarea>
            <div style="margin-top: 20px; text-align: center;">
                <button onclick="reviewCode()">Review Code</button>
            </div>
        </div>

        <div class="panel">
            <h2>Review Results</h2>
            <div id="results">
                <p style="text-align: center; color: #666;">Submit code for review...</p>
            </div>
        </div>
    </div>

    <script>
        const editor = CodeMirror.fromTextArea(document.getElementById('codeInput'), {
            lineNumbers: true,
            mode: 'python',
            theme: 'default',
            value: \`# Example Python code
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# TODO: Add error handling
password = "admin123"  # This should be in env vars

try:
    result = eval(user_input)  # Dangerous!
except Exception:
    print("Error occurred")
\`
        });

        editor.setValue(editor.getValue());

        async function reviewCode() {
            const code = editor.getValue();

            const response = await fetch('/api/review', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code: code,
                    language: 'python',
                    filename: 'example.py'
                })
            });

            const result = await response.json();
            displayResults(result);
        }

        function displayResults(result) {
            const container = document.getElementById('results');

            let scoreClass = 'good';
            if (result.score < 70) scoreClass = 'bad';
            else if (result.score < 85) scoreClass = 'medium';

            let html = \`
                <div class="score \${scoreClass}">\${result.score}/100</div>

                <div class="stats">
                    <div class="stat">
                        <div class="stat-number">\${result.summary.total_issues}</div>
                        <div class="stat-label">Total Issues</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number" style="color: #dc3545;">\${result.summary.high_severity}</div>
                        <div class="stat-label">High Severity</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number" style="color: #ffc107;">\${result.summary.medium_severity}</div>
                        <div class="stat-label">Medium Severity</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number" style="color: #17a2b8;">\${result.summary.low_severity}</div>
                        <div class="stat-label">Low Severity</div>
                    </div>
                </div>

                <h3>Issues Found:</h3>
            \`;

            result.issues.forEach(issue => {
                html += \`
                    <div class="issue \${issue.severity}">
                        <div class="line-number">Line \${issue.line}</div>
                        <div class="code-snippet">\${escapeHtml(issue.code)}</div>
                        <strong>\${issue.issue}</strong><br>
                        💡 \${issue.suggestion}<br>
                        <small>Example: \${issue.example}</small>
                    </div>
                \`;
            });

            if (result.ai_suggestions.length > 0) {
                html += '<h3>AI Suggestions:</h3>';
                result.ai_suggestions.forEach(suggestion => {
                    html += \`
                        <div class="suggestion">
                            <strong>Pattern Match (\${(suggestion.confidence * 100).toFixed(1)}%)</strong><br>
                            \${suggestion.suggestion}
                        </div>
                    \`;
                });
            }

            container.innerHTML = html;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
    """
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003)
