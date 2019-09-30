# -----------------------------------------------------------------
# Tecnológico de Costa Rica
# Curso: Redes
# TCP / UDP Sockets Connection
# Katherine Tuz Carrillo
# 2019
# -----------------------------------------------------------------
from socket import *
import sys
from _thread import *
import threading
import os
# -----------------------------------------------------------------
# TCP client functions
# -----------------------------------------------------------------
def tcpClientOn(param, dirip, portn, filename):
    host = dirip
    port = int(portn)
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
    except error:
        return ('Sorry, the server TCP is off work')

    s.sendall(bytes(param,"utf8")) # Sending param to server
    # -----------------------------------------------------------------
    # List
    # -----------------------------------------------------------------
    if (param == '-l'): # Msg received from server
        replace= " "
        while True:
            try:
                data = s.recv(1024)
                if ((str(data.decode('ascii'))).find("Finish") != -1):
                    print('Msg from the server: ',(str(data.decode('ascii'))).replace("Finish",replace))
                    print('Process finished')
                    break
                print('Msg from the server: ', str(data.decode('ascii'))+ " ")
            except error:
                print('Error exception')
    # -----------------------------------------------------------------
    # Download
    # -----------------------------------------------------------------
    elif (param == '-d'):
        try:
            data = filename
            s.send(bytes(data, "utf8"))  # Sending name file
            filebytes = s.recv(1024)
            if ((str(filebytes.decode('ascii'))) == "not"):
                print("There are no files with that name")
            else:
                fSize = int((str(filebytes.decode('ascii'))))
                f = open(".\\mydownloads\\" + data, 'wb')
                obtain = s.recv(1024)
                limit = len(obtain)
                f.write(obtain)
                while limit < fSize:
                    obtain = s.recv(1024)
                    limit += len(obtain)
                    f.write(obtain)
                print('Process finished')
            s.close()
        except error:
            print('Error exception')
    # -----------------------------------------------------------------
    # Upload
    # -----------------------------------------------------------------
    else:
        try:
            data = filename
            listing = os.listdir('./myfiles')
            getSize = str(os.path.getsize('.\\myfiles\\' + data))
            s.send(bytes(data, "utf8"))
            response = s.recv(1024)
            s.send(bytes(getSize, "utf8"))
            if listing.count(data) > 0:
                with open('.\\myfiles\\' + data, 'rb') as f:
                    sendBytes = f.read(1024)
                    s.send(sendBytes)
                    while True:
                        upload_status = s.recv(1024)
                        upload_status = str(upload_status.decode('ascii'))
                        if upload_status == "Continue":
                            sendBytes = f.read(1024)
                            s.send(sendBytes)
                        else:
                            print('Process finished')
                            break
                s.close()
            else:
                print('No file founded')
            s.close()
        except error:
            print('Error exception')

    s.close()

# -----------------------------------------------------------------
# UDP client functions
# -----------------------------------------------------------------
def udpClientOn(param, dirip, portn, filename):
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect((dirip, portn))
    except error:
        return('Sorry, the server UDP is off work')

    s.sendto(bytes(param,"utf8"), (dirip, portn)) # sending param to server
    # -----------------------------------------------------------------
    # List
    # -----------------------------------------------------------------
    if (param == '-l'):
        while True:
            try:
                d = s.recvfrom(1024)
                data= d[0]
                addr= d[1]
                if ((str(data.decode('ascii')))== " Finish"):
                    print('Process finished')
                    break
                print('Msg from the server:', str(data.decode('ascii')))
            except error:
                print('Error exception')
    # -----------------------------------------------------------------
    # Download
    # -----------------------------------------------------------------
    elif (param == '-d'):
        try:
            data = filename
            s.sendto(bytes(data, "utf8"), (dirip, portn))  # Sending name file
            filebytes = s.recvfrom(1024)
            filebytesData = filebytes[0]
            addr = filebytes[1]
            if ((str(filebytesData.decode('ascii'))) == "not"):
                print("There are no files with that name")
            else:
                fSize = int((str(filebytesData.decode('ascii'))))
                f = open(".\\mydownloads\\" + data, 'wb')
                obtain = s.recvfrom(1024)
                obtainData = obtain[0]
                limit = len(obtainData)
                f.write(obtainData)
                while limit < fSize:
                    obtain = s.recv(1024)
                    obtainData = obtain[0]
                    limit += len(obtainData)
                    f.write(obtainData)
                print('Process finished')
            s.close()
        except error:
            print('Error exception')
    # -----------------------------------------------------------------
    # Upload
    # -----------------------------------------------------------------
    else:
        try:
            data = filename
            listing = os.listdir('./myfiles')
            getSize = str(os.path.getsize('.\\myfiles\\' + data))
            s.sendto(bytes(data, "utf8"), (dirip, portn))
            response = s.recvfrom(1024)
            addr = response [1]
            s.sendto(bytes(getSize, "utf8"), addr)
            if listing.count(data) > 0:
                with open('.\\myfiles\\' + data, 'rb') as f:
                    sendBytes = f.read(1024)
                    s.sendto(sendBytes, addr)
                    while True:
                        status = s.recvfrom(1024)
                        statusData = status[0]
                        addr = status[1]
                        cstatus = str(statusData.decode('ascii'))
                        if cstatus == "Continue":
                            sendBytes = f.read(1024)
                            s.sendto(sendBytes, addr)
                        else:
                            print('Process finished')
                            break
                s.close()
            else:
                print('No file founded')
            s.close()
        except error:
            print('Error exception')

    s.close()

# -----------------------------------------------------------------
# Main
# -----------------------------------------------------------------
if __name__ == '__main__':
    # CMD format: py client.py programType dirIp #port -param nombreArchivo
    # On the server side, run the corresponding file:
    # -> server: if programType = tcp
    # -> udpServer: if programType = udp
    global param
    programType = sys.argv[1] # upd or tcp
    dirip= sys.argv[2] # ip
    portn= int(sys.argv[3]) # port
    param = sys.argv[4]  # param given. Options: -l -u -d
    filename= sys.argv[5] #file name

    if programType == 'tcp':
        tcpClientOn(param, dirip, portn, filename)
    else:
        udpClientOn(param, dirip, portn, filename)
