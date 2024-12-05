import time
import streamlit as st
import requests
import sys
import json
import openai
import os
from tqdm import tqdm
from PyPDF2 import PdfReader



api_key = st.secrets["API_KEY"]
base_url = "https://api.sambanova.ai/v1"


def first_reasoning(text):
    prompt = f'Q. {text}\n A. Давай порассуждаем и подумаем. На мой взгляд эту проблему можно разделить на под-проблемы.'
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    response_first_thoughts = client.chat.completions.create(
        model='Meta-Llama-3.1-405B-Instruct',
        messages=[{"role": "system",
                   "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Так же ты хорошо выражаешь свои мысли."},
                  {"role": "user",
                   "content": prompt}],
        temperature=0.1,
        top_p=0.1
    )
    prompt = f'Q. {text}\n A1. {response_first_thoughts.choices[0].message.content}. Q - задача, А1 - это то, как ты ответил на нее. Теперь надо убедится в ответах в источниках. Отвечай только ключевыми словами для поиска в формате "*ключевое слово*,\n"'
    response_query = client.chat.completions.create(
        model='Meta-Llama-3.1-405B-Instruct',
        messages=[{"role": "system",
                   "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Так же ты хорошо выражаешь свои мысли."},
                  {"role": "user",
                   "content": prompt}],
        temperature=0.1,
        top_p=0.1
    )
    return response_first_thoughts.choices[0].message.content, response_query.choices[0].message.content


def final_thoughts(text, rag_info):
    prompt = f'Q. {text}\n База знаний: {rag_info}. A. Давайте разложим ответ по полочкам и доступным фактам.'
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    response_final_thoughts = client.chat.completions.create(
        model='Meta-Llama-3.1-405B-Instruct',
        messages=[{"role": "system",
                   "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Так же ты хорошо выражаешь свои мысли."},
                  {"role": "user",
                   "content": prompt}],
        temperature=0.1,
        top_p=0.1
    )
    return response_final_thoughts.choices[0].message.content


def retrieving_key_information(contents, query):
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    useful_info = []
    for idx, content in enumerate(tqdm(contents, desc="Processing Texts")):
        try:
            response = client.chat.completions.create(
                model='Meta-Llama-3.1-405B-Instruct',
                messages=[{"role": "system",
                           "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Так же ты хорошо выражаешь свои мысли."},
                          {"role": "user",
                           "content": f'Найди в этом тексте то, что может подходить к этим ключевым словам. Формат ответа: "-" если нет информации. Если есть информация, то процитируй полную статью. Что искать: {query}. Где искать: {content}.'}],
                temperature=0.1,
                top_p=0.1
            )
            if response.choices[0].message.content != '-':
                useful_info.append(response.choices[0].message.content)
                print(useful_info)
        except Exception:
            time.sleep(10)

        time.sleep(3)
    useful_info = '\n'.join(useful_info)
    response = client.chat.completions.create(
        model='Meta-Llama-3.1-405B-Instruct',
        messages=[{"role": "system",
                   "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Так же ты хорошо выражаешь свои мысли."},
                  {"role": "user",
                   "content": f'Оставь полные цитаты тех статей, про которые есть информации. Если в тексте есть сомнение, не включай статью. {useful_info}'}],
        temperature=0.1,
        top_p=0.1
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def laws_for_text(chunk):
    laws_set = set()
    for obj in chunk:
        if len(obj) > 0:
            laws = vector_db.query_vector_db(obj, db, vector_db.model, 2)[0]
            for law in laws:
                laws_set.add(law)
    return laws_set


def break_down_problem(text):
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    response = client.chat.completions.create(
        model='Meta-Llama-3.1-405B-Instruct',
        messages=[{"role": "system",
                   "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Ты НЕ пишешь статьи кодекса, ЕСЛИ эти статьи не упомянены напрямую в задаче"},
                  {"role": "user",
                   "content": f"Напиши список преступлений, которые могут привлекаться по статьям УК РФ. НИ В КОЕМ СЛУЧАЙ НЕ ОТВЕЧАЙ КАКИЕ ЭТО СТАТЬИ. Формат ответа: * Пункт1\n * Пункт2\n. '{text}'"}],
        temperature=0.1,
        top_p=0.1
    )

    return response.choices[0].message.content


def translate(text, from_lang, to_lang):
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    response = client.chat.completions.create(
        model='Meta-Llama-3.1-405B-Instruct',
        messages=[{"role": "system",
                   "content": "You are professional translator"},
                  {"role": "user",
                   "content": f"Translate this from {from_lang} language to {to_lang}. ANSWER ONLY WITH TRANSLATION '{text}'"}],
        temperature=0.1,
        top_p=0.1
    )

    return response.choices[0].message.content


def main_summary(text):
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    response = client.chat.completions.create(
        model='Meta-Llama-3.1-405B-Instruct',
        messages=[{"role": "system",
                   "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Ты НЕ пишешь статьи кодекса, ЕСЛИ эти статьи не упомянены напрямую в задаче"},
                  {"role": "user",
                   "content": f"Напиши краткое содержание этого текста с главным смыслом. НИ В КОЕМ СЛУЧАЙ НЕ ОТВЕЧАЙ КАКИЕ ЭТО СТАТЬИ.'{text}'"}],
        temperature=0.1,
        top_p=0.1
    )

    return response.choices[0].message.content


def reply(text, rag_list):
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    response = client.chat.completions.create(
        model='Meta-Llama-3.1-405B-Instruct',
        messages=[{"role": "system",
                   "content": "Ты профессиональный юрист и хорошо понимаешь суть текста. Для решения задачи возможно подойдут эти материалы:"
                              f"{rag_list}"},
                  {"role": "user",
                   "content": f"{text}"}],
        temperature=0.1,
        top_p=0.1
    )

    return response.choices[0].message.content


def split_into_chunks(text, caption, chunk_size=150000):
    """
    Split a text into chunks of approximately `chunk_size` characters.

    Args:
        text (str): The input text to be split.
        chunk_size (int): The target size of each chunk in characters (default: 27,000 for ~15 pages).

    Returns:
        list of str: A list of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        # Ensure we do not split words by finding the last space before the cutoff
        if end < len(text):
            end = text.rfind(" ", start, end) + 1  # Find last space
        chunks.append(caption + '\n' + text[start:end].strip())
        start = end
    return chunks


def read_pdf(file):
    """
    Extract text from a PDF file using PyPDF2.

    Args:
        file: A file-like object representing the uploaded PDF.

    Returns:
        str: The extracted text from the PDF.
    """
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def inference(text, uploaded_files):
    contents = []
    for file in uploaded_files:
        try:
            content = read_pdf(file)
            chunks = split_into_chunks(content, file.name)
            contents += chunks
        except Exception as e:
            print(e)
            continue
    first_stage = None
    second_stage = None
    third_stage = None
    for i in range(10):
        try:
            if first_stage is None:
                first_stage = first_reasoning(text)
            if second_stage is None:
                second_stage = retrieving_key_information(contents, first_stage[1])
            if third_stage is None:
                third_stage = final_thoughts(text, second_stage)
            return third_stage
        except Exception as e:
            print(e)
            time.sleep(10)
    return 'Sorry, there is an error. Try again!'



