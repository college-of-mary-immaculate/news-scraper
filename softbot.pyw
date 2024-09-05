import os
import re
import time
import socket
import json
import requests
import platform

from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from tkinter import messagebox
from summarizer import summarize
from datetime import datetime, timedelta

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class Current_Datetime(Command):
    def __init__(self):
        self.execute()

    def execute(self):
        now = datetime.now()
        format_now = now.strftime("%m/%d/%Y %I:%M %p")
        parse_now = datetime.strptime(format_now, "%m/%d/%Y %I:%M %p")

        return parse_now
    
class Date_Parser(Command):
    def __init__(self, date):
        self.dt = date

    def execute(self):
        pattern = r"([0-9]{2}:[0-9]{2} (?:AM|PM))\s+(\w+) ([0-9]{2}), ([0-9]{4})"
        result = re.search(pattern, self.dt)
        month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].index(result[2]) + 1
        day = result[3]
        year = result[4]
        time_parse = result[1]

        parsed_datetime = datetime.strptime(f"{month}/{day}/{year} {time_parse}",  "%m/%d/%Y %I:%M %p")

        return parsed_datetime

class Directory(Command):
    def __init__(self):
        pass

    def execute(self):
        if platform.system() == "Windows":
            directory = "softbot"
            parent = "C:\\"
            path = os.path.join(parent, directory)

            if  not os.path.exists(path):
                os.mkdir(path)
                print(f"Created {path}")
        else:
            directory = "softbot"
            parent = os.environ.get('HOMR', '/home/default-user')
            path = os.path.join(parent, directory)

            if  not os.path.exists(path):
                os.mkdir(path)
                print(f"Created {path}")

class Save_JSON(Command):
    def __init__(self, data, file_path):
        self.data = data
        self.file_path = file_path        

    def execute(self):
        with open(self.file_path, "w") as filewrite:
            json.dump(self.data, filewrite, indent=4)

class Load_JSON(Command):
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as fileread:
                return json.load(fileread)
        else:
            return {}

class Scraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

class Scraper_Url(Scraper):
    def scrape_url(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            section = soup.find('section', id='inq_section')
            infos = section.find_all('div', id='ncg-info')
            links_dict = {} # title: url
            for info in infos:
                h1_tag = info.find('h1')
                a_tag = h1_tag.find('a')
                # links_dict["title"] = a_tag.get_text()
                # links_dict["url"] = a_tag['href']
                links_dict[a_tag.get_text()] = a_tag['href']
            return links_dict
        else:
            print(f"Failed to retrieve URL: {response.status_code}")
            return None

class Scraper_Article(Scraper):
    def scrape_article(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            article = soup.find('section', id='inq_section')
            # author = article.find('div', id='art_author')
            # print(f"Author: {author.get_text()}")
            date = article.find('div', id='art_plat')
            # print(f"Date: {date.get_text()}")
            parsed_date = Date_Parser(date.get_text()).execute()
            content = article.find('div', id='article_content')
            paragraphs = content.find_all('p')

            fetch_paragraphs = []
            for paragraph in paragraphs:
                divs = paragraph.find_all('div')
                strong = paragraph.find_all('strong')

                if divs:
                    continue
                if strong:
                    continue
                if 'wp-caption-text' in paragraph.get('class', []):
                    continue
                if 'headertext' in paragraph.get('class', []):
                    break
                if paragraph.get_text(strip=True):
                    fetch_paragraphs.append(paragraph)
                
            converted_article = self.convert_paragraph(fetch_paragraphs)
            return converted_article, parsed_date
        else:
            print(f"Failed to retrieve article: {response.status_code}")
            return None, None
    
    def convert_paragraph(self, paragraphs):
        converted_paragraph = ""
        for paragraph in paragraphs:
            converted_paragraph += paragraph.get_text(strip=True) + " "
        return converted_paragraph.strip()

class App:
    def __init__(self):
        Directory().execute()
        self.file_path = self.check_os()
        self.cache = Load_JSON(self.file_path).execute()
        self.current_time = datetime.now()
        self.end_day = self.current_time.replace(hour=23, minute=59, second=0, microsecond=0)
        self.start_day = self.current_time.replace(hour=00, minute=00, second=0, microsecond=0)

        self.base_url = "https://newsinfo.inquirer.net/"

        self.wheather_related_keywords = ["storm", "rain", "tsunami",  "tornado", "heatwave",  "cyclone"]
        self.land_related_keywords = ["earthquakes", "earthquake", "landslide", "landslides", "drought", "volcano", "eruption"]
        self.emergency_situation_keywords = ["outbreak", "pandemic", "fire", "accident", "explosion"]
        self.health_related_keywords = ["disease", "virus", "infection", "vaccine"]
        self.general_keywords = ["warning", "danger", "hazard", "security", "suspend", "suspension"]
        self.keywords = self.wheather_related_keywords + self.land_related_keywords + self.emergency_situation_keywords + self.health_related_keywords + self.general_keywords

    def check_os(self):
        if platform.system() == "Windows":
            directory = Directory().execute()
            path = f"{directory}\\data.json"
            return path
        elif platform.system() == "Linux":
            directory = Directory().execute()
            path = f"{directory}/data.json"
            return path
        
    def check_connection(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            return False

    def send_alert(self, message):
        messagebox.showinfo("Alert", message)

    def check_keyword(self, title, date, article, keywords):
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', article):
                summary = summarize(title, article)
                converted = ' '.join(summary)
                
                message = f"Keyword: {keyword}\n{date}\n\n\"{title}\"\n-->{converted}"

                self.send_alert(message)
                break
    
    def remove_old_titles(self):
        days_ago = self.current_time - timedelta(days=3)

        list_titles = []
        for title, data in self.cache.items():
            convert_date = datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S")

            if convert_date < days_ago:
                list_titles.append(title)
        
        for title in list_titles:
            del self.cache[title]

    def scrape(self):
        if self.check_connection():
            scraper = Scraper_Url(self.base_url)
            links = scraper.scrape_url()

            for title, url in links.items():
                if title in self.cache:
                    print("Title scraped already!")
                    continue
                else:
                    self.remove_old_titles()
                    scraper_article = Scraper_Article(url)
                    article, date = scraper_article.scrape_article()

                    if article is None and date is None:
                        continue

                    if date > self.start_day and date < self.end_day:
                        self.check_keyword(title, date, article, self.keywords)
                    else:
                        print(f"{date} News is not news today")

                    self.cache[title] = {
                        "url": url,
                        "date": date.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    Save_JSON(self.cache, self.file_path).execute()
            return True
        else:
            messagebox.showerror("Error", "Please connect to the internet!\nThen rerun the program.")
            return True
        
if __name__ =='__main__':
    app = App()
    running = True
    # result = app.scrape()
    while running:
        result = app.scrape()
        if result:
            time.sleep(900)
        else:
            running = False