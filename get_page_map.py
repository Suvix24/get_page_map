import requests
from lxml import html, etree


page_url = "https://wokamid.pl"#https://www.softwarestudio.com.pl"
main_url_name = "wokamid.pl"#softwarestudio.com.pl"
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
        request = requests.get(url_to_get_page)
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
i = 0
while urls_holder != []:
    last_url = urls_holder[0]
    html_str_in_processing = get_html_str(last_url)
    if html_str_in_processing in wrong_url or html_str_in_processing in good_url:
        wrong_url.append(html_str_in_processing)
        html_str_in_processing = ""
        continue
    if html_str_in_processing == "":
        wrong_url.append(last_url)
        urls_holder.remove(last_url)
    else:
        if last_url not in good_url:
            good_url.append(last_url)
             
        holder = get_full_links_base(html_str_in_processing)
        # if i == 40:
        #     print(holder)
        for link in holder:
            if link not in urls_holder:
                urls_holder.append(link)
                
        for link in urls_holder:
            if link in wrong_url or link in good_url:
                urls_holder.remove(link)
    
    # i+=1
    # if i == 100:
    #     print(urls_holder)
    #     break
    
    urls_holder = list(dict.fromkeys(urls_holder))
    print("wrong_url {}".format(wrong_url))
    print("good_url {}".format(good_url))
    print("urls_holder {}".format(urls_holder))
    print("holder {}".format(holder))
    # print(len(urls_holder))
    # print(len(good_url))
    

print(good_url)
print(len(good_url))





