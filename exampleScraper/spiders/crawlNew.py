import scrapy
import json

class SimpleData (scrapy. Spider):
    name = 'compNew'
    start_urls = ['https://yts.mx/movies/the-great-ziegfeld-1936','https://yts.mx/movies/the-transporter-2002']
    # start_urls = ['https://yts.mx/movies/the-transporter-2002']
    # start_urls = ['https://yts.mx/movies/dream-scenario-2023']



    def parse(self, response):
        
        nextpageurl = response.xpath("//a[@title='Next page']/@href").extract_first()
        nextpage = response.urljoin(nextpageurl)
        
        print(nextpage)
        yield scrapy.Request(nextpage, callback=self.cral,dont_filter=True)
        
    
    def cral(self, response):
        name = list()
        magnet = list()
        data = list()
        
        for products in response.css('div.modal-torrent'):
            name.append(products.css('a.magnet-download').attrib['title'])
            magnet.append(products.css('a.magnet-download').attrib['href'])
            
        for info in response.xpath('//*[@id="movie-tech-specs"]/div/div/div/text()').getall():
            if info == ' ':
                continue
            data.append(info)
                
                
                
        if(len(data)<7*len(name)):
            for i in range(len(name)+1):
                data.insert(i*7+6, "100+") 
                
        for i in range(len(name)+1):
            yield{
                'name' : name[i],
                'magnet': magnet[i],
                'size':data[i*7],
                'resolution':data[i*7+1],
                'lang':data[i*7+2],
                'rating':data[i*7+3],
                'duration':data[i*7+5],
                'seeds':data[i*7+6]
            }