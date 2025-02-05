# Analysis of the Impact of an Event on Rental Prices on Booking

## Project Description
This project investigates the effect of a major annual event in Barcelona on rental prices on Booking. Data is collected for at least two different weeks for Barcelona and another city (Milan) as a control group, aiming to analyze price variations using a difference-in-differences (DiD) model. Additionally, a text analysis is performed on accommodation descriptions to identify patterns in texts associated with prices.

## Project Structure
```
booking/
│── packages/
│   │── __pycache__/
│   │── __init__.py               # Package initialization file
│   │── dataloading.py            # Data loading and cleaning
│   │── processing.py             # Data processing
│   │── scraper.py                # Scraper to obtain data from Booking
│   │── selenium_setup.py         # Selenium setup for web scraping
│── Barcelona_MWC.csv             # Extracted data from Barcelona
│── Milan_MWC.csv                 # Extracted data from the control city (Milan)
│── geckodriver.exe               # Driver for Selenium (Firefox)
│── ITM_HW1.ipynb                 # Notebook with exploratory analysis and regressions
│── hw1.pdf                       # Document with project details
│── README.md                     # Project description and structure
│── requirements.txt               # Necessary dependencies for running the project
│── setup.py                       # Setup and installation script
```

## Installation and Setup
### Requirements
To install the required dependencies, run:
```sh
pip install -r requirements.txt
```
### Usage
1. **Selenium Setup:**
   - Download `geckodriver.exe` for Firefox or use the appropriate driver for Chrome.
   - Place it in the project folder.
   
2. **Run the Files:**
   ```sh
   python packages/scraper.py
   python packages/dataloading.py
   python packages/processing.py
   ```
    These files generate searches on Booking webpages, extract data according to our delimitations, and preprocess the description of each hotel.

3. **Data Analysis:**
   - Run the `ITM_HW1.ipynb` notebook in Jupyter Notebook to visualize exploratory analysis, data cleaning, and the DiD regression. In this notebook, we use pipelines to call all the functions from the .py files.

## Methodology
### 1. Web Scraping
- Rental price data is collected from Booking for Barcelona and Milan.
- Navigation through multiple result pages is automated.
- Accommodation descriptions are also extracted for text analysis.

### 2. Text Analysis
- Text preprocessing is performed by removing stopwords and applying stemming.
- Wordclouds are generated before and after preprocessing.
- Terms associated with higher prices are explored.

### 3. DiD Regression
- The impact of the event on prices is estimated using a difference-in-differences model.
- Additional controls based on text descriptions are included.
- Heterogeneous effects are explored according to accommodation quality.

## Contributions
This project was developed as part of an academic assignment. It is recommended to follow good practices in web scraping and respect the terms of service of the platforms used.


