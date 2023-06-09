import requests
from lxml import html, etree


page_url = "https://www.softwarestudio.com.pl"#https://wokamid.pl
main_url_name = "softwarestudio.com.pl"#wokamid.pl
baza_rozszerzen = ["jpg", "svg", "png", "ebp", ".js", "peg"]


def get_full_links_base(html_str):
    to_find = "http"
    i = 0
    index_of_links = []
    while i < len(html_str)-len(to_find):
        if html_str[i:i+len(to_find)] == to_find:
            index_of_links.append(i)
        i +=1
    
    links_main_base = []
    for index in index_of_links:
        j = index
        link = ""
        while html_str[j] != '"' and html_str[j] != "'" and html_str[j] != " " and html_str[j] != "?" and html_str[j:j+1] != "\\":
            link += html_str[j]
            j += 1
        if link.find(main_url_name) != -1:
            links_main_base.append(link)
    
    clean_links_base = []
    for i_link in links_main_base:
        if i_link[-3:] not in baza_rozszerzen:
            if "\\\\" not in i_link:
                clean_links_base.append(i_link)
    return clean_links_base

def get_html_str(url_to_get_page):
    try:
        request = requests.get(url_to_get_page, timeout=(3.05, 27))
        if request.status_code == 200:
            page = etree.HTML(request.content)
            html_in_bits = etree.tostring(page)
            html_in_str = str(html_in_bits)
            if "<" in html_in_str:
                return html_in_str
            else:
                return ""
        else:
            return ""
    except:
        return ""

urls_holder = [page_url]
wrong_url = []
good_url = []

while urls_holder != []:
    i = 0
    for link in urls_holder:
        # i += 1
        # print(i)
        html_from_link = get_html_str(link)
        if html_from_link == "":
            wrong_url.append(link)
        else:
            good_url.append(link)
        
    if get_full_links_base(html_from_link) != []:
        holder = get_full_links_base(html_from_link)
    else:
        holder = []
        
    for url_from_holder in holder:
        if url_from_holder not in good_url or url_from_holder not in wrong_url:
            urls_holder.append(url_from_holder)

    urls_holder = [*set(urls_holder)]
    for url in urls_holder:
        if url in wrong_url or url in good_url:
            urls_holder.remove(url)
            
    print(len(good_url))
    # print(urls_holder)
    print(len(wrong_url))
# print(good_url)
# print(wrong_url)

good_url = [*set(good_url)]

import openpyxl

urls_base = openpyxl.Workbook()
urls_base_sheet = urls_base.active

i = 1
for item in good_url:
    urls_base_sheet.cell(column=1, row=i, value=item)
    i+=1
urls_base.save(filename='urls_base.xlsx')