import requests as req
from urllib.parse import urlparse

   
class Shortener_Bitly():
    
    def __init__(self, token):         
        self.headers = {'Authorization': f'Bearer {token}'}
        self.base_url = 'https://api-ssl.bitly.com/v4/bitlinks/'
        
    
    def is_short_link(self, link):         
        url_parts = urlparse(link)    
        
        return req.get(
            f'{self.base_url}{url_parts.netloc}{url_parts.path}',
            headers=self.headers
        ).ok    
    
    
    def count_click(self, link):         
        url_parts = urlparse(link)    
        url = f'{self.base_url}{url_parts.netloc}{url_parts.path}/clicks/summary'                         
        
        response = req.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()['total_clicks']
    
    
    def shorten_link(self, link): 
        if link.find('://', 0, 8) == -1:
            link = f'http://{link}'
                
        response = req.post(self.base_url, headers=self.headers, json={'long_url': link})
        response.raise_for_status()        

        return f"{response.json()['link']}|{response.json()['id']}"
