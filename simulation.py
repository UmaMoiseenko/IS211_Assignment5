import argparse
import csv
import urllib2

class Server:
    def __init__(self):
        self.currentTask = None
        self.timeRemaining = 0

    def tick(self):
        if self.currentTask != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    def busy(self):
        if self.currentTask != None:
            return True
        else:
            return False

    def startNext(self,newreq):
        self.currentTask = newreq
        self.timeRemaining = newreq.getTime() #get seconds

class Request:
    def __init__(self,request):
        self.timestamp = request[0]
        self.timeleft = request[2]

    def getStamp(self):
        return self.timestamp

    def getTime(self): #secs
        return self.timeleft 

    def waitTime(self, currenttime):
        return currenttime - self.timestamp

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def pop(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

def simulateOneServer(filename):
    server = Server()
    queue = Queue()
    waitingtimes = []
    sortedReqests = {}

    for request in filename:
        newSec = int(request[0])
        queue.enqueue(request)

        if newSec in sortedReqests: 
            sortedReqests[newSec].append(request)
        else:
            sortedReqests[newSec] = [request] 

    for currentSecond in sortedReqests:
        for req in sortedReqests[currentSecond]:
            Request(req)
            queue.dequeue()

        if (not server.busy()) and (not queue.isEmpty()):
            nextreq = Request(queue.dequeue())
            waitingtimes.append(nextreq.waitTime(nextreq))
            #breaks after this line
            server.startNext(nextreq)

        server.tick()

    averageWait=sum(waitingtimes)/len(waitingtimes) * 0.001
    print("Average Wait %2.2f secs for %3d requests."%(averageWait,queue.size()))


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
