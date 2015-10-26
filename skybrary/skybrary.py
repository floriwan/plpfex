#http://www.skybrary.aero/index.php?title=Special:BrowseData/Aircraft&limit=500&offset=0&_cat=Aircraft

import re
import urllib2
import time

'''
download all aircarft description html pages
from skybrary and save for every icao code a file into the output director.

<li><a href="/index.php/M339" title="M339">AERMACCHI MB-339</a></li><li><a href="/index.php/F260" title="F260">AERMACCHI SF.260</a></li><li><a href="/index.php/AC56" title="AC56">AERO (1) Commander 560</a></li><li><a href="/index.php/AC68" title="AC68">AERO (1) Commander 680F</a></li><li><a href="/index.php/L159" title="L159">AERO (2) L-159</a></li><li><a href="/index.php/L39" title="L39">AERO (2) L-39</a></li><li><a href="/index.php/SGUP" title="SGUP">AERO SPACELINES 377SGT Super Guppy</a></li><li><a href="/index.php/CONC" title="CONC">AEROSPATIALE - BRITISH AEROSPACE Concorde</a></li><li><a href="/index.php/AS32" title="AS32">AEROSPATIALE AS-332 Super Puma</a></li><li><a href="/index.php/AS3B" title="AS3B">AEROSPATIALE AS-332L2 Super Puma Mk2</a></li><li><a href="/index.php/AS50" title="AS50">AEROSPATIALE AS-350 Ecureuil</a></li><li><a href="/index.php/AS55" title="AS55">AEROSPATIALE AS-355 Ecureuil 2</a></li><li><a href="/index.php/AS65" title="AS65">AEROSPATIALE AS-365 Dauphin 2</a></li><li><a href="/index.php/ALO2" title="ALO2">AEROSPATIALE Alouette 2</a></li><li><a href="/index.php/ALO3" title="ALO3">AEROSPATIALE Alouette 3</a></li><li><a href="/index.php/N262" title="N262">AEROSPATIALE Mohawk 298</a></li><li><a href="/index.php/LAMA" title="LAMA">AEROSPATIALE SA-315 Lama</a></li><li><a href="/index.php/PUMA" title="PUMA">AEROSPATIALE SA-330 Puma</a></li><li><a href="/index.php/GAZL" title="GAZL">AEROSPATIALE SA-341 Gazelle</a></li><li><a href="/index.php/S601" title="S601">AEROSPATIALE SN-601 Corvette</a></li><li><a href="/index.php/FREL" title="FREL">AEROSPATIALE Super Frelon</a></li><li><a href="/index.php/M20P" title="M20P">AEROSTAR (1) 200</a></li><li><a href="/index.php/AEST" title="AEST">AEROSTAR (1) 600</a></li><li><a href="/index.php/A109" title="A109">AGUSTA A-109</a></li><li><a href="/index.php/A119" title="A119">AGUSTA A-119</a></li><li><a href="/index.php/A129" title="A129">AGUSTA A-129</a></li><li><a href="/index.php/LYNX" title="LYNX">AGUSTAWESTLAND AH-11 Super Lynx</a></li><li><a href="/index.php/EH10" title="EH10">AGUSTAWESTLAND AW-101</a></li><li><a href="/index.php/A139" title="A139">AGUSTAWESTLAND AW-139</a></li><li><a href="/index.php/A149" title="A149">AGUSTAWESTLAND AW-149</a></li><li><a href="/index.php/A169" title="A169">AGUSTAWESTLAND AW-169</a></li><li><a href="/index.php/A189" title="A189">AGUSTAWESTLAND AW-189</a></li><li><a href="/index.php/CKUO" title="CKUO">AIDC F-CK-1 Ching-Kuo</a></li><li><a href="/index.php/A30B" title="A30B">AIRBUS A-300</a></li><li><a href="/index.php/A306" title="A306">AIRBUS A-300-600</a></li><li><a href="/index.php/A3ST" title="A3ST">AIRBUS A-300ST</a></li><li><a href="/index.php/A310" title="A310">AIRBUS A-310</a></li><li><a href="/index.php/A318" title="A318">AIRBUS A-318</a></li><li><a href="/index.php/A319" title="A319">AIRBUS A-319</a></li><li><a href="/index.php/A320" title="A320">AIRBUS A-320</a></li><li><a href="/index.php/A321" title="A321">AIRBUS A-321</a></li><li><a href="/index.php/A332" title="A332">AIRBUS A-330-200</a></li><li><a href="/index.php/A333" title="A333">AIRBUS A-330-300</a></li><li><a href="/index.php/A342" title="A342">AIRBUS A-340-200</a></li><li><a href="/index.php/A343" title="A343">AIRBUS A-340-300</a></li><li><a href="/index.php/A345" title="A345">AIRBUS A-340-500</a></li><li><a href="/index.php/A346" title="A346">AIRBUS A-340-600</a></li><li><a href="/index.php/A388" title="A388">AIRBUS A-380-800</a></li><li><a href="/index.php/A35J" title="A35J">AIRBUS A350-1000</a></li><li><a href="/index.php/A358" title="A358">AIRBUS A350-800</a></li><li><a href="/index.php/A359" title="A359">AIRBUS A350-900</a></li><li><a href="/index.php/A400" title="A400">AIRBUS A400M Atlas</a></li><li><a href="/index.php/EC20" title="EC20">AIRBUS HELICOPTERS EC-120 Colibri</a></li><li><a href="/index.php/EC30" title="EC30">AIRBUS HELICOPTERS EC-130</a></li><li><a href="/index.php/EC35" title="EC35">AIRBUS HELICOPTERS EC-135</a></li><li><a href="/index.php/EC45" title="EC45">AIRBUS HELICOPTERS EC-145</a></li><li><a href="/index.php/EC55" title="EC55">AIRBUS HELICOPTERS EC-155</a></li><li><a href="/index.php/EC75" title="EC75">AIRBUS HELICOPTERS EC-175</a></li><li><a href="/index.php/EC25" title="EC25">AIRBUS HELICOPTERS EC-225 Super Puma Mk II+</a></li><li><a href="/index.php/TIGR" title="TIGR">AIRBUS HELICOPTERS EC-665</a></li><li><a href="/index.php/G222" title="G222">ALENIA G-222</a></li><li><a href="/index.php/AMXM" title="AMXM">AMX Alenia AMX</a></li><li><a href="/index.php/AN12" title="AN12">ANTONOV An-12</a></li><li><a href="/index.php/A124" title="A124">ANTONOV An-124 Ruslan</a></li><li><a href="/index.php/AN22" title="AN22">ANTONOV An-22 Antheus</a></li><li><a href="/index.php/A225" title="A225">ANTONOV An-225 Mriya</a></li><li><a href="/index.php/AN24" title="AN24">ANTONOV An-24</a></li><li><a href="/index.php/AN26" title="AN26">ANTONOV An-26</a></li><li><a href="/index.php/AN30" title="AN30">ANTONOV An-30</a></li><li><a href="/index.php/AN32" title="AN32">ANTONOV An-32 Sutlej</a></li><li><a href="/index.php/AN38" title="AN38">ANTONOV An-38</a></li><li><a href="/index.php/AN70" title="AN70">ANTONOV An-70</a></li><li><a href="/index.php/AN72" title="AN72">ANTONOV An-72</a></li><li><a href="/index.php/AT43" title="AT43">ATR ATR-42-300/320</a></li><li><a href="/index.php/AT44" title="AT44">ATR ATR-42-400</a></li><li><a href="/index.php/AT45" title="AT45">ATR ATR-42-500</a></li><li><a href="/index.php/AT46" title="AT46">ATR ATR-42-600</a></li><li><a href="/index.php/AT72" title="AT72">ATR ATR-72</a></li><li><a href="/index.php/AT73" title="AT73">ATR ATR-72-210</a></li><li><a href="/index.php/AT75" title="AT75">ATR ATR-72-500</a></li><li><a href="/index.php/AT76" title="AT76">ATR ATR-72-600</a></li><li><a href="/index.php/VULC" title="VULC">AVRO Vulcan</a></li><li><a href="/index.php/ZZZZ" title="ZZZZ"> Aircraft type not (yet) assigned a designator</a></li>				</ul>
'''

skybrary_line = 'http://www.skybrary.aero/index.php/'

#link_pattern = re.compile('^.*<li><a href="(?P<link>[A-Za-z0-9/]+)" title="(?P<title>[A-Z0-9]+)">[0-9a-zA-z ]+</a></li>.*$')

link_pattern = re.compile('<li><a href="(?P<link>[A-Za-z0-9/\.]+)" title="(?P<title>[A-Z0-9]+)">')

f = open('skybrary_index-html')

count = 0

for line in f:
    match = link_pattern.findall(line)
    if match:
        #print (match)
        count += len(match)   
        
        for link, title in match:
            print link
            
            html_content = urllib2.urlopen(skybrary_line+title)
            outf = open('skybrary_out/'+title, 'w')
            outf.write(html_content.read())
            outf.close()  
            time.sleep(2)

f.close()
        
print count
