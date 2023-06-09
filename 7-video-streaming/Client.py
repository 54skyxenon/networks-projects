# Client.py

from tkinter import *
import tkinter.messagebox as tkMessageBox
from PIL import Image, ImageTk
import socket, threading, os
from time import time, sleep

from RtpPacket import RtpPacket

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

class Client:
    INIT = 0
    READY = 1
    PLAYING = 2
    state = INIT
    
    SETUP = 0
    PLAY = 1
    PAUSE = 2
    TEARDOWN = 3
    DESCRIBE = 4
    
    # Initiation..
    def __init__(self, master, serveraddr, serverport, rtpport, filename):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.handler)
        self.createWidgets()
        self.serverAddr = serveraddr
        self.serverPort = int(serverport)
        self.rtpPort = int(rtpport)
        self.fileName = filename
        self.rtspSeq = 0
        self.sessionId = 0
        self.requestSent = -1
        self.teardownAcked = 0
        self.connectToServer()
        self.frameNbr = 0

        # OPTIONAL EXERCISE: Summarize session
        self.startTime = None
        self.endTime = None
        self.packetsReceived = 0
        self.receivedSize = 0
        self.bandwidths = []

        # OPTIONAL EXERCISE: Setup automatically upon program entry
        self.setupMovie()
        
    def createWidgets(self):
        """Build GUI."""
        # OPTIONAL EXERCISE: Omit setup button
        # Create Play button        
        self.start = Button(self.master, width=20, padx=3, pady=3)
        self.start["text"] = "Play"
        self.start["command"] = self.playMovie
        self.start.grid(row=1, column=0, padx=2, pady=2)
        
        # Create Pause button            
        self.pause = Button(self.master, width=20, padx=3, pady=3)
        self.pause["text"] = "Pause"
        self.pause["command"] = self.pauseMovie
        self.pause.grid(row=1, column=1, padx=2, pady=2)
        
        # Create Stop button
        # OPTIONAL EXERCISE: Stop button automatically does the teardown, just renamed
        self.stop = Button(self.master, width=20, padx=3, pady=3)
        self.stop["text"] = "Stop"
        self.stop["command"] = self.exitClient
        self.stop.grid(row=1, column=2, padx=2, pady=2)

        # OPTIONAL EXERCISE: Create Describe button
        self.describe = Button(self.master, width=20, padx=3, pady=3)
        self.describe["text"] = "Describe"
        self.describe["command"] = self.getDescription
        self.describe.grid(row=1, column=3, padx=2, pady=2)
        
        # Create a label to display the movie
        self.label = Label(self.master, height=19)
        self.label.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S, padx=5, pady=5) 
    
    def setupMovie(self):
        """Setup button handler."""
        if self.state == self.INIT:
            self.sendRtspRequest(self.SETUP)
    
    def exitClient(self):
        """Teardown button handler."""
        self.sendRtspRequest(self.TEARDOWN)        
        self.master.destroy() # Close the gui window

        # OPTIONAL EXERCISE: Print summary statistics
        print('\n==== SUMMARY ====')
        if self.bandwidths:
            total_bytes = sum(b for b, t in self.bandwidths)
            total_time = sum(t for b, t in self.bandwidths)
            avg_bandwidth = total_bytes / total_time
            print(f'Average bandwidth: {avg_bandwidth / 1024:.2f} KiB/s')

        if self.frameNbr > 0:
            loss_rate = 100 * (1 - self.packetsReceived / self.frameNbr)
            print(f'Packet loss rate: {loss_rate:.2f}%\n')
        
        os.remove(CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT) # Delete the cache image from video

    def pauseMovie(self):
        """Pause button handler."""
        if self.state == self.PLAYING:
            self.sendRtspRequest(self.PAUSE)
    
    def playMovie(self):
        """Play button handler."""
        if self.state == self.READY:
            # Create a new thread to listen for RTP packets
            threading.Thread(target=self.listenRtp).start()
            self.playEvent = threading.Event()
            self.playEvent.clear()
            self.sendRtspRequest(self.PLAY)
    
    def getDescription(self):
        """OPTIONAL EXERCISE: Describe button handler."""
        self.sendRtspRequest(self.DESCRIBE)
    
    def listenRtp(self):        
        """Listen for RTP packets."""
        while True:
            try:
                data = self.rtpSocket.recv(20480)
                if data:
                    rtpPacket = RtpPacket()
                    rtpPacket.decode(data)
                    
                    currFrameNbr = rtpPacket.seqNum()
                    print("Current Seq Num: " + str(currFrameNbr))
                                        
                    if currFrameNbr > self.frameNbr: # Discard the late packet
                        # OPTIONAL EXERCISE: maintain stats on packet loss rate and bandwidth
                        self.packetsReceived += 1
                        self.receivedSize += len(rtpPacket.getPacket())

                        self.endTime = int(time())
                        self.frameNbr = currFrameNbr
                        self.updateMovie(self.writeFrame(rtpPacket.getPayload()))
            except:
                # Stop listening upon requesting PAUSE or TEARDOWN
                if self.playEvent.isSet(): 
                    break
                
                # Upon receiving ACK for TEARDOWN request,
                # close the RTP socket
                if self.teardownAcked == 1:
                    self.rtpSocket.shutdown(socket.SHUT_RDWR)
                    self.rtpSocket.close()
                    break
                    
    def writeFrame(self, data):
        """Write the received frame to a temp image file. Return the image file."""
        cachename = CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT
        file = open(cachename, "wb")
        file.write(data)
        file.close()
        
        return cachename
    
    def updateMovie(self, imageFile):
        """Update the image file as video frame in the GUI."""
        photo = ImageTk.PhotoImage(Image.open(imageFile))
        self.label.configure(image = photo, height=288) 
        self.label.image = photo
        
    def connectToServer(self):
        """Connect to the Server. Start a new RTSP/TCP session."""
        self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.rtspSocket.connect((self.serverAddr, self.serverPort))
        except:
            tkMessageBox.showwarning('Connection Failed', 'Connection to \'%s\' failed.' %self.serverAddr)
    
    def sendRtspRequest(self, requestCode):
        """Send RTSP request to the server."""
        # OPTIONAL EXERCISE: Describe request
        if requestCode == self.DESCRIBE:
            # Update RTSP sequence number.
            self.rtspSeq += 1

            # Write the RTSP request to be sent.
            request = f'DESCRIBE {self.fileName} RTSP/1.0\nCSeq: {self.rtspSeq}\nSession: {self.sessionId}'

            # Keep track of the sent request.
            self.requestSent = self.DESCRIBE
        # Setup request
        elif requestCode == self.SETUP and self.state == self.INIT:
            threading.Thread(target=self.recvRtspReply).start()
            # Update RTSP sequence number.
            self.rtspSeq += 1
            
            # Write the RTSP request to be sent.
            request = f'SETUP {self.fileName} RTSP/1.0\nCSeq: {self.rtspSeq}\nTransport: RTP/UDP; client_port= {self.rtpPort}'
            
            # Keep track of the sent request.
            self.requestSent = self.SETUP
        # Play request
        elif requestCode == self.PLAY and self.state == self.READY:
            # Update RTSP sequence number.
            self.rtspSeq += 1
            
            # Write the RTSP request to be sent.
            request = f'PLAY {self.fileName} RTSP/1.0\nCSeq: {self.rtspSeq}\nSession: {self.sessionId}'
            
            # Keep track of the sent request.
            self.requestSent = self.PLAY
        # Pause request
        elif requestCode == self.PAUSE and self.state == self.PLAYING:
            # Update RTSP sequence number.
            self.rtspSeq += 1
            
            # Write the RTSP request to be sent.
            request = f'PAUSE {self.fileName} RTSP/1.0\nCSeq: {self.rtspSeq}\nSession: {self.sessionId}'
            
            # Keep track of the sent request.
            self.requestSent = self.PAUSE
        # Teardown request
        elif requestCode == self.TEARDOWN and not self.state == self.INIT:
            # Update RTSP sequence number.
            self.rtspSeq += 1
            
            # Write the RTSP request to be sent.
            request = f'TEARDOWN {self.fileName} RTSP/1.0\nCSeq: {self.rtspSeq}\nSession: {self.sessionId}'
            
            # Keep track of the sent request.
            self.requestSent = self.TEARDOWN
        else:
            return
        
        # Send the RTSP request using rtspSocket.
        self.rtspSocket.send(request.encode())        
        print('\nData sent:\n' + request)
    
    def startProfilingBandwidth(self):
        """OPTIONAL EXERCISE: For profiling bandwidth statistics."""
        self.startTime = int(time())
        self.endTime = int(time())
    
    def stopProfilingBandwidth(self):
        """OPTIONAL EXERCISE: For profiling bandwidth statistics."""
        if self.startTime is not None:
            b = self.receivedSize
            t = self.endTime - self.startTime
            self.bandwidths.append((b, t))
            
        self.startTime = None
        self.endTime = None
        self.receivedSize = 0
    
    def recvRtspReply(self):
        """Receive RTSP reply from the server."""
        while True:
            reply = self.rtspSocket.recv(1024)
            
            if reply: 
                self.parseRtspReply(reply.decode("utf-8"))
            
            # Close the RTSP socket upon requesting Teardown
            if self.requestSent == self.TEARDOWN:
                self.rtspSocket.shutdown(socket.SHUT_RDWR)
                self.rtspSocket.close()
                break
    
    def parseRtspReply(self, data):
        """Parse the RTSP reply from the server."""
        lines = data.split('\n')
        seqNum = int(lines[1].split(' ')[1])
        
        # Process only if the server reply's sequence number is the same as the request's
        if seqNum == self.rtspSeq:
            session = int(lines[2].split(' ')[1])
            # New RTSP session ID
            if self.sessionId == 0:
                self.sessionId = session
            
            # Process only if the session ID is the same
            if self.sessionId == session:
                if int(lines[0].split(' ')[1]) == 200:
                    # OPTIONAL EXERCISE: Process describe reply
                    if self.requestSent == self.DESCRIBE:
                        # Pause is for mitigating Tkinter concurrency issues
                        sleep(0.5)
                        tkMessageBox.showinfo('Session Description', '\n'.join(lines[3:]))
                    elif self.requestSent == self.SETUP:
                        # Update RTSP state.
                        if self.state == self.INIT:
                            self.state = self.READY
                        
                        # Open RTP port.
                        self.openRtpPort() 
                    elif self.requestSent == self.PLAY:
                        if self.state == self.READY:
                            self.startProfilingBandwidth()
                            self.state = self.PLAYING
                    elif self.requestSent == self.PAUSE:
                        if self.state == self.PLAYING:
                            self.stopProfilingBandwidth()
                            self.state = self.READY
                        
                        # The play thread exits. A new thread is created on resume.
                        self.playEvent.set()
                    elif self.requestSent == self.TEARDOWN:
                        if self.state == self.PLAYING or self.state == self.READY:
                            self.stopProfilingBandwidth()
                            self.state = self.INIT

                        # Flag the teardownAcked to close the socket.
                        self.teardownAcked = 1 
    
    def openRtpPort(self):
        """Open RTP socket binded to a specified port."""
        # Create a new datagram socket to receive RTP packets from the server
        self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rtpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Set the timeout value of the socket to 0.5sec
        self.rtpSocket.settimeout(0.5)
        
        try:
            # Bind the socket to the address using the RTP port given by the client user
            self.rtpSocket.bind((self.serverAddr, self.rtpPort))
        except:
            tkMessageBox.showwarning('Unable to Bind', 'Unable to bind PORT=%d' %self.rtpPort)

    def handler(self):
        """Handler on explicitly closing the GUI window."""
        self.pauseMovie()
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            self.exitClient()
        else: # When the user presses cancel, resume playing.
            self.playMovie()
