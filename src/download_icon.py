import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import cairosvg



def get_icon_urls(page_url):
    response = requests.get(page_url)
    icons = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找所有可能的图标链接
        icon_links = soup.find_all('link', rel='icon')
        for link in icon_links:
            if link.has_attr('href'):
                full_url = urljoin(page_url, link['href'])
                icons.append(full_url)
    return icons

def save_icon(icon_url, default_name):
    response = requests.get(icon_url)
    if response.status_code == 200:
        # 从URL或Content-Type猜测文件扩展名
        content_type = response.headers.get('content-type')
        if '.' in icon_url:
            extension = icon_url.rsplit('.', 1)[1].split('?')[0]
        elif content_type:
            extension = content_type.split('/')[-1]
        else:
            extension = 'ico'  # 默认扩展名

        if extension == 'svg':
            cairosvg.svg2png(bytestring=response.content, write_to=f'{default_name}.png')
        else:   
            file_name = f"{default_name}.{extension}"

            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f'Icon saved as {file_name}')
    else:
        print(f'Failed to retrieve the icon from {icon_url}')


def save_svg_as_png(svg_url, file_name):
    response = requests.get(svg_url)
    if response.status_code == 200:
        # 将SVG内容转换为PNG
        cairosvg.svg2png(bytestring=response.content, write_to=f'{file_name}.png')
        print(f'SVG has been converted and saved as {file_name}.png')
    else:
        print('Failed to retrieve the SVG')

def down_load_icon(name, url):
    # 主执行流程
    icons = get_icon_urls(url)
    if icons:
        for i, icon_url in enumerate(icons):
            save_icon(icon_url, f'{name}_{i}')
    else:
        print('No icons found on the page')


if __name__ == '__main__':
    import fire
    fire.Fire(down_load_icon)


