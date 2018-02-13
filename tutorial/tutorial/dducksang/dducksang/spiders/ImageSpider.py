# image_spider.py 
# https://doc.scrapy.org/en/latest/intro/tutorial.html 
import scrapy 
class ImageSpider(scrapy.Spider): 
    name = "raingall" 
    start_urls = ['http://gall.dcinside.com/board/lists/?id=rain&page=1&exception_mode=recommend'] 
    # 현재 페이지의 공지글을 제외하고 게시판의 모든 글을 추출 
    def parse(self, response): 
        for post in response.css('td.t_subject'): 
            next_post = post.css('a:not(.icon_notice)::attr(href)').extract_first() 
            if next_post is not None:
                next_post = response.urljoin(next_post)
                yield scrapy.Request(next_post, callback=self.parse_img)

        # 현재 페이지가 완료되면 다음 페이지로 넘어가서 추출
        next_page = response.css('div#dgn_btn_paging a.on+a::attr(href)').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    # 게시글안의 이미지를 모두 추출
    def parse_img(self, response):
        for link in response.css('div.s_write'):
            post_link = response.url
            img_list = link.css('img::attr(src)').extract()

            # json 포맷으로 저장
            for img in img_list:
                if img is not None:
                    yield {
                        'info': {
                            'img': img,
                            'link': post_link }
                    }


