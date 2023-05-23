from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.chrome.options import Options
import airbnb.const as const
from bs4 import BeautifulSoup
import time
import requests


class Airbnb(webdriver.Chrome):
    def __init__(self, driver_path=const.PATH_TO_DRIVER):
        os.environ['PATH'] += driver_path
        self.url = const.BASE_URL
        self.__start_date = '2023-07-01'
        self.__end_date = '2023-07-31'
        self.__max_price = 0
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        super(Airbnb, self).__init__(options=chrome_options)
        self.implicitly_wait(10)
        self.maximize_window()

    @property
    def max_price(self):
        return self.__max_price

    @max_price.setter
    def max_price(self, value):
        self.__max_price = value

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, value: str):
        self.__start_date = value

    @property
    def end_date(self):
        return self.__end_date

    @end_date.setter
    def end_date(self, value: str):
        self.__end_date = value

    def __click_button(self, data: str, key=1, error_handle=True):
        """
        1 - by CSS (default)
        2 - by ID
        """
        button = None
        for _ in range(10):
            try:
                if key == 1:
                    button = self.find_element(By.CSS_SELECTOR, data)
                elif key == 2:
                    button = self.find_element(By.ID, data)
                else:
                    raise Exception('!!Wrong key number!!')
                button.click()
                break
            except:
                if error_handle:
                    print(f'Something happened. Retry #{_ + 1}')
                else:
                    break
        return button

    def __find_input_field(self, id_tag: str, text_to_input: str):
        for _ in range(10):
            try:
                input_field = self.find_element(By.ID, id_tag)
                input_field.clear()
                input_field.send_keys(text_to_input)
                break
            except:
                print(f'Something happened. Retry #{_ + 1}')
        return input_field

    def __get_all_elements(self, data, key=1, error_handle=True):
        """
             1 - by XPATH (default)
             2 - by CLASS_NAME
             """
        button = None
        for _ in range(10):
            try:
                if key == 1:
                    button = self.find_elements(By.XPATH, data)
                    break
                elif key == 2:
                    button = self.find_element(By.CLASS_NAME, data)
                    break
                else:
                    raise Exception('!!! WRONG KEY !!!')
            except:
                if error_handle:
                    print(f'Something happened. Retry #{_ + 1}')
                else:
                    break
        return button


    def set_filters(self):
        new_url = self.current_url + f'&date_picker_type=calendar&checkin={self.__start_date}&checkout={self.__end_date}&adults=2' + f'&price_filter_input_type=1&price_min=0&price_max={str(self.max_price)}'

        self.get(new_url)


    def __go_through_all_places(self):
        start_url = self.current_url
        links = []
        while True:
            places = self.__get_all_elements('//a[@rel="noopener noreferrer nofollow"]')
            new_links = tuple(elem.get_attribute('href') for elem in places)
            reloaded_links = []
            for elem in new_links:
                if elem not in reloaded_links:
                    reloaded_links.append(elem + '/')
            links += reloaded_links
            next_butt = self.__click_button('a[aria-label="Далее"]', error_handle=False)
            self.get(self.current_url)
            if not next_butt:
                break
        self.get(start_url)
        return links

    def __get_places_with_reviews_only(self):
        links = self.__go_through_all_places()
        places = {}
        for link in links:
            self.get(link)
            self.__click_button('button[aria-label="Закрыть"]', error_handle=False)
            soup = BeautifulSoup(self.page_source, 'html.parser')
            reviews = soup.find_all(text='Отзывов пока нет')
            if len(reviews) != 0:
                links.remove(link)
            else:
                is_price = soup.find('span', class_='_1y74zjx') or soup.find('span', class_='_tyxjp1')
                if is_price:
                    price = soup.find('span', class_='_1y74zjx')
                    if price is None:
                        price = soup.find('span', class_='_tyxjp1')
                    places.update({link: price})
        return places

    def run(self, location):
        self.get(self.url)
        # Установление срока
        self.__click_button('button[data-index="1"]')
        # Ввод локации
        self.__find_input_field('bigsearch-query-location-input', location)
        # Нажатие на поиск
        self.__click_button('button[data-testid="structured-search-input-search-button"]')
        # Переход на новый url
        self.get(self.current_url)
        #Установление фильтра
        self.set_filters()
        #Пройтись по всем апартам и получить ссылки на них, оставить только с отзывами
        places = self.__get_places_with_reviews_only()
        return places

        # Гибкий срок
        # self.__click_button('tab--tabs--2', 2)
        # Срок на месяц
        # self.__click_button('flexible_trip_lengths-one_month', key=2)












