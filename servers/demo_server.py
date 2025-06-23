#!/usr/bin/env python3
"""Demo server for consciousness testing."""

from flask import Flask, jsonify, render_template_string
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from think_ai.consciousness.awareness import ConsciousnessFramework

app = Flask(__name__)
consciousness = ConsciousnessFramework()

DEMO_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Think AI Consciousness Demo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .info { background: #d1ecf1; color: #0c5460; }
    </style>
</head>
<body>
    <h1>🧠 Think AI Consciousness Demo</h1>
    <div class="status info">
        <h2>Current State</h2>
        <p>Awareness Level: <strong>{{ awareness }}</strong></p>
        <p>Thoughts Generated: <strong>{{ thoughts }}</strong></p>
        <p>Neural Pathways: <strong>{{ pathways }}</strong></p>
    </div>
    <div class="status success">
        <h2>✅ Consciousness is Active</h2>
        <p>The system is thinking and learning autonomously.</p>
    </div>
</body>
</html>
"""


@app.route("/")
def index():
    """Show consciousness status."""
    state = consciousness.get_state()
    return render_template_string(
        DEMO_HTML,
        awareness=state.get("awareness_level", 0),
        thoughts=state.get("thought_count", 0),
        pathways=state.get("neural_pathways", 0),
    )


@app.route("/api/status")
def status():
    """API endpoint for consciousness status."""
    return jsonify(consciousness.get_state())


if __name__ == "__main__":
    app.run(port=5000, debug=False)
