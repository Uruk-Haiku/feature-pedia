import requests
import spacy
import json
from bs4 import BeautifulSoup
import random

#####################################################################
#                       ARTICLE FEATURES                            #
#####################################################################
def get_article_categories(title):
  """Get the number of the categories this article belongs to.
  """
  categories = 0

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

  categories += len(data['categories']) if 'categories' in data else 0

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
  contributors = 0

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

  
  contributors += data['anoncontributors'] if 'anoncontributors' in data else 0
  contributors += len(data['contributors']) if 'contributors' in data else 0

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

  return data['extract'], data['length']


def get_article_sections(title):
  """Get the article section information of this article.
  """
  payload = {
    'action': 'parse',
    'page': title,
    'format': 'json',
    'prop': 'sections'
  }

  r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
  return len(r.json()['parse']['sections'])


def get_article_references(title):
  """Get the number of references for this article.
  """
  article_title = title.replace(' ', '_')

  page = requests.get(f'https://en.wikipedia.org/wiki/{article_title}')
  soup = BeautifulSoup(page.content,'html.parser')

  return len(soup.find_all('span', attrs={'class':'reference-text'}))


def get_article_images(title):
  """Get the number of images this article has.
  """
  images = 0

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

  images += len(data['images']) if 'images' in data else 0

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
  links = 0
  extlinks = 0
  iwlinks = 0

  payload = {
    "action": "query",
    "format": "json",
    "titles": title,
    "prop": "links|iwlinks|extlinks",
    "pllimit": "max",
    "iwlimit": "max",
    "ellimit": "max"
  }

  # Make the first request to grab all of the links on the first page.
  r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
  pageid = next(iter(r.json()['query']['pages']))
  data = r.json()['query']['pages'][pageid]

  links += len(data['links']) if 'links' in data else 0
  iwlinks += len(data['iwlinks']) if 'iwlinks' in data else 0
  extlinks += len(data['extlinks']) if 'extlinks' in data else 0

  # Make a request for all subsequent pages to grab the rest of the contributors.
  while 'continue' in r.json():
    addLinks = False
    addIwLinks = False
    addExtLinks = False

    if 'plcontinue' in r.json()['continue']:
      payload['plcontinue'] = r.json()['continue']['plcontinue']
      addLinks = True

    if 'iwcontinue' in r.json()['continue']:
      payload['iwcontinue'] = r.json()['continue']['iwcontinue']
      addIwLinks = True

    if 'elcontinue' in r.json()['continue']:
      payload['elcontinue'] = r.json()['continue']['elcontinue']
      addExtLinks = True

    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    data = r.json()['query']['pages'][pageid]

    if addLinks:
      links += len(data['links'])

    if addIwLinks:
      iwlinks += len(data['iwlinks'])

    if addExtLinks:
      extlinks += len(data['extlinks'])

  return links, iwlinks, extlinks


def get_links_to_article(title):
  """Get the number of articles that link to this article
  """
  linkshere = 0

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

  linkshere += len(data['linkshere']) if 'linkshere' in data else 0

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
  pageviews = 0

  payload = {
    "action": "query",
    "format": "json",
    "titles": title,
    "prop": "pageviews"
  }

  # Make the first request to grab all of the links on the first page.
  r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
  pageid = next(iter(r.json()['query']['pages']))
  data = r.json()['query']['pages'][pageid]

  for date in data['pageviews']:
    views = data['pageviews'][date]
    pageviews += views if type(views) == int else 0

  return pageviews


def get_article_redirects(title):
  """Get the number of pages that redirect to this article.
  """
  redirects = 0

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

  redirects += len(data['redirects']) if 'redirects' in data else 0

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
  revisions = 0

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

  revisions += len(data['revisions']) if 'revisions' in data else 0

  # Make a request for all subsequent pages to grab the rest of the contributors.
  while 'continue' in r.json():
    payload['rvcontinue'] = r.json()['continue']['rvcontinue']

    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    data = r.json()['query']['pages'][pageid]

    revisions += len(data['revisions'])

  return revisions


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
  featured_dictionary.update({article['title']:1 for article in r.json()['query']['categorymembers']})

  # Make a request for all subsequent pages to grab the rest of the featured articles.
  while 'continue' in r.json():
    payload['cmcontinue'] = r.json()['continue']['cmcontinue']

    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    featured_list.extend(article['title'] for article in r.json()['query']['categorymembers'])
    featured_dictionary.update({article['title']:1 for article in r.json()['query']['categorymembers']})

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
      print("Retrieved %d articles" %(i))
    i += 1

  return article_dictionary, article_list


def get_article_data(title):
  """Get all the necessary data about a single Wikipedia article.
  """
  article = {}

  # Add 1 if featured, 0 if regular
  article['categories'] = get_article_categories(title)
  article['contributors'] = get_article_contributors(title)
  article['images'] = get_article_images(title)
  article['links'], article['iwlinks'], article['extlinks'] = get_article_links(title)
  article['links to article'] = get_links_to_article(title)
  article['page views'] = get_article_views(title)
  article['redirects'] = get_article_redirects(title)
  article['revisions'] = get_article_revisions(title)
  # find a way to numerically represent the text (using spaCy?)
  # article['text'], article['length'] = get_article_text(title)
  article['sections'] = get_article_sections(title)
  article['references'] = get_article_references(title)

  return article


def text_processing(text):
  """analyze the text using SpaCy.
  """
  nlp = spacy.load("en_core_web_sm")
  doc = nlp(text)

  return len(list(doc.sents))


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

  # Test if the data collection for a single article works
  regular_titles = read_list_from_file("titles_regular.json")

  i = random.randrange(10000)

  for i in range(100):
    data = get_article_data(regular_titles[i])
    print(data)
