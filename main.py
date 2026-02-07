import os
import runpy
import sys

def main():
    repo_root = os.path.dirname(__file__)
    frontend_dir = os.path.join(repo_root, "Front-End (IVR system)")
    frontend_path = os.path.join(frontend_dir, "main.py")

    if not os.path.isfile(frontend_path):
        print(f"Error: could not find IVR entry script at {frontend_path}")
        sys.exit(1)

    # Ensure the front-end directory is first on sys.path so local imports (like `ivr`) resolve
    if frontend_dir not in sys.path:
        sys.path.insert(0, frontend_dir)

    # Change working directory to the front-end folder so relative assets/imports work
    os.chdir(frontend_dir)

    # Execute the IVR app's main.py as a script
    runpy.run_path(frontend_path, run_name="__main__")

if __name__ == "__main__":
    main()
