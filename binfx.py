def raw_input(msg):
    print(msg)
    from sys import stdin
    return stdin.buffer.read()
def raw_print(*msgs, end=False, sep=False, fsp=False):
    from sys import stdout
    for msg in msgs:
        if sep:
            if fsp: stdout.buffer.write(sep)
            else: fsp=True
        try: stdout.buffer.write(msg)
        except: stdout.buffer.write(tobin(msg))
    if end: stdout.buffer.write(end)
def toint(inp, b=0, e='big'):
    try: return int.from_bytes(inp, e)
    except: None
    try: return int(inp, b)
    except: None
    try: return int(inp)
    except: None
    return None
def tobin(inp, p=0, e='big'):
    try:
        return bytes.fromhex(inp)
    except: None
    try:
        from math import ceil, log
        if not p: p=ceil(log(inp+1,256))
        return int.to_bytes(inp, p, e)
    except: None
    try:
        if inp.startswith('0x'): inp=inp[2:]
        if len(inp)%2: inp='0'+inp
        return bytes.fromhex(inp)
    except: None
    return None
def tohex(inp, b=0, p=0):
    try: return inp.hex()
    except: None
    try: return hex(inp)
    except: None
    if p==0:
        try: return format(inp, 'x')
        except: None
    elif p>0:
        try: return format(inp, '0'+str(p*2)+'x')
        except: None
    try: return format(int(inp), 'x')
    except: None
    return None
def sample():
    print("Examples for using binfx: ")
    print()
    print("toint(b'\x20\x04', e='little') =",toint(b'\x20\x04', e='little'))
    print("toint('0x420') =",toint('0x420'))
    print("toint('420', b=16) =",toint('420', b=16))
    print("toint('420') =",toint('420'))
    print("toint(b'\x01\xa4') =",toint(b'\x01\xa4'))
    print()
    print("tobin(420) =",tobin(420))
    print("tobin(420, p=3) =",tobin(420, p=3))
    print("tobin(420, e='little') =",tobin(420, e='little'))
    print("tobin('1a4') =",tobin('01a4'))
    print("tobin('0x01a4') =",tobin('0x01a4'))
    print()
    print("tohex(b'\x01\xa4') =",tohex(b'\x01\xa4'))
    print("tohex('420') =",tohex('420'))
    print("tohex(420) =",tohex(420))
    print("tohex(420, p=-1) =",tohex(420, p=-1))
    print("tohex(420, p=4) =",tohex(420, p=4))
    print("tohex(420.0) =",tohex(420.0))
    print()
#binread
"""
file = open("sample.bin", "rb")
byte = file.read(1)
while byte:
    print(byte)
    byte = file.read(1)
file.close()
"""
#from https://python-list.python.narkive.com/ka6eUCSF/read-stdin-as-bytes-rather-than-a-string
"""
sys.stdin wraps a buffered reader which itself wraps a raw file reader.
sys.stdin <_io.TextIOWrapper name='<stdin>' mode='r' encoding='UTF-8'>
sys.stdin.buffer <_io.BufferedReader name='<stdin>'>
sys.stdin.buffer.raw <_io.FileIO name='<stdin>' mode='rb'>

You should read from sys.stdin.buffer unless you really need the bare metal.
"""