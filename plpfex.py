'''
author: florian

eurocontrol performce data url
https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=A109&

'''

import sys
import os.path
import urllib2
import time
import re
from optparse import OptionParser

verbose = False

id_mtow = 'gMTOW'
id_cruise_speed = 'gVCSknots'

id_length = 'wsLabelLength'
id_ceiling = 'gCeiling'
id_range = 'gRange'

aircraft_data = {}

# regular expression to extract the data in the html page
data_pattern = re.compile("^.*<span id=\"[a-zA-z]*\">(?P<data>.*)</span>$")

#-------------------------------------------------------------------------------
def extract_data(line, data_type):
    match = data_pattern.match(line.strip())
    print match.group('data')
    aircraft_data[data_type] = match.group('data')
    
#-------------------------------------------------------------------------------
def parse_html_page(html_content):
    for line in html_content:
        
        if verbose: print "parse html line :%s" % line.strip
        
        if line.find(id_mtow) != -1:            
            extract_data(line, id_mtow)
            
        if line.find(id_cruise_speed) != -1:
            extract_data(line, id_cruise_speed)

#-------------------------------------------------------------------------------
def send_request(url_request):
    if verbose: print "request url : %s" % url_request
    html_content = urllib2.urlopen(url_request)
    if verbose: print html_content   
    parse_html_page(html_content.readlines())
    
    print aircraft_data
    
#-------------------------------------------------------------------------------
def parse_icao_list(filename):

    print "read icao designator list : %s" % filename
    
    icao_file = open(filename, "r")
   
    for icao_line in icao_file:
        print "get data for icao type : %s" % icao_line.strip()
        url = "https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=%s&" % icao_line.strip()
        send_request(url)
        
        # sleep 5 seconds to send not to many request to eurocontrol :-)
        time.sleep(5)
        
#-------------------------------------------------------------------------------
def usage():
    prog_name = os.path.basename(sys.argv[0])
    print "usage: %s -i icao_list" % format(prog_name)

#-------------------------------------------------------------------------------
def main():

    parser = OptionParser()
    parser.add_option("-i", "--icaofile", dest="icao_filename",
                  help="icao designator list", metavar="FILE")
    parser.add_option("-o", "--outfile", dest="output_filename",
                  help="csv output filename", metavar="FILE")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    (options, args) = parser.parse_args()
    
    if options.verbose:
        global verbose
        verbose = True
    
    if not options.icao_filename or not options.output_filename:
        parser.error("no in/out filename given")
    
    parse_icao_list(options.icao_filename)
    
if __name__ == '__main__':
    main()
    
