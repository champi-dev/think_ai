"""Code generation templates for Think AI."""

# Python templates
PYTHON_TEMPLATES = {
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
}

# Web templates
WEB_TEMPLATES = {
    "html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    {styles}
</head>
<body>
    {content}
    {scripts}
</body>
</html>''',
}