import requests
from lxml import html, etree


page_url = "https://www.softwarestudio.com.pl"
main_url_name = "softwarestudio.com.pl"


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
        if i_link[-3:] != "jpg" and i_link[-3:] != "svg" and i_link[-3:] != "png" and i_link[-3:] != "ebp" and i_link[-3:] != ".js" and i_link[-3:] != "peg":
            if "\\\\" not in i_link:
                clean_links_base.append(i_link)
    return clean_links_base


all_links = []
check_links = []
bad_links = []
check_links.append(page_url)
while check_links != []:
    for i in check_links:
        if i in bad_links:
            check_links.remove(i)
    try:
        check_link = check_links[0]
    except:
        continue
    
    check_links.remove(check_link)
    bad_links.append(check_link)
    try:
        request = requests.get(check_link)
    except:
        continue
    if request.status_code == 200:
        all_links.append(check_link)
        page = etree.HTML(request.content)
        html_in_bits = etree.tostring(page)
        html_in_str = str(html_in_bits)
        
        clean_links = get_full_links_base(html_in_str)

        for link in clean_links:
            if link not in all_links and link not in check_links:
                check_links.append(link)
                bad_links.append(link)

    else:
        print("Request fail!" + check_link)
        bad_links.append(check_link)

    print(len(check_links))
    print(len(all_links))

print(all_links)
print(check_links)