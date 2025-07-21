from setuptools import setup, find_packages

HYPHEN_E_DOT = "-e ."
with open("requirements.txt", "r") as f:
    requirements = f.readlines()
    if requirements:
        requirements = [req.strip() for req in requirements if req.strip()]
    if HYPHEN_E_DOT in requirements:
        requirements.remove(HYPHEN_E_DOT)
setup(
    name="MindMateAI",
    author="Nithin Kumar",
    author_email="nithinnagireddy8374@gmail.com",
    version="0.0.0",
    description="An AI assistant for your mind",
    url="https://github.com/Nithin218/MindMate-AI.git",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
)