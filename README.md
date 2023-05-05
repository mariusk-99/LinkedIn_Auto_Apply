# LinkedIn_Auto_Apply
This repository helps you automatically apply to jobs on LinkedIn

Follow these instructions to run the code on your machine

## Installing libraries and packages

### Install selenium:
`pip install selenium`


Follow the instructions [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) to install the Chrome driver.

Selenium requires a driver to interface with the chosen browser. Make sure the driver is in your path, you will need to add your `driver_path` to the `config.json` file.

### Download and modify files for local use:

Change the configuration file with:

- Your email linked to LinkedIn.
- Your password.  
- Keywords for finding specific job titles.  
- The location where you are currently looking for a position.  
- The driver path to your downloaded webdriver.  
- Run `python main.py`
