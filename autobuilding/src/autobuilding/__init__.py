"""
autobuilding v1.0.0
Description: Auto-building tool for python modules.
Author: wirnty (skedovichusjdj@gmail.com)
"""
__version__ = "1.0.0"

# module_builder.py

import json, os, shutil, subprocess

def BuildModule(folder_path: str):
    settings_file = os.path.join(folder_path, "buildsettings.json")
    script_file = os.path.join(folder_path, "script.py")

    with open(settings_file) as f:
        settings = json.load(f)

    name = settings["name"]
    version = settings["version"]
    description = settings["description"]
    owner = settings["owner"]
    email = settings["email"]

    project_dir = os.path.join(folder_path, name)
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)

    src_dir = os.path.join(project_dir, "src", name)
    os.makedirs(src_dir, exist_ok=True)

    # __init__.py
    with open(script_file) as f:
        user_code = f.read()

    init_code = f'''"""
{name} v{version}
Description: {description}
Author: {owner} ({email})
"""
__version__ = "{version}"

{user_code}
'''
    with open(os.path.join(src_dir, "__init__.py"), "w") as f:
        f.write(init_code)

    # pyproject.toml
    pyproject = f"""
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{name}"
version = "{version}"
description = "{description}"
authors = [{{name="{owner}", email="{email}"}}]
"""
    with open(os.path.join(project_dir, "pyproject.toml"), "w") as f:
        f.write(pyproject)

    # build wheel
    subprocess.run(["python", "-m", "build"], cwd=project_dir)

    print(f"Module {name} built at {os.path.join(project_dir, 'dist')}")
