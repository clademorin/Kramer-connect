import socket
import struct
import argparse

#Method to send the preformatted payload to the device
def send(ip, port, payload):
    print("Preparing payload...")
    hexstring = struct.pack('!I', payload)
    print("Payload prepared, preparing channel...")
    con  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        con.connect((ip,port))
    except:
        print(f"Error: target unreachable")
        return False
    print("Target locked....")
    print("!!!!FIRE!!!!")
    try:
        con.send(hexstring)
    except:
        print("Target missed...")
        return
    risp = con.recv(1024)
    con.close()
    print("Direct hit")
    print(f'Response received: {risp}')
    return risp

#Preformat a payload to send a "set to preset" command
def preset(ip, port, pres):
    return send(ip, port, int(f"0x048{pres}8081", 16))

#Preformat a payload to activate a simple video switch
def switch(ip, port, input, output):
    return send(ip, port, int(f"0x018{str(input)}8{str(output)}81", 16))

#Preformat a status request
def status(ip, port, output):
    response = str(send(ip, port, int(f"0x05808{str(output)}81",16)))
    if response == "False":
        return False
    print(response[9:12])
    return int(response[10])


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type=str, help="Video Input")
parser.add_argument("-o", "--output", default=0, help="Video Input")
parser.add_argument("-p", "--port", type=int, dest="port", default=5000, help="Target port")
parser.add_argument("-P", "--preset",nargs='?', dest="preset", help="Preset selection")
parser.add_argument("ip", help="Target ip address")


try:
    args = parser.parse_args()
    if args.preset:
        print(f"Payload for preset {args.preset} selected")
        send(args.ip, args.port, int(f"0x048{args.preset}8081",16))
    else:
        print(f"Payload for for video {args.input} in {args.output} selected")
        send(args.ip, args.port, int(f"0x018{args.input}8{args.output}81",16))
except:
    print("invalid arguments")
