from setuptools import setup

# read the contents of your README file as GitHub-flavored Markdown
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='sustainable_wage_tool_data',
    version='1.0.0.dev1',
    packages=['sustainable_wage_tool_data'],
 
    author='Angel Febles'
)