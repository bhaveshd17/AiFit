import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
import tensorflow as tf
import random
from aifit.settings import BASE_DIR
import os
from .apps import AppConfig

seed_constant = 23
np.random.seed(seed_constant)
random.seed(seed_constant)
tf.random.set_seed(seed_constant)

# Initialize mediapipe pose class.
mp_pose = mp.solutions.pose
pose_image = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.7,
                          min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

CLASSES_LIST =  ['Bicep Curl', 'Overhead Press', 'Shoulder Raise', 'Squats']

def detectPose(image_pose, pose, draw=False, display=False):
    try:
        image_in_RGB = cv2.cvtColor(image_pose, cv2.COLOR_BGR2RGB)
        resultant = pose.process(image_in_RGB)
        marked_img = np.zeros(image_pose.shape)
        if resultant.pose_landmarks == None:
            return image_pose, marked_img
        if resultant.pose_landmarks and draw:    
            mp_drawing.draw_landmarks(image=marked_img, landmark_list=resultant.pose_landmarks,
                                    connections=mp_pose.POSE_CONNECTIONS,
                                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255),
                                                                                thickness=6, circle_radius=3),
                                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(49,125,237),
                                                                                thickness=3, circle_radius=2))


        if display:
                plt.figure(figsize=[5,5])
                plt.subplot(121);plt.imshow(image_pose[:,:,::-1]);plt.title("Input Image");plt.axis('off');
                plt.subplot(122);plt.imshow(marked_img[:,:,::-1]);plt.title("Pose detected Image");plt.axis('off');

        else:
            return image_pose, marked_img
    except:
        return image_pose, image_pose


def detectPoseWithoutNormalize(image_pose, pose=pose_image, draw=True, display=False):
    # try:
    image_in_RGB = cv2.cvtColor(image_pose, cv2.COLOR_BGR2RGB)
    resultant = pose.process(image_in_RGB)
    marked_img = image_pose
    if resultant.pose_landmarks and draw:    
        mp_drawing.draw_landmarks(image=marked_img, landmark_list=resultant.pose_landmarks,
                                connections=mp_pose.POSE_CONNECTIONS,
                                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255),
                                                                            thickness=6, circle_radius=3),
                                connection_drawing_spec=mp_drawing.DrawingSpec(color=(49,125,237),
                                                                            thickness=3, circle_radius=2))

    if display:
            plt.figure(figsize=[5,5])
            plt.subplot(121);plt.imshow(image_pose[:,:,::-1]);plt.title("Input Image");plt.axis('off');
            plt.subplot(122);plt.imshow(marked_img[:,:,::-1]);plt.title("Pose detected Image");plt.axis('off');

    else:
        return image_pose, marked_img
    # except:
    #     return image_pose, image_pose



def predict_single_action(video_file_path, SEQUENCE_LENGTH):
    aifit_lrcn_model = AppConfig.aifit_lrcn_model
    IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64
    print(video_file_path)
    # video_file_path = "E:/Final Year/Major/AiFit/AiFit Web App/static/images/recorded_videos/bhavesh_dhake.mp4"
    video_reader = cv2.VideoCapture(video_file_path)
    original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames_list = []
    predicted_class_name = ''
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
    skip_frames_window = max(int(video_frames_count/SEQUENCE_LENGTH),1)
    print(video_frames_count)
    print(skip_frames_window)

    for frame_counter in range(SEQUENCE_LENGTH):
        video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)
        success, frame = video_reader.read() 
        if not success:
            break
        image_frame, marked_frame = detectPose(frame, pose_image, draw=True, display=False)
        resized_frame = cv2.resize(marked_frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        
        frames_list.append(resized_frame)

    predicted_labels_probabilities = aifit_lrcn_model.predict(np.expand_dims(frames_list, axis = 0))[0]
    predicted_label = np.argmax(predicted_labels_probabilities)
    predicted_class_name = CLASSES_LIST[predicted_label]
    confidence = round(predicted_labels_probabilities[predicted_label]*100, 2)
    print(predicted_labels_probabilities)
    print(f'Action Predicted: {predicted_class_name}\nConfidence: {confidence}')
        
    # Release the VideoCapture object. 
    video_reader.release()
    return {
        'class':predicted_class_name,
        'confidence':confidence, 
    }
    

def predict_real_time_detection(frame, predicted_class_name, confidence, frames_queue, check_class):
    aifit_lrcn_model = AppConfig.aifit_lrcn_model
    SEQUENCE_LENGTH = 25
    IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64
        
    # Resize the Frame to fixed Dimensions.
    image_frame, marked_frame = detectPose(frame, pose_image, draw=True, display=False)
    image_frame, clear_marked_frame = detectPoseWithoutNormalize(frame, pose_image, draw=True, display=False)
    resized_frame = cv2.resize(marked_frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
    print(np.shape(frames_queue))
    frames_queue.append(resized_frame)
    if len(frames_queue) == SEQUENCE_LENGTH:
        predicted_labels_probabilities = aifit_lrcn_model.predict(np.expand_dims(frames_queue, axis = 0))[0]
        predicted_label = np.argmax(predicted_labels_probabilities)
        predicted_class_name = CLASSES_LIST[predicted_label]
        confidence = round(predicted_labels_probabilities[predicted_label]*100, 2)
        if check_class.upper() != predicted_class_name.upper():
            predicted_class_name = 'Inaccurate Workout'
            confidence = str(random.randint(1, 10)*0.01)
        
    clear_marked_frame = cv2.flip(clear_marked_frame, 1)
    cv2.putText(clear_marked_frame, f"{predicted_class_name} - {confidence}%"
                , (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    return {
        'class':predicted_class_name,
        'confidence': confidence,
        'frames_queue':frames_queue,
        'frame':clear_marked_frame
    }


def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return round(angle,1)

def repcounterMedia(frame, counter, stage):
        # Curl counter variables

    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make detection
    results = pose.process(image)

    # Recolor back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Extract landmarks
    try:
        landmarks = results.pose_landmarks.landmark
        
        # Get coordinates
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        
        # Calculate angle
        angle = calculate_angle(shoulder, elbow, wrist)
        # Visualize angle
        cv2.putText(image, str(angle), 
                    tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )
        
        # Curl counter logic
        if angle > 160:
            stage = "down"
        if angle < 30 and stage =='down':
            stage="up"
            counter += 1
        
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        # Rep data
        cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 ) 
        return counter, stage, image
            
                
    except:
        return counter, stage, image
    