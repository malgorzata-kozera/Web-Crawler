import requests
from bs4 import BeautifulSoup as bs
from requests.exceptions import InvalidSchema, ConnectionError,MissingSchema
import sys

'''
site_map()

Function takes as an argument site base url path (including 'http://') and returns mapping
of that domain as a Python dictionary:
key: URL
* value: dictionary with:
** site title (HTML `<title>` tag)
** links - set of all target URLs within the domain on the page but without anchor links
'''


def site_map(enter_url):

    print('New site map is being created, it may takes a while, if it is a big website, please wait')

    # if given url end with '/' strips it (it prevent double "//").
    if enter_url.endswith('/'):
        enter_url = enter_url.strip('/')

    # empty dictionary which will contain site map

    dictionary = {}
    url_to_do = {enter_url}

    while len(url_to_do) > 0:

        url_base = enter_url
        url = url_to_do.pop()

        if url not in dictionary.keys():

                # takes content of the website
            try:
                r = requests.get(url)
                content = r.content
                soup = bs(content, 'html.parser')

                # empty set with all links from the website

                links = set()

                # searches for title

                title = soup.find_all('title')[0]
                title_text = title.text

                # searches for all links inside this website
                # adding base url to the link name when there is not
                # takes only url of the domain (excluding external links)

                for item in soup.find_all('a', href=True):

                    single_link = item['href']
                    if url_base in single_link:
                        links.add(single_link)
                        url_to_do.add(single_link)

                    elif single_link.startswith('/'):
                        link_ad_base_url = "".join([url_base, single_link])
                        links.add(link_ad_base_url)
                        url_to_do.add(link_ad_base_url)

                # creates a dictionary which is a map of the domain, with new keys and values

                dictionary[url] = {'title': title_text, 'links': links}
            except InvalidSchema as e:
                print(e, file=sys.stderr)
                print("Check once again whether you entered correct domain url (it should include 'http://').")
                exit()
            except ConnectionError as e:
                print(e, file=sys.stderr)
                print("Failed to establish a new connection. Check once again whether you enter correct domain url.")
                exit()
            except MissingSchema as e:
                print(e, file=sys.stderr)
                print("Map can't be created. Check once again whether you entered correct domain url (it should include 'http://').")
                exit()

    return dictionary


if __name__ == '__main__':
    enter_url = input("Please enter a URL (including 'http://'). Then You will receive a map of that domain:\n")
    print(site_map(enter_url))
