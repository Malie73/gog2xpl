#coding: utf8
#    Created: 21.05.2015
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.#
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.#
#
#    Dieses Programm ist Freie Software: Sie können es unter den Bedingungen
#    der GNU General Public License, wie von der Free Software Foundation,
#    Version 3 der Lizenz oder (nach Ihrer Wahl) jeder neueren
#    veröffentlichten Version, weiterverbreiten und/oder modifizieren.
#
#    Dieses Programm wird in der Hoffnung, dass es nützlich sein wird, aber
#    OHNE JEDE GEWÄHRLEISTUNG, bereitgestellt; sogar ohne die implizite
#    Gewährleistung der MARKTFÄHIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.
#    Siehe die GNU General Public License für weitere Details.
#
#    Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
#    Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.
#
import ConfigParser

start = []
end = []

def getCoords (min, max):
    if min[0] > max[0]:
        tmp = min[0]
        min[0] = max[0]
        max[0] = tmp
    if min[1] > max[1]:
        tmp = min[1]
        min[1] = max[1]
        max[1] = tmp
    coords = []
    print min
    print max
    for i in range(min[0],max[0]+1):
        for j in range(min[1], max[1]+1):
            if i > 0 and i < 10:
                #tmp_i = '+0' + str(i) + '.000000'
                tmp_i = '0' + str(i) + '.000000'
            #elif i > 0 and i >= 10:
            #   tmp_i = '+' + str(i) + '.000000'
            elif i < 0 and i > -10:
                tmp_i = '-0' + str(abs(i)) + '.000000'
            else:
                tmp_i = str(i) + '.000000'
            if j > 0 and j < 10:
                #tmp_j = '+0' + str(j) + '.000000'
                tmp_j = '0' + str(j) + '.000000'
            elif j < 0 and j > -10:
                tmp_j = '-0' + str(abs(j)) + '.000000'
            #elif j > 0 and j >= 10:
            #    tmp_j = '+' + str(j) + '.000000'
            else:
                tmp_j = str(j) + '.000000'
                
            coords.append([tmp_i,tmp_j])
    return coords

def init():
    global start
    global end
    cfg = ConfigParser.ConfigParser()
    cfg.read('gog2xpl.ini')
    start.append(int(cfg.get('Coords','long1')))
    end.append(int(cfg.get('Coords','long2')))
    start.append(int(cfg.get('Coords','lat1')))
    end.append(int(cfg.get('Coords','lat2')))
    
def main():
    init()
    coords = getCoords(start, end) # (long - , lat |)
    f = open('geo_coods.txt','w')
    for entry in coords:
        f.write(str(entry[0]) + ', ' + str(entry[1]) + '\n' )
        print str(entry)
    f.close()
if __name__ == '__main__':
    main()
