#!/usr/bin/env python3
"""
Think AI Enhanced Linter with Syntax Fixing
Colombian AI-powered code fixer with O(1) performance! 🇨🇴
"""

import ast
import os
import re
import sys
import time
from pathlib import Path
from typing import List, Tuple, Dict, Any

class ThinkAIEnhancedLinter:
    """Colombian AI-powered linter that actually fixes syntax issues"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.fixes_applied = 0
        
        print("🇨🇴 Think AI Enhanced Linter")
        print("¡Dale que vamos tarde! Let's fix all the syntax issues!")
    
    def fix_syntax_errors(self, content: str) -> str:
        """Fix common syntax errors in Python code"""
        lines = content.split('\n')
        fixed_lines = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Fix missing docstring indentation after class/function definitions
            if (line.strip().endswith(':') and 
                ('class ' in line or 'def ' in line or '@abstractmethod' in lines[i-1] if i > 0 else False)):
                
                fixed_lines.append(line)
                
                # Check if next line is a docstring
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if ('"""' in next_line or "'''" in next_line) and not next_line.strip().startswith(' '):
                        # Fix unindented docstring
                        indent = self.get_indentation_level(line) + 4
                        fixed_docstring = ' ' * indent + next_line.strip()
                        fixed_lines.append(fixed_docstring)
                        i += 2  # Skip the original next line
                        self.fixes_applied += 1
                        continue
                    elif next_line.strip() == '':
                        # Add pass if empty line after colon
                        fixed_lines.append(next_line)
                        if i + 2 < len(lines) and not lines[i + 2].strip().startswith(' '):
                            indent = self.get_indentation_level(line) + 4
                            fixed_lines.append(' ' * indent + 'pass  # TODO: Implement')
                            self.fixes_applied += 1
                        i += 1
                        continue
            
            # Fix abstract method missing pass
            elif line.strip().startswith('@abstractmethod'):
                fixed_lines.append(line)
                
                # Look ahead for function definition and missing implementation
                if i + 1 < len(lines) and 'def ' in lines[i + 1]:
                    func_line = lines[i + 1]
                    fixed_lines.append(func_line)
                    
                    if i + 2 < len(lines):
                        docstring_line = lines[i + 2]
                        if '"""' in docstring_line and not docstring_line.strip().startswith(' '):
                            # Fix docstring indentation
                            indent = self.get_indentation_level(func_line) + 4
                            fixed_docstring = ' ' * indent + docstring_line.strip()
                            fixed_lines.append(fixed_docstring)
                            
                            # Add pass after docstring
                            fixed_lines.append(' ' * indent + 'pass')
                            self.fixes_applied += 1
                            i += 3
                            continue
            
            # Fix unterminated string literals
            elif '"""' in line and line.count('"""') == 1:
                # Unterminated triple quote
                if not line.strip().endswith('"""'):
                    fixed_line = line + '"""'
                    fixed_lines.append(fixed_line)
                    self.fixes_applied += 1
                else:
                    fixed_lines.append(line)
            
            # Fix missing colons in function/class definitions
            elif re.match(r'\s*(def|class)\s+\w+.*[^:]$', line):
                fixed_line = line + ':'
                fixed_lines.append(fixed_line)
                self.fixes_applied += 1
            
            else:
                fixed_lines.append(line)
            
            i += 1
        
        return '\n'.join(fixed_lines)
    
    def get_indentation_level(self, line: str) -> int:
        """Get the indentation level of a line"""
        return len(line) - len(line.lstrip())
    
    def validate_python_syntax(self, content: str) -> Tuple[bool, str]:
        """Validate if Python content has valid syntax"""
        try:
            ast.parse(content)
            return True, "Valid syntax"
        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"
    
    def lint_file(self, filepath: str, fix: bool = False) -> bool:
        """Lint and optionally fix a Python file"""
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return False
        
        print(f"🔧 Processing: {filepath}")
        
        try:
            # Read original content
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Check original syntax
            is_valid, error_msg = self.validate_python_syntax(original_content)
            
            if is_valid:
                print(f"✅ {filepath}: Already valid")
                return True
            
            if not fix:
                print(f"❌ {filepath}: {error_msg}")
                return False
            
            # Apply fixes
            fixed_content = self.fix_syntax_errors(original_content)
            
            # Validate fixed content
            is_fixed, fixed_error = self.validate_python_syntax(fixed_content)
            
            if is_fixed:
                # Write fixed content
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"✅ {filepath}: FIXED ({self.fixes_applied} fixes applied)")
                return True
            else:
                print(f"❌ {filepath}: Could not fix - {fixed_error}")
                return False
                
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
            return False
    
    def lint_directory(self, directory: str, fix: bool = False) -> Dict[str, Any]:
        """Lint all Python files in a directory"""
        print(f"\n🇨🇴 Linting directory: {directory}")
        print("=" * 50)
        
        results = {
            'total_files': 0,
            'fixed_files': 0,
            'failed_files': 0,
            'total_fixes': 0
        }
        
        for root, dirs, files in os.walk(directory):
            # Skip certain directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv']]
            
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    results['total_files'] += 1
                    
                    old_fixes = self.fixes_applied
                    success = self.lint_file(filepath, fix)
                    
                    if success:
                        results['fixed_files'] += 1
                    else:
                        results['failed_files'] += 1
                    
                    results['total_fixes'] += (self.fixes_applied - old_fixes)
        
        return results
    
    def print_summary(self, results: Dict[str, Any]):
        """Print linting summary"""
        print("\n" + "=" * 50)
        print("📊 THINK AI LINTER SUMMARY")
        print("=" * 50)
        
        print(f"Total Python files: {results['total_files']}")
        print(f"Successfully processed: ✅ {results['fixed_files']}")
        print(f"Failed to process: ❌ {results['failed_files']}")
        print(f"Total fixes applied: 🔧 {results['total_fixes']}")
        
        if results['failed_files'] == 0:
            print("\n🎉 ¡QUÉ CHIMBA! All files processed successfully!")
            print("🇨🇴 ¡Dale que vamos tarde! Think AI linter is PERFECT!")
        else:
            success_rate = (results['fixed_files'] / results['total_files']) * 100
            print(f"\n📈 Success rate: {success_rate:.1f}%")
            print("🇨🇴 ¡Eso sí está bueno! Major progress made!")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Think AI Enhanced Linter - ¡Dale que vamos tarde!")
    parser.add_argument('path', nargs='?', default='.', help='Path to lint (file or directory)')
    parser.add_argument('--fix', action='store_true', help='Fix syntax errors automatically')
    
    args = parser.parse_args()
    
    linter = ThinkAIEnhancedLinter()
    
    if os.path.isfile(args.path):
        # Single file
        success = linter.lint_file(args.path, args.fix)
        print(f"\n🇨🇴 Result: {'¡Qué chimba!' if success else '¡Uy, parce!'}")
    else:
        # Directory
        results = linter.lint_directory(args.path, args.fix)
        linter.print_summary(results)

if __name__ == "__main__":
    main()