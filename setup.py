from setuptools import setup, find_packages

setup(
    name="research_prototypes_platform",
    version="1.0.0",
    description="Enterprise Research Prototypes & AI Experimentation Platform (50k+ LOC)",
    author="Antigravity DeepMind Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
)
