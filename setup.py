from setuptools import setup, find_packages

setup(
    name='mcq_generator',
    version='0.1.0',
    author='Priyanka',
    install_requirements=["google-generativeai","langchain","langchain-google-genai","streamlit","python-dotenv","PyPDF2"]
    packages=find_packages()
    )

