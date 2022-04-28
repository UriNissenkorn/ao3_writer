import scrapy


class Ao3Spider(scrapy.Spider):
    name = 'ao3'
    allowed_domains = ['archiveofourown.org']
    start_urls = [ # using single chapter and english language
            'https://archiveofourown.org/works/search?work_search%5Bquery%5D=&work_search%5Btitle%5D=&work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bsingle_chapter%5D=1&work_search%5Bword_count%5D=&work_search%5Blanguage_id%5D=en&work_search%5Bfandom_names%5D=&work_search%5Brating_ids%5D=&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&work_search%5Bsort_column%5D=_score&work_search%5Bsort_direction%5D=desc&commit=Search'
        ]

    def parse(self, response):
        story_links = response.css('ol.work>li h4.heading a[href*=work]::attr(href)').getall()
        story_links = [link+'?view_adult=true' for link in story_links]
        yield from response.follow_all(story_links, self.parse_story)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


    def parse_story(self, response):
        yield {
            "rating":response.css('dd.rating a.tag::text').getall(),
            "warning":response.css('dd.warning a.tag::text').getall(),
            "category":response.css('dd.category a.tag::text').getall(),
            "fandom":response.css('dd.fandom a.tag::text').getall(),
            "relationship":response.css('dd.relationship a.tag::text').getall(),
            "character":response.css('dd.character a.tag::text').getall(),
            "freeform":response.css('dd.freeform a.tag::text').getall(),
            "title":response.css('#workskin .title::text').get(),
            "summary":response.xpath("//*[@id='workskin']//*[@class='summary module']//blockquote//text()").getall(),
            "story":response.xpath("//*[@id='workskin']//*[@id='chapters']//text()").getall(),
        }