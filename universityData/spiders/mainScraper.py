# import the required libraries
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class UniversityScraper(scrapy.Spider):
    ''' 
    name and start_urls are two required parameters, where the name has to be unique, 
    the name is used generally to perform the crawling job, e.g scrapy crawl universityData
    '''

    name="universityData"
    start_urls=["https://www.4icu.org/reviews/index2.htm"]


    def parse(self,response):
        ''' This function provides the HTML code as response
        The main page shows the University's name and also a link to detailed information about University.
        So we will extract each University's name and the URL of the detailed info page.
        '''

        # Using css-selector to select table based on the class text-left
        dataTable=response.css('table.text-left')
        dataRows=dataTable.css('tbody tr')

        for item in dataRows:
            pageURL=item.css('a::attr(href)').get() 
            university=item.css('a::text').get()
            country=item.css('td.text-right img::attr(alt)').get()

            # the href attribute contains partial URL i.e href="/reviews/18013.htm" 
            pageUrl="https://www.4icu.org"+pageURL
            
            '''
            After retrieving the detail page's URL, University's name, and country, the data is passed 
            to another function parseDetailPage, the parseDetailPage takes the URL and scrapes the 
            address and telephone from each page and dumps all the data.
            '''

            yield scrapy.Request(url=pageUrl,meta={'country':country,'university':university},callback=self.parseDetailPage)
        

        # Now we check if there is a next page available or not and call the whole function again
        next_page=response.xpath('/html/body/div[1]/div[4]/div/ul[2]/li[3]/a/@href').get()
        next_page="https://www.4icu.org/reviews/"+next_page
        
        if next_page is not None:
            next_page=response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)

    

    def parseDetailPage(self,response):
        country=response.meta['country']
        university = response.meta['university']
        address=response.css('div[itemprop="address"] td')[0].xpath(".//text()").extract()
        #the below three lines of code removes any extra white space
        address=" ".join(address)
        address=address.strip()
        address=" ".join(address.split())
        telephone=response.css('span[itemprop="telephone"]::text').get()

        yield{
            'country':country,
            'address':address,
            'phone':telephone,
            'name':university
        }

# Below code describes the output format 
process = CrawlerProcess(settings={
    "FEEDS": {
        'data.json': {
            'format': 'json',
            'encoding': 'utf8',
            'fields': None,
            'indent': 4,
            'overwrite':True, 
            'item_export_kwargs': {
                'export_empty_fields': True,
                },
            },
        },
    })

# Start the crawling job by passing the class name
process.crawl(UniversityScraper)
process.start()


    




