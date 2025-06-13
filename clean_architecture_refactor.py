"""
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set
from typing import Tuple
import ast
import os

import shutil

Clean Architecture Auto-Refactoring Tool
Automatically refactors Think AI codebase to follow clean architecture principles
"""

import ast
import os
import shutil
from pathlib import Path
from typing import Dict, List, Set,
Tuple


class CleanArchitectureRefactor:
"""Refactors codebase to clean architecture"""

    def __init__(self):
        self.base_path = Path('.')
        self.domain_entities = {}
        self.use_cases = {}
        self.repositories = {}
        self.infrastructure = {}

        def analyze_codebase(
        self) -> Dict:
"""Analyze current structure"""
            analysis = {
            'domain_logic': [],
            'use_cases': [],
            'infrastructure': [],
            'interfaces': [],
            'mixed_concerns': []
            }

            for py_file in self.base_path.rglob(
            '*.py'):
                if self._should_skip(
                py_file):
                    continue

                file_analysis = self._analyze_file(
                py_file)
                for category,
                items in file_analysis.items():
                    analysis[category].extend(
                    items)

                    return analysis

                def _should_skip(self,
                path: Path) -> bool:
"""Check if path should be skipped"""
                    skip_dirs = {
                    '.venv',
                    'venv',
                    '__pycache__',

                    'build',
                    'dist',
                    '.git',
                    'node_modules',
                    '.tox',
                    '.pytest_cache'
                    }

                    return any(
                skip in path.parts
                for skip in skip_dirs
                )

                def _analyze_file(
                self,
                filepath: Path
                ) -> Dict[str,
                List]:
"""Analyze a single file"""
                    result = {
                    'domain_logic': [],

                    'use_cases': [],

                    'infrastructure': [],

                    'interfaces': [],

                    'mixed_concerns': []
                    }

                    try:
                        with open(filepath,
                        'r') as f:
                            content = f.read(
                            )

                            tree = ast.parse(
                            content)

# Check imports
                            imports = self._extract_imports(
                            tree)

# Categorize based on content
                            has_db = any(
                            'db' in imp or
                            'sql' in imp or
                            'redis' in imp or
                            'scylla' in imp
                            for imp in imports
                            )
                            has_http = any(
                            'http' in imp or
                            'request' in imp or
                            'fastapi' in imp or
                            'flask' in imp
                            for imp in imports
                            )
                            has_model = any(
                            'model' in imp or
                            'torch' in imp or
                            'transformers' in imp
                            for imp in imports
                            )

# Count different concerns
                            concerns = 0
                            if has_db:
                                concerns += 1
                                if has_http:
                                    concerns += 1
                                    if has_model:
                                        concerns += 1

# Categorize
                                        if concerns > 1:
                                            result['mixed_concerns'].append({
                                            'file': str(filepath),

                                            'concerns': {
                                            'database': has_db,

                                            'http': has_http,

                                            'ml_model': has_model
                                            }
                                            })
                                        elif has_db or
                                        has_http:
                                            result['infrastructure'].append(
                                            str(
                                            filepath)
                                            )
                                        elif self._is_use_case(
                                        tree):
                                            result['use_cases'].append(
                                            str(
                                            filepath)
                                            )
                                        elif self._is_domain_entity(
                                        tree):
                                            result['domain_logic'].append(
                                            str(
                                            filepath)
                                            )

                                            except Exception as e:
                                                print(
                                                f"Error analyzing {filepath}: {e}")

                                                return result

                                            def _extract_imports(
                                            self,

                                            tree: ast.AST
                                            ) -> Set[str]:
"""Extract all imports from AST"""
                                                imports = set(
                                                )

                                                for node in ast.walk(
                                                tree):
                                                    if isinstance(node,
                                                    ast.Import):
                                                        for alias in node.names:
                                                            imports.add(
                                                            alias.name)
                                                        elif isinstance(node,
                                                        ast.ImportFrom):
                                                            if node.module:
                                                                imports.add(
                                                                node.module)

                                                                return imports

                                                            def _is_use_case(self,
                                                            tree: ast.AST) -> bool:
"""Check if file contains use cases"""
                                                                for node in ast.walk(
                                                                tree):
                                                                    if isinstance(node,
                                                                    ast.ClassDef):
# Look
# for
# use
# case
# patterns
                                                                        if any(
                                                                        pattern in node.name.lower(
                                                                        )
                                                                        for pattern in [
                                                                        'usecase',
                                                                        'service',

                                                                        'handler',
                                                                        'processor'
                                                                        ]
                                                                        ):
                                                                            return True
                                                                        return False

                                                                    def _is_domain_entity(
                                                                    self,

                                                                    tree: ast.AST
                                                                    ) -> bool:
"""Check if file contains domain entities"""
                                                                        for node in ast.walk(
                                                                        tree):
                                                                            if isinstance(node,
                                                                            ast.ClassDef):
# Look
# for
# entity
# patterns
                                                                                if any(
                                                                                pattern in node.name.lower(
                                                                                )
                                                                                for pattern in [
                                                                                'entity',
                                                                                'model',

                                                                                'domain',
                                                                                'value'
                                                                                ]
                                                                                ):
                                                                                    return True
                                                                                return False

                                                                            def create_clean_structure(
                                                                            self):
"""Create clean architecture directories"""
                                                                                structure = {
                                                                                'domain': [
                                                                                'entities',

                                                                                'value_objects',

                                                                                'exceptions',

                                                                                'interfaces'
                                                                                ],
                                                                                'application': [
                                                                                'use_cases',

                                                                                'dto',

                                                                                'interfaces'
                                                                                ],
                                                                                'infrastructure': [
                                                                                'persistence',

                                                                                'external_services',

                                                                                'web',

                                                                                'ml_models'
                                                                                ],
                                                                                'presentation': [
                                                                                'api',

                                                                                'cli',

                                                                                'web'
                                                                                ]
                                                                                }

                                                                                for layer,
                                                                                subdirs in structure.items():
                                                                                    layer_path = self.base_path / layer
                                                                                    layer_path.mkdir(
                                                                                    exist_ok=True)

# Create
# __init__.py
                                                                                    (
                                                                                    layer_path / '__init__.py').touch()

                                                                                    for subdir in subdirs:
                                                                                        subdir_path = layer_path / subdir
                                                                                        subdir_path.mkdir(
                                                                                        exist_ok=True)
                                                                                        (
                                                                                        subdir_path / '__init__.py').touch()

                                                                                        def refactor_file(
                                                                                        self,

                                                                                        filepath: Path,

                                                                                        target_layer: str
                                                                                        ):
"""Refactor a file to clean architecture"""
                                                                                            with open(filepath,
                                                                                            'r') as f:
                                                                                                content = f.read(
                                                                                                )

                                                                                                tree = ast.parse(
                                                                                                content)

# Extract
# different
# concerns
                                                                                                domain_classes = []
                                                                                                use_case_classes = []
                                                                                                infra_classes = []

                                                                                                for node in ast.walk(
                                                                                                tree):
                                                                                                    if isinstance(node,
                                                                                                    ast.ClassDef):
                                                                                                        class_type = self._classify_class(
                                                                                                        node)

                                                                                                        if class_type == 'domain':
                                                                                                            domain_classes.append(
                                                                                                            node)
                                                                                                        elif class_type == 'use_case':
                                                                                                            use_case_classes.append(
                                                                                                            node)
                                                                                                        elif class_type == 'infrastructure':
                                                                                                            infra_classes.append(
                                                                                                            node)

# Generate
# refactored
# files
                                                                                                            if domain_classes:
                                                                                                                self._create_domain_file(
                                                                                                                filepath.stem,

                                                                                                                domain_classes
                                                                                                                )

                                                                                                                if use_case_classes:
                                                                                                                    self._create_use_case_file(
                                                                                                                    filepath.stem,

                                                                                                                    use_case_classes
                                                                                                                    )

                                                                                                                    if infra_classes:
                                                                                                                        self._create_infra_file(
                                                                                                                        filepath.stem,

                                                                                                                        infra_classes
                                                                                                                        )

                                                                                                                        def _classify_class(
                                                                                                                        self,

                                                                                                                        node: ast.ClassDef
                                                                                                                        ) -> str:
"""Classify a class node"""
# Check
# methods
# for
# infrastructure
# concerns
                                                                                                                            for item in node.body:
                                                                                                                                if isinstance(item,
                                                                                                                                ast.FunctionDef):
# Check
# for
# DB
# operations
                                                                                                                                    if any(
                                                                                                                                    keyword in item.name
                                                                                                                                    for keyword in [
                                                                                                                                    'save',
                                                                                                                                    'load',
                                                                                                                                    'query',

                                                                                                                                    'fetch',
                                                                                                                                    'persist'
                                                                                                                                    ]
                                                                                                                                    ):
                                                                                                                                        return 'infrastructure'

# Check
# for
# use
# case
# patterns
                                                                                                                                    if any(
                                                                                                                                    keyword in item.name
                                                                                                                                    for keyword in [
                                                                                                                                    'execute',
                                                                                                                                    'handle',

                                                                                                                                    'process',
                                                                                                                                    'run'
                                                                                                                                    ]
                                                                                                                                    ):
                                                                                                                                        return 'use_case'

# Default
# to
# domain
                                                                                                                                    return 'domain'

                                                                                                                                def _create_domain_file(
                                                                                                                                self,

                                                                                                                                original_name: str,

                                                                                                                                classes: List[
                                                                                                                                ast.ClassDef]
                                                                                                                                ):
"""Create domain entity file"""
                                                                                                                                    filepath = (
                                                                                                                                    self.base_path /
                                                                                                                                    'domain' /
                                                                                                                                    'entities' /
                                                                                                                                    f'{original_name}_entity.py'
                                                                                                                                    )

                                                                                                                                    content = '''"""
                                                                                                                                    Domain entities for {name}
                                                                                                                                    Pure business logic with no external dependencies
"""

from dataclasses import dataclass
from typing import Optional

'''.format(
                                                                                                                                    name=original_name)

# Add
# classes
                                                                                                                                    for cls in classes:
                                                                                                                                        content += ast.unparse(
                                                                                                                                        cls) + '\n\n'

                                                                                                                                        with open(filepath,
                                                                                                                                        'w') as f:
                                                                                                                                            f.write(
                                                                                                                                            content)

                                                                                                                                            def _create_use_case_file(
                                                                                                                                            self,

                                                                                                                                            original_name: str,

                                                                                                                                            classes: List[
                                                                                                                                            ast.ClassDef]
                                                                                                                                            ):
"""Create use case file"""
                                                                                                                                                filepath = (
                                                                                                                                                self.base_path /
                                                                                                                                                'application' /
                                                                                                                                                'use_cases' /
                                                                                                                                                f'{original_name}_use_case.py'
                                                                                                                                                )

                                                                                                                                                content = '''"""
                                                                                                                                                Use cases for {name}
                                                                                                                                                Application business logic
"""

from typing import Protocol

'''.format(
                                                                                                                                                name=original_name)

# Add
# classes
                                                                                                                                                for cls in classes:
                                                                                                                                                    content += ast.unparse(
                                                                                                                                                    cls) + '\n\n'

                                                                                                                                                    with open(filepath,
                                                                                                                                                    'w') as f:
                                                                                                                                                        f.write(
                                                                                                                                                        content)

                                                                                                                                                        def _create_infra_file(
                                                                                                                                                        self,

                                                                                                                                                        original_name: str,

                                                                                                                                                        classes: List[
                                                                                                                                                        ast.ClassDef]
                                                                                                                                                        ):
"""Create infrastructure file"""
                                                                                                                                                            filepath = (
                                                                                                                                                            self.base_path /
                                                                                                                                                            'infrastructure' /
                                                                                                                                                            'persistence' /
                                                                                                                                                            f'{original_name}_repository.py'
                                                                                                                                                            )

                                                                                                                                                            content = '''"""
                                                                                                                                                            Infrastructure implementation for {name}
                                                                                                                                                            Handles external dependencies
"""

from typing import List,
                                                                                                                                                            Optional

'''.format(
                                                                                                                                                            name=original_name)

# Add
# classes
                                                                                                                                                            for cls in classes:
                                                                                                                                                                content += ast.unparse(
                                                                                                                                                                cls) + '\n\n'

                                                                                                                                                                with open(filepath,
                                                                                                                                                                'w') as f:
                                                                                                                                                                    f.write(
                                                                                                                                                                    content)

                                                                                                                                                                    def generate_report(
                                                                                                                                                                    self,

                                                                                                                                                                    analysis: Dict
                                                                                                                                                                    ) -> str:
"""Generate refactoring report"""
                                                                                                                                                                        report = """
                                                                                                                                                                        Clean Architecture Refactoring Report
                                                                                                                                                                        ====================================

                                                                                                                                                                        Current Structure Analysis:
                                                                                                                                                                            --------------------------
"""

                                                                                                                                                                            for category,
                                                                                                                                                                            items in analysis.items():
                                                                                                                                                                                report += f"\n{category}: {len(
                                                                                                                                                                                items)} files\n"

                                                                                                                                                                                if category == 'mixed_concerns':
# First
# 5
                                                                                                                                                                                    for item in items[
                                                                                                                                                                                    : 5]:
                                                                                                                                                                                        report += f"  - {
                                                                                                                                                                                        item['file']}\n"
                                                                                                                                                                                        for concern,
                                                                                                                                                                                        has in item['concerns'].items():
                                                                                                                                                                                            if has:
                                                                                                                                                                                                report += f"    * {concern}\n"
                                                                                                                                                                                            else:
# First
# 5
                                                                                                                                                                                                for item in items[
                                                                                                                                                                                                : 5]:
                                                                                                                                                                                                    report += f"  - {item}\n"

                                                                                                                                                                                                    if len(
                                                                                                                                                                                                    items) > 5:
                                                                                                                                                                                                        report += f"  ... and
                                                                                                                                                                                                        {len(items) - 5} more\n"

                                                                                                                                                                                                        report += """
                                                                                                                                                                                                        Recommended Actions:
                                                                                                                                                                                                            -------------------
                                                                                                                                                                                                            1. Separate mixed concerns into layers
                                                                                                                                                                                                            2. Extract domain entities
                                                                                                                                                                                                            3. Create repository interfaces
                                                                                                                                                                                                            4. Implement use cases
                                                                                                                                                                                                            5. Move infrastructure to adapters
"""

                                                                                                                                                                                                            return report

                                                                                                                                                                                                        def main():
"""Run the refactoring tool"""
                                                                                                                                                                                                            refactor = CleanArchitectureRefactor(
                                                                                                                                                                                                            )

                                                                                                                                                                                                            print("🔍 Analyzing codebase...")
                                                                                                                                                                                                            analysis = refactor.analyze_codebase(
                                                                                                                                                                                                            )

                                                                                                                                                                                                            print(
                                                                                                                                                                                                            "📁 Creating clean architecture structure...")
                                                                                                                                                                                                            refactor.create_clean_structure()

                                                                                                                                                                                                            print("📝 Generating report...")
                                                                                                                                                                                                            report = refactor.generate_report(
                                                                                                                                                                                                            analysis)

                                                                                                                                                                                                            with open('clean_architecture_report.txt',
                                                                                                                                                                                                            'w') as f:
                                                                                                                                                                                                                f.write(report)

                                                                                                                                                                                                                print(report)
                                                                                                                                                                                                                print(
                                                                                                                                                                                                                "\n✅ Report saved to clean_architecture_report.txt")
                                                                                                                                                                                                                print(
                                                                                                                                                                                                                "🚀 Ready to refactor files!")

                                                                                                                                                                                                                if __name__ == '__main__':
                                                                                                                                                                                                                    main()
