import threading #lets me do multiple things at once, here it will check faces without freezing the camera video feed

import cv2 #the OpenCV library works with images and video
from deepface import DeepFace #a library for facial recognition

import os

cap = cv2.VideoCapture(0) #opens up the first webcame available

#sets the width and height of the video to 640x480 pixels
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0 #helps us check faces only once every 30 frames (else it would check every single frame, which woulud be slow)

face_match = False #keeps track if a face matches any of the reference images

reference_folder = "references"
reference_imgs = []

for filename in os.listdir(reference_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(reference_folder, filename)
        img = cv2.imread(img_path) #reads the image into a NumPy array
        if img is not None:
            reference_imgs.append(img)
print(f"Loaded {len(reference_imgs)} reference images.")

def check_face(frame): #checks if the webcam frame matches any reference image
    global face_match #we want to modify face_match with is a variable outside the function
    try:
        match_found = False #assume no match until proven otherwise
        for ref in reference_imgs: #loops through every reference image
            result = DeepFace.verify(frame, ref.copy()) #compares the current webcam frame to a reference image
            if result['verified']: #if face match
                match_found = True
                break
        face_match = match_found #updates the global variable

    except ValueError as e: #if DeepFace can't read a face, it just sets the match to False
        print("Error verifying:", e)
        face_match = False

while True: #this runs the webcam
    ret, frame = cap.read() #grabs one frame from the webcam, ret is True if it worked

    if ret:
        if counter % 30 == 0: #checks face every 30 frames
            try:
                threading.Thread(target=check_face, args =(frame.copy(),)).start() #runs check_face in the background so the video doesn't freeze, frame.copy() makes a copy of the frame for processing
                #Python always expects args to be a tuple, so that is why it is (frame.copy(),) with an empty space
            except ValueError:
                pass
        counter += 1 #adds 1 to the counter for each frame

        #draws video text
        if face_match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), thickness = 3)
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), thickness = 3)
        cv2.imshow("video", frame) #opens a window called 'video' showing the webcam feed with the text
    key = cv2.waitKey(1) #waits 1 millisecond for a key press
    if key == ord("q"): #if you press q, the loop breaks and the program ends
        break

cv2.destroyAllWindows() #closes the webcam program
