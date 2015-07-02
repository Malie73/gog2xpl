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
import fnmatch
import ConfigParser


def clear(pattern, path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in fnmatch.filter(files, pattern):
            print 'delete file: ' +os.path.join(root, name)
            os.remove(os.path.join(root, name))

def start():
    del_files = ['*.dsf.ready','*.cached']
    cfg = ConfigParser.ConfigParser()
    cfg.read('gog2xpl.ini')
    path = cfg.get('XPlane','ortho')
    for pat in del_files:
        clear(pat, path)
    
def main():
    start()
            
if __name__ == '__main__':
    main()
