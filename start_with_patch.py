#!/usr/bin/env python3
"""Start Think AI with transformers patch."""

# Apply the patch FIRST
import transformers.models.auto.configuration_auto as config_auto

config_auto.replace_list_option_in_docstrings = lambda *args, **kwargs: lambda fn: fn

# Now start the actual application
import os

os.system("python think_ai_full.py")
