import importlib
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv


def load_config(pipeline_name: str) -> dict:
    """Load configuration from YAML file based on pipeline name."""
    config_path = Path(__file__).parent / "configs" / f"{pipeline_name}.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path) as f:
        return yaml.safe_load(f)


def main():
    # Load .env variables
    load_dotenv()

    pipeline_name = os.getenv("PIPELINE", "default")
    env = os.getenv("ENV", "dev")

    try:
        # Ensure current dir is in the path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # Load pipeline configuration
        config = load_config(pipeline_name)
        print(f"Loaded configuration for pipeline '{pipeline_name}'")

        # Dynamically import the pipeline module
        pipeline_module = importlib.import_module(pipeline_name)

        # Run the pipeline using its `run()` function
        if hasattr(pipeline_module, "run") and callable(pipeline_module.run):
            print(f"Running pipeline '{pipeline_name}' in environment '{env}'")
            pipeline_module.run(config=config, env=env)
        else:
            raise AttributeError(
                f"Module '{pipeline_name}' does not have a callable 'run(config=..., env=...)' function.",
            )

    except ModuleNotFoundError as e:
        print(f"Pipeline module '{pipeline_name}' not found: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    # except Exception as e:
    #    print(f"Error while running pipeline '{pipeline_name}': {e}")
    #    sys.exit(1)


if __name__ == "__main__":
    main()
