#!/usr/bin/env python
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

import os
import subprocess as sub
import sys
import ConfigParser


counter = 0

def pack(source, dest, tag):
    global counter
    finish = []
    if os.path.exists('finish_pack.txt'):
        f = open('finish_pack.txt','r')
        for line in f:
            finish.append(line.strip())
        f.close()
    for dir in os.listdir(source):
        if tag in dir and dir not in finish:
            try:
                sub.call(['7z.exe', 'a', dir+'.7z', source+'/'+dir])
                print "Move File"
                print (dir+'.7z',dest+'/'+dir+'.7z')
                os.rename(dir+'.7z',dest+'/'+dir+'.7z')
                f = open('finish_pack.txt','a')
                f.write(dir+'\n')
                f.close()
                counter = counter + 1
                print ''
                print 'Finish'
            except OSError as e:
                print('error: %s' % e)
                f = open('error.txt','a')
                f.write('ERROR: '+dir+': '+str(e)+'\n')
                f.close()

def start():
    cfg = ConfigParser.ConfigParser()
    cfg.read('gog2xpl.ini')
    dest = cfg.get('XPlane','backup')
    src = cfg.get('XPlane','ortho')
    tag = cfg.get('g2xpl','scenery')
    scenery= 'xxx_'+tag
    pack(src, dest, scenery)
    
def main():
    try:
        start()
    except KeyboardInterrupt:
        print 'Nutzerabbruch'
        print ('%s Archive erstellt' % str(counter))     
    except Exception as error:
        print error
        
if __name__ == '__main__':
    main()
