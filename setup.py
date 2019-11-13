from setuptools import setup


with open("README.md") as f:
    LONG_DESCR = f.read()


setup(
    name="Montyhall",
    author="Sam Morley",
    author_email="sam@inakleinbottle.com",
    version="1.0.0",
    description="Simulator for the Monty Hall problem in conditional probability",
    py_modules=["montyhall"],
    url="https://github.com/inakleinbottle/montyhall",
    long_description=LONG_DESCR,
    long_description_content_type="text/markdown",

)
