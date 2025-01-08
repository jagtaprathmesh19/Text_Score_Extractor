"""
The web_scraper module: Support for scraping data form blogging site or any article site and saving 
in text files.

At large scale, the structure of the module is following:
* Imports and exports, all required depandencies.
* Internal helper functions: these should never be used in code outside this module.

"""
from xml.dom import NotFoundErr
from isort import file
import requests
from bs4 import BeautifulSoup as bs
import logger as log


class WebScrapper:
    """The WebScrapper base class.

    WebScrapper fetch the data from provided url then store in text files
    as a string.

    """

    def __init__(self) -> None:
        """
        Instantiated all information which is needed
        """
        self.__url = None         # Url name for scraping
        self.__fileloc = None     # location of file
        self.__document = None    # content for text file

    def __scraping(self) -> str:
        '''
        This methods helps to scrape data by requesting url and 
        finding all the data based on tags provided

        Returns: It returns text data which stores as document.
        '''
        log.info(f"Fetching URL: {self.__url}")
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        # parsing the web page data using url
        web_page = requests.get(self.__url, headers=header, timout = 10)
        web_page.raise_for_status()
        soup = bs(web_page.content, 'html.parser')
        # scraping the header of the web page
        try:
            title = soup.find(
                'h1', attrs={'class': 'entry-title'}).text.replace('– Blackcoffer Insights', '')
        except AttributeError as e:
            title = ''
            log.error(f"Error fetching {title}: {e}")

        try:
            paragraphs = soup.find('div', attrs={'class': 'td-post-content'})
        except NotFoundErr as e:
            paragraphs = None
            log.error(f"Error fetching paragraph {paragraphs}: {e}")

        self.__document = title
        if paragraphs is not None:
            for paragraph in paragraphs.findAll({"p", 'h3', 'li'}):
                text = paragraph.text
                if len(text) < 1:
                    continue
                self.__document = ''.join((self.__document, '\n', text))

    def __save_text_file(self) -> file:
        '''
        This methods helps to write documetn which we scrape and create a new text file
        '''
        try:
            file = open(self.__fileloc, "w")
            file.write(self.__document)
            logging.info(f"Data saved to {self.__fileloc}")
        except:
            file = open(self.__fileloc, 'wb')
            file.write(self.__document.encode('utf-8', 'ignore'))
            logging.info(f"Data saved to {self.__fileloc}")

        file.close()

    def scrape(self, cur_entry_info):
        '''
        This methoda takes all information url and file location and returns text files with
        scraped data.
        '''
        self.__url = cur_entry_info['URL']
        self.__fileloc = cur_entry_info['File Loc']
        # self.__scraping()
        # self.__save_text_file()
        with ThreadPoolExecutor() as executor:
            executor.submit(self.__scraping)

        with ThreadPoolExecutor() as executor:
            executor.submit(self.__save_text_file)
