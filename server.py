from datetime import datetime
from _thread import *
import socket as soc
import random
from time import sleep


hostList = {}
checkUpdate = {}
dashBoard = {}


def Update():
    global dashBoard
    global checkUpdate
    while(True):
        dateTime = list(datetime.now().timetuple())
        day = str(dateTime[2])
        month = str(dateTime[1])
        year = str(dateTime[0])
        hour = str(dateTime[3])
        minute = str(dateTime[4])
        second = str(dateTime[5])
        time = "%s/%s/%s %s:%s:%s" % (day, month, year,
                                      hour, minute, second)
        value = str(random.randrange(-10_000, 10_001))
        dashBoard[time] = value

        print("\t" + time + "\t" + dashBoard[time])

        for address in checkUpdate:
            checkUpdate[address] = True

        sleep_time = random.randrange(1, 10)
        sleep(sleep_time)


def thread_client(conn, addr):
    global dashBoard
    global checkUpdate
    data = ""
    for item in dashBoard:
        data += item + "\t" + dashBoard[item]
    conn.send(data.encode())
    while(True):
        if checkUpdate[addr]:
            # get the last dashBoard
            time = list(dashBoard.keys())[-1]
            data = time + "\t" + dashBoard[time]
            # send update to client
            conn.send(data.encode())
            checkUpdate[addr] = False


if __name__ == "__main__":
    _ERROR = 0
    try:
        socketServer = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
    except soc.error as error:
        print(error)
        _ERROR = 1
    if (_ERROR == 0):
        host = '127.0.0.1'
        port = 4444
        end_point = (host, port)
        socketServer.bind(end_point)
        socketServer.listen(10)
        id = 0
        try:
            print("Server is running...")
            start_new_thread(Update, ())
            while (True):
                connect, address = socketServer.accept()
                hostList[address] = connect
                checkUpdate[address] = False
                id = id + 1
                start_new_thread(
                    thread_client, (connect, address))
        except KeyboardInterrupt:
            socketServer.close()
