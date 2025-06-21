import os
import sys
from pathlib import Path

from think_ai.cli import main

"""Start Think AI in local mode without external dependencies.
This mode uses SQLite for storage and runs without Neo4j, Redis, etc.
"""

import os
import sys
from pathlib import Path

from think_ai.cli import main

# Set environment variable for local mode
os.environ["THINK_AI_MODE"] = "local"
os.environ["THINK_AI_CONFIG"] = "config / local_only_config.yaml"

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    # Run the CLI in local mode
    sys.argv.extend(["--mode", "local"])
    main()
