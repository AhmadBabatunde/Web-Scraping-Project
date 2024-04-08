import scrapy


class CasespiderSpider(scrapy.Spider):
    name = "casespider"
    allowed_domains = ["nigerialii.org"]
    start_urls = ["https://nigerialii.org/"]
    def parse(self, response):
        sup = response.css('div.courts__column-wrapper li a ::attr(href)')[9].get()
        yield response.follow(sup, callback= self.parse_sup_page) 
        

    def parse_sup_page(self, response):
        # Extracting links to individual cases
        case_links = response.css('td a::attr(href)').getall()
        for case_url in case_links:
            yield response.follow(case_url, callback=self.parse_case_page)

        # Extracting link to the next page of cases
        next_page_url = response.css('ul li a:contains("Next")::attr(href)').get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse_sup_page)

    def parse_case_page(self, response):
        # Extracting metadata
        metadata = {}
        cols = response.css('dl.document-metadata-list dd::text')
        metadata['Jurisdiction'] = cols[0].get()
        metadata['Citation'] = cols[1].get()
        metadata['Media Neutral Citation'] = cols[2].get()
        metadata['Court'] = cols[3].get()
        metadata['Case number'] = cols[4].get()
        metadata['Judges'] = cols[5].get()
        metadata['Judgment date'] = cols[6].get()
        metadata['Language'] = cols[7].get()
        metadata['Flynote'] = cols[8].get()

        # Extracting case data
        case_data = response.css('div.document-content p::text').getall()

        yield {
            'metadata': metadata,
            'data': case_data
        }