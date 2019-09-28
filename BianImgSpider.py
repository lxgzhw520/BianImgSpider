# _*_ coding:UTF-8 _*_
# 开发人员: 理想国真恵玩-张大鹏
# 开发团队: 理想国真恵玩
# 开发时间: 2019/9/27 15:39
# 文件名称: BianImgSpider.py
# 开发工具: PyCharm

import requests, os, time
from bs4 import BeautifulSoup


# 1.准备url和请求头
# 2.发送get,获取响应数据,转换为html
# 3.提取本页图片和下一页地址
# 4.保存图片
# 5.循环执行第三步操作
class BianImgSpider:
    def __init__(self, url, base_url='http://pic.netbian.com'):
        self.base_url = base_url
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"}
        self.has_next = True  # 判断是否有下一页

    def get_html(self):
        """
        获取url地址的html源码
        :return: html源码
        """
        response = requests.get(self.url, headers=self.headers)
        response.encoding = 'gbk'
        return response.text

    def get_imgs_next_url(self):
        """
        获取图片本页的图片列表和下一页的地址
        :return: 图片列表,下一页url
        """
        print("正在爬取网页:", self.url)
        html = self.get_html()
        # print(html)
        # exit()
        soup = BeautifulSoup(html, 'lxml')
        img_list = soup.select('.slist ul li a img')
        # print(img_list)
        # 提取图片的src,装进列表
        imgs = []
        for i in img_list:
            src = i['src']
            src = self.base_url + src
            # print(src)
            # exit()
            imgs.append(src)
        # 提取下一页
        try:
            # next_url = soup.select('.page > a:nth-child(13)')[0]
            # print(next_url['href'])
            # exit()
            # 找到page
            page = soup.select('.page')[0]
            # print(page, type(page))
            # 下一页是最后一个a
            # print(page.a)
            # print(page.contents)
            # print(page.contents[-1])
            href = page.contents[-1]['href']
            # print(href)
            next_url = self.base_url + href
            # print(next_url)
            return next_url, imgs
        except:
            print("没有下一页了")
            # 告知没有下一页了,方便操作
            self.has_next = False

    def save_img(self, imgs):
        """
        保存列表中的图片
        :param imgs: 图片列表
        :return: True
        """
        try:
            for img in imgs:
                # 提取图片名字
                # print(type(img))
                img_name = img.split('/')[-1]
                # print(img_name)
                # 设置图片保存地址
                save_path = 'imgs'
                if not os.path.exists(save_path):
                    os.mkdir(save_path)
                response = requests.get(img, headers=self.headers)
                # 获取图片流
                with open(save_path + "/" + img_name, 'wb') as f:
                    # 每次读写1M数据
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                # exit()
            print("一个图片列表被保存成功")
            return True
        except:
            print("保存失败")
            return False

    def run(self):
        """
        运行爬虫,保存图片
        :return: 成功返回True,失败返回False
        """
        try:
            while self.has_next:
                next_url, imgs = self.get_imgs_next_url()
                # print(imgs)
                # print(next_url)
                # 保存图片pip
                self.save_img(imgs)
                # 将url改为下一页的url
                self.url = next_url
                # 文明爬取,每爬取一页,休息一秒钟,防止破坏服务器
                time.sleep(1)
            return True
        except:
            print("保存图片失败")
            return False


if __name__ == '__main__':
    spider = BianImgSpider('http://pic.netbian.com/index_5.html')
    spider.run()
