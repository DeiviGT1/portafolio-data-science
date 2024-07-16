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

    user_name = os.getenv("PRIME_VIDEO_USERNAME")
    password = os.getenv("PRIME_VIDEO_PASSWORD")

    # Check if environment variables are loaded
    if not user_name or not password:
        print("Error: Please ensure that PRIME_VIDEO_USERNAME and PRIME_VIDEO_PASSWORD are set in the .env file.")
        return

    # Initialize the Chrome driver
    driver = webdriver.Chrome()
    driver.get("https://www.primevideo.com/")

    wait = WebDriverWait(driver, 20)

    try:
        # Click on the login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, './/a[@class="dv-copy-button"]')))
        login_button.click()

        # Enter email
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@type="email"]')))
        email_field.send_keys(user_name)

        # Click continue
        continue_button = driver.find_element(By.XPATH, './/input[@id="continue"]')
        continue_button.click()

        # Enter password
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@type="password"]')))
        password_field.send_keys(password)

        # Click sign in
        sign_in_button = driver.find_element(By.XPATH, './/input[@id="signInSubmit"]')
        sign_in_button.click()

        # Enter search term
        search_field = wait.until(EC.presence_of_element_located((By.XPATH, './/input[@aria-label="Buscar en Prime Video"]')))
        search_field.send_keys("two and a half men")
        search_field.send_keys(u'\ue007')  # Press Enter key

        # Collect seasons
        wait.until(EC.presence_of_element_located((By.XPATH, './/div[@class="klzoqL"]/div/ul/li/a')))
        season_elements = driver.find_elements(By.XPATH, './/div[@class="klzoqL"]/div/ul/li/a')
        season_links = [season.get_attribute("href") for season in season_elements]

        series_data = {}
        current_season = 1

        for season_link in season_links:
            driver.get(season_link)
            print(season_link)
            time.sleep(3)

            episode_elements = driver.find_elements(By.XPATH, './/div[@class="dCocJw"]')
            episodes = {}
            current_episode = 1

            for episode_element in episode_elements:
                try:
                    link = episode_element.find_element(By.XPATH, './div/a').get_attribute("href")
                    chapter_name = episode_element.text
                    episodes[f"episode_{current_episode}"] = {
                        "link": link,
                        "chapter_name": chapter_name
                    }
                except NoSuchElementException:
                    episodes[f"episode_{current_episode}"] = {
                        "link": "",
                        "chapter_name": ""
                    }
                current_episode += 1

            series_data[f"season_{current_season}"] = episodes
            current_season += 1

    except TimeoutException as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    # Output the collected data
    for season, episodes in series_data.items():
        print(f"{season}:")
        for episode, details in episodes.items():
            print(f"  {episode}: {details['chapter_name']} - {details['link']}")

if __name__ == "__main__":
    main()
