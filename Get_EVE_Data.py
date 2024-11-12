# -*- coding: utf-8 -*-



# import requests
import pycurl
import certifi

from io import BytesIO

start_date = '2005-05-05T12:00'
end_date = '2005-05-06T12:00'

url =  "https://lasp.colorado.edu/lisird/latis/dap/\
timed_see_ssi_l3a.txt?\
time,wavelength,irradiance&\
time>="+start_date+"&time<"+end_date 
        
print (url)

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, url)
c.setopt(c.WRITEDATA, buffer)
c.setopt(c.CAINFO, certifi.where())
c.perform()
c.close()

body = buffer.getvalue()
data = body.decode('iso-8859-1')

# Body is a byte string.
# We have to know the encoding in order to print it to a text file
# such as standard output.
print(data)


