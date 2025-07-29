import json
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_amazon_book_cover_url_selenium(url, wait_time=30):
    from selenium.common.exceptions import NoSuchElementException
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(wait_time)

        image_url = None

        # Lista de seletores para tentar encontrar a imagem
        selectors = [
            '#imgTagWrapperId > img',
            'img[data-a-dynamic-image]',
            'img#imgBlkFront',
            'img#ebooksImgBlkFront',
            'img[src*="images-na.ssl-images-amazon.com"]',
        ]

        for selector in selectors:
            try:
                img = driver.find_element(By.CSS_SELECTOR, selector)
                # Fallback para pegar diretamente do src
                src = img.get_attribute('src')
                if src:
                    image_url = src
                    break
            except NoSuchElementException:
                continue  # Tenta o próximo seletor

        if not image_url:   
            src = driver.execute_script('return document.getElementById("imgTagWrapperId")?.children[0]?.getAttribute("src");')
            if src:
                image_url = src
            if not image_url:
                raise Exception("Nenhum seletor encontrou uma imagem válida")

        return image_url

    except Exception as e:
        raise Exception(f"Erro ao obter imagem: {e}")
    finally:
        driver.quit()


def process_json_file_with_selenium(file_path):
    # Faz backup
    backup_path = file_path.replace(".json", "_backup.json")
    shutil.copy(file_path, backup_path)
    print(f"Backup criado: {backup_path}")

    # Lê o JSON
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Itera nos livros
    for book in data.get("2-5 anos", []):
        if "imageUrl" not in book or book["imageUrl"] is None:
            try:
                image_url = get_amazon_book_cover_url_selenium(book["url"])
                book["imageUrl"] = image_url
                print(f"✓ {book['title']}: {image_url}")
            except Exception as e:
                book["imageUrl"] = None
                print(f"✗ {book['title']}: {e}")
        else:
            print(f"⏩ {book['title']}: já possui imageUrl, pulando.")

    # Salva o arquivo modificado
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Arquivo atualizado salvo: {file_path}")

# ⬇️ Substitua pelo caminho do seu arquivo JSON
if __name__ == "__main__":
    caminho_arquivo = "indicacoes.json"
    process_json_file_with_selenium(caminho_arquivo)
