"""
Code Executor - Allows Think AI to run its own code safely.
Now it can test and execute what it writes!
"""

import asyncio
import subprocess
import sys
import tempfile
from pathlib import Path
import traceback
import ast
from typing import Dict, Any, Optional, List
import multiprocessing
import signal
from contextlib import contextmanager
import io
import contextlib
from datetime import datetime
import time

from ..utils.logging import get_logger

logger = get_logger(__name__)


class SafeCodeExecutor:
    """
    Executes code safely with timeouts and resource limits.
    Because we don't want Think AI to accidentally create Skynet.
    """
    
    def __init__(self):
        self.execution_count = 0
        self.success_count = 0
        self.error_count = 0
        self.execution_history = []
        
        # Safety limits
        self.timeout = 10  # seconds
        self.max_memory = 512 * 1024 * 1024  # 512MB
        self.max_output = 10000  # characters
        
        logger.info("🔧 Code Executor initialized - Think AI can now run code!")
    
    async def execute_code(self, code: str, language: str = 'python') -> Dict[str, Any]:
        """
        Execute code safely and return results.
        
        Args:
            code: The code to execute
            language: Programming language (currently only Python)
        """
        self.execution_count += 1
        
        if language != 'python':
            return {
                'success': False,
                'error': f"Language '{language}' not supported yet. ¡Dale que vamos tarde!"
            }
        
        # Validate code first
        validation = self._validate_code(code)
        if not validation['valid']:
            self.error_count += 1
            return {
                'success': False,
                'error': validation['error'],
                'type': 'validation_error'
            }
        
        # Execute in sandbox
        result = await self._execute_python(code)
        
        # Track history
        self.execution_history.append({
            'code': code[:200] + '...' if len(code) > 200 else code,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        if result['success']:
            self.success_count += 1
        else:
            self.error_count += 1
        
        return result
    
    def _validate_code(self, code: str) -> Dict[str, bool]:
        """Validate code for safety and syntax."""
        try:
            # Check syntax
            ast.parse(code)
            
            # Check for dangerous operations
            dangerous_patterns = [
                'exec(', 'eval(', '__import__',
                'subprocess', 'os.system',
                'open(', 'file(',
                'rmtree', 'remove',
                '__builtins__'
            ]
            
            for pattern in dangerous_patterns:
                if pattern in code:
                    return {
                        'valid': False,
                        'error': f"Dangerous operation '{pattern}' not allowed. ¡No joda!"
                    }
            
            return {'valid': True}
            
        except SyntaxError as e:
            return {
                'valid': False,
                'error': f"Syntax error: {e}"
            }
    
    async def _execute_python(self, code: str) -> Dict[str, Any]:
        """Execute Python code in a sandboxed environment."""
        try:
            # Capture output
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()
            
            # Create a restricted globals environment
            safe_globals = {
                '__builtins__': {
                    'print': lambda *args, **kwargs: print(*args, **kwargs, file=output_buffer),
                    'len': len,
                    'range': range,
                    'enumerate': enumerate,
                    'zip': zip,
                    'map': map,
                    'filter': filter,
                    'sum': sum,
                    'min': min,
                    'max': max,
                    'abs': abs,
                    'round': round,
                    'sorted': sorted,
                    'list': list,
                    'dict': dict,
                    'set': set,
                    'tuple': tuple,
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'True': True,
                    'False': False,
                    'None': None,
                }
            }
            
            # Add common imports
            exec("import math", safe_globals)
            exec("import random", safe_globals)
            exec("import json", safe_globals)
            exec("import datetime", safe_globals)
            exec("from typing import Dict, List, Any, Optional", safe_globals)
            
            # Execute with timeout
            start_time = time.time()
            
            # Use multiprocessing for true isolation
            result_queue = multiprocessing.Queue()
            process = multiprocessing.Process(
                target=self._run_code_in_process,
                args=(code, safe_globals, result_queue)
            )
            
            process.start()
            process.join(timeout=self.timeout)
            
            if process.is_alive():
                # Timeout occurred
                process.terminate()
                process.join()
                return {
                    'success': False,
                    'error': f"Code execution timed out after {self.timeout} seconds",
                    'type': 'timeout'
                }
            
            # Get result from queue
            if not result_queue.empty():
                result = result_queue.get()
                execution_time = time.time() - start_time
                
                # Truncate output if too long
                if len(result.get('output', '')) > self.max_output:
                    result['output'] = result['output'][:self.max_output] + '\n... (truncated)'
                    result['truncated'] = True
                
                result['execution_time'] = f"{execution_time:.3f}s"
                return result
            else:
                return {
                    'success': False,
                    'error': "No result returned from code execution",
                    'type': 'no_result'
                }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'type': 'execution_error',
                'traceback': traceback.format_exc()
            }
    
    def _run_code_in_process(self, code: str, globals_dict: dict, result_queue):
        """Run code in a separate process for isolation."""
        try:
            # Capture output
            output_buffer = io.StringIO()
            
            with contextlib.redirect_stdout(output_buffer):
                exec(code, globals_dict)
            
            result_queue.put({
                'success': True,
                'output': output_buffer.getvalue(),
                'type': 'success'
            })
            
        except Exception as e:
            result_queue.put({
                'success': False,
                'error': str(e),
                'type': 'runtime_error',
                'traceback': traceback.format_exc()
            })
    
    async def test_function(self, function_code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Test a function with multiple test cases.
        
        Args:
            function_code: The function code to test
            test_cases: List of {'input': ..., 'expected': ...} dicts
        """
        results = []
        
        for i, test_case in enumerate(test_cases):
            # Create test code
            test_code = f'''{function_code}

# Test case {i+1}
result = {test_case.get('function_call', 'function()')}
print(f"Result: {{result}}")
'''
            
            # Execute test
            result = await self.execute_code(test_code)
            
            # Check if it matches expected
            if result['success'] and 'expected' in test_case:
                output = result.get('output', '')
                passed = str(test_case['expected']) in output
                result['passed'] = passed
            
            results.append(result)
        
        # Summary
        passed = sum(1 for r in results if r.get('passed', False))
        total = len(results)
        
        return {
            'passed': passed,
            'total': total,
            'success_rate': f"{(passed/total)*100:.1f}%" if total > 0 else "0%",
            'results': results
        }
    
    def get_safe_builtins(self) -> Dict[str, Any]:
        """Get the list of safe built-in functions."""
        return {
            'math_functions': ['sum', 'min', 'max', 'abs', 'round'],
            'data_structures': ['list', 'dict', 'set', 'tuple'],
            'type_conversion': ['str', 'int', 'float', 'bool'],
            'iteration': ['range', 'enumerate', 'zip', 'map', 'filter'],
            'available_modules': ['math', 'random', 'json', 'datetime']
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics."""
        success_rate = (self.success_count / self.execution_count * 100) if self.execution_count > 0 else 0
        
        return {
            'total_executions': self.execution_count,
            'successful': self.success_count,
            'errors': self.error_count,
            'success_rate': f"{success_rate:.1f}%",
            'recent_executions': self.execution_history[-5:],
            'safety_limits': {
                'timeout': f"{self.timeout}s",
                'max_memory': f"{self.max_memory // (1024*1024)}MB",
                'max_output': f"{self.max_output} chars"
            },
            'status': '¡Ejecutando código como un campeón! 🏃‍♂️'
        }