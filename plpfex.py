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

id_plane_desc = 'plane_desc'
id_icao = 'icao_code'
id_pax = 'pax'
id_mtow = 'gMTOW'
id_cruise_speed = 'gVCSknots'
id_ceiling = 'gCeiling'
id_range = 'gRange'
id_length = 'wsLabelLength'

aircraft_data = {}

# regular expression to extract the data in the html page
data_pattern = re.compile("^.*(<span id=\"[a-zA-z]+\">|<span id=\"[a-zA-z]+\" class=\"[a-zA-z]+\">)(?P<data>.+)</span>.*$")

#perf_pattern = re.compile("^.*<span id=\"[a-zA-z]+\">(?P<data>.+)</span>$")
#data_pattern = re.compile("^.*<span id=\"[a-zA-z]+\" class=\"[a-zA-z]+\">(?P<data>.+)</span><br />$")

#-------------------------------------------------------------------------------
def extract_data(line, data_type):
    match = data_pattern.match(line.strip())
    if verbose: print match.group('data')
    aircraft_data[data_type] = match.group('data')
    
#-------------------------------------------------------------------------------
def parse_html_page(html_content):
    for line in html_content:
        
        if verbose: print "parse html line :%s" % line.strip
        
        if line.find(id_mtow) != -1:            
            extract_data(line, id_mtow)
            
        if line.find(id_cruise_speed) != -1:
            extract_data(line, id_cruise_speed)

        if line.find(id_ceiling) != -1:
            extract_data(line, id_ceiling)
            
        if line.find(id_range) != -1:
            extract_data(line, id_range)
            
        if line.find(id_length) != -1:
            extract_data(line, id_length)
   
        if line.find('passengers') != -1:
            pos = line.find('passengers')
            aircraft_data[id_pax] = line[pos-4: pos]

#-------------------------------------------------------------------------------
def send_request(url_request):
    if verbose: print "request url : %s" % url_request
    html_content = urllib2.urlopen(url_request)
    if verbose: print html_content   
    parse_html_page(html_content.readlines())
    
    print aircraft_data

#-------------------------------------------------------------------------------
def append_data(outfilename):
    
    line_count = 1
    out_string = ""
    
    out_string += str(line_count)+','+aircraft_data[id_icao]+','
    out_string += aircraft_data[id_plane_desc]+','
    out_string += ','+aircraft_data[id_pax]+','+aircraft_data[id_range]+','
    out_string += ','+aircraft_data[id_length]+',,,'+aircraft_data[id_mtow]+','
    out_string += aircraft_data[id_ceiling]+','+aircraft_data[id_cruise_speed]+','
    out_string += ',,,'
    
    print out_string
    
    #with open(outfilename, "a") as outfile:
    #    out_string += line_count
            
    #outfile.close()
    
#-------------------------------------------------------------------------------
def parse_icao_list(infile, outfile):

    print "read icao designator list : %s" % infile
    
    icao_file = open(infile, "r")
   
    for icao_line in icao_file:
    
        icao_line = icao_line.split(' ')
        
        # no icao designator found, skip line
        if not icao_line[0].strip(): continue
        
        print "get data for icao type : %s / %s" % (icao_line[0].strip(), ' '.join(icao_line[1:]))
        aircraft_data[id_icao] = icao_line[0].strip()
        aircraft_data[id_plane_desc] = ' '.join(icao_line[1:]).strip()
        url = "https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=%s&" % aircraft_data[id_icao]
        send_request(url)
        
        # append data for this aircraft to file
        append_data(outfile)
        
        # todo clean up the dictonary
        # aircraft_data.empty()
        
        # sleep 5 seconds to send not to many request to eurocontrol :-)
        time.sleep(5)
    
    # close file    
    icao_file.close()
    
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
    
    parse_icao_list(options.icao_filename, options.output_filename)
    
if __name__ == '__main__':
    main()
    
