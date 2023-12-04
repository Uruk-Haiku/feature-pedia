import requests
import spacy
import json
from bs4 import BeautifulSoup
import random
from unidecode import unidecode
import torch
import torchtext
import time
import csv


#####################################################################
#                       ARTICLE FEATURES                            #
#####################################################################
def get_article_categories(title):
    """Get the number of the categories this article belongs to.
    """
    categories = 0.0

    payload = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "categories",
        "cllimit": "max"
    }

    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    pageid = next(iter(r.json()['query']['pages']))
    data = r.json()['query']['pages'][pageid]

    categories += len(data['categories']) if 'categories' in data else 0.0

    # Make a request for all subsequent pages to grab the rest of the contributors.
    while 'continue' in r.json():
        payload['clcontinue'] = r.json()['continue']['clcontinue']

        r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
        data = r.json()['query']['pages'][pageid]

        categories += len(data['categories'])

    return categories


def get_article_contributors(title):
    """Get the number of contributors for this article.
    """
    contributors = 0.0

    payload = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "contributors",
        "pclimit": "max"
    }

    # Make the first request to grab all of the contributors on the first page.
    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    pageid = next(iter(r.json()['query']['pages']))
    data = r.json()['query']['pages'][pageid]

    contributors += data['anoncontributors'] if 'anoncontributors' in data else 0.0
    contributors += len(data['contributors']) if 'contributors' in data else 0.0

    # Make a request for all subsequent pages to grab the rest of the contributors.
    while 'continue' in r.json():
        payload['pccontinue'] = r.json()['continue']['pccontinue']

        r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
        data = r.json()['query']['pages'][pageid]

        contributors += len(data['contributors'])

    return contributors


def get_article_text(title):
    """Get the content (text) and the length of this article.
    """
    payload = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts|info",
        "exlimit": "max",
        "explaintext": True,
        "exsectionformat": "plain"
    }

    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    pageid = next(iter(r.json()['query']['pages']))
    data = r.json()['query']['pages'][pageid]

    return data['extract'], float(data['length'])


def get_article_sections(title):
    """Get the article section information of this article.
    """
    sections = 0.0

    payload = {
        'action': 'parse',
        'page': title,
        'format': 'json',
        'prop': 'sections'
    }

    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    sections += len(r.json()['parse']['sections'])

    return sections


def get_article_references(title):
    """Get the number of references for this article.
    """
    references = 0.0

    article_title = title.replace(' ', '_')
    page = requests.get(f'https://en.wikipedia.org/wiki/{article_title}')
    soup = BeautifulSoup(page.content, 'html.parser')
    references += len(soup.find_all('span', attrs={'class': 'reference-text'}))

    return references


def get_article_images(title):
    """Get the number of images this article has.
    """
    images = 0.0

    payload = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "images",
        "imlimit": "max"
    }

    # Make the first request to grab all of the images on the first page.
    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    pageid = next(iter(r.json()['query']['pages']))
    data = r.json()['query']['pages'][pageid]

    images += len(data['images']) if 'images' in data else 0.0

    # Make a request for all subsequent pages to grab the rest of the contributors.
    while 'continue' in r.json():
        payload['imcontinue'] = r.json()['continue']['imcontinue']

        r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
        data = r.json()['query']['pages'][pageid]

        images += len(data['images'])

    return images


def get_article_links(title):
    """Get the number of links, external links, and internal links of this article.
    """
    links = 0.0
    extlinks = 0.0
    iwlinks = 0.0

    payload = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "links|extlinks|iwlinks",
        "pllimit": "max",
        "iwlimit": "max",
        "ellimit": "max"
    }

    # Make the first request to grab all of the links on the first page.
    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    pageid = next(iter(r.json()['query']['pages']))
    data = r.json()['query']['pages'][pageid]

    links += len(data['links']) if 'links' in data else 0.0
    extlinks += len(data['extlinks']) if 'extlinks' in data else 0.0
    iwlinks += len(data['iwlinks']) if 'iwlinks' in data else 0.0

    # Make a request for all subsequent pages to grab the rest of the contributors.
    while 'continue' in r.json():
        addLinks = False
        addExtLinks = False
        addIwLinks = False

        if 'plcontinue' in r.json()['continue']:
            payload['plcontinue'] = r.json()['continue']['plcontinue']
            addLinks = True

        if 'elcontinue' in r.json()['continue']:
            payload['elcontinue'] = r.json()['continue']['elcontinue']
            addExtLinks = True

        if 'iwcontinue' in r.json()['continue']:
            payload['iwcontinue'] = r.json()['continue']['iwcontinue']
            addIwLinks = True

        r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
        data = r.json()['query']['pages'][pageid]

        if addLinks:
            links += len(data['links'])

        if addExtLinks:
            extlinks += len(data['extlinks'])

        if addIwLinks:
            iwlinks += len(data['iwlinks'])

    return links, extlinks, iwlinks


def get_links_to_article(title):
    """Get the number of articles that link to this article
    """
    linkshere = 0.0

    payload = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "linkshere",
        "lhlimit": "max"
    }

    # Make the first request to grab all of the links on the first page.
    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    pageid = next(iter(r.json()['query']['pages']))
    data = r.json()['query']['pages'][pageid]

    linkshere += len(data['linkshere']) if 'linkshere' in data else 0.0

    # Make a request for all subsequent pages to grab the rest of the contributors.
    while 'continue' in r.json():
        payload['lhcontinue'] = r.json()['continue']['lhcontinue']

        r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
        data = r.json()['query']['pages'][pageid]

        linkshere += len(data['linkshere'])

    return linkshere


def get_article_views(title):
    """Get the number of page views for this article in the last 60 days.
    """
    pageviews = 0.0

    payload = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "pageviews"
    }

    # Make the first request to grab all of the links on the first page.
    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)

    if 'error' in r.json():
        return pageviews

    pageid = next(iter(r.json()['query']['pages']))
    data = r.json()['query']['pages'][pageid]

    for date in data['pageviews']:
        views = data['pageviews'][date]
        pageviews += views if type(views) == int else 0.0

    return pageviews


def get_article_redirects(title):
    """Get the number of pages that redirect to this article.
    """
    redirects = 0.0

    payload = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "redirects",
        "rdlimit": "max"
    }

    # Make the first request to grab all of the links on the first page.
    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    pageid = next(iter(r.json()['query']['pages']))
    data = r.json()['query']['pages'][pageid]

    redirects += len(data['redirects']) if 'redirects' in data else 0.0

    # Make a request for all subsequent pages to grab the rest of the contributors.
    while 'continue' in r.json():
        payload['rdcontinue'] = r.json()['continue']['rdcontinue']

        r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
        data = r.json()['query']['pages'][pageid]

        redirects += len(data['redirects'])

    return redirects


def get_article_revisions(title):
    """Get the number of edits for this article.
    """
    revisions = 0.0

    payload = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "revisions",
        "rvlimit": "max"
    }

    # Make the first request to grab all of the links on the first page.
    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    pageid = next(iter(r.json()['query']['pages']))
    data = r.json()['query']['pages'][pageid]

    revisions += len(data['revisions']) if 'revisions' in data else 0.0

    # Make a request for all subsequent pages to grab the rest of the contributors.
    while 'continue' in r.json():
        payload['rvcontinue'] = r.json()['continue']['rvcontinue']

        r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
        data = r.json()['query']['pages'][pageid]

        revisions += len(data['revisions'])

    return revisions


def get_article_sentences(text):
    """Get the number of sentences in this article.
    """
    sentences = 0.0

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences += len(list(doc.sents))

    return sentences


def get_article_embedding(text):
    """Get the article's embedding vector.
    """
    # processing
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # TODO determine preprocessing methods
    filtered_tokens = [unidecode(token.lemma_.lower()) for token in doc if
                       not (token.is_stop or token.is_punct or token.is_space)]  # Remove crap

    # Torch
    dim = 100  # TODO HYPER PARAMETER
    glove = torchtext.vocab.GloVe(name="6B",  # trained on Wikipedia 2014 corpus
                                  dim=dim)  # Embedding size = 50
    n = 0
    accumulator = torch.zeros(dim)
    for token in filtered_tokens:
        accumulator += glove[token]
        n += 1

    # Average embedding vector for all the KEY words in the article.
    embedding_vector = accumulator / n

    return embedding_vector


#####################################################################
#                        DATA COLLECTION                            #
#####################################################################
def get_featured_article_titles():
    """Get all of the featured article titles on Wikipedia.
    """
    featured_dictionary = {}
    featured_list = []

    payload = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": "Category:Featured articles",
        "cmlimit": "max"
    }

    # Make the first request to grab all of the featured articles on the first page.
    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    featured_list.extend(article['title'] for article in r.json()['query']['categorymembers'])
    featured_dictionary.update(
        {article['title']: 1 for article in r.json()['query']['categorymembers']})

    # Make a request for all subsequent pages to grab the rest of the featured articles.
    while 'continue' in r.json():
        payload['cmcontinue'] = r.json()['continue']['cmcontinue']

        r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
        featured_list.extend(article['title'] for article in r.json()['query']['categorymembers'])
        featured_dictionary.update(
            {article['title']: 1 for article in r.json()['query']['categorymembers']})

    return featured_dictionary, featured_list


def get_regular_article_titles(num_articles, featured_dictionary):
    """Get num_artciles article titles on Wikipedia.
    """
    i = 0
    article_dictionary = {}
    article_list = []

    payload = {
        'action': 'query',
        'format': 'json',
        'list': 'random',
        'rnnamespace': 0  # 0 for articles
    }

    while len(article_list) != num_articles:
        # Make the request to grab the article title.
        r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
        title = r.json()['query']['random'][0]['title']

        # Check if the article is not a duplicate and not featured.
        if title not in article_dictionary and title not in featured_dictionary:
            article_dictionary[title] = 0
            article_list.append(title)

        # print the number of articles retrieved so far.
        if i % 100 == 0:
            print("Retrieved %d articles" % (i))
        i += 1

    return article_dictionary, article_list


def get_article_data(title):
    """Get all the necessary features about a single Wikipedia article
    and save it as a vector. The format is as follows:

    [
        0. categories
        1. contributors
        2. extlinks
        3. images
        4. iwlinks
        5. length
        6. links
        7. links to article
        8. views
        9. redirects
        10. references
        11. revisions
        12. sections
        13. sentences
        14 - 113. vector embedding
    ]
    """
    article = []

    # Get all of the multi-return values of this article.
    links, extlinks, iwlinks = get_article_links(title)
    text, length = get_article_text(title)
    embedding_vector = get_article_embedding(text)

    # Add all of the features to the article vector.
    article.append(get_article_categories(title))
    article.append(get_article_contributors(title))
    article.append(extlinks)
    article.append(get_article_images(title))
    article.append(iwlinks)
    article.append(length)
    article.append(links)
    article.append(get_links_to_article(title))
    article.append(get_article_views(title))
    article.append(get_article_redirects(title))
    article.append(get_article_references(title))
    article.append(get_article_revisions(title))
    article.append(get_article_sections(title))
    article.append(get_article_sentences(text))
    article.extend(embedding_vector.tolist())

    return article


#####################################################################
#                       SAVING DATA COLLECTION                      #
#####################################################################
def save_list_to_file(filename, lst):
    """Save a Python list in JSON format to a file.
    """
    with open(filename, "w") as fp:
        json.dump(lst, fp)


def read_list_from_file(filename):
    """Read in a list from a file into Python.
    """
    with open(filename, 'rb') as fp:
        lst = json.load(fp)
        return lst


if __name__ == "__main__":
    # 1. Save all of the articles being used for this machine learning model.
    # 1.1 Get all of the featured article titles and save them to a file.
    # featured_dictionary, featured_list = get_featured_article_titles()
    # save_list_to_file("titles_featured.json", featured_list)

    # 1.2 Get all of the regular article titles and save them to a file.
    # regular_dictionary, regular_list = get_regular_article_titles(10000, lst)
    # save_list_to_file("titles_regular.json", regular_list)

    # 2. Get all of the data for all of the articles being used.
    # 2.1 Get the data for all of the featured articles and save them to a file.
    # featured_titles = read_list_from_file("titles_featured.json")

    # with open('articles_featured.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)

    #     for i in range(len(featured_titles)):
    #         writer.writerow(get_article_data(featured_titles[i]))

    #         # print to show how the process is going.
    #         if i % 100 == 0:
    #             print("Retrieved %d articles" % (i))

    # 2.2 Get the data for all of the regular articles and save them to a file.
    # regular_titles = read_list_from_file("titles_regular.json")

    # with open('articles_regular.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)

    #     for i in range(len(regular_titles)):
    #         writer.writerow(get_article_data(regular_titles[i]))

    #         # print to show how the process is going.
    #         if i % 100 == 0:
    #             print("Retrieved %d articles" % (i))

    # 3. Get all of the featured and regular article data into memory.
    featured_articles = []
    with open('articles_featured.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            featured_articles.append(row)

    regular_articles = []
    with open('articles_regular.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            regular_articles.append(row)

    print("number of featured articles:", len(featured_articles))
    print("number of regular articles:", len(regular_articles))
