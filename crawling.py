import requests
from bs4 import BeautifulSoup


def parsing_beautifulsoup(url):
    """
    뷰티풀 수프로 파싱하는 함수
    :param url: paring할 URL. 여기선 YES24 Link
    :return: BeautifulSoup soup Object
    """

    data = requests.get(url)

    html = data.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def extract_book_data_yes24():
    """
    BeautifulSoup Object에서 book data를 추출하는 함수
    :param soup: BeautifulSoup soup Object
    :return: contents(str)
    """
    
    book_url = "https://www.yes24.com/24/Category/NewProductList/001001003?sumGb=01"
    soup = parsing_beautifulsoup(book_url)

    upload_contents = ''
    new_books = soup.select(".goodsTxtInfo")
    url_prefix = "http://www.yes24.com"

    for new_book in new_books:
        book_name = new_book.select("a")[0].text
        url_suffix = new_book.select("a")[1].attrs['href']
        url = url_prefix + url_suffix
        price = new_book.select(".priceB")[0].text

        content = f"<a href={url}>" + book_name + "</a>" + ", " + price + "<br/>\n"
        upload_contents += content

    return upload_contents


def extract_book_data_aladin():
    """
    BeautifulSoup Object에서 book data를 추출하는 함수
    알라딘 컴퓨터/모바일 섹션 (출간일 4주 이내, 50개 필터링)
    :param soup: BeautifulSoup soup Object
    :return: contents(str)
    """

    book_url = "https://www.aladin.co.kr/shop/common/wnew.aspx?ViewRowsCount=50&ViewType=Detail&SortOrder=6&page=0&BranchType=1&PublishDay=28&CID=351&NewType=SpecialNew&SearchOption="
    soup = parsing_beautifulsoup(book_url)

    upload_contents = ''
    new_books = soup.find_all('div', 'ss_book_list')

    for i, new_book in enumerate(new_books):

        try:
            book_name = new_book.find('a', 'bo3').text + new_book.find('span', 'ss_f_g2').text
        except AttributeError:
            try:
                book_name = new_book.find('a', 'bo3').text
            except AttributeError:
                continue

        url = new_book.find('a', 'bo3').attrs['href']
        price = new_book.find_all('span', {'class': ''})[-1].text

        content = f'<a href="{url}">' + book_name + '</a>' + ', ' + price + '<br/>\n'
        upload_contents += content

    return upload_contents
