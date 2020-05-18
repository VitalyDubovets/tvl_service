import re


def get_unique_domains_from_links(links: list) -> list:
    unique_domains = set()
    for link in links:
        link = re.sub(r'^http[s]?://', '', link)
        link = re.sub(r'^www.', '', link)
        link = re.findall(r'^\w*.\w*', link)
        unique_domains.add(link[0])
    return list(unique_domains)
