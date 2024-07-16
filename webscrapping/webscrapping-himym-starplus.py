from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()

    user_name = os.getenv("STARPLUS_USERNAME")
    password = os.getenv("STARPLUS_PASSWORD")

    # Initialize the Chrome driver
    driver = webdriver.Chrome()
    driver.get("https://www.starplus.com")

    wait = WebDriverWait(driver, 20)

    try:
        # Click on the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, './/a[@href="/login"]')))
        login_button.click()

        # Enter email
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@id="email"]')))
        email_field.send_keys(user_name)

        # Click continue
        continue_button = driver.find_element(By.XPATH, './/button[@aria-label="Aceptar y continuar"]')
        continue_button.click()

        # Enter password
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@aria-label="Escribir contraseña"]')))
        password_field.send_keys(password)

        # Click login
        login_button = driver.find_element(By.XPATH, './/button[@aria-label="INICIAR SESIÓN"]')
        login_button.click()

        # Select user profile
        user = "Jose"
        user_profile = wait.until(EC.presence_of_element_located((By.XPATH, f'.//h3[text()="{user}"]')))
        user_profile.click()

        # Click on the search button
        search_button = wait.until(EC.presence_of_element_located((By.XPATH, './/a[@aria-label="BÚSQUEDA"]')))
        search_button.click()

        # Search for the series
        serie = "How I Met Your Mother"
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@aria-label="Título o equipo"]')))
        search_field.send_keys(serie)
        time.sleep(5)

        # Select the first search result
        first_result = wait.until(EC.presence_of_element_located((By.XPATH, './/div[@aria-label="Search results"]/div[1]')))
        first_result.click()

        # Wait for the seasons to load
        wait.until(EC.presence_of_element_located((By.XPATH, './/div[@class="slick-track"]')))

        # Collect seasons and episodes information
        serie_data = {}
        season_elements = driver.find_elements(By.XPATH, './/div[@class="slick-track"]/div')

        for season_index, season_element in enumerate(season_elements, start=1):
            season_element.click()
            time.sleep(5)

            episodes = {}
            current_episode = 0

            while True:
                current_episode += 1
                try:
                    episode_link_element = driver.find_element(By.XPATH, f'.//div[@data-gv2containerkey="details_episodes"]/div/div/div/div/div[{current_episode}]/div/div/div/a')
                    chapter_name_element = driver.find_element(By.XPATH, f'.//div[@data-gv2containerkey="details_episodes"]/div/div/div/div/div[{current_episode}]/div')

                    link = episode_link_element.get_attribute("data-gv2elementvalue")
                    chapter_name = chapter_name_element.text

                    if chapter_name:
                        episodes[f"episode_{current_episode}"] = {
                            "link": f"https://www.starplus.com/es-419/video/{link}",
                            "chapter_name": chapter_name
                        }
                    else:
                        break
                except NoSuchElementException:
                    break

            serie_data[f"season_{season_index}"] = episodes

    except TimeoutException as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    # Output the collected data
    for season, episodes in serie_data.items():
        print(f"{season}:")
        for episode, details in episodes.items():
            print(f"  {episode}: {details['chapter_name']} - {details['link']}")

if __name__ == "__main__":
    main()
