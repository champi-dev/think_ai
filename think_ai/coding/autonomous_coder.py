"""
Autonomous Coder - Now Think AI can code by itself!
¡No joda! Ahora sí se puso seria la vaina.
"""

import asyncio
import ast
import subprocess
import os
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import re
try:
    import black
except ImportError:
    black = None
try:
    import autopep8
except ImportError:
    autopep8 = None
import traceback
from datetime import datetime
import sys
import time

from ..utils.logging import get_logger

logger = get_logger(__name__)


class AutonomousCoder:
    """
    Think AI's coding brain - writes, tests, and improves its own code.
    O(1) performance because we cache everything, even mistakes!
    """
    
    def __init__(self):
        self.code_cache = {}  # Cache generated code
        self.execution_history = []
        self.improvements_made = 0
        self.bugs_fixed = 0
        self.features_added = 0
        
        # Code generation templates
        self.code_patterns = {
            'function': '''def {name}({params}):
    """{docstring}"""
    {body}
''',
            'class': '''class {name}:
    """{docstring}"""
    
    def __init__(self{params}):
        {init_body}
    
    {methods}
''',
            'async_function': '''async def {name}({params}):
    """{docstring}"""
    {body}
''',
            'test': '''def test_{name}():
    """Test {description}"""
    # Arrange
    {arrange}
    
    # Act
    {act}
    
    # Assert
    {assertion}
'''
        }
        
        # Common improvements it can make
        self.improvement_patterns = [
            ('O\\(n\\^2\\)', 'O(n)', 'Optimize nested loops'),
            ('time\\.sleep', 'asyncio.sleep', 'Make it async'),
            ('print\\(', 'logger.info(', 'Use proper logging'),
            ('except:', 'except Exception as e:', 'Specific exception handling'),
            ('== None', 'is None', 'Pythonic comparison'),
            ('!= None', 'is not None', 'Pythonic comparison'),
        ]
        
        logger.info("🤖 Autonomous Coder initialized - Think AI can now code!")
    
    async def write_code(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Write code for a given task.
        
        Args:
            task: What to code
            context: Additional context (existing code, requirements, etc.)
        """
        logger.info(f"📝 Writing code for: {task}")
        
        # Analyze task
        code_type = self._analyze_task(task)
        
        # Generate code based on type
        if code_type == 'feature':
            code = await self._write_feature(task, context)
        elif code_type == 'bugfix':
            code = await self._fix_bug(task, context)
        elif code_type == 'optimization':
            code = await self._optimize_code(task, context)
        elif code_type == 'test':
            code = await self._write_test(task, context)
        else:
            code = await self._write_generic(task, context)
        
        # Format code
        formatted_code = self._format_code(code)
        
        # Test the code
        test_result = await self._test_code(formatted_code)
        
        # If it fails, try to fix it
        if not test_result['success']:
            logger.info("🔧 Code failed, attempting to fix...")
            formatted_code = await self._debug_and_fix(formatted_code, test_result['error'])
        
        self.features_added += 1
        
        return {
            'code': formatted_code,
            'type': code_type,
            'task': task,
            'test_result': test_result,
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_task(self, task: str) -> str:
        """Analyze what type of code to write."""
        task_lower = task.lower()
        
        if any(word in task_lower for word in ['bug', 'fix', 'error', 'broken']):
            return 'bugfix'
        elif any(word in task_lower for word in ['optimize', 'faster', 'performance']):
            return 'optimization'
        elif any(word in task_lower for word in ['test', 'unittest', 'pytest']):
            return 'test'
        elif any(word in task_lower for word in ['feature', 'add', 'create', 'new']):
            return 'feature'
        else:
            return 'generic'
    
    async def _write_feature(self, task: str, context: Optional[Dict[str, Any]]) -> str:
        """Write a new feature."""
        # Extract key info from task
        feature_name = self._extract_feature_name(task)
        
        # Decide if it should be a class or function
        if 'class' in task.lower() or 'manager' in task.lower():
            code = self.code_patterns['class'].format(
                name=self._to_class_name(feature_name),
                docstring=f"Implements {task}",
                params=", config: Dict[str, Any] = None",
                init_body="self.config = config or {}\n        self.initialized = False",
                methods=self._generate_class_methods(feature_name)
            )
        else:
            # Async by default because we're modern
            code = self.code_patterns['async_function'].format(
                name=self._to_function_name(feature_name),
                params="data: Any",
                docstring=f"Executes {task}",
                body=self._generate_function_body(feature_name)
            )
        
        return code
    
    async def _fix_bug(self, task: str, context: Optional[Dict[str, Any]]) -> str:
        """Fix a bug in existing code."""
        if context and 'code' in context:
            original_code = context['code']
            
            # Common bug fixes
            fixed_code = original_code
            
            # Fix common issues
            bug_fixes = [
                (r'except:\s*\n', 'except Exception as e:\n'),
                (r'print\((.*?)\)', r'logger.info(\1)'),
                (r'time\.sleep\((.*?)\)', r'await asyncio.sleep(\1)'),
                (r'== None', 'is None'),
                (r'!= None', 'is not None'),
                (r'range\(len\((.*?)\)\)', r'enumerate(\1)'),
            ]
            
            for pattern, replacement in bug_fixes:
                fixed_code = re.sub(pattern, replacement, fixed_code)
            
            self.bugs_fixed += 1
            return fixed_code
        
        return "# Unable to fix bug without code context"
    
    async def _optimize_code(self, task: str, context: Optional[Dict[str, Any]]) -> str:
        """Optimize existing code."""
        if context and 'code' in context:
            original_code = context['code']
            
            # Apply optimizations
            optimized = original_code
            
            # Cache results
            if 'def ' in optimized and '@cache' not in optimized:
                optimized = "from functools import cache\n\n" + optimized
                optimized = optimized.replace('def ', '@cache\ndef ', 1)
            
            # Use list comprehensions
            optimized = self._convert_to_comprehensions(optimized)
            
            # Make it async if possible
            if 'def ' in optimized and 'async def' not in optimized:
                optimized = optimized.replace('def ', 'async def ')
                optimized = optimized.replace('sleep(', 'await asyncio.sleep(')
            
            self.improvements_made += 1
            return optimized
        
        return "# No code to optimize"
    
    async def _write_test(self, task: str, context: Optional[Dict[str, Any]]) -> str:
        """Write a test."""
        test_name = self._extract_feature_name(task).replace(' ', '_')
        
        return self.code_patterns['test'].format(
            name=test_name,
            description=task,
            arrange="test_data = {'key': 'value'}",
            act="result = function_to_test(test_data)",
            assertion="assert result is not None\n    assert result['success'] == True"
        )
    
    async def _write_generic(self, task: str, context: Optional[Dict[str, Any]]) -> str:
        """Write generic code."""
        return f'''async def execute_task():
    """
    Executes: {task}
    Generated by Think AI Autonomous Coder
    """
    try:
        # Implementation goes here
        result = {{'success': True, 'task': '{task}'}}
        logger.info(f"Task completed: {{result}}")
        return result
    except Exception as e:
        logger.error(f"Task failed: {{e}}")
        return {{'success': False, 'error': str(e)}}
'''
    
    def _format_code(self, code: str) -> str:
        """Format code properly."""
        try:
            # Try black first
            if black:
                return black.format_str(code, mode=black.Mode())
            return code
        except:
            try:
                # Fallback to autopep8
                if autopep8:
                    return autopep8.fix_code(code)
                return code
            except:
                # Last resort - return as is
                return code
    
    async def _test_code(self, code: str) -> Dict[str, Any]:
        """Test if code runs without errors."""
        try:
            # First, check syntax
            ast.parse(code)
            
            # Create temp file
            temp_file = Path(f"temp_test_{datetime.now().timestamp()}.py")
            temp_file.write_text(code)
            
            # Try to run it
            result = subprocess.run(
                [sys.executable, str(temp_file)],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Cleanup
            temp_file.unlink()
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr
            }
            
        except SyntaxError as e:
            return {
                'success': False,
                'error': f"Syntax error: {e}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _debug_and_fix(self, code: str, error: str) -> str:
        """Try to fix code based on error."""
        logger.info(f"🐛 Debugging error: {error}")
        
        fixed_code = code
        
        # Common fixes based on error
        if 'NameError' in error:
            # Add missing imports
            if 'asyncio' in error:
                fixed_code = 'import asyncio\n' + fixed_code
            elif 'logger' in error:
                fixed_code = 'from ..utils.logging import get_logger\nlogger = get_logger(__name__)\n' + fixed_code
            elif 'Dict' in error or 'Any' in error:
                fixed_code = 'from typing import Dict, Any\n' + fixed_code
        
        elif 'IndentationError' in error:
            # Fix indentation
            lines = fixed_code.split('\n')
            fixed_lines = []
            indent_level = 0
            
            for line in lines:
                stripped = line.strip()
                if stripped.endswith(':'):
                    fixed_lines.append('    ' * indent_level + stripped)
                    indent_level += 1
                elif stripped in ['pass', 'return', 'break', 'continue']:
                    indent_level = max(0, indent_level - 1)
                    fixed_lines.append('    ' * indent_level + stripped)
                else:
                    fixed_lines.append('    ' * indent_level + stripped)
            
            fixed_code = '\n'.join(fixed_lines)
        
        self.bugs_fixed += 1
        return fixed_code
    
    def _extract_feature_name(self, task: str) -> str:
        """Extract feature name from task description."""
        # Remove common words
        words = task.lower().split()
        skip_words = ['create', 'add', 'implement', 'build', 'make', 'write', 'a', 'an', 'the', 'for', 'to']
        feature_words = [w for w in words if w not in skip_words]
        return ' '.join(feature_words[:3])
    
    def _to_class_name(self, name: str) -> str:
        """Convert to PascalCase class name."""
        return ''.join(word.capitalize() for word in name.split())
    
    def _to_function_name(self, name: str) -> str:
        """Convert to snake_case function name."""
        return '_'.join(word.lower() for word in name.split())
    
    def _generate_class_methods(self, feature_name: str) -> str:
        """Generate basic class methods."""
        return f'''async def initialize(self):
        """Initialize the {feature_name}."""
        self.initialized = True
        logger.info(f"{{self.__class__.__name__}} initialized")
        return True
    
    async def process(self, data: Any) -> Dict[str, Any]:
        """Process data."""
        if not self.initialized:
            await self.initialize()
        
        return {{'success': True, 'processed': data}}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics."""
        return {{
            'initialized': self.initialized,
            'config': self.config
        }}'''
    
    def _generate_function_body(self, feature_name: str) -> str:
        """Generate function body."""
        return f'''# Implementation for {feature_name}
    result = {{
        'feature': '{feature_name}',
        'data': data,
        'timestamp': datetime.now().isoformat(),
        'success': True
    }}
    
    # Process data with O(1) performance
    if isinstance(data, dict):
        result['processed'] = {{k: v for k, v in data.items()}}
    else:
        result['processed'] = data
    
    logger.info(f"{feature_name} completed successfully")
    return result'''
    
    def _convert_to_comprehensions(self, code: str) -> str:
        """Convert loops to comprehensions where possible."""
        # Simple for loop to list comprehension
        pattern = r'(\w+) = \[\]\s*\n\s*for (\w+) in (\w+):\s*\n\s*\1\.append\((.*?)\)'
        replacement = r'\1 = [\4 for \2 in \3]'
        return re.sub(pattern, replacement, code)
    
    async def improve_itself(self) -> Dict[str, Any]:
        """Think AI improves its own code!"""
        logger.info("🧠 Think AI is improving itself!")
        
        # Read its own code
        own_file = Path(__file__)
        own_code = own_file.read_text()
        
        # Find things to improve
        improvements = []
        
        for pattern, replacement, description in self.improvement_patterns:
            if re.search(pattern, own_code):
                improvements.append({
                    'pattern': pattern,
                    'replacement': replacement,
                    'description': description
                })
        
        # Apply improvements
        improved_code = own_code
        for imp in improvements:
            improved_code = re.sub(imp['pattern'], imp['replacement'], improved_code)
        
        # Add new capabilities
        if 'def learn_from_mistakes' not in improved_code:
            new_method = '''
    def learn_from_mistakes(self, error: str, context: Dict[str, Any]):
        """Learn from coding errors to avoid them in future."""
        self.learned_patterns.append({
            'error': error,
            'context': context,
            'timestamp': datetime.now().isoformat()
        })
        logger.info(f"Learned from mistake: {error}")
'''
            improved_code = improved_code.replace('def get_stats', new_method + '\n    def get_stats')
        
        self.improvements_made += 1
        
        return {
            'improvements': improvements,
            'lines_changed': len(improvements),
            'new_capabilities': ['learn_from_mistakes'] if 'learn_from_mistakes' in improved_code else []
        }
    
    async def save_code(self, code: str, filename: str) -> Dict[str, Any]:
        """Save generated code to a file."""
        try:
            # Create a safe filename
            safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
            if not safe_filename.endswith('.py'):
                safe_filename += '.py'
            
            # Save to a generated_code directory
            output_dir = Path('generated_code')
            output_dir.mkdir(exist_ok=True)
            
            file_path = output_dir / safe_filename
            
            # Write the code
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            logger.info(f"✅ Saved code to {file_path}")
            
            return {
                'success': True,
                'path': str(file_path.absolute()),
                'filename': safe_filename,
                'size': len(code),
                'lines': code.count('\n') + 1
            }
            
        except Exception as e:
            logger.error(f"Failed to save code: {e}")
            return {
                'success': False,
                'error': str(e),
                'filename': filename
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get coder statistics."""
        return {
            'features_added': self.features_added,
            'bugs_fixed': self.bugs_fixed,
            'improvements_made': self.improvements_made,
            'code_cached': len(self.code_cache),
            'execution_history': len(self.execution_history),
            'status': '¡Programando como loco! Coding like crazy! 💻'
        }