from subprocess import CREATE_NO_WINDOW

from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

import requests
import os
import time

import json


class Downloader:

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)

        self.service = Service(ChromeDriverManager().install())
        self.service.creation_flags = CREATE_NO_WINDOW

        self.make_search()

    def download_image(self, url, folder_name, img_name):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(os.path.join(folder_name, str(img_name) + '.jpg'), 'wb') as file:
                file.write(response.content)
        else:
            raise Exception('Não foi possivel baixar a imagem com sucesso')

    def users_input(self):
        term_to_search = input('Informe o nome do objeto a ser pesquisado: ')
        while True:
            try:
                quant_images = int(input('Informe a quantidade de imagens a ser baixado:'))
                if quant_images <= 0:
                    print('Por favor, digite um número maior do que 0!!!')
                    continue
                break

            except ValueError:
                print('Por favor, digite um número inteiro!!!')

        return term_to_search, quant_images

    def make_search(self):
        term_to_search, quant_images = self.users_input()

        images_to_search = term_to_search.replace(" ", "+")

        folder_name = os.path.join('images/', term_to_search.replace(" ", "_"))

        driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        driver.maximize_window()

        search_url = f'https://www.google.com/search?q={images_to_search}&source=lnms&tbm=isch'
        driver.get(search_url)

        time.sleep(2)

        # ir para topo da página
        driver.execute_script("window.scrollTo(0, 0);")
        self.select_images_containers(driver, folder_name, term_to_search, quant_images)

    def scroll_to_end(self, driver):
        for i in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

    def select_images_containers(self, driver: webdriver, folder_name, term_to_search, quant_images):
        os.makedirs(folder_name, exist_ok=True)

        with open(os.path.join(folder_name, 'last_index_div.json'), 'a+') as file:
            file.seek(0)
            content = json.loads(file.read() or '{}')
            current_index = content['last_index'] if content else 0
            index_image = content['last_img_saved_index'] if content else 0

        self.scroll_to_end(driver)

        num_downloaded_imgs = 0

        while True:
            current_index += 1
            if current_index % 25 == 0:
                continue

            try:
                # WebDriverWait(driver, 5).until(
                #     EC.presence_of_element_located((By.XPATH, f"""//*[@id="islrg"]/div[1]/div[{current_index}]"""))).click()
                # time.sleep(1)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"""//*[@id="rso"]/div/div/div[1]/div/div/div[{current_index}]"""))).click()
                time.sleep(1)

                imageElement = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    """//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]""")))
                imageURL = imageElement.get_attribute('src')

                index_image += 1

                file_name = term_to_search.replace(" ", "_")

                img_name = f'{file_name}_{index_image}'

                self.download_image(imageURL, folder_name, img_name)
                num_downloaded_imgs += 1
                print(f"Imagem nº{num_downloaded_imgs} baixada. URL: {imageURL}\nNome da imagem: {img_name}.jpg",
                      end="\n\n")

                with open(os.path.join(folder_name, 'last_index_div.json'), 'w') as file:
                    values = {'last_index': current_index, 'last_img_saved_index': index_image, }
                    json.dump(values, file, indent=6)

            except TimeoutException:
                print("Tempo Esgotado! Indo para próxima imagem")
                continue
            except Exception as e:
                print(f"Não foi possível baixar a imagem Nº{current_index}, indo para próxima. Erro:{e}")

            if quant_images == num_downloaded_imgs:
                driver.quit()
                print(f'{quant_images} {"imagem baixada" if quant_images == 1 else "imagens baixadas"}!!!')
                break
