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


class Downloader:

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)

        self.service = Service(ChromeDriverManager().install())
        # self.service.creation_flags = CREATE_NO_WINDOW

        self.make_search()

    def download_image(self, url, folder_name, img_name):
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder_name, str(img_name) + '.jpg'), 'wb') as file:
                file.write(response.content)

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

        folder_name = 'images/' + term_to_search.replace(" ", "_")

        driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        search_url = f'https://www.google.com/search?q={images_to_search}&source=lnms&tbm=isch'
        driver.get(search_url)

        time.sleep(2)

        # ir para topo da página
        driver.execute_script("window.scrollTo(0, 0);")
        self.select_images_containers(driver, folder_name, term_to_search, quant_images)

    def select_images_containers(self, driver: webdriver, folder_name, term_to_search, quant_images):
        i = 0
        num_images_baixadas = 0

        while True:
            i += 1
            if i % 25 == 0:
                continue

            try:
                # WebDriverWait(driver, 5).until(
                #     EC.presence_of_element_located((By.XPATH, f"""//*[@id="islrg"]/div[1]/div[{i}]"""))).click()
                # time.sleep(1)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"""//*[@id="rso"]/div/div/div[1]/div/div/div[{i}]"""))).click()
                time.sleep(1)

                imageElement = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    """//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]""")))
                imageURL = imageElement.get_attribute('src')

                if not os.path.isdir(folder_name):
                    os.makedirs(folder_name)

                files = os.listdir(folder_name)
                index_image = 1

                if len(files) > 0:
                    time.sleep(1)
                    index_last_img = max(int(f.replace(".jpg", "").split("_")[-1]) for f in files)

                    index_image = index_last_img + 1

                file_name = term_to_search.replace(" ", "_")

                img_name = f'{file_name}_{index_image}'

                self.download_image(imageURL, folder_name, img_name)
                num_images_baixadas += 1
                print(f"Imagem nº{num_images_baixadas} baixada. URL: {imageURL}\nNome da imagem: {img_name}.jpg",
                      end="\n\n")

            except TimeoutException:
                print("Tempo Esgotado! Indo para próxima imagem")
                continue
            except Exception as e:
                print(f"Não foi possível baixar a imagem Nº{i}, indo para próxima. Erro:{e}")

            if quant_images == num_images_baixadas:
                driver.quit()
                print(f'{quant_images} {"imagem baixada" if quant_images == 1 else "imagens baixadas"}!!!')
                break
