'''
author: florian

extract aircaft data from flugzeuginfo.net
http://www.flugzeuginfo.net/acdata_dt.php#0

the detail page:
http://www.flugzeuginfo.net/acdata_php/acdata_aeronca_c3_dt.php

'''

import re
import urllib2
import time

overview_url = "http://www.flugzeuginfo.net/acdata_dt.php#0"
detail_url = "http://www.flugzeuginfo.net"

# -- some regular expressions --
aircraft_pattern = re.compile("^<td class='photo75'></td><td><a href='(?P<url>.*)' title='.*'>(?P<code>.*)</a><br>\
<span class='aircrafttype'>\[(?P<aircrafttype>[A-Za-z]*)\]</span></td></tr>$")

ignore_pattern = re.compile("(Jagdflugzeug|(B|.*b)omber|Erdkampfflugzeug|(H|.*h)ubschrauber|Strahltrainer)")

#-------------------------------------------------------------------------------
class AircraftData:
    def __init__(self):
        pass
    
    def extract_data(self, html_page):
        page_url = detail_url + html_page
        page_content = send_html_request(page_url)
        
#-------------------------------------------------------------------------------
def parse_html_line(line):
    match = aircraft_pattern.match(line)
    if match:
        if ignore_pattern.match(match.group('aircrafttype')):
            print 'ignore type [' + match.group('aircrafttype') + '] aircraft [' + match.group('code') + ']'
        else:
            print 'send request for aircraft [' + match.group('code') + ']'
            aircraft_data = AircraftData()
            aircraft_data.extract_data(match.group('url'))
            # do not send do many request, wait a short time
            time.sleep(4) 
            
#-------------------------------------------------------------------------------
def send_html_request(url_request):
    html_content = urllib2.urlopen(url_request)
    return html_content.readlines()
    
#-------------------------------------------------------------------------------
def main():
    
    page_content = send_html_request(overview_url)

    for line in page_content:
        parse_html_line(line)

    
if __name__ == '__main__':
    main()
    
