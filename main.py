import streamlit as st

import requests # Needed to connect to the website
from bs4 import BeautifulSoup # Extracts the html from website
from lxml import etree # Converts the html into readable format
import openpyxl
import pandas as pd

st.title('Name Popularity Check')

headers = {'User-Agent': 'python-requests/2.27.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}

uploaded_file = st.file_uploader("Upload your name list:")

if st.button('GO'):

    df1 = pd.read_excel(uploaded_file, engine='openpyxl')

    namelist = []
    popularitylist = []

    progress_text = "Scraping Popularity..."
    my_bar = st.progress(0, text=progress_text)
    total = len(df1)

    for index, row in df1.iterrows():

        my_bar.progress(index/total, text=progress_text)

        name = row[0]
        # Connects to the website for each name
        url = 'https://www.popular-babynames.com/name/' + name
        st.write(url)
        try:
            response = requests.get(url, headers=headers, timeout=5)
        except:
            continue

        # Convert the html
        soup = BeautifulSoup(response.content, "html.parser")
        root = etree.HTML(str(soup))

        # Find the popularity value
        elements = root.xpath('//*[@id="aspnetForm"]/div[5]/div/div[1]/div[3]/p/strong[3]')

        # If there is no popularity value (or the name is not available) make the popularity 0.
        if elements == []:
            namelist.append(name)
            popularitylist.append(0)
            continue

        # Else, set the popularity value
        text = elements[0].text
        text = text.replace(",", "")
        namelist.append(name)
        popularitylist.append(text)


    my_bar.empty()
    st.success('All good. Excel was saved to your folder.')
    st.balloons()

    df = pd.DataFrame(list(zip(namelist, popularitylist)),
                      columns=['Name', 'Popularity'])

    df.to_excel("Popularity_Check.xlsx", index=False)

