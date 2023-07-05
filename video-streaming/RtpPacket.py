from time import time

class RtpPacket:
    HEADER_SIZE = 12
    
    def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
        """Encode the RTP packet with header fields and payload."""
        timestamp = int(time())
        header = bytearray(RtpPacket.HEADER_SIZE)
        
        # Fill the header bytearray with RTP header fields
        header[0] = ((version & 0x3) << 6) | ((padding & 0x1) << 5) | ((extension & 0x1) << 4) | (cc & 0xF)
        header[1] = ((marker & 0x1) << 7) | (pt & 0x7F)
        header[2] = (seqnum >> 8) & 0xFF
        header[3] = seqnum & 0xFF

        header[4] = (timestamp >> 24) & 0xFF
        header[5] = (timestamp >> 16) & 0xFF
        header[6] = (timestamp >> 8) & 0xFF
        header[7] = timestamp & 0xFF

        header[8] = (ssrc >> 24) & 0xFF
        header[9] = (ssrc >> 16) & 0xFF
        header[10] = (ssrc >> 8) & 0xFF
        header[11] = ssrc & 0xFF

        self.header = header

        # Get the payload from the argument
        self.payload = payload
        
    def decode(self, byteStream):
        """Decode the RTP packet."""
        self.header = bytearray(byteStream[:RtpPacket.HEADER_SIZE])
        self.payload = byteStream[RtpPacket.HEADER_SIZE:]
    
    def version(self):
        """Return RTP version."""
        return int(self.header[0] >> 6)
    
    def seqNum(self):
        """Return sequence (frame) number."""
        seqNum = self.header[2] << 8 | self.header[3]
        return int(seqNum)
    
    def timestamp(self):
        """Return timestamp."""
        timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
        return int(timestamp)
    
    def payloadType(self):
        """Return payload type."""
        pt = self.header[1] & 127
        return int(pt)
    
    def getPayload(self):
        """Return payload."""
        return self.payload
        
    def getPacket(self):
        """Return RTP packet."""
        return self.header + self.payload