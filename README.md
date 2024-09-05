# News Scraper

[![Static Badge](https://img.shields.io/badge/Licence-GNU%20GPL%203.0-blue)](https://opensource.org/license/gpl-3-0)
![Static Badge](https://img.shields.io/badge/Platform-Linux%20Windows-white)

News Scraper is a program that uses the internet as its advantage to gather latest news on the internet through
[INQUIRER.NET](https://newsinfo.inquirer.net/) as its main source of news. It filters out general related news with
use of keywords such as rain, storm, earthquake and many more that's related with general information dissimenation.
With this, it can provide news information without directly surfing to the internet.

## :zap: Update
No current update

## :bulb: Contributors
* Ponce, Michael Alexis [@Mikeru02](https://github.com/Mikeru02)
* Perez, Jessie [@PerezJessieM07](https://github.com/PerezJessieM07)

## :pencil: Pre-requisites
### For Using
#### If using the `softbot.pyw` file
* Python 3.11
* Modules 
    * To install the modules at the same time:
    ```bash
    pip install -r requirements.txt
    ```
    * [requests 2.32.2](https://pypi.org/project/requests/)
    Requests is a simple, yet elegant, HTTP library.
    ```bash
    pip install requests
    ```
    * [beautifulsoup4 4.12.3](https://pypi.org/project/beautifulsoup4/)
    Beautiful Soup is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.
    ```bash
    pip install beautifulsoup4
    ```
    * [summarizer 0.0.7](https://pypi.org/project/summarizer/)
    Summarizer is an automatic summarization algorithm.
    ```bash
    pip install summarizer
    ```
#### If using the `softbot.exe` file
* Operating System (Windos, Linux-WSL)

### For Modifying
* Any code editor that supports Python 3.11
* Modules mentioned in `If using the softbot.pyw file`

## :rocket: Direction
### For Using
#### If using the `softbot.pyw` file
* Step 1
Download the repository as `.zip`. To download, click the releases then find the lastest then click
the `Source Code (zip)`.
* Step 2
Locate the file then extract it. You can use the built in extractor of some operating system, you can
also use `7-zip` or `WinRAR`.
* Step 3
Click the `softbot.pyw`. It will run to the background of your operating system. If you want to stop it
you can open the `Task Manager` the search the `softbot.pyw`, right click then `End Task`.
`Note: Befor you click or run the softbot.pyw make sure you install the need modules in pre-requisites`
* Optional Step
If you want to add the `softbot.pyw` into the start up, open the extracted folder first then
press `Win + R` then type:
```bash
shell:startup
```
Then copy the `softbot.pyw` file from the extracted folder the paste it to the start up folder.

#### If using the `softbot.exe` file
* Step 1
Download the repository as `.zip`. To download, click the releases then find the lastest then click
`softbot.exe`.
* Step 2
Click the `softbot.exe`. It will run to the background of your operating system. If you want to stop it
you can open the `Task Manager` the search the `softbot.exe`, right click then `End Task`.
* Optional Step
If you want to add the `softbot.exe` into the start up, open the extracted folder first then
press `Win + R` then type:
```bash
shell:startup
```
Then copy the `softbot.pyw` file from the extracted folder the paste it to the start up folder.

### For Modifying
* Step 1
Download the repository as `.zip`. To download, click the green button that says `Code` then
under it click 'Local` the click `Download ZIP`.
* Step 2
Locate the file then extract it. You can use the built in extractor of some operating system, you can
also use `7-zip` or `WinRAR`,
* Step 3
Open it on your preferred code editor. Happy moding!
* Optional Step
If you are done modifying the code and want it to be an exe file, 
    * Install pyinstaller if you haven't installed it yet.
    ```bash
    pip install pyinstaller
    ```
    * After you install the pyinstaller type this in the terminal
    ```bash
    pyinstaller --noconsole --onefile softbot.pyw
    ```
    * Wait for a while the under the `dist` folder you will find `softbot.exe`

## :sparkling_heart: Author's Note
If you find this useful enough, kindly give follow to the `contributors` and star the repository. Also
give credit and share the open-source distribution. Any closed ditribution will violate the [GNU GPL-3.0 License](https://opensource.org/license/gpl-3-0). Thank you so much, have a great day!

## :lock: License
The `news-scraper` is an open-sourced software under the [GNU GPL-3.0 License](https://opensource.org/license/gpl-3-0).

