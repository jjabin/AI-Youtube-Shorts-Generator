import os

project_dir = os.getcwd()
env_path = os.path.join(project_dir, '.env')
print(f"Looking for .env file at: {env_path}")
print(f"File exists: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        content = f.read()
        print("\nContent of .env file:")
        print(content)
