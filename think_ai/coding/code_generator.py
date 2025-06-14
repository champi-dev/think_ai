#!/usr/bin/env python3
"""
Advanced Code Generator for Think AI
Generates complete applications from descriptions
"""

import asyncio
import re
from typing import Dict, List, Any, Optional, Tuple
import ast
import json
from datetime import datetime
import hashlib

from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


class CodeGenerator:
    """Advanced code generator that creates complete applications."""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.patterns = self._load_patterns()
        self.generated_count = 0
        
    def _load_templates(self) -> Dict[str, str]:
        """Load code generation templates."""
        return {
            "class": '''class {name}:
    """{description}"""
    
    def __init__(self{params}):
        """Initialize {name}."""
{init_body}
    
{methods}''',
            
            "function": '''def {name}({params}){return_type}:
    """{description}"""
{body}''',
            
            "async_function": '''async def {name}({params}){return_type}:
    """{description}"""
{body}''',
            
            "method": '''    def {name}(self{params}){return_type}:
        """{description}"""
{body}''',
            
            "async_method": '''    async def {name}(self{params}){return_type}:
        """{description}"""
{body}''',
            
            "html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
{styles}
</head>
<body>
{content}
{scripts}
</body>
</html>''',
            
            "react_component": '''import React{imports} from 'react';

const {name} = ({props}) => {{
    {state}
    {effects}
    
    return (
{jsx}
    );
}};

export default {name};''',
            
            "api_endpoint": '''@app.{method}('{path}')
async def {name}({params}):
    """{description}"""
{body}''',
        }
    
    def _load_patterns(self) -> Dict[str, re.Pattern]:
        """Load regex patterns for code analysis."""
        return {
            "function": re.compile(r'def\s+(\w+)\s*\(([^)]*)\)'),
            "class": re.compile(r'class\s+(\w+)(?:\s*\(([^)]*)\))?:'),
            "import": re.compile(r'(?:from\s+(\S+)\s+)?import\s+(.+)'),
            "variable": re.compile(r'(\w+)\s*=\s*(.+)'),
            "method_call": re.compile(r'(\w+)\.(\w+)\s*\('),
        }
    
    async def generate_from_description(self, description: str, language: str = "python") -> Dict[str, str]:
        """Generate complete code from natural language description."""
        logger.info(f"Generating {language} code from description")
        
        # Analyze description
        analysis = self._analyze_description(description)
        
        # Generate appropriate code based on analysis
        if analysis["type"] == "web_app":
            return await self._generate_web_app(analysis)
        elif analysis["type"] == "api":
            return await self._generate_api(analysis)
        elif analysis["type"] == "script":
            return await self._generate_script(analysis)
        elif analysis["type"] == "class":
            return await self._generate_class(analysis)
        elif analysis["type"] == "game":
            return await self._generate_game(analysis)
        else:
            return await self._generate_generic(analysis, language)
    
    def _analyze_description(self, description: str) -> Dict[str, Any]:
        """Analyze description to determine code type and requirements."""
        desc_lower = description.lower()
        
        analysis = {
            "type": "generic",
            "features": [],
            "framework": None,
            "database": None,
            "description": description
        }
        
        # Detect type
        if any(word in desc_lower for word in ["web", "website", "webapp", "site"]):
            analysis["type"] = "web_app"
        elif any(word in desc_lower for word in ["api", "rest", "endpoint", "service"]):
            analysis["type"] = "api"
        elif any(word in desc_lower for word in ["script", "tool", "utility", "cli"]):
            analysis["type"] = "script"
        elif any(word in desc_lower for word in ["class", "object", "model"]):
            analysis["type"] = "class"
        elif any(word in desc_lower for word in ["game", "play", "score", "level"]):
            analysis["type"] = "game"
        
        # Detect features
        if "database" in desc_lower or "db" in desc_lower:
            analysis["features"].append("database")
            if "postgres" in desc_lower:
                analysis["database"] = "postgresql"
            elif "mysql" in desc_lower:
                analysis["database"] = "mysql"
            else:
                analysis["database"] = "sqlite"
        
        if any(word in desc_lower for word in ["auth", "login", "user", "password"]):
            analysis["features"].append("authentication")
        
        if any(word in desc_lower for word in ["real-time", "realtime", "websocket", "live"]):
            analysis["features"].append("realtime")
        
        if "test" in desc_lower:
            analysis["features"].append("testing")
        
        # Detect framework preferences
        if "react" in desc_lower:
            analysis["framework"] = "react"
        elif "vue" in desc_lower:
            analysis["framework"] = "vue"
        elif "flask" in desc_lower:
            analysis["framework"] = "flask"
        elif "django" in desc_lower:
            analysis["framework"] = "django"
        elif "fastapi" in desc_lower:
            analysis["framework"] = "fastapi"
        
        return analysis
    
    async def _generate_web_app(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate a complete web application."""
        files = {}
        
        # Choose framework
        framework = analysis.get("framework", "flask")
        
        if framework == "flask":
            # Main app file
            files["app.py"] = self._generate_flask_app(analysis)
            files["requirements.txt"] = self._generate_requirements(["flask"], analysis)
            
            # Templates
            files["templates/index.html"] = self._generate_html_template(analysis)
            files["templates/base.html"] = self._generate_base_template()
            
            # Static files
            files["static/style.css"] = self._generate_css()
            files["static/script.js"] = self._generate_javascript(analysis)
            
            # Database models if needed
            if "database" in analysis["features"]:
                files["models.py"] = self._generate_models(analysis)
                files["database.py"] = self._generate_database_setup(analysis)
            
            # Authentication if needed
            if "authentication" in analysis["features"]:
                files["auth.py"] = self._generate_auth_module()
                files["templates/login.html"] = self._generate_login_template()
                files["templates/register.html"] = self._generate_register_template()
        
        elif framework == "react":
            # React app structure
            files["package.json"] = self._generate_package_json(analysis)
            files["src/App.js"] = self._generate_react_app(analysis)
            files["src/index.js"] = self._generate_react_index()
            files["src/App.css"] = self._generate_react_css()
            
            # Components
            files["src/components/Header.js"] = self._generate_react_component("Header")
            files["src/components/Footer.js"] = self._generate_react_component("Footer")
            
            if "authentication" in analysis["features"]:
                files["src/components/Login.js"] = self._generate_react_component("Login", with_form=True)
                files["src/components/Register.js"] = self._generate_react_component("Register", with_form=True)
        
        # Add tests if requested
        if "testing" in analysis["features"]:
            files["tests.py"] = self._generate_tests(analysis)
        
        # Add README
        files["README.md"] = self._generate_readme(analysis)
        
        self.generated_count += 1
        return files
    
    async def _generate_api(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate a complete API."""
        files = {}
        
        framework = analysis.get("framework", "fastapi")
        
        if framework == "fastapi":
            files["main.py"] = self._generate_fastapi_app(analysis)
            files["requirements.txt"] = self._generate_requirements(["fastapi", "uvicorn"], analysis)
            files["models.py"] = self._generate_pydantic_models(analysis)
            
            if "database" in analysis["features"]:
                files["database.py"] = self._generate_database_setup(analysis)
                files["crud.py"] = self._generate_crud_operations(analysis)
            
            if "authentication" in analysis["features"]:
                files["auth.py"] = self._generate_auth_api()
                files["security.py"] = self._generate_security_module()
            
            files["README.md"] = self._generate_api_readme(analysis)
        
        return files
    
    async def _generate_script(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate a Python script."""
        files = {}
        
        # Main script
        script_content = f'''#!/usr/bin/env python3
"""
{analysis["description"]}
Generated by Think AI
"""

import argparse
import sys
import os
from pathlib import Path

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="{analysis["description"]}")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("-o", "--output", help="Output file", default="output.txt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Process input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {{input_path}} does not exist")
        return 1
    
    # Main logic here
    if input_path.is_file():
        process_file(input_path, args.output, args.verbose)
    elif input_path.is_dir():
        process_directory(input_path, args.output, args.verbose)
    
    return 0

def process_file(file_path: Path, output: str, verbose: bool = False):
    """Process a single file."""
    if verbose:
        print(f"Processing {{file_path}}")
    
    # Add processing logic here
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Process content
    result = transform_content(content)
    
    # Write output
    with open(output, 'w') as f:
        f.write(result)
    
    if verbose:
        print(f"Output written to {{output}}")

def process_directory(dir_path: Path, output: str, verbose: bool = False):
    """Process all files in directory."""
    files = list(dir_path.glob("**/*"))
    
    if verbose:
        print(f"Found {{len(files)}} files")
    
    results = []
    for file_path in files:
        if file_path.is_file():
            # Process each file
            results.append(process_single_file(file_path))
    
    # Combine results
    with open(output, 'w') as f:
        f.write("\\n".join(results))

def transform_content(content: str) -> str:
    """Transform content based on requirements."""
    # Add transformation logic
    return content.upper()  # Example transformation

def process_single_file(file_path: Path) -> str:
    """Process single file and return result."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return f"{{file_path}}: {{len(content)}} bytes"
    except Exception as e:
        return f"{{file_path}}: Error - {{e}}"

if __name__ == "__main__":
    sys.exit(main())
'''
        
        files["script.py"] = script_content
        files["requirements.txt"] = self._generate_requirements([], analysis)
        
        if "testing" in analysis["features"]:
            files["test_script.py"] = self._generate_script_tests()
        
        return files
    
    async def _generate_class(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate a Python class."""
        # Extract class name from description
        words = analysis["description"].split()
        class_name = "".join(word.capitalize() for word in words[:2])
        
        class_code = self.templates["class"].format(
            name=class_name,
            description=analysis["description"],
            params=", name=None, **kwargs",
            init_body='''        self.name = name or self.__class__.__name__
        self.created_at = datetime.now()
        self.attributes = kwargs
        self._initialize()''',
            methods='''    def _initialize(self):
        """Initialize the object."""
        pass
    
    def __str__(self):
        """String representation."""
        return f"{self.name} ({self.created_at})"
    
    def __repr__(self):
        """Developer representation."""
        return f"<{self.__class__.__name__}(name='{self.name}')>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "attributes": self.attributes
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create from dictionary."""
        instance = cls(name=data.get("name"))
        instance.attributes = data.get("attributes", {})
        return instance'''
        )
        
        files = {
            f"{class_name.lower()}.py": f"from datetime import datetime\n\n{class_code}"
        }
        
        return files
    
    async def _generate_game(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate a simple game."""
        files = {}
        
        game_code = '''"""
Simple Game generated by Think AI
{description}
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Player(pygame.sprite.Sprite):
    """Player class."""
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 5
        
    def update(self):
        """Update player position."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

class Enemy(pygame.sprite.Sprite):
    """Enemy class."""
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)
        
    def update(self):
        """Update enemy position."""
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 3)

class Game:
    """Main game class."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Think AI Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Create player
        self.player = Player()
        self.all_sprites.add(self.player)
        
        # Create enemies
        for _ in range(10):
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
    
    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Update game state."""
        self.all_sprites.update()
        
        # Check collisions
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for hit in hits:
            self.score += 10
            # Create new enemy
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
    
    def draw(self):
        """Draw everything."""
        self.screen.fill(BLACK)
        
        # Draw sprites
        self.all_sprites.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {{self.score}}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw instructions
        inst_text = self.font.render("Arrow keys to move, ESC to quit", True, YELLOW)
        self.screen.blit(inst_text, (SCREEN_WIDTH // 2 - 200, 50))
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Main function."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
'''.format(description=analysis["description"])
        
        files["game.py"] = game_code
        files["requirements.txt"] = "pygame>=2.0.0\n"
        files["README.md"] = f"""# {analysis["description"]}

A simple game created by Think AI.

## Installation
```bash
pip install -r requirements.txt
```

## How to Play
```bash
python game.py
```

Use arrow keys to move, avoid red enemies!
"""
        
        return files
    
    async def _generate_generic(self, analysis: Dict[str, Any], language: str) -> Dict[str, str]:
        """Generate generic code based on language."""
        files = {}
        
        if language == "python":
            code = f'''"""
{analysis["description"]}
Generated by Think AI
"""

def main():
    """Main function."""
    print("Hello from Think AI!")
    # Add your code here

if __name__ == "__main__":
    main()
'''
            files["main.py"] = code
            
        elif language == "javascript":
            code = f'''/**
 * {analysis["description"]}
 * Generated by Think AI
 */

function main() {{
    console.log("Hello from Think AI!");
    // Add your code here
}}

main();
'''
            files["main.js"] = code
            
        elif language == "html":
            code = self.templates["html"].format(
                title=analysis["description"],
                styles="<style>body { font-family: Arial, sans-serif; }</style>",
                content=f"<h1>{analysis['description']}</h1>\n<p>Generated by Think AI</p>",
                scripts=""
            )
            files["index.html"] = code
        
        return files
    
    # Helper methods for generating specific components
    def _generate_flask_app(self, analysis: Dict[str, Any]) -> str:
        """Generate Flask application."""
        imports = ["from flask import Flask, render_template, request, jsonify"]
        
        if "database" in analysis["features"]:
            imports.append("from database import db, init_db")
            imports.append("from models import *")
        
        if "authentication" in analysis["features"]:
            imports.append("from flask_login import LoginManager, login_required")
            imports.append("from auth import auth_bp")
        
        code = f'''"""
{analysis["description"]}
Flask Web Application generated by Think AI
"""

{chr(10).join(imports)}
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'think-ai-secret-key')
'''
        
        if "database" in analysis["features"]:
            code += '''
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)
'''
        
        if "authentication" in analysis["features"]:
            code += '''
# Authentication setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register authentication blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')
'''
        
        code += '''
@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """API status endpoint."""
    return jsonify({
        'status': 'running',
        'message': 'Think AI Web App is running!'
    })
'''
        
        if "database" in analysis["features"]:
            code += '''
@app.route('/api/data')
@login_required
def api_data():
    """Get data from database."""
    # Add your database queries here
    return jsonify({'data': []})
'''
        
        code += '''
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
        
        return code
    
    def _generate_requirements(self, base_requirements: List[str], analysis: Dict[str, Any]) -> str:
        """Generate requirements.txt file."""
        requirements = set(base_requirements)
        
        if "database" in analysis["features"]:
            requirements.add("flask-sqlalchemy")
            requirements.add("sqlalchemy")
            
            if analysis.get("database") == "postgresql":
                requirements.add("psycopg2-binary")
            elif analysis.get("database") == "mysql":
                requirements.add("mysqlclient")
        
        if "authentication" in analysis["features"]:
            requirements.add("flask-login")
            requirements.add("werkzeug")
            requirements.add("email-validator")
        
        if "realtime" in analysis["features"]:
            requirements.add("flask-socketio")
            requirements.add("python-socketio")
        
        if "testing" in analysis["features"]:
            requirements.add("pytest")
            requirements.add("pytest-cov")
        
        return "\n".join(sorted(requirements))
    
    def _generate_html_template(self, analysis: Dict[str, Any]) -> str:
        """Generate HTML template."""
        features_html = ""
        
        if "authentication" in analysis["features"]:
            features_html += '''
        <div class="auth-section">
            <a href="/auth/login">Login</a> | 
            <a href="/auth/register">Register</a>
        </div>'''
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{analysis["description"]}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>{analysis["description"]}</h1>
        <p>Welcome to your AI-generated web application!</p>
        {features_html}
        
        <div id="app">
            <!-- Dynamic content goes here -->
        </div>
    </div>
    
    <script src="/static/script.js"></script>
</body>
</html>'''
    
    def _generate_base_template(self) -> str:
        """Generate base template for template inheritance."""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Think AI App{% endblock %}</title>
    <link rel="stylesheet" href="/static/style.css">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar">
        <a href="/" class="logo">Think AI</a>
        <div class="nav-links">
            <a href="/">Home</a>
            {% if current_user.is_authenticated %}
                <a href="/dashboard">Dashboard</a>
                <a href="/auth/logout">Logout</a>
            {% else %}
                <a href="/auth/login">Login</a>
                <a href="/auth/register">Register</a>
            {% endif %}
        </div>
    </nav>
    
    <main class="main-content">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </main>
    
    <footer class="footer">
        <p>&copy; 2024 Think AI. Generated with consciousness.</p>
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>'''
    
    def _generate_css(self) -> str:
        """Generate CSS styles."""
        return '''/* Think AI Generated Styles */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.navbar {
    background-color: #333;
    color: white;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    transition: background-color 0.3s;
}

.navbar a:hover {
    background-color: #555;
    border-radius: 4px;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
}

.nav-links {
    display: flex;
    gap: 1rem;
}

.main-content {
    min-height: calc(100vh - 120px);
    padding: 2rem;
}

.alert {
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 4px;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.footer {
    background-color: #333;
    color: white;
    text-align: center;
    padding: 1rem;
    position: relative;
    bottom: 0;
    width: 100%;
}

/* Forms */
.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    background-color: #007bff;
    color: white;
    text-decoration: none;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #0056b3;
}

.btn-secondary {
    background-color: #6c757d;
}

.btn-secondary:hover {
    background-color: #545b62;
}

/* Cards */
.card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.card h2 {
    margin-bottom: 1rem;
    color: #333;
}

/* Responsive */
@media (max-width: 768px) {
    .nav-links {
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .container {
        padding: 10px;
    }
}'''
    
    def _generate_javascript(self, analysis: Dict[str, Any]) -> str:
        """Generate JavaScript code."""
        js_code = '''// Think AI Generated JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('Think AI App loaded!');
    
    // Initialize app
    const app = new App();
    app.init();
});

class App {
    constructor() {
        this.apiUrl = '/api';
        this.data = [];
    }
    
    init() {
        this.loadData();
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Add event listeners here
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                console.log('Button clicked:', e.target);
            });
        });
    }
    
    async loadData() {
        try {
            const response = await fetch(`${this.apiUrl}/status`);
            const data = await response.json();
            console.log('API Status:', data);
            this.updateUI(data);
        } catch (error) {
            console.error('Error loading data:', error);
        }
    }
    
    updateUI(data) {
        const appDiv = document.getElementById('app');
        if (appDiv && data.message) {
            appDiv.innerHTML = `
                <div class="card">
                    <h2>API Status</h2>
                    <p>${data.message}</p>
                </div>
            `;
        }
    }'''
        
        if "realtime" in analysis["features"]:
            js_code += '''
    
    connectWebSocket() {
        const socket = io();
        
        socket.on('connect', () => {
            console.log('WebSocket connected');
        });
        
        socket.on('message', (data) => {
            console.log('Received:', data);
            this.handleRealtimeUpdate(data);
        });
    }
    
    handleRealtimeUpdate(data) {
        // Handle real-time updates
        const updates = document.getElementById('updates');
        if (updates) {
            updates.innerHTML += `<p>${data.message}</p>`;
        }
    }'''
        
        js_code += '''
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}'''
        
        return js_code
    
    def _generate_models(self, analysis: Dict[str, Any]) -> str:
        """Generate database models."""
        return '''"""
Database models for the application.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model."""
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    """Post model."""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Post {self.title}>'

class Category(db.Model):
    """Category model."""
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Category {self.name}>'
'''
    
    def _generate_database_setup(self, analysis: Dict[str, Any]) -> str:
        """Generate database setup code."""
        return '''"""
Database setup and initialization.
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_db(app: Flask):
    """Initialize database with app."""
    db.init_app(app)
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Add initial data if needed
        seed_database()

def seed_database():
    """Seed database with initial data."""
    from models import User, Category
    
    # Check if already seeded
    if User.query.first() is not None:
        return
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create categories
    categories = ['Technology', 'Science', 'Art', 'Music', 'Sports']
    for cat_name in categories:
        category = Category(name=cat_name)
        db.session.add(category)
    
    # Commit changes
    db.session.commit()
    print("Database seeded successfully!")
'''
    
    def _generate_auth_module(self) -> str:
        """Generate authentication module."""
        return '''"""
Authentication module.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        # Validation
        if password != password2:
            flash('Passwords do not match', 'error')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
        else:
            # Create user
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
'''
    
    def _generate_login_template(self) -> str:
        """Generate login template."""
        return '''{% extends "base.html" %}

{% block title %}Login - Think AI{% endblock %}

{% block content %}
<div class="container">
    <div class="card" style="max-width: 400px; margin: 0 auto;">
        <h2>Login</h2>
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="form-group">
                <label>
                    <input type="checkbox" name="remember"> Remember me
                </label>
            </div>
            
            <button type="submit" class="btn">Login</button>
            
            <p style="margin-top: 1rem;">
                Don't have an account? <a href="{{ url_for('auth.register') }}">Register here</a>
            </p>
        </form>
    </div>
</div>
{% endblock %}'''
    
    def _generate_register_template(self) -> str:
        """Generate registration template."""
        return '''{% extends "base.html" %}

{% block title %}Register - Think AI{% endblock %}

{% block content %}
<div class="container">
    <div class="card" style="max-width: 400px; margin: 0 auto;">
        <h2>Register</h2>
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="form-group">
                <label for="password2">Confirm Password</label>
                <input type="password" id="password2" name="password2" required>
            </div>
            
            <button type="submit" class="btn">Register</button>
            
            <p style="margin-top: 1rem;">
                Already have an account? <a href="{{ url_for('auth.login') }}">Login here</a>
            </p>
        </form>
    </div>
</div>
{% endblock %}'''
    
    def _generate_package_json(self, analysis: Dict[str, Any]) -> str:
        """Generate package.json for React app."""
        dependencies = {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1"
        }
        
        if "authentication" in analysis["features"]:
            dependencies["react-router-dom"] = "^6.0.0"
            dependencies["axios"] = "^1.0.0"
        
        if "realtime" in analysis["features"]:
            dependencies["socket.io-client"] = "^4.0.0"
        
        return json.dumps({
            "name": "think-ai-react-app",
            "version": "0.1.0",
            "private": True,
            "dependencies": dependencies,
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "eslintConfig": {
                "extends": ["react-app", "react-app/jest"]
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
            }
        }, indent=2)
    
    def _generate_react_app(self, analysis: Dict[str, Any]) -> str:
        """Generate React App.js."""
        imports = ["import React, { useState, useEffect } from 'react';"]
        imports.append("import './App.css';")
        
        if "authentication" in analysis["features"]:
            imports.append("import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';")
            imports.append("import Login from './components/Login';")
            imports.append("import Register from './components/Register';")
        
        code = f'''{chr(10).join(imports)}
import Header from './components/Header';
import Footer from './components/Footer';

function App() {{
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {{
    // Fetch initial data
    fetchData();
  }}, []);

  const fetchData = async () => {{
    try {{
      const response = await fetch('/api/status');
      const result = await response.json();
      setData(result);
    }} catch (error) {{
      console.error('Error fetching data:', error);
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <div className="App">
      <Header />
      
      <main className="main-content">
        <h1>{analysis["description"]}</h1>
        
        {{loading ? (
          <p>Loading...</p>
        ) : (
          <div>
            {{data && <p>{{data.message}}</p>}}
          </div>
        )}}
'''
        
        if "authentication" in analysis["features"]:
            code += '''
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </Router>
'''
        
        code += '''      </main>
      
      <Footer />
    </div>
  );
}

export default App;'''
        
        return code
    
    def _generate_react_index(self) -> str:
        """Generate React index.js."""
        return '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);'''
    
    def _generate_react_css(self) -> str:
        """Generate React App.css."""
        return '''.App {
  text-align: center;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 2rem;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
}

.App-header h1 {
  margin: 0;
}

button {
  background-color: #61dafb;
  border: none;
  color: black;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
}

button:hover {
  background-color: #4fa8c5;
}'''
    
    def _generate_react_component(self, name: str, with_form: bool = False) -> str:
        """Generate a React component."""
        if with_form:
            jsx = '''        <div className="form-container">
            <h2>{name}</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Submit</button>
            </form>
        </div>'''
            
            state = '''const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');'''
            
            effects = '''
    const handleSubmit = (e) => {
        e.preventDefault();
        // Handle form submission
        console.log('Form submitted:', { username, password });
    };'''
        else:
            jsx = f'''        <div className="{name.lower()}">
            <h2>{{name}}</h2>
            <p>This is the {{name}} component.</p>
        </div>'''
            state = ""
            effects = ""
        
        return self.templates["react_component"].format(
            name=name,
            imports=", { useState }" if with_form else "",
            props="{ name = '" + name + "' }",
            state=state,
            effects=effects,
            jsx=jsx
        )
    
    def _generate_fastapi_app(self, analysis: Dict[str, Any]) -> str:
        """Generate FastAPI application."""
        imports = ["from fastapi import FastAPI, HTTPException, Depends"]
        imports.append("from fastapi.middleware.cors import CORSMiddleware")
        imports.append("from pydantic import BaseModel")
        imports.append("from typing import List, Optional")
        
        if "database" in analysis["features"]:
            imports.append("from database import get_db, engine")
            imports.append("from models import Base")
            imports.append("import crud")
        
        if "authentication" in analysis["features"]:
            imports.append("from auth import get_current_user, create_access_token")
            imports.append("from security import verify_password")
        
        code = f'''"""
{analysis["description"]}
FastAPI application generated by Think AI
"""

{chr(10).join(imports)}
import uvicorn

# Create app
app = FastAPI(
    title="{analysis["description"]}",
    description="API generated by Think AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
        
        if "database" in analysis["features"]:
            code += '''
# Create database tables
Base.metadata.create_all(bind=engine)
'''
        
        code += '''
# Root endpoint
@app.get("/")
def read_root():
    """Welcome endpoint."""
    return {"message": "Welcome to Think AI API!", "status": "running"}

# Health check
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now()}
'''
        
        if "database" in analysis["features"]:
            code += '''
# CRUD endpoints
@app.get("/items", response_model=List[Item])
def get_items(skip: int = 0, limit: int = 100, db = Depends(get_db)):
    """Get all items."""
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int, db = Depends(get_db)):
    """Get specific item."""
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item)
def create_item(item: ItemCreate, db = Depends(get_db)):
    """Create new item."""
    return crud.create_item(db=db, item=item)

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate, db = Depends(get_db)):
    """Update item."""
    updated_item = crud.update_item(db=db, item_id=item_id, item=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db = Depends(get_db)):
    """Delete item."""
    success = crud.delete_item(db=db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
'''
        
        if "authentication" in analysis["features"]:
            code += '''
# Authentication endpoints
@app.post("/auth/login")
def login(username: str, password: str):
    """Login endpoint."""
    # Verify user credentials
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me")
def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user info."""
    return current_user
'''
        
        code += '''
# Error handlers
@app.exception_handler(404)
def not_found(request, exc):
    """Handle 404 errors."""
    return {"error": "Not found", "message": str(exc.detail)}

@app.exception_handler(500)
def server_error(request, exc):
    """Handle 500 errors."""
    return {"error": "Server error", "message": "Internal server error"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
'''
        
        return code
    
    def _generate_pydantic_models(self, analysis: Dict[str, Any]) -> str:
        """Generate Pydantic models."""
        return '''"""
Pydantic models for API.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Base models
class ItemBase(BaseModel):
    """Base item model."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    is_active: bool = True

class ItemCreate(ItemBase):
    """Model for creating items."""
    pass

class ItemUpdate(BaseModel):
    """Model for updating items."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None

class Item(ItemBase):
    """Complete item model."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# User models
class UserBase(BaseModel):
    """Base user model."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    """Model for creating users."""
    password: str = Field(..., min_length=8)

class User(UserBase):
    """Complete user model."""
    id: int
    is_active: bool = True
    created_at: datetime
    
    class Config:
        orm_mode = True

# Response models
class MessageResponse(BaseModel):
    """Generic message response."""
    message: str

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    message: str
    details: Optional[dict] = None

class PaginatedResponse(BaseModel):
    """Paginated response model."""
    items: List[dict]
    total: int
    page: int
    per_page: int
    pages: int
'''
    
    def _generate_crud_operations(self, analysis: Dict[str, Any]) -> str:
        """Generate CRUD operations."""
        return '''"""
CRUD operations for database models.
"""

from sqlalchemy.orm import Session
from models import Item, User
from schemas import ItemCreate, ItemUpdate, UserCreate
from typing import List, Optional

# Item CRUD
def get_item(db: Session, item_id: int) -> Optional[Item]:
    """Get item by ID."""
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    """Get all items with pagination."""
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate) -> Item:
    """Create new item."""
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemUpdate) -> Optional[Item]:
    """Update existing item."""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    
    if db_item:
        update_data = item.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db.commit()
        db.refresh(db_item)
    
    return db_item

def delete_item(db: Session, item_id: int) -> bool:
    """Delete item."""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    
    return False

# User CRUD
def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create new user."""
    from security import get_password_hash
    
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()
'''
    
    def _generate_auth_api(self) -> str:
        """Generate authentication API module."""
        return '''"""
Authentication module for API.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "think-ai-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    # user = get_user_by_username(db, username=username)
    # if user is None:
    #     raise credentials_exception
    
    return {"username": username}  # Return user object in real implementation
'''
    
    def _generate_security_module(self) -> str:
        """Generate security module."""
        return '''"""
Security utilities.
"""

from passlib.context import CryptContext
import secrets
import string

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def generate_random_password(length: int = 12) -> str:
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_api_key() -> str:
    """Generate a random API key."""
    return secrets.token_urlsafe(32)

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"
'''
    
    def _generate_tests(self, analysis: Dict[str, Any]) -> str:
        """Generate tests for the application."""
        framework = analysis.get("framework", "flask")
        
        if framework == "flask":
            return self._generate_flask_tests()
        elif framework == "fastapi":
            return self._generate_fastapi_tests()
        else:
            return self._generate_generic_tests()
    
    def _generate_flask_tests(self) -> str:
        """Generate Flask tests."""
        return '''"""
Tests for Flask application.
"""

import pytest
from app import app, db
from models import User

@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_index(client):
    """Test index page."""
    response = client.get('/')
    assert response.status_code == 200

def test_api_status(client):
    """Test API status endpoint."""
    response = client.get('/api/status')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'running'
    assert 'message' in data

def test_404(client):
    """Test 404 error."""
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_user_registration(client):
    """Test user registration."""
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'password2': 'testpass123'
    })
    
    assert response.status_code in [200, 302]  # Redirect after success

def test_user_login(client):
    """Test user login."""
    # First create a user
    user = User(username='testuser', email='test@example.com')
    user.set_password('testpass123')
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
    
    # Then try to login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    assert response.status_code in [200, 302]
'''
    
    def _generate_fastapi_tests(self) -> str:
        """Generate FastAPI tests."""
        return '''"""
Tests for FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_item():
    """Test creating an item."""
    response = client.post(
        "/items",
        json={"name": "Test Item", "description": "Test", "price": 10.99}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 10.99

def test_get_items():
    """Test getting all items."""
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_nonexistent_item():
    """Test getting non-existent item."""
    response = client.get("/items/99999")
    assert response.status_code == 404

def test_update_item():
    """Test updating an item."""
    # First create an item
    create_response = client.post(
        "/items",
        json={"name": "Original", "description": "Test", "price": 10.0}
    )
    item_id = create_response.json()["id"]
    
    # Then update it
    update_response = client.put(
        f"/items/{item_id}",
        json={"name": "Updated", "price": 20.0}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated"

def test_delete_item():
    """Test deleting an item."""
    # First create an item
    create_response = client.post(
        "/items",
        json={"name": "To Delete", "description": "Test", "price": 10.0}
    )
    item_id = create_response.json()["id"]
    
    # Then delete it
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404
'''
    
    def _generate_generic_tests(self) -> str:
        """Generate generic Python tests."""
        return '''"""
Tests for the application.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import *

class TestMain(unittest.TestCase):
    """Test cases for main module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = {
            "input": "test",
            "expected": "result"
        }
    
    def test_main_function(self):
        """Test main function."""
        # Test that main function exists and runs
        result = main()
        self.assertIsNotNone(result)
    
    def test_data_processing(self):
        """Test data processing."""
        # Add specific tests based on your functions
        pass
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Test with empty input
        # Test with None
        # Test with large input
        pass
    
    def test_error_handling(self):
        """Test error handling."""
        # Test that errors are handled gracefully
        pass

if __name__ == '__main__':
    unittest.main()
'''
    
    def _generate_script_tests(self) -> str:
        """Generate tests for script."""
        return '''"""
Tests for the script.
"""

import pytest
import sys
import os
from pathlib import Path
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from script import process_file, process_directory, transform_content

def test_transform_content():
    """Test content transformation."""
    input_text = "hello world"
    result = transform_content(input_text)
    assert result == "HELLO WORLD"

def test_process_file():
    """Test file processing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_file = f.name
    
    output_file = "test_output.txt"
    
    try:
        process_file(Path(temp_file), output_file, verbose=True)
        assert os.path.exists(output_file)
        
        with open(output_file, 'r') as f:
            content = f.read()
            assert content == "TEST CONTENT"
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(output_file):
            os.remove(output_file)

def test_process_directory():
    """Test directory processing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        for i in range(3):
            with open(os.path.join(temp_dir, f"test{i}.txt"), 'w') as f:
                f.write(f"content {i}")
        
        output_file = "test_dir_output.txt"
        
        try:
            process_directory(Path(temp_dir), output_file, verbose=True)
            assert os.path.exists(output_file)
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)
'''
    
    def _generate_readme(self, analysis: Dict[str, Any]) -> str:
        """Generate README.md file."""
        features_list = "\n".join([f"- {feature.title()}" for feature in analysis["features"]])
        
        return f'''# {analysis["description"]}

This project was automatically generated by Think AI.

## Features

{features_list}
- Fully functional out of the box
- Production-ready code
- Comprehensive error handling
- Well-documented

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Running the application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Documentation

### Endpoints

- `GET /` - Home page
- `GET /api/status` - API status

## Testing

Run tests with:
```bash
pytest tests.py
```

## Deployment

This application is ready for deployment on:
- Heroku
- AWS
- Google Cloud
- Any VPS with Python support

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT

---

Generated with ❤️ by Think AI
'''
    
    def _generate_api_readme(self, analysis: Dict[str, Any]) -> str:
        """Generate README for API project."""
        return f'''# {analysis["description"]}

FastAPI application generated by Think AI.

## Features

- RESTful API with automatic documentation
- Pydantic models for data validation
- Async support
- CORS enabled
- Error handling

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`

## Documentation

- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Core Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check

### CRUD Endpoints

- `GET /items` - List all items
- `GET /items/{id}` - Get specific item
- `POST /items` - Create new item
- `PUT /items/{id}` - Update item
- `DELETE /items/{id}` - Delete item

## Testing

```bash
pytest
```

## Deployment

Ready for deployment on:
- Docker
- Kubernetes
- Heroku
- AWS Lambda

---

Generated by Think AI with 🧠 and ☕
'''
    
    def generate_code_improvements(self, code: str, language: str = "python") -> str:
        """Generate improvements for existing code."""
        improvements = []
        
        if language == "python":
            # Check for missing docstrings
            if 'def ' in code and '"""' not in code:
                improvements.append("Add docstrings to functions")
            
            # Check for type hints
            if 'def ' in code and '->' not in code:
                improvements.append("Add type hints")
            
            # Check for error handling
            if 'try:' not in code and 'except' not in code:
                improvements.append("Add error handling")
            
            # Check for logging
            if 'logging' not in code and 'logger' not in code:
                improvements.append("Add logging")
            
            # Generate improved code
            improved_code = self._add_improvements(code, improvements)
            
            return improved_code
        
        return code
    
    def _add_improvements(self, code: str, improvements: List[str]) -> str:
        """Add improvements to code."""
        improved = code
        
        if "Add docstrings" in improvements:
            # Add docstrings to functions
            improved = re.sub(
                r'def (\w+)\((.*?)\):',
                r'def \1(\2):\n    """TODO: Add docstring."""',
                improved
            )
        
        if "Add type hints" in improvements:
            # Add basic type hints
            improved = re.sub(
                r'def (\w+)\((.*?)\):',
                r'def \1(\2) -> None:',
                improved
            )
        
        if "Add error handling" in improvements:
            # Wrap main code in try-except
            lines = improved.split('\n')
            main_index = next((i for i, line in enumerate(lines) if 'if __name__' in line), -1)
            
            if main_index > 0:
                lines.insert(main_index + 1, "    try:")
                lines.append("    except Exception as e:")
                lines.append('        logger.error(f"Error: {e}")')
                lines.append("        sys.exit(1)")
                improved = '\n'.join(lines)
        
        if "Add logging" in improvements:
            # Add logging import and setup
            improved = "import logging\n\nlogger = logging.getLogger(__name__)\n\n" + improved
        
        return improved


# Example usage
async def demo_code_generator():
    """Demonstrate code generation."""
    generator = CodeGenerator()
    
    # Generate different types of applications
    descriptions = [
        "Create a web application with user authentication and database",
        "Build a REST API for managing products with CRUD operations",
        "Make a simple game where players collect coins",
        "Create a Python script that processes CSV files",
        "Build a task management system with real-time updates"
    ]
    
    for desc in descriptions:
        print(f"\n{'='*60}")
        print(f"Generating: {desc}")
        print('='*60)
        
        files = await generator.generate_from_description(desc)
        
        print(f"\nGenerated {len(files)} files:")
        for filename in sorted(files.keys()):
            print(f"  - {filename}")
        
        # Show a sample of the main file
        main_file = next((f for f in files.keys() if 'main' in f or 'app' in f), None)
        if main_file:
            print(f"\nSample from {main_file}:")
            print("-"*40)
            print(files[main_file][:500] + "...")


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_code_generator())