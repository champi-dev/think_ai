#!/usr/bin/env python3
"""Enhanced CLI with TUI launch support."""

import click
import sys

from ..cli import main as cli_main
from ..core.config import Config
from .app import run_ui


@click.command()
@click.option('--config', '-c', help='Path to configuration file')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def tui(config, debug):
    """Launch the Think AI Terminal User Interface."""
    try:
        # Load configuration
        cfg = Config.from_env()
        if debug:
            cfg.debug = True
            cfg.ui.log_level = "DEBUG"
        
        # Run the TUI
        run_ui(cfg)
        
    except KeyboardInterrupt:
        click.echo("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


# Add TUI command to main CLI
cli_main.add_command(tui)