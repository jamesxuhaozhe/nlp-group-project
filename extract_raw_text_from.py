import sys
import newspaper
from newspaper import Article

FILE_EXT = '.txt'

def check_arg():
    if len(sys.argv) != 2:
        print 'You have to specify the news source. Run it like the following\
        python get_raw_text_from.py http://cnn.com'
        sys.exit()

def get_raw_text():
    """Top level caller."""

    for url in get_popular_news_urls():
        paper = get_paper_from_url(url)
        paper_text_list = get_text_from_paper(paper)
        create_file_for_paper(paper.brand, paper_text_list)
        print '-----------------------------------------------'

def get_popular_news_urls():
    """Return Popular news urls.
    - Input type: void
    - Return type: list"""

    urls = [sys.argv[1]]
    print 'We are processing %d of urls' % len(urls)

    return urls

def get_paper_from_url(url):
    """Return a build for the given url
    - Input type: url string
    - Return type: paper
    """

    paper = newspaper.build(url)
    print 'Successfully built %s.' % paper.brand

    return paper

def get_text_from_paper(paper):
    """Return a large text body from the given paper.
    - Note: No more than 10 articles from the given paper is processed.
    - Input: paper - paper build
    - Return: text body list from paper."""

    print 'Starting generating text for %s.' % paper.brand
    paper_text_list = []
    print 'There are %d articles in this sources.' % len(paper.articles)
    for article in paper.articles:
        paper_text_list.append(get_text_from_article(article))
    print 'Finished generating text for %s, and %d articles are included.' % (paper.brand, len(paper_text_list))

    return paper_text_list

def get_text_from_article(article):
    """Return a text body from the given article.
    - Input: article - article handle
    - Return: text from the article string"""

    text = ''
    try:
        article.download()
        article.parse()
        text = article.text
    except:
        print 'Something is wrong when extracting text.'
        pass

    return text

def create_file_for_paper(paper_brand, paper_text_list):
    """Create a text file for the given paper brand and with its text body.
    - Note: file will be named as brand.txt
    - Input: paper_brand - string brand of the paper, for cnn, it will be 'cnn'
             paper_text_list - list contains all the text from the given news brand.
    - Return: no value will be returned but only file will be created."""

    try:
        with open(paper_brand + FILE_EXT, 'w') as f:
            if paper_text_list:
                f.write('\n'.join(paper_text_list).encode('utf-8').strip())
                print 'Successfully created file for %s.' % paper_brand
    except IOError:
        print 'Something is wrong when creating file for %s.' % paper_brand

if __name__ == '__main__':
    check_arg()
    get_raw_text()