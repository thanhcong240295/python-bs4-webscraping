from typing import List
from requests import get
from bs4 import BeautifulSoup

class WebCom:
    def  __init__(self, html_content: str = '') -> None:
        self.content = html_content
        self.result = []

    def execute(self) -> List[List[str]]:
        self._get_urls()
        return self.result

    def _get_product_attribute(self, html: str) -> {}:
        product_detail_html = html.find_all('div', { 'class': 'chitietsanpham' })
        image = f"https://web.com/{html.find('div', { 'class': 'hinhchitiet' }).find('a')['href']}"

        result = {
            'product_name':  html.find('h1', { "class": 'vcard fn' }).text,
            'product_code': product_detail_html[0].find('span').text,
            'mspr': self._convert_price_to_number(product_detail_html[3].find('span').text),
            'standard_price':  self._convert_price_to_number(product_detail_html[1].find('span').text),
            'description': html.find('div', { 'class': 'noidung' }),
            'image_url': image,
            'in_stock': product_detail_html[5].text == 'Tình trạng: Còn hàng',
        }
        return result
    
    def _convert_price_to_number(self, price: str) -> float:
        return price.replace(' đ', '').replace('.', '')
    
    def _get_urls(self) -> List[str]:
        cats = self._get_cats()

        for index in range(len(cats)):
            cat_id = cats[index]['value']

            if cat_id != '':
              sub_cats = self._get_sub_cats(cat_id)

              for sub_cat_idx in range(len(sub_cats)):
                sub_cat_id = sub_cats[sub_cat_idx]['value']
                if sub_cat_id != '':
                    products = self._get_pagination(f'https://web.com/index.php?com=tim-kiem&id_list={cat_id}&id_cat={sub_cat_id}')
                    for product_idx in range(len(products)):
                        self.result.append([
                          cat_id,
                          cats[index].text,
                          sub_cat_id,
                          sub_cats[sub_cat_idx].text,
                          products[product_idx]['product_code'],
                          products[product_idx]['product_name'],
                          products[product_idx]['mspr'],
                          products[product_idx]['standard_price'],
                          products[product_idx]['description'],
                          products[product_idx]['image_url'],
                          products[product_idx]['in_stock']
                      ])

    
    def _get_cats(self) -> List[str]:
        return self.content.find(id="id_list").find_all('option')
    
    def _get_sub_cats(self, parent_cat_id: str):
        url: str = f'https://web.com/index.php?com=tim-kiem&id_list={parent_cat_id}'
        html_content = get(url, timeout=500).content
        html = BeautifulSoup(html_content, features="html.parser")
        return html.find(id="id_cat").find_all('option')
    
    def _get_pagination(self, url: str) -> List[dict]:
        html_content = get(url, timeout=500).content
        html = BeautifulSoup(html_content, features="html.parser")
        list_pagination = html.find("ul", { "class": "pagination" })
        result = []
        
        if list_pagination is not None:
            list_pagination = list_pagination.find_all('li')

            for pagination in range(len(list_pagination)):
                a_tag = list_pagination[pagination].find('a')
                current = list_pagination[pagination].find('a', { "class": "current" })

                if a_tag is None:
                    continue

                current_page_url = f'{url}&amp;page={a_tag.string}'
                if current is None:
                    current_page_url = a_tag['href']

                html_content = get(current_page_url, timeout=500).content
                html = BeautifulSoup(html_content, features="html.parser")

                all_product = html.find_all('div', { 'class': "ten-product" })

                for index in range(len(all_product)):
                    product_detail_url = all_product[index].find('h3').find('a')['href']
                    product_detail_html_content = get(f'https://web.com/{product_detail_url}', timeout=500).content
                    product_detail_html = BeautifulSoup(product_detail_html_content, features="html.parser")
                    result.append(self._get_product_attribute(product_detail_html))

        return result
