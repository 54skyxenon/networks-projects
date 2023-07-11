# VideoStream.py

class VideoStream:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.file = open(filename, 'rb')
        except:
            raise IOError
        self.frameNum = 0

    def __len__(self):
        """OPTIONAL EXERCISE: Calculate number of frames in video stream."""
        videoLength = 0
        lengthStream = open(self.filename, 'rb')

        while data := lengthStream.read(5):
            framelength = int(data)
            data = lengthStream.read(framelength)
            videoLength += 1

        return videoLength
    
    def nextFrame(self):
        """Get next frame."""
        data = self.file.read(5) # Get the framelength from the first 5 bits
        if data: 
            framelength = int(data)
                            
            # Read the current frame
            data = self.file.read(framelength)
            self.frameNum += 1
        return data
        
    def frameNbr(self):
        """Get frame number."""
        return self.frameNum