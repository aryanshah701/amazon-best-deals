# Amazon Best Deals

Have you ever spend hours browsing through Amazon searching for the best deals on a product that you've been waiting to purchase on Black Friday? Well, same! So I created a Python script that does just that.

The script uses Selenium to go through over 10 pages of Amazon search results in under 60 seconds. It looks for the cheapest price and best deal available for the product you're looking for.

Input: Space-separated keywords as command-line arguments. The script searches for the given keywords and only looks at search results that, at a minimum, have the provided keywords as a prefix of any of its words!

## Getting Started

Once you've cloned the project, use the command line to navigate to the project's directory.

Then, use the following command to run the script. You can replace "samasung tv 55" with your choice of keywords.

    python3 amazon-scraper.py samsung tv 55

### Prerequisites

This script is written in Python and uses the Selenium library for Web Scraping. Hence, you will need those two things.

[Install Python](https://www.python.org/downloads/)

Once you've installed Python, selenium can be installed from the command line using pip as follows:

    pip install selenium

Finally, Selenium uses a Chrome Driver to do its web scraping. You will need to ensure that you have Google Chrome and the chrome driver installed.

[Install Chrome](https://www.google.com/chrome/)

[Install Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

Note: Once you've installed the Chrome Driver, move it to the project directory.
