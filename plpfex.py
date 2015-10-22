'''
author: florian

eurocontrol performce data url
https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=A109&

'''

import sys
import os.path
import urllib2
import time
from optparse import OptionParser
from HTMLParser import HTMLParser

verbose = False

id_mtow = 'gMTOW'
id_length = 'wsLabelLength'
id_ceiling = 'gCeiling'
id_range = 'gRange'

#-------------------------------------------------------------------------------
class MyHTMLParser(HTMLParser):

    def __init__(self):
        self.mtow = 0

    def handle_starttag(self, tag, attrs):
        
        for name, value in attrs:
            if name == 'id' and value == 'gMTOW':
                self.mtow = 1
                
    def handle_data(self, data):
        if self.mtow == 1:
            print "MTOW ", data
                
        
#    def handle_endtag(self, tag):
#        print "Encountered an end tag :", tag
#    def handle_data(self, data):
#        print "Encountered some data  :", data

#-------------------------------------------------------------------------------
def send_request(url_request):
    print "request url : %s" % url_request
    html_content = urllib2.urlopen(url_request).read()
    if verbose: print html_content
    
    parser = MyHTMLParser()
    parser.feed(html_content)
    
#-------------------------------------------------------------------------------
def parse_icao_list(filename):

    print "read icao designator list : %s" % filename
    
    icao_file = open(filename, "r")
   
    for icao_line in icao_file:
        if verbose: print icao_line.strip()

        url = "https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=%s&" % icao_line.strip()
        if verbose: print url
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
    
