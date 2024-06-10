
import os, sys, time
import random
random.uniform(1, 10)

def randomeDelayCode(f_amp):
    assert f_amp < 1.0
    if random.random() > 0.5: sym = 1.0
    else: sym = -1.0
    return random.random() * f_amp * sym

KEYCODE_DICT = {
    '\n' : { 'code' : b'\x28', 'isUpcase' : False}, #ENTER
    '\r' : { 'code' : b'\x28', 'isUpcase' : False}, #ENTER 按键对应数据包
    # '\x8' : { 'code' : b'\x29', 'isUpcase' : False},#ESCAPE
    # '\x8' : { 'code' : b'\x2A', 'isUpcase' : False}, #DELETE
    '	' : { 'code' : b'\x2B', 'isUpcase' : False}, #TAB
    ' ' : { 'code' : b'\x2C', 'isUpcase' : False},  #SPACE
    '-' : { 'code' : b'\x2D', 'isUpcase' : False},
    '=' : { 'code' : b'\x2E', 'isUpcase' : False},
    '[' : { 'code' : b'\x2F', 'isUpcase' : False},
    ']' : { 'code' : b'\x30', 'isUpcase' : False},
    '\\' : { 'code' : b'\x31', 'isUpcase' : False},
    #'' : { 'code' : b'\x32', 'isUpcase' : False},
    ';' : { 'code' : b'\x33', 'isUpcase' : False},
    '\'' : { 'code' : b'\x34', 'isUpcase' : False},
    #'' : { 'code' : b'\x35', 'isUpcase' : False},
    ',' : { 'code' : b'\x36', 'isUpcase' : False},
    '.' : { 'code' : b'\x37', 'isUpcase' : False},
    '/' : { 'code' : b'\x38', 'isUpcase' : False},
    #'' : { 'code' : b'\x39', 'isUpcase' : False},

    '!' : { 'code' : b'\x1E', 'isUpcase' : True},
    '@' : { 'code' : b'\x1F', 'isUpcase' : True},
    '#' : { 'code' : b'\x20', 'isUpcase' : True},
    '$' : { 'code' : b'\x21', 'isUpcase' : True},
    '%' : { 'code' : b'\x22', 'isUpcase' : True},
    '^' : { 'code' : b'\x23', 'isUpcase' : True},
    '&' : { 'code' : b'\x24', 'isUpcase' : True},
    '*' : { 'code' : b'\x25', 'isUpcase' : True},
    '(' : { 'code' : b'\x26', 'isUpcase' : True},
    ')' : { 'code' : b'\x27', 'isUpcase' : True},

    '_' : { 'code' : b'\x2D', 'isUpcase' : True},
    '+' : { 'code' : b'\x2E', 'isUpcase' : True},

    '{' : { 'code' : b'\x2F', 'isUpcase' : True},
    '}' : { 'code' : b'\x30', 'isUpcase' : True},
    '|' : { 'code' : b'\x31', 'isUpcase' : True},
    ':' : { 'code' : b'\x33', 'isUpcase' : True},
    '"' : { 'code' : b'\x34', 'isUpcase' : True},
    '<' : { 'code' : b'\x36', 'isUpcase' : True},
    '>' : { 'code' : b'\x37', 'isUpcase' : True},
    '?' : { 'code' : b'\x38', 'isUpcase' : True}
}

KEYBOARD_LEFT_CTRL = b"\x01" + b"\x00" * 7
KEYBOARD_LEFT_SHIFT = b"\x02" + b"\x00" * 7
KEYBOARD_RELEASE = b"\x00" * 8

def StringToKeyCode(str):
    lkey = []
    for a in str:
        if a >= 'a' and a <= 'z':
            key = ((ord(a) - ord('a') + 4).to_bytes(length=1, byteorder="little", signed=False))
            lkey.append(b"\x00" * 2 + key + b"\x00" * 5)
        elif a >= 'A' and a <= 'Z':
            lkey.append(KEYBOARD_LEFT_SHIFT)
            key = ((ord(a) - ord('A') + 4).to_bytes(length=1, byteorder="little", signed=False))
            lkey.append(b"\x02\x00" + key + b"\x00" * 5)
            lkey.append(KEYBOARD_LEFT_SHIFT)
        elif a >= '0' and a <= '9':
            key = ((ord(a) - ord('0') + 30).to_bytes(length=1, byteorder="little", signed=False))
            lkey.append(b"\x00" * 2 + key + b"\x00" * 5)
        else:
            x = KEYCODE_DICT.get(a)
            if x != None:
                if x['isUpcase'] == True:
                    lkey.append(KEYBOARD_LEFT_SHIFT)
                    lkey.append(b"\x02\x00" + x['code'] + b"\x00" * 5)
                    if x['isUpcase'] == True: lkey.append(KEYBOARD_LEFT_SHIFT)
                else:
                    lkey.append(b"\x00\x00" + x['code'] + b"\x00" * 5)
            
        lkey.append(KEYBOARD_RELEASE)
    return lkey

def KeyboardInput(s_buf):
    l = StringToKeyCode(s_buf)
    print("%d ascii, %d key press" % (len(s_buf), len(l)))
    f_hid = open("/dev/hidg0","wb")
    # f_hid = open("./test.bin", "wb") #output to a binary file for chechking
    for i in range(0, len(l)):
        try:
            d_code = randomeDelayCode(0.6)
            d_code = 0.1 * ( 1 - d_code )
            print("input '%s' %d/%d (%dms)" % (str(l[i]), i, len(l), (int(d_code * 1000))))
            f_hid.write(l[i])
            f_hid.flush()
            time.sleep(d_code)
        except KeyboardInterrupt:
            print("USER CANCEL")
            f_hid.write(b'\x00' * 8)
            f_hid.flush()
            f_hid.close()
            sys.exit()

    f_hid.close()

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("a file to input")
        exit()
    for d in range(5, 0, -1):
        print("left %d seconds start" % d)
        time.sleep(1)
    f = open(sys.argv[1],"r")
    f_buf = f.read()
    f.close()
    KeyboardInput(f_buf)
    exit()
