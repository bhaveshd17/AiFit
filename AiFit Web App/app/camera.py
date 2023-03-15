import numpy as np
import cv2
from app.model_detection import detectPoseWithoutNormalize
from app.model_detection import predict_real_time_detection

class VideoCamera(object):
    def __init__(self, path):
        self.video = cv2.VideoCapture(path)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        if success:
            image_pose, marked_pose = detectPoseWithoutNormalize(image, 'uploaded')
            cv2.waitKey(1)
            ret, jpeg = cv2.imencode('.jpg', marked_pose)
            return jpeg.tobytes()
        else:
            return False

class VideoCameraRealTime(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self, key, frames_queue, predicted_class_name, confidence, check_class):
        success, image = self.video.read()
        if success:
            res = predict_real_time_detection(key, image, predicted_class_name, confidence, frames_queue, check_class)
            marked_frame = res['frame']
            
            
            ret, jpeg = cv2.imencode('.jpg', marked_frame)
            return jpeg.tobytes(), res['frames_queue'], res['class'], res['confidence']
        else:
            return False, False, False, False


from .model_detection import repcounterMedia
class VideoCameraRepCounter(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self, counter, stage):
        success, image = self.video.read()
        if success:
            counter, stage, image = repcounterMedia(image, counter, stage)
            cv2.waitKey(1)
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes(), counter, stage
        else:
            return False, False, False


