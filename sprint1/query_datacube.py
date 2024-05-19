#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.display import Image
import requests
import numpy as np
import warnings
warnings.filterwarnings("ignore")


# In[2]:


class dbc:
    # initalizing our dbc by providing it with the service endpoint, from which we can get a datacube
    def __init__(self, url):
        self.server_url = url
    
    def send_query(self, wcps_query):
        """
        method for sending a WCPS query to the server
        wcps_query must be a string
        """
        # getting a response from the server
        response = requests.post(self.server_url, data = {'query': wcps_query}, verify = False)
        return response


# In[11]:


class dco:
    # initializing the dco
    def __init__(self, dbc_being_used):
        self.query = ''
        self.DBC = dbc_being_used
        
    def w_for(self, text):
        self.query += f'''for {text}\n'''
        return self
          
    def where(self, text):
        self.query += f'''where {text}\n'''
        return self
    
    def encode(self, text):
        self.query += f'''return \n encode({text})\n'''
        
        return self


    def average(self, text):
        self.query += f'''return \n encode(avg({text}))\n'''
        return self

    def minimum(self, text):
        pass

    def maximum(self, text):
        pass
    
    def execute(self):
        response = self.DBC.send_query(self.query)
        return response
        
    
        



my_dbc = dbc("https://ows.rasdaman.org/rasdaman/ows")
my_dco = dco(my_dbc)

my_dco = my_dco.w_for('$c in ( AvgTemperatureColorScaled )').encode('$c[ansi("2003-03")], "image/png"')
print(my_dco.query)
response = my_dco.execute()
Image(data=response.content)


my_dco2 = my_dco.w_for('$c in (AvgLandTemp)').average('$c[ansi("2015-01:2015-12")]')
print(my_dco.query)



