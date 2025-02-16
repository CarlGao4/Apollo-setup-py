import os
import shutil
from setuptools import setup
import subprocess
import stat


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


# Remove the existing look2hear and apollo_repo folders
if os.path.exists("look2hear"):
    shutil.rmtree("look2hear", onerror=remove_readonly)
if os.path.exists("apollo_repo"):
    shutil.rmtree("apollo_repo", onerror=remove_readonly)

# Clone the specific folder from the GitHub repository
subprocess.check_call(
    [
        "git",
        "clone",
        "--depth",
        "1",
        "--filter=blob:none",
        "--sparse",
        "https://github.com/JusperLee/Apollo.git",
        "apollo_repo",
    ]
)

subprocess.check_call(["git", "sparse-checkout", "init", "--cone"], cwd="apollo_repo")
subprocess.check_call(["git", "sparse-checkout", "set", "look2hear"], cwd="apollo_repo")

# Get git hash
git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd="apollo_repo").decode("utf-8").strip()[:7]

# Move the look2hear folder to the current directory
shutil.move("apollo_repo/look2hear", ".")

# Remove the cloned repository
shutil.rmtree("apollo_repo", onerror=remove_readonly)

requirements = [
    "torch>=2.0,<2.5",
    "numpy<2",
    "huggingface-hub",
    "ml-collections",
    "omegaconf",
    "librosa",
]

setup(
    name="Apollo",
    description="Apollo: Band-sequence Modeling for High-Quality Audio Restoration",
    version="0.1+git" + git_hash,
    url="https://github.com/JusperLee/Apollo",
    install_requires=requirements,
    packages=["look2hear"],
    package_data={
        "look2hear": ["**/*"],
    },
    include_package_data=True,
)
