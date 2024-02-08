import scrapy

class PopularSpider (scrapy. Spider):
    name = 'ytsTrending'
    start_urls = ['https://yts.mx/trending-movies']

    def parse(self, response):
        for products in response.css('div.browse-movie-bottom'):
            yield {
                'name': products.css('a.browse-movie-title::text').get(),
                'link': products.css('a.browse-movie-title').attrib['href']
            }
            
class MainPopularSpider (scrapy. Spider):
    name = 'mainYtsTrending'
    start_urls = ['https://yts.mx']

    def parse(self, response):
        for products in response.css('div.browse-movie-bottom'):
            yield {
                'name': products.css('a.browse-movie-title::text').get(),
                'link': products.css('a.browse-movie-title').attrib['href']
            }
            
class MovieSpider (scrapy. Spider):
    name = 'movie'
    # start_urls = ['https://yts.mx/movies/the-transporter-2002']
    start_urls = ['https://yts.mx/movies/dream-scenario-2023']

    def parse(self, response):
        for products in response.css('div.modal-torrent'):
            yield {
                'name': products.css('a.magnet-download').attrib['title'],
                'magnet': products.css('a.magnet-download').attrib['href'],
                'size':products.css('p.quality-size::text')[1].get()
            }
            
class MovieData (scrapy. Spider):
    name = 'data'
    # start_urls = ['https://yts.mx/movies/the-transporter-2002']
    start_urls = ['https://yts.mx/movies/dream-scenario-2023']

    def parse(self, response):
        
        pixels = list()
        data = list()
        
        for pixel in response.xpath('//*[@id="movie-tech-specs"]/span/text()').getall():
            if pixel == ' ':
                continue
            pixels.append(pixel)
            
        for info in response.xpath('//*[@id="movie-tech-specs"]/div/div/div/text()').getall():
            if info == ' ':
                continue
            data.append(info)
                
                
        if(len(data)<7*len(data)):
            for i in range(len(pixel)+1):
                data.insert(i*7+6, "100+") 
            
                
        for i in range(len(pixel)+1):
            yield{
                'resolution':pixels[i],
                'size':data[i*7],
                'seeds':data[i*7+6]
            }
            
            
class SimpleData (scrapy. Spider):
    name = 'comp'
    start_urls = ['https://yts.mx/movies/the-great-ziegfeld-1936']
    # start_urls = ['https://yts.mx/movies/the-transporter-2002']
    # start_urls = ['https://yts.mx/movies/dream-scenario-2023']

    def parse(self, response):
        
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