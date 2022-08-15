import os
import requests as req
import json


class Shortener_Rebrandly():        
    
    def __init__(self, token):
        self.headers = {
            "Accept": "application/json", 
            "Content-Type": "application/json",
            "apikey": token            
        }        
        self.base_url = 'https://api.rebrandly.com/v1/links/'        

    
    def shorten_link(self, link):   
        if link.find('://', 0, 8) == -1:
            link = f'http://{link}'
        
        response = req.post(self.base_url, headers=self.headers, data=json.dumps({ "destination": link }))        
        response.raise_for_status()        
        
        short_url = response.json()['shortUrl']
        link_id = response.json()['id']
        return  f'{short_url}|{link_id}'

  
    def count_click(self, link_id):    
        response = req.get(f'{self.base_url}{link_id}', headers=self.headers)
        response.raise_for_status()
        
        return response.json()['clicks']


    def is_short_link(self, link_id):                           
        return req.get(f'{self.base_url}{link_id}', headers=self.headers).ok
