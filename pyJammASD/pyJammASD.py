#!/usr/bin/python
# -*- coding: utf-8 -*-
############################################
# 
# 
# 
############################################

import binascii
import sys
import configparser
import struct
from hidapi import *
from optparse import OptionParser

import codecs
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
                   "45":"APEX",
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
                   "86":"KP_-",
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
                   "100":"MINOR",
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
    
    msg_body = bytearray()
    msg_body.extend(msg_bodyhex)
    msg_crc = codecs.decode(jammasd_crc8(msg_body), "hex_codec")

    msg_array = bytearray()
    msg_array.extend(msg_header)
    msg_array.extend(msg_body)
    msg_array.extend(msg_crc)
    msg_array.extend(bytearray(codecs.decode("000000000000000000000000000000", "hex_codec")))
    hidapi.hid_send_feature_report(jammasd_id, msg_array)    
    
    msg_buffer = bytearray(codecs.decode("0000000000000000000000000000000000", "hex_codec"))
    msg_data = hidapi.hid_get_feature_report(jammasd_id, msg_buffer)
    print(len(msg_data))
    print(str(msg_data))
    print(len(msg_buffer))
    print(str(msg_buffer))
        
    jammasd_hid_close(jammasd_id)
    sys.exit(0)

def jammasd_hid_video_read():
    hidapi.hid_init()
    jammasd_id = jammasd_hid_open()
    
    jammasd_state = hidapi.hid_read(jammasd_id, 8)
    print(str(jammasd_state))
    jammasd_video_frequency_h_raw = jammasd_state[4:6]
    jammasd_video_frequency_v_raw = jammasd_state[7:9]
    for i in jammasd_video_frequency_v_raw:
        print(str(i))
    
    jammasd_video_frequency_h = struct.unpack(">H", jammasd_video_frequency_h_raw)[0]*10
    jammasd_video_frequency_v = 1/(struct.unpack(">H", jammasd_video_frequency_v_raw)[0]*16*0.000000667)
    print("H Frequency: %s" % str(jammasd_video_frequency_h))
    print("V Frequency: %s" % str(jammasd_video_frequency_v))
    
    jammasd_hid_close(jammasd_id)
    sys.exit(0)


def jammasd_rule_write_hid(hid_id, rule, pin_jamma, key_jamma, flagEnable, flagShifted, flagInverse, flagToggle, flagRepeat, flagPulse):
    """byte 1: 12
    byte 2: numero di regola da 1 a 100. la numero 0 ha una funzione particolare che poi ci arriviamo

    byte 3: pin jamma (da prendere in una tabella)
    byte 4: tasto da emulare (da prendere in una tabella)"""

        
    #Init message is 00  +  length(5)  +  decimal 12 (0C), so 00050C
    msg_bodyhex = codecs.decode("0C", "hex_codec")
    
    msg_header = bytearray(codecs.decode("0005", "hex_codec"))
    
    #msg_bit:  enable|shifted<<1|inverse<<2|toggle<<3|repeat<<4|pulse<<5
    msg_bit = codecs.decode("%02x" % (flagEnable|flagShifted<<1|flagInverse<<2|flagToggle<<3|flagRepeat<<4|flagPulse<<5), "hex_codec")
    
    msg_pin_jamma = codecs.decode("%02x" % int(getKeysByValue(jammasdPIN, pin_jamma)[0]), "hex_codec")
    msg_key_jamma = codecs.decode("%02x" % int(getKeysByValue(jammasdKEY, key_jamma)[0]), "hex_codec")
    msg_rule = codecs.decode("%02x" % int(rule), "hex_codec")
    
    #msg_body = b''.join([msg_bodyhex, msg_rule, msg_bit, msg_pin_jamma, msg_key_jamma])
    msg_body = bytearray()
    msg_body.extend(msg_bodyhex)
    msg_body.extend(msg_rule)
    msg_body.extend(msg_bit)
    msg_body.extend(msg_pin_jamma)
    msg_body.extend(msg_key_jamma)

    #.extend(msg_rule).extend(msg_bit).extend(msg_pin_jamma).extend(msg_key_jamma)
    msg_crc = codecs.decode(jammasd_crc8(msg_body), "hex_codec")
    #msg_array = [msg_header, msg_body, msg_crc, bytearray(codecs.decode("0000000000000000000000", "hex_codec"))]
    msg_array = bytearray()
    msg_array.extend(msg_header)
    msg_array.extend(msg_body)
    msg_array.extend(msg_crc)
    msg_array.extend(bytearray(codecs.decode("0000000000000000000000", "hex_codec")))
    for i in msg_array:
        print("%02x" % i)

    #msg = b''.join(msg_array)
    print(str(msg_array))
    xx = hidapi.hid_send_feature_report(hid_id, msg_array)    


def jammasd_rule_write(rule, pin_jamma, key_jamma, flagEnable, flagShifted, flagInverse, flagToggle, flagRepeat, flagPulse):
    hidapi.hid_init()
    jammasd_id = jammasd_hid_open()
        
    jammasd_rule_write_hid(jammasd_id, rule, pin_jamma, key_jamma, flagEnable, flagShifted, flagInverse, flagToggle, flagRepeat, flagPulse)
    jammasd_hid_close(jammasd_id)
    sys.exit(0)


def jammasd_init_jamma():
    rule_list = [
        {"rule":0,  "pin_jamma":"P1_START", "key_jamma":"1", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":1,  "pin_jamma":"TEST", "key_jamma":"9", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":2,  "pin_jamma":"P1_COIN", "key_jamma":"5", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":3,  "pin_jamma":"P1_START", "key_jamma":"1", "flagEnable":0, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":4,  "pin_jamma":"P1_UP", "key_jamma":"U_ARROW", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":5,  "pin_jamma":"P1_DOWN", "key_jamma":"D_ARROW", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":6,  "pin_jamma":"P1_LEFT", "key_jamma":"L_ARROW", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":7,  "pin_jamma":"P1_RIGHT", "key_jamma":"R_ARROW", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":8,  "pin_jamma":"P1_BUTTON_1", "key_jamma":"L_CTRL", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":9,  "pin_jamma":"P1_BUTTON_2", "key_jamma":"L_ALT", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":10, "pin_jamma":"P1_BUTTON_3", "key_jamma":"SPACE", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":11, "pin_jamma":"P1_BUTTON_4", "key_jamma":"L_SHIFT", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":12, "pin_jamma":"P1_BUTTON_5", "key_jamma":"Z", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":13, "pin_jamma":"P1_BUTTON_6", "key_jamma":"X", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":14, "pin_jamma":"P1_BUTTON_7", "key_jamma":"C", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":15, "pin_jamma":"P1_BUTTON_8", "key_jamma":"V", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":16, "pin_jamma":"SERVICE", "key_jamma":"F2", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":17, "pin_jamma":"P2_COIN", "key_jamma":"6", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":18, "pin_jamma":"P2_START", "key_jamma":"2", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":19, "pin_jamma":"P2_UP", "key_jamma":"R", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":20, "pin_jamma":"P2_DOWN", "key_jamma":"F", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":21, "pin_jamma":"P2_LEFT", "key_jamma":"D", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":22, "pin_jamma":"P2_RIGHT", "key_jamma":"G", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":23, "pin_jamma":"P2_BUTTON_1", "key_jamma":"A", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":24, "pin_jamma":"P2_BUTTON_2", "key_jamma":"S", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":25, "pin_jamma":"P2_BUTTON_3", "key_jamma":"Q", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":26, "pin_jamma":"P2_BUTTON_4", "key_jamma":"W", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":27, "pin_jamma":"P2_BUTTON_5", "key_jamma":"I", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":28, "pin_jamma":"P2_BUTTON_6", "key_jamma":"K", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":29, "pin_jamma":"P2_BUTTON_7", "key_jamma":"J", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":30, "pin_jamma":"P2_BUTTON_8", "key_jamma":"L", "flagEnable":1, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":31, "pin_jamma":"TEST", "key_jamma":"NONE", "flagEnable":0, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},        
        {"rule":32, "pin_jamma":"P1_BUTTON_1", "key_jamma":"5", "flagEnable":1, "flagShifted":1, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":33, "pin_jamma":"P1_BUTTON_2", "key_jamma":"6", "flagEnable":1, "flagShifted":1, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":34, "pin_jamma":"P1_BUTTON_6", "key_jamma":"TAB", "flagEnable":1, "flagShifted":1, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":35, "pin_jamma":"P2_START", "key_jamma":"ESC", "flagEnable":1, "flagShifted":1, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":36, "pin_jamma":"P1_UP", "key_jamma":"KP_+", "flagEnable":1, "flagShifted":1, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":37, "pin_jamma":"P1_DOWN", "key_jamma":"KP_-", "flagEnable":1, "flagShifted":1, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
        {"rule":38, "pin_jamma":"P1_COIN", "key_jamma":"6", "flagEnable":1, "flagShifted":1, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0},
]
        
    for i in range(39,101):
        rule_list.append({"rule":i, "pin_jamma":"TEST", "key_jamma":"NONE", "flagEnable":0, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0})
    
    #p2 start+coin = 6 (gettone per player 2)
    
    hidapi.hid_init()
    jammasd_id = jammasd_hid_open()
        
    for rule in rule_list:
        jammasd_rule_write_hid(jammasd_id,
                               rule["rule"],
                               rule["pin_jamma"],
                               rule["key_jamma"],
                               rule["flagEnable"],
                               rule["flagShifted"],
                               rule["flagInverse"],
                               rule["flagToggle"],
                               rule["flagRepeat"],
                               rule["flagPulse"])

    jammasd_hid_close(jammasd_id)

def jammasd_load_config(filename):
    import json
    with open(filename, 'r') as f:
        datastore = json.load(f)
    #print(str(datastore))
    
    rules = {}
    for i in range(0, 101):
        rules.update({"rule_%d" % i:{"pin_jamma":"TEST", "key_jamma":"NONE", "flagEnable":0, "flagShifted":0, "flagInverse":0, "flagToggle":0, "flagRepeat":0, "flagPulse":0}})
    for rule in datastore:
        rules["rule_%s" % rule["rule"]].update({"pin_jamma":rule["pin_jamma"],
                                                "key_jamma":rule["key_jamma"],
                                                "flagEnable":rule["flagEnable"],
                                                "flagShifted":rule["flagShifted"],
                                                "flagInverse":rule["flagInverse"],
                                                "flagToggle":rule["flagToggle"],
                                                "flagRepeat":rule["flagRepeat"],
                                                "flagPulse":rule["flagPulse"]})

    hidapi.hid_init()
    jammasd_id = jammasd_hid_open()        

    for i in range(0, 101):
        rule = rules["rule_%s" % i]
        jamma_pin = rule["pin_jamma"]
        keycode = rule["key_jamma"]
        flagEnable = rule["flagEnable"]
        flagShifted = rule["flagShifted"]
        flagInverse = rule["flagInverse"]
        flagToggle = rule["flagToggle"]
        flagRepeat = rule["flagRepeat"]
        flagPulse = rule["flagPulse"]
        jammasd_rule_write_hid(jammasd_id, i, jamma_pin, keycode, flagEnable, flagShifted, flagInverse, flagToggle, flagRepeat, flagPulse)

    jammasd_hid_close(jammasd_id)

    sys.exit(0)

def jammasd_print_infotable(info_table):
    if info_table == "P":
        print("JAMMA_PIN table:")
        print("------------------------------------------------------")
        for k in jammasdPIN.values():
            print(k)
            
    if info_table == "K":
        print("JAMMA KEYCODE table:")
        print("------------------------------------------------------")
        for k in jammasdKEY.values():
            print(k)
    sys.exit(0)


def jammasd_main():
    parser = OptionParser()
    parser.add_option('-r', '--rule',      default=None, dest='rule',           help='Rule, range 0..100')
    parser.add_option('-p', '--jammapin',  default=None, dest='jamma_pin',      help='set jamma pin')
    parser.add_option('-k', '--keycode',   default=None, dest='keycode',        help='set scancode keyboard emulated')
    parser.add_option('-f', '--flag',      default=None, dest='flag',           help='set additional flag to the key')
    parser.add_option('-i', '--info',      default=None, dest='info_table',     help='show info about jamma_pin or keycode tables [p,k]')
    parser.add_option('-g', '--get',       default=None, dest='action_get',     help='get a rule', action='store_true')
    parser.add_option('-s', '--set',       default=None, dest='action_set',     help='set a rule', action='store_true')
    parser.add_option('-v', '--video',     default=None, dest='action_video',   help='get video frequency', action='store_true')
    parser.add_option('-l', '--list-hid',  default=None, dest='action_list',    help='list all hid', action='store_true')
    parser.add_option('-c', '--config',    default=None, dest='action_config',  help='read a config')
    args, argCmdLine = parser.parse_args()
        
    if not argCmdLine:
        if not args.action_get and \
           not args.action_set and \
           not args.action_list and \
           not args.info_table and \
           not args.flag and \
           not args.action_config and \
           not args.action_video:
            parser.error('Please give a right command, see -h for help')
            sys.exit(1)
        
        if (args.action_config):
            jammasd_load_config(args.action_config)
            sys.exit(0)
                
        if (args.action_get or args.action_set):
            if args.action_video:
                print("Option video not compatible with get or set")
                sys.exit(1)
                
            if args.info_table:
                print("Option info-table not compatible with get or set")
                sys.exit(1)
                
            if args.action_list:
                print("Option list not compatible with get or set")
                sys.exit(1)
                
            if not args.rule:
                print("Please give a rule with --rule argument")
                sys.exit(1)
            
            rule = int(args.rule)
            if not (rule in range(0, 100)):
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
                
                flagEnable = 1
                flagShifted = 0
                flagInverse = 0
                flagToggle = 0
                flagRepeat = 0
                flagPulse = 0
                if args.flag:
                    if len(args.flag) != 6:
                        print("Error button flag")
                        
                        sys.exit(1)
                    flagEnable = int(args.flag[0:1])
                    flagShifted = int(args.flag[1:2])
                    flagInverse = int(args.flag[2:3])
                    flagToggle = int(args.flag[3:4])
                    flagRepeat = int(args.flag[4:5])
                    flagPulse = int(args.flag[5:6])
                    if flagEnable not in (0, 1) or \
                       flagShifted not in (0, 1) or \
                       flagInverse not in (0, 1) or \
                       flagToggle not in (0, 1) or \
                       flagRepeat not in (0, 1) or \
                       flagPulse not in (0, 1):
                        print("Error button flag")
                        sys.exit(1)

                jammasd_rule_write(args.rule, jamma_pin, keycode, flagEnable, flagShifted, flagInverse, flagToggle, flagRepeat, flagPulse)
        
        if args.action_list:
            if args.action_video:
                print("Option video not compatible")
                sys.exit(1)
                
            if args.info_table:
                print("Option info_table not compatible")
                sys.exit(1)

            jammasd_hid_list_devices()
        
        if args.action_video:                
            if args.info_table:
                print("Option info_table not compatible")
                sys.exit(1)
            jammasd_hid_video_read()
            sys.exit(0)
        
        if args.info_table:
            info_table = args.info_table.upper()
            if info_table not in ["P", "K"]:
                print("Info table must be use with P or K option")
                sys.exit(1)

            jammasd_print_infotable(info_table)
            sys.exit(0)

        print("Please see -h for help")
        sys.exit(0)
    else:
        print("Please see -h for help")
        sys.exit(1)

