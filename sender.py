#Names:
#Adam Stecklov
#Gulnar Saharya

from common import *

class sender:
    RTT = 20

    def isCorrupted(self, packet):
        '''Checks if a received packet (acknowledgement) has been corrupted
        during transmission.
        Return true if computed checksum is different than packet checksum.
        '''
        ccs = checksumCalc(packet.payload)
        if(ccs + packet.ackNum + packet.seqNum == packet.checksum):
            return False
        else:
            return True

    def isDuplicate(self, packet):
        '''checks if an acknowledgement packet is duplicate or not
        similar to the corresponding function in receiver side
        '''
        if(self.seqnum == packet.ackNum):
            return False
        else:
            return True

    def getNextSeqNum(self):
        '''generate the next sequence number to be used.
        '''
        self.seqnum = (self.seqnum + 1)%2
        return

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        self.piT = None
        self.seqnum = None
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        '''initialize the sequence number and the packet in transit.
        Initially there is no packet is transit and it should be set to None
        '''
        self.piT = None
        self.seqnum = 0
        return

    def timerInterrupt(self):
        '''This function implements what the sender does in case of timer
        interrupt event.
        This function sends the packet again, restarts the time, and sets
        the timeout to be twice the RTT.
        You never call this function. It is called by the simulator.
        '''
        newPacket = self.piT
        #self.networkSimulator.stopTimer(A)
        self.networkSimulator.udtSend(A,newPacket)
        self.networkSimulator.startTimer(A, float(2*self.RTT))

        return

    def output(self, message):
        '''prepare a packet and send the packet through the network layer
        by calling calling utdSend.
        It also start the timer.
        It must ignore the message if there is one packet in transit
        '''
        #check for packet in transit
        if(self.piT is not None):
            return

        newPacket = Packet(self.seqnum,0,checksumCalc(message.data)+self.seqnum,message.data)
        self.piT = newPacket
        self.networkSimulator.udtSend(A,newPacket)
        self.networkSimulator.startTimer(A, float(self.RTT))

        return

    def input(self, packet):

        '''If the acknowlegement packet isn't corrupted or duplicate,
        transmission is complete. Therefore, indicate there is no packet
        in transition.
        The timer should be stopped, and sequence number  should be updated.

        In the case of duplicate or corrupt acknowlegement packet, it does
        not do anything and the packet will be sent again since the
        timer will be expired and timerInterrupt will be called by the simulator.
        '''
        #print("acknum = ", packet.ackNum,"seqnum = ", packet.seqNum, ", checksum = ",packet.checksum)
        if(self.isCorrupted(packet) or self.isDuplicate(packet)):
            return
        else:
            self.getNextSeqNum()
            self.piT = None
            self.networkSimulator.stopTimer(A)
            return
