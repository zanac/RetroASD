#!/usr/bin/python
# -*- coding: utf-8 -*-
############################################
# 
# 
# 
############################################

import binascii
import sys
#import hid
from hidapi import *
from optparse import OptionParser

if sys.version_info[0] == 3:
    import codecs

jammasdPIN = {"0":"TEST",
              "1":"P1_COIN",
              "2":"P1_START",
              "3":"P1_UP",
              "4":"P1_DOWN",
              "5":"P1_LEFT",
              "6":"P1_RIGHT",
              "7":"P1_BUTTON_1",
              "8":"P1_BUTTON_2",
              "9":"P1_BUTTON_3",
              "10":"P1_BUTTON_4",
              "11":"P1_BUTTON_5",
              "12":"P1_BUTTON_6",
              "13":"P1_BUTTON_7",
              "14":"P1_BUTTON_8",
              "15":"SERVICE",
              "16":"P2_COIN",
              "17":"P2_START",
              "18":"P2_UP",
              "19":"P2_DOWN",
              "20":"P2_LEFT",
              "21":"P2_RIGHT",
              "22":"P2_BUTTON_1",
              "23":"P2_BUTTON_2",
              "24":"P2_BUTTON_3",
              "25":"P2_BUTTON_4",
              "26":"P2_BUTTON_5",
              "27":"P2_BUTTON_6",
              "28":"P2_BUTTON_7",
              "29":"P2_BUTTON_8"}

jammasdKEY = {     "0":"NONE",
                   "4":"A",
                   "5":"B",
                   "6":"C",
                   "7":"D",
                   "8":"E",
                   "9":"F",
                   "10":"G",
                   "11":"H",
                   "12":"I",
                   "13":"J",
                   "14":"K",
                   "15":"L",
                   "16":"M",
                   "17":"N",
                   "18":"O",
                   "19":"P",
                   "20":"Q",
                   "21":"R",
                   "22":"S",
                   "23":"T",
                   "24":"U",
                   "25":"V",
                   "26":"W",
                   "27":"X",
                   "28":"Y",
                   "29":"Z",
                   "30":"1",
                   "31":"2",
                   "32":"3",
                   "33":"4",
                   "34":"5",
                   "35":"6",
                   "36":"7",
                   "37":"8",
                   "38":"9",
                   "39":"0",
                   "40":"ENTER",
                   "41":"ESC",
                   "42":"BKSP",
                   "43":"TAB",
                   "44":"SPACE",
                   "45":"'",
                   "46":"IGRAVE",
                   "47":"EGRAVE",
                   "48":"+",
                   "49":"UGRAVE",
                   "51":"OGRAVE",
                   "52":"AGRAVE",
                   "53":"BACKSLASH",
                   "54":",",
                   "55":".",
                   "56":"-",
                   "57":"CAPS",
                   "58":"F1",
                   "59":"F2",
                   "60":"F3",
                   "61":"F4",
                   "62":"F5",
                   "63":"F6",
                   "64":"F7",
                   "65":"F8",
                   "66":"F9",
                   "67":"F10",
                   "68":"F11",
                   "69":"F12",
                   "70":"PRNT",
                   "71":"SCROLL",
                   "72":"PAUSE",
                   "73":"INSERT",
                   "74":"HOME",
                   "75":"PGUP",
                   "76":"CANC",
                   "77":"END",
                   "78":"PGDOWN",
                   "79":"R_ARROW",
                   "80":"L_ARROW",
                   "81":"D_ARROW",
                   "82":"U_ARROW",
                   "83":"NUM",
                   "84":"KP_/",
                   "85":"KP_*",
                   "86":"KP_--",
                   "87":"KP_+",
                   "88":"KP_ENTER",
                   "89":"KP_1",
                   "90":"KP_2",
                   "91":"KP_3",
                   "92":"KP_4",
                   "93":"KP_5",
                   "94":"KP_6",
                   "95":"KP_7",
                   "96":"KP_8",
                   "97":"KP_9",
                   "98":"KP_0",
                   "99":"KP_.",
                   "100":"<",
                   "101":"APPS",
                   "102":"L_CTRL",
                   "103":"L_SHIFT",
                   "104":"L_ALT",
                   "105":"L_GUI",
                   "106":"R_CTRL",
                   "107":"R_SHIFT",
                   "108":"R_ALT",
                   "109":"R_GUI",
                   "110":"NEXT_TRACK",
                   "111":"PREV_TRACK",
                   "112":"STOP",
                   "113":"PLAY",
                   "114":"MUTE",
                   "115":"VOL_UP",
                   "116":"VOL_DOWN",
                   "117":"MEDIA_SELECT",
                   "118":"POWER_DOWN",
                   "119":"SLEEP",
                   "120":"WAKE_UP",
                   "121":"OB_VOL_UP",
                   "122":"OB_VOL_DOWN"}

    
def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return listOfKeys    




def calc(incoming):
    # convert to bytearray
    if sys.version_info[0] == 3:
        hex_data = codecs.decode(incoming, "hex_codec")
    else:
        hex_data = incoming.decode("hex")
    msg = bytearray(hex_data)
    check = 0
    for i in msg:
        check = AddToCRC(i, check)
    return hex(check)

def AddToCRC(b, crc):
    if (b < 0):
        b += 256
    for i in range(8):
        odd = ((b^crc) & 1) == 1
        crc >>= 1
        b >>= 1
        if (odd):
            crc ^= 0x8C # this means crc ^= 140
    return crc

def check(incoming):
    """Returns True if CRC Outcome Is 0xx or 0x0"""
    result = calc(incoming)
    if result == "0x0" or result == "0x00":
        return True
    else:
        return False

def append(incoming):
    """Returns the Incoming message after appending it's CRC CheckSum"""
    result = calc(incoming).split('x')[1].zfill(2)
    return incoming + result
    
def jammasd_crc8(msg):
    # convert to bytearray
    check = 0
    for i in msg:
        check = AddToCRC(i, check)

    return bytearray(b"%02x" % check)


def jammasd_hid_open():
    return hidapi.hid_open(vendor_id=0x04d8, product_id=0xf3ad)
    #return hidapi.hid_open(vendor_id=0x06cb, product_id=0x82f1)

def jammasd_hid_close(jammasd_id):
    return hidapi.hid_close(jammasd_id)

def jammasd_hid_list_devices():
    hidapi.hid_init()
    for dev in hidapi.hid_enumerate():
        print ('------------------------------------------------------------')
        print (str(dev.description()))

def jammasd_hid_read(rule):
    hidapi.hid_init()
    jammasd_id = jammasd_hid_open()
        
    #Init message is 00  +  length(2)  +  decimal 112 (70), so 000270
    msg_bodyhex = codecs.decode("70", "hex_codec")
    
    msg_header = bytearray(codecs.decode("0002", "hex_codec"))
    msg_body = bytearray(msg_bodyhex)
    msg_crc = codecs.decode(jammasd_crc8(bytearray(msg_bodyhex)), "hex_codec")
    
    msg_array = [msg_header, msg_body, msg_crc, bytearray(codecs.decode("000000000000000000000000", "hex_codec"))]
    msg = b''.join(msg_array)
    
    hidapi.hid_send_feature_report(jammasd_id, msg)    
    msg_data = hidapi.hid_get_feature_report(jammasd_id, bytearray(codecs.decode("0000000000000000000000000000000000", "hex_codec")))
    print(str(msg_data))
        
    jammasd_hid_close(jammasd_id)
    sys.exit(0)

def jammasd_hid_write(rule, pin_jamma, key_jamma):
    hidapi.hid_init()
    jammasd_id = jammasd_hid_open()
        
        
    """byte 1: 12
    byte 2: numero di regola da 1 a 100. la numero 0 ha una funzione particolare che poi ci arriviamo

    byte 3: pin jamma (da prendere in una tabella)
    byte 4: tasto da emulare (da prendere in una tabella)"""

        
    #Init message is 00  +  length(5)  +  decimal 12 (0C), so 00050C
    msg_bodyhex = codecs.decode("0C", "hex_codec")
    
    msg_header = bytearray(codecs.decode("0500", "hex_codec"))
    
    #msg_bit:  enable|shifted<<1|inverse<<2|toggle<<3|repeat<<4|pulse<<5
    msg_bit = codecs.decode("01", "hex_codec")
    
    msg_pin_jamma = codecs.decode("%02x" % int(getKeysByValue(jammasdPIN, pin_jamma)[0]), "hex_codec")
    msg_key_jamma = codecs.decode("%02x" % int(getKeysByValue(jammasdKEY, key_jamma)[0]), "hex_codec")
    msg_rule = codecs.decode("%02x" % int(rule), "hex_codec")
    
    msg_body = b''.join([msg_bodyhex, msg_rule, msg_bit, msg_pin_jamma, msg_key_jamma])
    msg_crc = codecs.decode(jammasd_crc8(msg_body), "hex_codec")
    msg_array = [msg_header, msg_body, msg_crc, bytearray(codecs.decode("000000000000000000", "hex_codec"))]
    msg = b''.join(msg_array)
    hidapi.hid_send_feature_report(jammasd_id, msg)    
    
    jammasd_hid_close(jammasd_id)
    sys.exit(0)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-r', '--rule',      default=None, dest='rule',       help='Rule, range 1..100')
    parser.add_option('-p', '--jammapin',  default=None, dest='jamma_pin',  help='set jamma pin')
    parser.add_option('-k', '--keycode',   default=None, dest='keycode',    help='set scancode keyboard emulated')
    parser.add_option('-g', '--get',       default=None, dest='action_get', help='get a rule', action='store_true')
    parser.add_option('-s', '--set',       default=None, dest='action_set', help='set a rule', action='store_true')
    parser.add_option('-l', '--list-hid',  default=None, dest='action_list', help='list all hid', action='store_true')
    args, argCmdLine = parser.parse_args()
    
    
    """incoming = "010203"
    if sys.version_info[0] == 3:
        hex_data = codecs.decode(incoming, "hex_codec")
    else:
        hex_data = incoming.decode("hex")
    print(hex_data)
    msg = bytearray(hex_data)
    sys.exit(0)"""
    
    #mydict = {'george':'16_','amber':19}
    #print (getKeysByValue(mydict, '16_'))
    #sys.exit(0)
    if not argCmdLine:
        if not args.action_get and not args.action_set and not args.action_list:
            parser.error('Please give a read or set argument')
            sys.exit(1)
        
                
        if (args.action_get or args.action_set):
            if args.action_list:
                print("Option list not compatible with get or set")
                sys.exit(1)
                
            if not args.rule:
                print("Please give a rule with --rule argument")
                sys.exit(1)
            
            if not args.rule.isnumeric():
                print("Rule is not numeric")
                sys.exit(1)

            rule = int(args.rule)
            if not (rule in range(1, 100)):
                print("Please give a rule between 1..100")
                sys.exit(1)
            
            if args.action_get:
                jammasd_hid_read(rule)
                sys.exit(0)
            
            if args.action_set:
                if not args.jamma_pin or not args.keycode:
                    print("Please give both jamma_pin and keycode")
                    sys.exit(1)

                jamma_pin = args.jamma_pin.upper()
                keycode = args.keycode.upper()
                if not getKeysByValue(jammasdPIN, jamma_pin):
                    print("Pin jamma not defined")
                    sys.exit(1)
                
                if not getKeysByValue(jammasdKEY, keycode):
                    print("keycode not defined")
                    sys.exit(1)

                jammasd_hid_write(args.rule, jamma_pin, keycode)
        
        if args.action_list:
            jammasd_hid_list_devices()

        sys.exit(0)
    else:
        sys.exit(1)

    """if not sys.stdin.isatty():
        # there's something in stdin
        msg = sys.stdin.read().strip()
        if msg == "":
            print("No data input. Either provide by stdin or arguments")
            sys.exit(1)
    elif len(sys.argv) > 1:
        msg = sys.argv[1]
    else:
        print("No data input. Either provide by stdin or arguments")
        sys.exit(1)

    try:
        sys.stdout.write(calc(msg))
        sys.exit(0)
    except Exception as err:
        print("An Error Occured: {0}".format(err))
        sys.exit(1)"""
