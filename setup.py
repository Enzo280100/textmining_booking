from setuptools import setup, find_packages

# Read dependencies from the requirements.txt file
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Configuration of setup.py
setup(
    name="hw01",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requirements,
    description="Webscraping of the Bookings.com website",
    author="Tarang Kadyan, Oriol Gelabert, Enzo Infantes",
    author_email="tarang.kadyan@bse.eu, oriol.gelabert@bse.eu, enzo.infantes@bse.eu",
    url="https://github.com/Enzo280100/textmining_booking",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

