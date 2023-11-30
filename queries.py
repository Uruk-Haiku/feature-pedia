import requests
import spacy
from bs4 import BeautifulSoup

def get_all_featured_articles():
  """Get all of the featured articles on Wikipedia.
  """
  featured_articles = []

  payload = {
    "action": "query",
    "format": "json",
    "list": "categorymembers",
    "cmtitle": "Category:Featured articles",
    "cmlimit": "max"
  }

  # Make the first request to grab all of the featured articles on the first page.
  r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
  featured_articles.extend(article['title'] for article in r.json()['query']['categorymembers'])

  # Make a request for all subsequent pages to grab the rest of the featured articles.
  while 'continue' in r.json():
    payload['cmcontinue'] = r.json()['continue']['cmcontinue']

    r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
    featured_articles.extend(article['title'] for article in r.json()['query']['categorymembers'])

  return featured_articles


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
  """Get the content (text) for this article.
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
  return r.json()['parse']['sections']


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
  """Get the number of all links, external links, and internal links of this article.
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


def get_article_page_views(title):
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


def get_article_page_redirects(title):
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


def get_article_page_revisions(title):
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


def get_article_data(title):
  """Get all the necessary data about an article.
  """
  article = {}

  article['categories'] = get_article_categories(title)
  article['contributors'] = get_article_contributors(title)
  article['images'] = get_article_images(title)
  article['links'] = get_article_links(title)
  article['links to article'] = get_links_to_article(title)
  article['page views'] = get_article_page_views(title)
  article['redirects'] = get_article_page_redirects(title)
  article['revisions'] = get_article_page_revisions(title)
  article['text'], article['length'] = get_article_text(title)
  article['sections'] = get_article_sections(title)
  article['references'] = get_article_references(title)

  return article


def text_processing(text):
  """analyze the text using SpaCy.
  """
  nlp = spacy.load("en_core_web_sm")
  doc = nlp(text)

  return len(list(doc.sents))


def get_article_titles():
  """Get article titles from Wikipedia.
  """
  # change when we actually get dataset
  num = 10
  articles = []

  payload = {
    'action': 'query',
    'format': 'json',
    'list': 'random',
    'rnnamespace': 0,  # 0 for articles
    'rnlimit': num   # Number of random articles
  }

  # Make the request to grab article titles.
  r = requests.get("https://en.wikipedia.org/w/api.php", params=payload)
  articles.extend(article['title'] for article in r.json()['query']['random'])

  return articles


if __name__ == "__main__":
  # featured_articles = get_all_featured_articles()
  articles = get_article_titles()

  dataset = []

  for article in articles:
    dataset.append(get_article_data(article))

  print(len(dataset))
  
  # data = get_article_images(articles[0])
  # print(data)
