import re
import os

'''
desc <span dir="auto">AIRBUS A-319</span>
icao <div id="contentSub">A319</div>

length
<th>Length
<span class="smw-highlighter" data-type="3" data-state="inline" data-title="Quantity"><span class="smwtext">33.84 m</span>

'''

desc_pattern = re.compile('^.*<span dir="auto">(?P<desc>[A-Za-z0-9() -/]+)</span>.*$')
icao_pattern = re.compile('^.*<div id="contentSub">(?P<icao>[A-Z0-9]{2,4})</div>.*$')
mtow_pattern = re.compile('^<td> MTOW </td>$')
range_pattern = re.compile('^<td> Range </td>$')
data_no_pattern = re.compile('^.*<span class="smwtext">(?P<data>[0-9]+)</span>.*$')
data_m_pattern = re.compile('^.*<span class="smwtext">(?P<data>[0-9\.]+ m)</span>.*$')
fl_pattern = re.compile('^<td> (?P<fl>FL[0-9]+) </td>$')
length_pattern = re.compile('^<th>Length$')
speed_pattern = re.compile('^<td> TAS </td>$')
speed2_pattern = re.compile('^<td> (?P<tas>[0-9]+ kts) </td>$')

data_directory = 'skybrary_out/'

p_desc = ""
p_icao = ""
p_mtow = ""
p_range = ""
p_fl = ""
p_length = ""

csv_content = []

aircraft_count = 0
error_count = 0

for filename in os.listdir(data_directory):
    print "read : " + filename
        
    infile = open(data_directory+'/'+filename)
    
    file_content = []
    for line in infile:
        file_content.append(line)
    
    aircraft_count += 1
    line_count = 0
    
    for line in file_content:
    
        match = speed_pattern.match(line)
        if match:
            speed_line = file_content[line_count+1]
            speed_match = speed2_pattern.match(speed_line)
            if speed_match:
                p_tas = speed_match.group('tas')
                
        match = desc_pattern.match(line)
        if match:
            p_desc = match.group('desc')
                        
        match = icao_pattern.match(line)
        if match:
            p_icao = match.group('icao')

        match = mtow_pattern.match(line)
        if match:
            mtow_line = file_content[line_count + 1]
            data_match = data_no_pattern.match(mtow_line)
            if data_match:
                p_mtow = data_match.group('data')

        match = fl_pattern.match(line)
        if match:
            p_fl = match.group('fl')
        
        match = length_pattern.match(line)
        if match:
            length_line = file_content[line_count+2]
            data_match = data_m_pattern.match(length_line)
            if data_match:
                p_length = data_match.group('data')
            
        match = range_pattern.match(line)
        if match:
            range_line = file_content[line_count+1]
            data_match = data_no_pattern.match(range_line)
            if data_match:
                p_range = data_match.group('data')
                    
        line_count += 1
        
    infile.close()

    if p_icao == "": print "-> no icao code"
    if p_desc == "": print "-> no description"
    if p_tas == "" : print "-> no tas"
    
    csv_line = str(aircraft_count)+','
    csv_line += p_icao+',"'+p_desc+'",,,"'+p_range+' km",,"'+p_length+'",,,'
    csv_line += '"'+p_mtow+' kg",'+p_fl+',"'+p_tas+'",,,,'
    csv_content.append(csv_line)

    p_desc = ""
    p_icao = ""
    p_mtow = ""
    p_range = ""
    p_fl = ""
    p_length = ""

print "number aircrafts : " + str(aircraft_count)
print "csv line count   : " + str(len(csv_content))

with open('csv_out.csv', 'w') as outfile:
    for csv_line in csv_content:
        outfile.write(csv_line+'\n')
outfile.close()

