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

verbose = False

id_mtow = 'gMTOW'
id_length = 'wsLabelLength'
id_ceiling = 'gCeiling'
id_range = 'gRange'

#-------------------------------------------------------------------------------
def send_request(url_request):
    print "request url : %s" % url_request
    content = urllib2.urlopen(url_request).read()
    print content
    
#-------------------------------------------------------------------------------
def parse_icao_list(filename):

    print "read icao designator list : %s" % filename
    
    icao_file = open(filename, "r")
   
    for icao_line in icao_file:
        if verbose: print icao_line.strip()

        url = "https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=%s&" % icao_line.strip()
        if verbose: print url
        send_request(url)
        
        # sleep 5 seconds to send not to much request to eurocontrol :-)
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
    
