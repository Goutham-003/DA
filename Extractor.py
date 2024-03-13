from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os

articles_dir = "./articles"
if not os.path.exists(articles_dir):
    os.makedirs(articles_dir)

def save_webpage_text_to_file(url, filename, driver):
    try:
        driver.get(url)
        paragraphs = driver.find_elements(By.CSS_SELECTOR, ".td-post-content.tagdiv-type p")
        file_path = os.path.join(articles_dir, filename + ".txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            for paragraph in paragraphs:
                file.write(paragraph.text + "\n\n")

        print(f"Content saved to {filename}.txt")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        data = pd.read_csv("./WebLinks.csv")
        for index, row in data.iterrows():
            url = row["URL"]
            filename = row['URL_ID']
            print(url, filename)
            save_webpage_text_to_file(url, filename, driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
