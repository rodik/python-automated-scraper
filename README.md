# python-automated-scraper
Dev Container for Python scraper automated with [Github Actions](https://docs.github.com/en/actions)

# About

The goal of this project is to demonstrate a method for automating Python scrapers using Github Actions. It is part of [OpenDataDay-2022](http://odd.codeforcroatia.org/) program by [CodeForCroatia](https://codeforcroatia.org/). Target audience is a mix of technical and non-technical users. The instructions are designed to help new developers get started.

To simplify setup, a VS Code [development container](https://code.visualstudio.com/docs/remote/containers) is created.
## Components

### Scraper

A simple Python scraper to get announcements from official Government of the Republic of Croatia [pages](https://vlada.gov.hr/) is provided. Python code is basic as the scraper is not the main focus of this demo. </br>
For more information on what scraping is start [here](https://en.wikipedia.org/wiki/Web_scraping).

### Data destination

Collected data needs to be stored in a database. Various types of databases can be used for this purpose. Some simple solutions include:
- Structured text files (CSV, JSON)
- Spreadsheets (Excel, Google spreadsheet)
- Your email inbox :)

This demo will show how to use a Google spreadsheet to write rows of data each time new data is available. This solution includes additional setup as the scraper must have access to this spreadsheet in your Google Drive.

### Automation
Github Workflow [file](/.github/workflows/run_scraper.yml) contains logic to execute scraper code on a schedule. It also allows manual runs [here](https://github.com/rodik/python-automated-scraper/actions/workflows/run_scraper.yml).



# Setup instructions

Start by creating a GitHub account if you don't have one.

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repository (_rodik/python-automated-scraper_).
1. Installation [instructions](https://code.visualstudio.com/docs/remote/containers#_installation) for local machine requirements:
    - Docker Desktop
    - Visual Studio Code (VS Code)
    - Remote Development [Extension](https://code.visualstudio.com/docs/editor/extension-marketplace#_browse-for-extensions) pack
1. Authorize your scraper application to edit destination spreadsheet. Follow the instructions [here](https://pygsheets.readthedocs.io/en/latest/authorization.html).
    - Use second option - Service Account
    - Download your `.json` file - the content will be passed to the development container using an Environment variable
    - Note the generated email associated with created Service Account. It is also available in downloaded config.json file under `client_email` key.
1. Create a Environment variable named `GDRIVE_API_CREDENTIALS` on your local machine and set the content of downloaded `.json` file from step 3 as value of this variable. There is a shell [script](.devcontainer/set_github_repo_secrets.sh) to help you do it using bash or Powershell.
    - Now your scraper can access the spreadsheet from your VS Code development container.
1. Open VS Code
    - Open the Command Palette (F1 key *or* Ctrl+Shift+P *or* View -> Command Palette)
    - Run `Remote-Containers: Clone Repository in Container Volume ...`
    - Select GitHub
    - Type `python-automated-scraper` and select **your-account/python-automated-scraper** repository
    - Select **main** branch
    - Your repo will be ready when the container is built
1. Create [Google spreadsheet](https://docs.google.com/spreadsheets/u/0/?tgif=d) in your Drive folder as a destination for scraped data
    - Name it `Python to Sheets`
    - Rename the worksheet to `Najave`
    - If you choose different names, update the names in [scraper.py](python/scraper.py)
1. In your `Python to Sheets` share the spreadsheet with Service Account by adding the generated email as Editor
![share screenshot](img/share-spreadsheet-with-service-acc.png?raw=true)
1. In your forked Github repository create new Action secret named `GDRIVE_API_CREDENTIALS` and copy the content of downloaded `.json` file from step 3 as **Value** for this secret. 
    - Now your scraper can access the spreadsheet from a Github Workflow.

# Usage instructions

1. Scraper can identify a blank worksheet and knows when to perform an "initial load run".
1. After the initial run, the scraper does incremental loads (appends only new data to bottom of worksheet table).
1. Do **NOT** edit the destination worksheet manually. Create a new worksheet and reference scraped data in a new table if you want to analyze it in the same spreadsheet. There you can create additional transformations, add columns, apply formats, etc.
1. Edit cron [schedule](.github/workflows/run_scraper.yml) if needed. Use [this](https://crontab.guru/#0_15_*_*_*) if new to cron schedule expressions.
``` yaml
# At 15:00 UTC on every day of month:
  schedule:
    - cron: '0 15 * * *'
```