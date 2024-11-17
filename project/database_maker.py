import pandas as pd
from docx import Document


def parse_docx_to_dataframe(file_path):
    # Load the .docx file
    doc = Document(file_path)

    # Initialize variables to store articles
    articles = []
    current_article = None

    for para in doc.paragraphs:
        text = para.text.strip()

        # Check if the paragraph starts with "Статья"
        if text.startswith("Статья"):
            # Save previous article if it exists
            if current_article:
                articles.append(current_article)

            # Start a new article entry
            current_article = { "content": text+'. '}

        # Otherwise, add the paragraph to the current article's content
        elif current_article and text:
            current_article["content"] += text + " "

    # Append the last article if exists
    if current_article:
        articles.append(current_article)

    # Convert the list of articles to a DataFrame
    df = pd.DataFrame(articles)

    return df


# Usage
file_path = 'project/laws.docx'
df = parse_docx_to_dataframe(file_path)
df.to_csv('project/laws_data.csv')
print(df)
