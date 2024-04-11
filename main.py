import sys
import os
import re

import requests
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
import shutil
import pdfplumber

from parser import Parser
from writer import Writer
from syntax import UrbanSyntax

links = [
    # "https://akbf.ru/about-us/about-us",
    # "https://akbf.ru/about-us/news",
    # "https://akbf.ru/about-us/license",
    # # "https://akbf.ru/assets/licences/20080415_info_L_3_page-0001.jpg",
    # # "https://akbf.ru/assets/licences/20080415_info_L_5_page-0001.jpg",
    # # "https://akbf.ru/assets/licences/20080415_info_L_6_page-0001.jpg",
    # # "https://akbf.ru/assets/licences/20090421_info_L_4_page-0001.jpg",
    # "https://akbf.ru/about-us/contacts",
    # "https://akbf.ru/analytics/reviews/all",
    # "https://akbf.ru/education-block/bonuses-and-privileges",
    # "https://api.akbf.ru/file/download/d5d20ecb-f127-4b8b-890a-70d82a24376a.pdf",
    # "https://api.akbf.ru/file/download/6db760ab-4692-4f62-9139-f6c04861b98d.pdf",
    # "https://api.akbf.ru/file/download/c278e7bc-cf95-4d1e-83ab-d43b0183b1f6.pdf",
    # "https://api.akbf.ru/file/download/bf574298-080a-4649-b6d4-61ee7579165f.pdf",
    # "https://api.akbf.ru/file/download/ec48486d-d440-4f41-880f-33da6370a88c.pdf",
    # "https://api.akbf.ru/file/download/8332bfa3-fa21-4406-825c-4441232abfc8.pdf",
    "https://api.akbf.ru/file/download/d166fa06-16d7-4ef4-b98b-50e07b9aa8d7.pdf",
    # "https://api.akbf.ru/file/download/9290e54e-2f8f-4c41-bb01-882185c25c0c.pdf",
    # "https://api.akbf.ru/file/download/d56f1877-2e5a-49b1-82a6-18148330ab68.pdf",
    # "https://api.akbf.ru/file/download/a8d26a46-9da9-44db-9005-d625d563a57b.pdf",
    # "https://api.akbf.ru/file/download/e8b4d507-9a40-4bb3-97fb-54c64dbd08fe.pdf",
    # "https://api.akbf.ru/file/download/8a50d14b-bf6b-4beb-a4bc-c23a88cbb9b5.pdf",
    # "https://api.akbf.ru/file/download/4a5805b3-0d5f-485f-bf63-76d969a97dae.pdf",
    # "https://api.akbf.ru/file/download/54319625-5311-4388-9e30-dd12cffced25.pdf",
    # "https://api.akbf.ru/file/download/55c45fc4-44e1-4d4f-9905-7eeec9a5c613.pdf",
    # "https://api.akbf.ru/file/download/4e5d830d-ca47-40c0-806f-d1774056ce03.pdf",
    # "https://api.akbf.ru/file/download/e6d03c88-19ac-4c17-bd77-02b0dac4a5a5.pdf",
    # "https://api.akbf.ru/file/download/86f84f02-0506-4690-97ff-ea517eacf793.pdf",
    # "https://api.akbf.ru/file/download/69032164-2429-4471-bc53-0b1767016154.pdf",
    # "https://api.akbf.ru/file/download/65606051-92ac-4f72-b363-110bead78e03.pdf",
    # "https://api.akbf.ru/file/download/ff9edc25-25c7-4531-b2e4-459728abbc83.pdf",
    # "https://api.akbf.ru/file/download/244b5218-88b2-49cb-a707-9130a62f2ff3.pdf",
    # "https://api.akbf.ru/file/download/c41f0f91-d537-447c-8f48-392a406a1fc5.pdf",
    # "https://api.akbf.ru/file/download/8343d626-f5ca-4f55-a4ca-1fd98fe6919c.pdf",
    # "https://api.akbf.ru/file/download/be9ae881-a738-4799-a0dc-d3adc3a06ec5.pdf",
    # "https://api.akbf.ru/file/download/543b79f9-6e48-401b-bb5e-35e24084b617.pdf",
    # "https://api.akbf.ru/file/download/2e873ef3-ed1c-4333-9acd-11c2f0a5c938.pdf",
    # "https://api.akbf.ru/file/download/e4c9eeca-a054-47f7-858a-0afff618ec2d.pdf",
    # "https://api.akbf.ru/file/download/eec350e4-5f93-4a28-bab8-c41ac52643ac.pdf",
    # "https://api.akbf.ru/file/download/d4d80adf-de0a-4bce-9eac-55f4a2bb90c3.pdf",
    # "https://api.akbf.ru/file/download/a32d51bb-9796-4179-9302-203ba81d2211.pdf",
    # "https://api.akbf.ru/file/download/5b2d9a1b-6cab-4a10-878c-bd87f262e052.pdf",
    # "https://api.akbf.ru/file/download/37401f93-771b-45bb-98d3-11f920fc19f6.pdf",
    # "https://api.akbf.ru/file/download/ace82ee7-2a52-49c3-ba2c-1a702022d13e.pdf",
    # "https://api.akbf.ru/file/download/d794c436-a44e-45ef-b624-8d1bb2926902.pdf",
    # "https://api.akbf.ru/file/download/be39fb21-b56a-4da2-8fae-9ccb239461dc.pdf",
    # "https://api.akbf.ru/file/download/46192bed-ceba-4fe1-9058-e00d30b510c4.pdf",
    # "https://api.akbf.ru/file/download/2b3f4066-6d8e-494a-9b3e-7e44bb55c7a8.pdf",
    # "https://api.akbf.ru/file/download/8fb26499-819e-4505-a64e-8283cfc613ef.pdf",
    # "https://api.akbf.ru/file/download/b5fb1ddd-7adb-444c-8f80-91bb530cc435.pdf",
    # "https://api.akbf.ru/file/download/10b16119-e048-4347-ab28-397046c3f48d.pdf",
    # "https://api.akbf.ru/file/download/ae0a7632-0738-47b4-9b8f-fc25e08ed48e.pdf",
    # "https://api.akbf.ru/file/download/cd63f933-a522-4f2b-aa35-0e269474cfe3.pdf",
    # "https://api.akbf.ru/file/download/7dc07b2c-77cc-488e-9d79-2f619eacfc57.pdf",
    # "https://api.akbf.ru/file/download/d38a9686-3c30-4e74-890d-aa7d0c7dce82.pdf",
    # "https://api.akbf.ru/file/download/2e72ef8e-0d37-4fac-aee6-c79a66ea173e.pdf",
    # "https://akbf.ru/solutions/mutual-funds/comparison",
    # "https://api.akbf.ru/file/download/4acedb21-3532-4732-bcab-ea8a122d6a25.pdf",
    # "https://akbf.ru/education-block/faq/general-issues",
    # "https://akbf.ru/education-block/faq/trading-account",
    # "https://akbf.ru/education-block/faq/adviser",
    # "https://akbf.ru/education-block/faq/mutual-funds",
    # "https://akbf.ru/education-block/faq/model-portfolios",
    # "https://akbf.ru/education-block/faq/trust-strategies",
    # "https://akbf.ru/education-block/faq/comparison-iis-bs",
    # "https://akbf.ru/education-block/faq/lifehack-individual-investment-account",
    # "https://akbf.ru/education-block/faq/margin-trading",
    # "https://akbf.ru/education-block/faq/ak-bars-trade",
    # "https://akbf.ru/education-block/faq/quik",
    # "https://akbf.ru/education-block/faq/Tax",
    # "https://akbf.ru/education-block/faq/testinvest",
    # "https://akbf.ru/education-block/faq/information-safety",
    # "https://akbf.ru/education-block/faq/individual-investment-account",
    # "https://akbf.ru/education-block/faq/individual-investment-account-3"
]

tmp_folder = 'docs'

# def convert_pdf_to_md(filename):
#     parser = Parser(filename)
#     parser.extract()
#     piles = parser.parse()
#
#     syntax = UrbanSyntax()
#
#     writer = Writer()
#     writer.set_syntax(syntax)
#     writer.set_mode('simple')
#     writer.set_title(filename.replace('.pdf', '')) # Name of file
#     writer.write(piles)
#
#     print('Your markdown is at', writer.get_location())
#
#     return writer.get_location()

def convert_pdf_to_md(filename):
    filepath = os.path.join(tmp_folder, filename)
    parser = Parser(filepath)
    parser.extract()
    piles = parser.parse()

    syntax = UrbanSyntax()

    writer = Writer()
    writer.set_syntax(syntax)
    writer.set_mode('simple')
    writer.set_title(filepath.replace('.pdf', '')) # Name of file
    writer.write(piles)

    print('Your markdown is at', writer.get_location())

    return writer.get_location()

def extract_content_from_pdf(url, rect, show=False):
    response = requests.get(url)
    filename = "PDF_" + os.path.basename(unquote(urlparse(url).path))
    filepath = os.path.join(tmp_folder, filename)
    with open(filepath, "wb") as f:
        f.write(response.content)

    ### Конвертация ПДФ
    loc = convert_pdf_to_md(filename)
    print(loc);
    return ""
    # with fitz.open(filepath) as doc:
    #     text = ''
    #     for page in doc:
    #         page_text = page.get_text('text', clip=fitz.Rect(*rect))
    #         text += remove_unwanted_line_breaks(page_text)  # Применение функции к тексту страницы

    if show:
      print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
      print(text)

    with open(filepath.replace('.pdf', '.txt'), "w") as text_file:
        text_file.write(text)

    return text


def extract_content_from_url(url, show=False):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    if show:
      print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
      print(text)


    filename = "LINK_" + url.split('/')[-1] + ".txt"
    filepath = os.path.join(tmp_folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    return text

def process_links(links):
    folder_path = tmp_folder
    rect = [0, 40, 595, 802]
    shutil.rmtree(folder_path, ignore_errors=True)
    os.makedirs(folder_path, exist_ok=True)
    data = []
    for link in links:
        if link.lower().endswith(".pdf"):
            data.append(extract_content_from_pdf(link, rect))
        else:
            data.append(extract_content_from_url(link))
    return data

def remove_unwanted_line_breaks(text):
    # Удаление случаев, когда есть пробел, перенос строки, и сразу за переносом идет маленькая буква
    text = re.sub(r"", ">", text)
    text = re.sub(r" \n(?=[а-я\(\«)])", " ", text)
    text = re.sub(r"(?<=[\–]) \n(?=[А-Я\(\-])", " ", text)
    text = re.sub(r"(?<=[\>\-]) \n", " ", text)

    # Дальнейшие правила для обработки текста
    # text = re.sub(r'(?<!\.\n)(?<!\n\n)(?<!\.\s)\n(?=[A-ZА-Я])', ' ', text)
    return text


process_links(links)


