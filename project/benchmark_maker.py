import pdfplumber
import re
import requests
from bs4 import BeautifulSoup

def extract_tasks_from_pdf(pdf_path):
    tasks = []
    current_task = []

    # Regular expression to detect task numbers like "1.", "2.", etc.
    task_start_pattern = re.compile(r'^\d+\.\s')

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.splitlines()

            for line in lines:
                # Check if the line starts with a task number
                if task_start_pattern.match(line):
                    # If there's an ongoing task, save it and start a new one
                    if current_task:
                        tasks.append(" ".join(current_task).strip())
                        current_task = []
                    # Start a new task from the current line
                    current_task.append(line)
                else:
                    # Append subsequent lines to the current task until a new one starts
                    current_task.append(line)

        # Add the last task if it exists
        if current_task:
            tasks.append(" ".join(current_task).strip())

    return tasks


def search_yandex_and_get_first_occurrence(text):
    # Format the search query for Yandex
    search_url = f"https://yandex.ru/search/?text={text[:30]} site:sinref.ru zinref.ru"
    response = requests.get(search_url)
    print(response)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the first result that links to sinref.ru or zinref.ru
        results = soup.find_all('a', href=True)
        for link in results:
            href = link['href']
            print(href)
            # Check if the link contains the desired domains
            if 'sinref.ru' in href or 'zinref.ru' in href:
                return href  # Return the first matching URL

        return None  # No matching result found
    else:
        print(f"Failed to fetch search results with status code {response.status_code}")
        return None


# Path to the PDF file
pdf_path = "project/tasks.pdf"
tasks = extract_tasks_from_pdf(pdf_path)

for task in tasks[2:239]:
    result_url = search_yandex_and_get_first_occurrence(task)
    if result_url:
        print(f'{result_url}')
    else:
        print(f'No occurrences found for task')
