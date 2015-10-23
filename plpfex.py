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
import pickle
from optparse import OptionParser

#-------------------------------------------------------------------------------

overview_url = "http://www.flugzeuginfo.net/acdata_dt.php#0"
detail_url = "http://www.flugzeuginfo.net"

# -- some regular expressions --
aircraft_pattern = re.compile("^<td class='photo75'></td><td><a href='(?P<url>.*)' title='.*'>(?P<code>.*)</a><br>\
<span class='aircrafttype'>\[(?P<aircrafttype>[A-Za-z]*)\]</span></td></tr>$")

name_pattern = re.compile("^.*<h3 class='name'>(?P<aircraft_name>[A-Za-z0-9\. /\-&]*)</h3>.*$")

crew_pattern = re.compile("^.*<td class='lc'>Besatzung</td><td class='middleright' colspan='2'>(?P<crew>[0-9-]+)</td>.*$")
pax_pattern = re.compile("^.*<td class='lc'>Passagiere</td><td class='middleright' colspan='2'>(?P<pax>([0-9]+, max\. [0-9]+|typ\. [0-9]+, max\. [0-9]+|(max\. )*[0-9-/ ]+))</td>.*$")
enging_system_pattern = re.compile("^.*<td class='lc'>Antriebsart</td><td class='middleright' colspan='2'>(?P<engine_system>[A-Za-z0-9 ]*)</td>.*$")
engine_type_pattern = re.compile("^.*<td class='lc'>Triebwerkstyp</td><td class='middleright' colspan='2'>(?P<engine_type>[A-Za-z0-9\-& ]*)</td>.*$")
power_pattern = re.compile("^.*<td class='lc'>Leistung( je TW)*</td><td class='middle'>(?P<power>[0-9,]* (kW|kN))</td><td class='right'>[0-9]* (shp|hp|lbf)</td>.*$")
speed_pattern = re.compile("^.*<td class='lc'>Geschwindigkeit</td><td class='middle'>[0-9]+ km/h</td><td class='right'>(?P<speed_kts>[0-9]+ kts)<br><span style='font-style: italic;'>.* mph</span></td>.*$")
service_ceiling_pattern = re.compile("^.*<td class='lc'>Dienstgipfelh.he</td><td class='middle'>(?P<service_ceiling_m>[0-9\.]+ m)</td><td class='right'>(?P<service_ceiling_ft>[0-9\.]+ ft)</td>.*$")
range_pattern = re.compile("^.*<td class='lc'>Reichweite</td><td class='middle'>(?P<range_km>[0-9\.]* km)</td><td class='right'>(?P<range_nm>[0-9\.]* NM)<br><span style='font-style: italic;'>(?P<range_mi>[0-9\.]* mi)\.</span></td>.*$")
sfw_patter = re.compile("^.*<td class='lc'>Leergewicht</td><td class='middle'>(?P<sfw_kg>[0-9\.]* kg)</td><td class='right'>(?P<sfw_lbs>[0-9\.]* lbs)</td>.*$")
mtow_pattern = re.compile("^.*<td class='lc'>max. Startmasse</td><td class='middle'>(?P<mtow_kg>[0-9\.]* kg)</td><td class='right'>(?P<mtow_lbs>[0-9\.]* lbs)</td>.*$")
length_pattern = re.compile("^.*<td class='lc'>L.nge</td><td class='middle'>(?P<length>[0-9,]* m)</td>.*$")
icao_pattern = re.compile("^.*<td class='lc'>ICAO Code</td><td class='middleright' colspan='2'>(?P<icao>[A-Z0-9]*)</td>.*$")

ignore_pattern = re.compile("(Jagdflugzeug|(B|.*b)omber|Erdkampfflugzeug|(H|.*h)ubschrauber|Strahltrainer)")

content = "<div class='content'>"
#content = "<table class='techdata'>"

aircraft_dict = {}

count = 0;

#-------------------------------------------------------------------------------
class AircraftData:
    
    def __init__(self):
        self.icao = ""
        self.name = ""
        self.pax = 0
        self.crew = 0
        self.engine_system = ""
        self.engine_type = ""
        self.power = ""
        self.speed = ""
        self.service_ceiling = ""
        self.sfw = ""
        self.mtow = ""
        self.length = ""
        self.range = ""
    
    def get_icao(self):
        return self.icao
            
    def request_data(self, html_page):
        page_url = detail_url + html_page
        page_content = send_html_request(page_url)
        self.parse_html_page(page_content)
    
    def parse_html_page(self, html_page):
        for html_line in html_page:
            
            match = name_pattern.match(html_line)
            if match:
                self.name = match.group('aircraft_name')
                
            match = crew_pattern.match(html_line)
            if match:
                self.crew = match.group('crew')
            
            match = pax_pattern.match(html_line)
            if match:
                self.pax = match.group('pax')
                
            match = enging_system_pattern.match(html_line)
            if match:
                self.engine_system = match.group('engine_system')
                
            match = engine_type_pattern.match(html_line)
            if match:
                self.engine_type = match.group('engine_type')
                
            match = power_pattern.match(html_line)
            if match:
                self.power = match.group('power')
                
            match = speed_pattern.match(html_line)
            if match:
                self.speed = match.group('speed_kts')
                
            match = service_ceiling_pattern.match(html_line)
            if match:
                self.service_ceiling = match.group('service_ceiling_ft')
                
            match = range_pattern.match(html_line)
            if match:
                self.range = match.group('range_nm')
                
            match = sfw_patter.match(html_line)
            if match:
                self.sfw = match.group('sfw_kg')
                
            match = mtow_pattern.match(html_line)
            if match:
                self.mtow = match.group('mtow_kg')
                
            match = length_pattern.match(html_line)
            if match:
                self.length = match.group('length')
                
            match = icao_pattern.match(html_line)
            if match:
                self.icao = match.group('icao')    
                                                       
    def debug_print(self):
        outstring = "["+self.icao+"] "+self.name+"\n"
        outstring += "\tcrew : "+str(self.crew)+" pax : "+str(self.pax)+"\n"
        outstring += "\tmtow : "+self.mtow+" speed : "+self.speed+" service ceiling : "+self.service_ceiling+"\n"
        outstring += "\trange : "+self.range+" length : "+self.length+"\n"
        return outstring 
                    
#-------------------------------------------------------------------------------
def parse_html_line(line):
    global count
    global aircraft_dict
    match = aircraft_pattern.match(line)
    if match:
        if ignore_pattern.match(match.group('aircrafttype')):
            print 'ignore type [' + match.group('aircrafttype') + '] aircraft [' + match.group('code') + ']'
        else:
            print 'send request for aircraft [' + match.group('code') + ']'
            aircraft_data = AircraftData()
            aircraft_data.request_data(match.group('url'))
            
            if len(aircraft_data.get_icao()) > 1:
                print aircraft_data.debug_print()
                aircraft_dict[aircraft_data.get_icao()] = aircraft_data
            else:
                print "no icao code, remove aircraft"
                
            # do not send do many request, wait a short time
            time.sleep(2)
            count += 1
        
#-------------------------------------------------------------------------------
def send_html_request(url_request):
    html_content = urllib2.urlopen(url_request)
    return html_content.readlines()
    
#-------------------------------------------------------------------------------
def main():

    global count
    global aircraft_dict
    
    parser = OptionParser()
    parser.add_option("-d", "--dump", dest="dump_file",
        help="dump all data to file", metavar="FILE")
    parser.add_option("-i", "--infile", dest="input_file",
        help="do not request data, read from file", metavar="FILE")
                
    (options, args) = parser.parse_args()
        
    if not options.input_file:
        page_content = send_html_request(overview_url)
    
        for line in page_content:
            parse_html_line(line)
            #if count == 2: break
    else:
        print "read data from file : %s" % options.input_file
        inputfile = open(options.input_file, 'rb')
        aircraft_dict = pickle.load(inputfile)
        for key, value in aircraft_dict.iteritems():
            print value.debug_print()

    if not options.input_file and options.dump_file:
        print "dump data to file : %s" % options.dump_file
        dump_file = open(options.dump_file, 'ab+')
        pickle.dump(aircraft_dict, dump_file)

#-------------------------------------------------------------------------------    
if __name__ == '__main__':
    main()
    
