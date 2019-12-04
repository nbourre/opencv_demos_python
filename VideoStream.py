from threading import Thread
import cv2
import time

class VideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)

        
        self.prop_framecount = self.stream.get (cv2.CAP_PROP_FRAME_COUNT)
        self.loopback = self.prop_framecount > 0
        self.loop_counter = 0

        (self.grabbed, self.frame) = self.stream.read()
 
		# initialize the variable used to indicate if the thread should
		# be stopped
        self.stopped = False
        self.delay = -1
        self.pause = False
    
    def start(self):
		# start the thread to read frames from the video stream
        self.mainThread = Thread(target=self.update, args=())
        self.mainThread.start()
        return self

    def update(self):
        time_acc = 0
        grab_it = True
        previous_time = 0

		# keep looping infinitely until the thread is stopped
        while True:
			# if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            
            
            if (self.loopback):
                if (self.stream.get (cv2.CAP_PROP_POS_FRAMES) >= self.prop_framecount):
                    self.stream.set (cv2.CAP_PROP_POS_FRAMES, 0)
                    self.loop_counter = self.loop_counter + 1
            
            if (self.delay > 0):

                ## Better time management that waitKey()
                current_time = int (round (time.time() * 1000))
                delta_time = current_time - previous_time
                previous_time = current_time

                time_acc += delta_time
                
                grab_it = False

                if time_acc >= self.delay:
                    grab_it = True
                    time_acc = 0
            else:
                grab_it = True

            if not self.pause and grab_it:
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
