from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
from bs4 import BeautifulSoup


def fetch_content_if_match(base_url, start, end, search_string):
    matched_texts = []

    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

    # Update this to your chromedriver path
    driver = webdriver.Chrome()

    for i in range(start, end + 1):
        url = f"{base_url}/{i}.htm"
        try:
            # Random delay to imitate human browsing
            time.sleep(random.uniform(1, 3))  # Delay between 1 to 3 seconds

            # Navigate to the URL
            driver.get(url)

            # Give the page some time to load
            time.sleep(2)  # Wait for the content to fully load

            # Get the page source
            content = driver.page_source

            # Parse the content with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            # Find the specific <td> tag with the given style and attributes
            td_tag = soup.find('td', valign='top',
                               style='border-bottom:1px solid windowtext; width: 744px; height: 171.0pt; border-left: 1px solid; padding-left: 5.4pt; padding-right: 5.4pt; padding-top: 0cm; padding-bottom: 0cm; border-right-color:windowtext; border-top-color:windowtext')

            if td_tag:
                # Find all <p> tags within the specified <td>
                paragraphs = td_tag.find_all('p')

                # Check if the search string is in the content
                page_text = soup.get_text()
                if search_string in page_text:
                    for p in paragraphs:
                        # Check if <p> contains any tags other than <b> or <p>
                        if all(child.name in ['b', 'br', None] and child.name not in ['i'] for child in p.children):
                            # If it only has <b> tags or no tags, join their text
                            matched_texts.append(' '.join([child.get_text().replace(" ", "") for child in p]))
                            print(f"Text added from: {url}")
                        else:
                            print(f"Skipped <p> due to other tags in: {url}")
                            break
                else:
                    print(f"No match for: {url}")
            else:
                print(f"<td> not found for: {url}")

        except Exception as e:
            print(f"Error fetching {url}: {e}")

    driver.quit()  # Close the browser after processing
    return matched_texts


if __name__ == "__main__":
    BASE_URL = "https://www.sinref.ru/000_uchebniki/04600_raznie_15/555-Ugolovn-pravo-zadachi-2008g_04600_raznie_15"
    START_PAGE = 600
    END_PAGE = 1000
    SEARCH_STRING = "Задача по уголовному праву РФ с решением"

    matched_contents = fetch_content_if_match(BASE_URL, START_PAGE, END_PAGE, SEARCH_STRING)

    # Optionally, save matched content to a file
    with open('project/matched_content.html', 'w', encoding='utf-8') as f:
        for content in matched_contents:
            f.write(content)
            f.write("\n\n")  # Separate each entry with a newline
