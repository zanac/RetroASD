"""da un nome rom cerca sul gamelist.xml le caratteristiche per la giusta modeline"""

import sys
from lxml import etree

"""Args.	Parsed Parameter	Usage
1	gameStart or gameStop	to distinguish between START or STOP condition
2	systemName	like in your es_system.cfg, for eg. atari2600
3	system.config['emulator']	The emulator settings, for eg. libretro
4	system.config['core']	The emulator core you have chosen, for eg. stella
5	args.rom	The full rom path, for eg. /userdata/roms/atari2600/Mysterious Thief, A (USA).zip"""
# xmlstr is your xml in a string

romName = sys.argv[1]   
context = etree.iterparse("rominfo_mame2010.xml", tag='game')
for event, elem in context:
    keys = elem.keys()
    #item = Game()
    #if 'cloneof' in keys:
    #    item.cloneof = elem.get('cloneof')
    #if 'sourcefile' in keys:
    #    item.gamesourcefile = elem.get('sourcefile')
    #    
    #item.romname = elem.get('romname')
    #item.description = elem.get('description')
    #item.manufacturer = elem.get('manufacturer')
    #item.year = elem.get('year')
    #item.players = elem.get('players')
    #item.control = elem.get('control')
    #item.genre = elem.get('genre')
    #item.estatus = elem.get('status')
    #item.ecolor = elem.get('color')
    #item.esound = elem.get('sound')
    name = elem.get('name')
    romof = elem.get('romof')
    description = ""
    display = None
    width = 0
    height = 0
    for child in elem:
        romNeoGeo = False
        romRotated = False
        buttons = False
        if child.tag == "description":
            description = child.text
        if child.tag == "input" and name == "popeyeman":
            buttons = child.attrib.get('buttons', None)
        if child.tag == "display":
            rotate = child.attrib['rotate']
            width = child.attrib.get('width', 0)
            height = child.attrib.get('height', 0)
            if rotate not in ("0", "180"):
                romRotated = True
                #print("%s:%s:" % (str(name), str(rotate)))
        """if romof == "neogeo" and child.tag == "display":
            #print("%s:" % (str(name)))
            romNeoGeo = True
        
        if romRotated and not romNeoGeo:    
            print("rotated1:%s:%s:" % (str(name), str(rotate)))
        if romNeoGeo and romRotated:
            print("rotated2:%s:%s:" % (str(name), str(rotate)))
        if romNeoGeo and not romRotated:
            print("neogeo:%s:%s:" % (str(name), str(rotate)))"""
        
        if name == romName or 1 == 1:
            if int(width) > 0 and int(height) > 0:
                if int(width) == 399:
                    width = 400
                if int(height) == 253:
                    height = 254
                
                new_width = width
                new_height = height
                if rotate not in ("0", "180"):
                    new_width = int(height)
                    new_height = int(width)
                print ("name:%s:%s:%s:%s:%s" % (name, new_width, new_height, rotate, description))
                #exit(0)
        
        #if buttons:
        #    print(str(buttons))
        
    #print(str(elem))
