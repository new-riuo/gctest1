import os
import sys
import venv
import traceback

def create_virtual_environment(env_dir):
    try:
        print(f"Creating virtual environment in {env_dir}")
        builder = venv.EnvBuilder(with_pip=True)
        builder.create(env_dir)
        print("Virtual environment created successfully!")
        return True
    except Exception as e:
        print(f"Failed to create virtual environment: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    env_dir = os.path.join(os.getcwd(), ".venv")
    create_virtual_environment(env_dir)