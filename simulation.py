import argparse
import csv
import urllib2

"""
data file:
http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv
"""

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Server:
    def __init__(self, ppm):
        self.pagerate = ppm
        self.currentRequest = None
        self.timeRemaining = 0

    def tick(self):
        if self.currentRequest != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentRequest = None

    def busy(self):
        if self.currentRequest != None:
            return True
        else:
            return False

    def startNext(self,newRequest):
        self.currentRequest = newRequest
        self.timeRemaining = newRequest.getPages()

class Request:
    def __init__(self, time, timeReq):
        self.time = time
        self.pages = timeReq

    def getStamp(self):
        return self.timestamp

    def getTimeReq(self):
        return self.timeReq

    def waitTime(self, currenttime):
        return currenttime - self.timestamp


def simulateOneServer(filename):
    myServer = Server(0)
    myQueue = Queue()
    waitingtimes = []

    for row in filename:
        numb_list.append(row[0])
        request = Request(row[0], row[2])
        myQueue.enqueue(request)

        if (not myServer.busy()) and (not myQueue.isEmpty()):
            nextRequest = myQueue.dequeue()
            waitingtimes.append(nextRequest.waitTime(currentSecond))
            myServer.startNext(nextRequest)

    myServer.tick()
    averageWait=sum(waitingtimes)/len(waitingtimes)
    print("Average Wait %6.2f secs %3d requests remaining."%(averageWait,myQueue.size()))
    

def main():

    url_parser = argparse.ArgumentParser()
    url_parser.add_argument("--file", help='enter URL to CSV file', type=str)
    args = url_parser.parse_args()

    if args.file:
        try:
            filename = csv.reader(urllib2.urlopen(args.file))
            simulateOneServer(filename)
        except:
            print "Invalid URL"
    else:
        print "insert url for csv file after --file. Bye"


if __name__ == "__main__":
    main()
