from threading import Thread
import cv2

class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)

        
        self.prop_framecount = self.stream.get (cv2.CAP_PROP_FRAME_COUNT)
        self.loopback = self.prop_framecount > 0

        (self.grabbed, self.frame) = self.stream.read()
 
		# initialize the variable used to indicate if the thread should
		# be stopped
        self.stopped = False
    
    def start(self):
		# start the thread to read frames from the video stream
        self.mainThread = Thread(target=self.update, args=())
        self.mainThread.start()
        return self

    def update(self):
		# keep looping infinitely until the thread is stopped
        while True:
			# if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            
            if (self.loopback):
                if (self.stream.get (cv2.CAP_PROP_POS_FRAMES) >= self.prop_framecount):
                    self.stream.set (cv2.CAP_PROP_POS_FRAMES, 0)

			# otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
		# return the frame most recently read
        return self.grabbed, self.frame

    def stop(self):
		# indicate that the thread should be stopped
        self.stopped = True

    def isOpened(self):
        return self.stream.isOpened()
    
    def release(self):
        self.stop()

        # Kill the thread
        self.mainThread.join()
        self.stream.release()
    
    def get(self, cap_prop):
        return self.stream.get(cap_prop)
    
    def set(self, cap_prop, value):
        return self.stream.set(cap_prop, value)
