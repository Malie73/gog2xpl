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

import re
import shutil
import sys
import os
import subprocess
from subprocess import Popen, PIPE
import time
import ConfigParser
import del_dsf_cache 
import pack_and_move

tasks = 0  # Anzahl gleichzeitiger Starts
sceneryName = ''
zoomLevel = ''
ori_dir = ''
geo_list = []
geo_list_finish = []
noerror_message = ''
script_path=''
pack = 0
delCache = 1

def write_finish_geos(entry):
    f = open('geo_finish.txt', 'a')
    f.write(entry + '\n')
    f.close()

def clearCache(dir):
    if os.path.exists(str(dir) + '/G2xpl_cache'):
        print "Cache gefunden, loesche"
        try:
            shutil.rmtree(str(dir) + '/G2xpl_cache')
            while not os.path.exists(str(dir)):
                pass
            print 'done'
        except shutil.Error as e:
            print('Verzeichniss konnte nicht gelöscht werden. Fehler: %s' % e)
        except OSError as e:
            print('Verzeichniss konnte nicht gelöscht werden. Fehler: %s' % e)
    if os.path.exists(str(dir) + '/G2xpl_temp'):
        print "Temp gefunden, loesche"
        try:
            shutil.rmtree(str(dir) + '/G2xpl_temp')
            while not os.path.exists(str(dir)):
                pass
            print 'done'
        except shutil.Error as e:
            print('Verzeichniss konnte nicht gelöscht werden. Fehler: %s' % e)
        except OSError as e:
            print('Verzeichniss konnte nicht gelöscht werden. Fehler: %s' % e)


def read_geos():
    global tasks
    global geo_list
    global geo_list_finish
    dummy = []
    if not os.path.isfile('geo.txt'):
        print 'geo.txt nicht gefunden, Abbruch!'
        sys.exit()
    f = open('geo.txt', 'r')
    for line in f:
        entry = line.strip()
        dummy.append(entry)
        geo_list.append(dummy)
        dummy = []
    f.close()
    if os.path.isfile('geo_finish.txt'):
        f = open('geo_finish.txt', 'r')
        for line in f:
            entry = line.strip()
            dummy.append(entry)
            geo_list_finish.append(dummy)
            dummy = []
        f.close()

    for entry in geo_list:
        if entry not in geo_list_finish:
            dummy.append(entry)
        else:
            print 'Datensatz %s bereits fertig, wird nicht erneut abgearbeitet!' % entry

    geo_list = dummy
    print 'Anzahl an Geo-Datensaetzen: %s' % str(len(geo_list))

    if (tasks > len(geo_list)):
        print "Mehr Tasks (%s) als Geo-Datensaetze (%s) gefunden, Tasks angepasst!" % (str(tasks), str(len(geo_list)))
        tasks = len(geo_list)


def write_config(configFile, lang, lat):
    print zoomLevel
    with open(configFile, 'r') as f:
        ini = f.read()
    ini = re.sub(
        'plane_long\s*=\s*[-+0-9.]+', 'plane_long=' + str(lang).strip(), ini)
    ini = re.sub(
        'plane_lat\s*=\s*[-+0-9.]+', 'plane_lat=' + str(lat).strip(), ini)
    ini = re.sub(
        'IS_zoom_level\s*=\s*[-+0-9.]+', 'IS_zoom_level=' + str(zoomLevel).strip(), ini)
    ini = re.sub('scenery_name\s*=\s*[-+0-9a-zA-Z._]+', 'scenery_name=xxx_'
                 + sceneryName +
                 str(lang.split('.', 1)[0].strip())
                 + str(lat.split('.', 1)[0].strip())
                 + '_Z' + str(zoomLevel).strip(), ini)

    with open(configFile, 'w') as f:
        f.write(ini)


def createTask():
    procs = {}
    success = 0
    name = ''
    si = subprocess.STARTUPINFO()
    si.dwFlags = subprocess.STARTF_USESTDHANDLES 
    for counter in range(0, len(geo_list), tasks):
        for t in range(tasks):
            procdir = str(t) + '/g2xpl.exe'
            clearCache(str(t))
            print 'Starte in %s' % script_path+'\\'+str(t)
            entry = geo_list[counter]
            entry = entry[0].split(',')
            write_config(str(t) + '/g2xpl.ini', entry[0], entry[1])
            f = open('logs/log_' + sceneryName + '_' + entry[0].strip() + '_' + entry[1].strip(), 'w')
            os.chdir(str(t))
            print 'Bearbeite %s (%s von %s)' % (entry, counter + 1, len(geo_list))
            print ''
            p = Popen('g2xpl.exe', stdout=f, stderr=f, stdin=f, shell=True,universal_newlines=True)
            print 'Prozess gestartet'
            print ''
            os.chdir(script_path)
            procs[p] = entry
            counter += 1
            if counter is len(geo_list):
                break
        while procs:
            for proc in procs:
                name = procs[proc]
                retcode = proc.poll()
                t = open('logs/log_' + sceneryName + '_' + name[0].strip() + '_' + name[1].strip(), 'r')
                view = t.read()
                view = view.strip('*\/|_ ')
                index = view.rfind('Remain')
                index2 = view.rfind('>')
                if index > 0 and index2 > 0 and index < index2:
                    print name
                    view = view[index-len(view):index2-len(view)]
                    print view.strip()
                    print ''
                    index = 0
                    index2 = 0
                t.close()    
                if retcode is not None:  # Process finished
                    print ''
                    print ''
                    print "Process beendet"
                    print name
                    print '###'
                    print '###'
                    f = open(
                        'logs/log_' + sceneryName + '_' + name[0].strip() + '_' + name[1].strip(), 'r')
                    output = f.read()
                    f.close()
                    del procs[proc]
                    if noerror_message in output:
                        print "Kein Fehler"
                        print '###'
                        print '###'
                        print ''
                        f = open('geo_finish.txt', 'a')
                        f.write(
                            name[0].strip() + ', ' + name[1].strip() + '\n')
                        f.close()
                        success += 1
                    else:
                        print "Prozess mit Fehler beendet"
                        print '???'
                        print '???'
                        print ''
                        f = open('geo_fehler.txt', 'a')
                        f.write(
                            name[0].strip() + ', ' + name[1].strip() + '\n')
                        f.close()
                    break
                else:
                    time.sleep(10)
                    continue
    if success == len(geo_list):
        print "Alle Tasks fehlerfrei beendet!"
    else:
        print "Tasks mit Fehlern beendet! %s von %s sind fehlerfrei." % (success, len(geo_list))


def copy_dir(src, dest):
    try:
        shutil.copytree(src, dest)
    except shutil.Error as e:
        print('Verzeichniss konnte nicht kopiert werden. Fehler: %s' % e)
    except OSError as e:
        print('Verzeichniss konnte nicht kopiert werden. Fehler: %s' % e)


def remove_dir(src):
    try:
        shutil.rmtree(src)
    except shutil.Error as e:
        print('Verzeichniss konnte nicht gelöscht werden. Fehler: %s' % e)
    except OSError as e:
        print('Verzeichniss konnte nicht gelöscht werden. Fehler: %s' % e)

def init():
    global tasks # Anzahl gleichzeitiger Starts
    global sceneryName
    global zoomLevel
    global ori_dir
    global noerror_message
    global tasks
    global pack
    global delCache
    cfg = ConfigParser.ConfigParser()
    cfg.read('gog2xpl.ini')
    sceneryName = cfg.get('g2xpl','scenery')
    zoomLevel = cfg.get('g2xpl','zoomLevel')
    ori_dir = cfg.get('g2xpl','ori_dir')
    noerror_message = cfg.get('g2xpl','noerror_message')
    dummy = cfg.get('g2xpl','tasks')
    tasks = int(dummy)
    dummy = cfg.get('Misc','pack')
    pack = int(dummy)
    dummy = cfg.get('Misc','delCache')
    delCache = int(dummy)


def del_workdirs(count):
    print 'Raume auf'
    try:
        for counter in range(count):
            remove_dir(str(counter))
    except Exception as error:
        print error

def create_workdirs(count):
    try:
        for counter in range(count):
            copy_dir(ori_dir, str(counter))
    except Exception as error:
        print error
    
def main():
    try:
        global script_path
        script_path = os.getcwd()
        print script_path
        init()
        read_geos()
        if len(geo_list) == 0:
            print "Keine Datensaetze zu bearbeiten"
            sys.exit(0)
        create_workdirs(tasks)
        createTask()
        del_workdirs(tasks)
        if delCache == 1:
            del_dsf_cache.start()
        if pack == 1:
            pack_and_move.start()
            
    except KeyboardInterrupt:
        print 'Nutzerabbruch'
        del_workdirs(tasks)
        
    except Exception as error:
        print error
    
if __name__ == '__main__':
    main()
