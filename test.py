import face_recognition
import cv2
import numpy as np
import serial
import time

ser = serial.Serial('/dev/ttyACM0',9600)
time.sleep(2)
start_time = time.monotonic()
t1=0
t2=0
check=False

# object video par defaut
video_capture = cv2.VideoCapture(0,cv2.CAP_V4L2)
if not video_capture.isOpened():
    raise IOError("Cannot open webcam")
# ADMIN DEFINITION
amaury_image = face_recognition.load_image_file("moi.jpg")
amaury_face_encoding = face_recognition.face_encodings(amaury_image)[0]

# Load a second sample picture and learn how to recognize it.
random_image = face_recognition.load_image_file("random.jpg")
random_face_encoding = face_recognition.face_encodings(random_image)[0]

# liste admin et noms
admin_face_encodings = [
    amaury_face_encoding,
    random_face_encoding
]
admin_names = [
    "Admin_1",
    "Admin_2"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
name="Unknown"
while True:
    # capture frame par frame
    ret, frame = video_capture.read()

    # resize pour rapidite, cf doc
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses) cf doc on inverse l'array
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        if not face_encodings:
            #print("heu")
            if(time.monotonic()-t2>1 and time.monotonic()-t1>1):
                ser.write('N'.encode('utf_8'))
                t2=time.monotonic()
            
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(admin_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(admin_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                if(time.monotonic()-t1>1 and time.monotonic()-t2>1):
                    ser.write('A'.encode('utf_8'))
                    t1=time.monotonic()
                    ms = ser.readline()
                name = admin_names[best_match_index]
            else:
                ser.write('N'.encode('utf_8'))
                
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        if(name=="Unknown"):
            rectangle_color=(0,0,255)
        else:
            rectangle_color=(0,255,0)
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), rectangle_color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom),rectangle_color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        check = True
    flipped_frame=cv2.flip(frame,1)
    width=video_capture.get(3)
    if(check):
        cv2.putText(flipped_frame, name, (int(width-right+6), bottom - 6), font, 1.0, (255, 255, 255), 1)
    check = False
    # Display the resulting image
    cv2.imshow('Video', flipped_frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Release handle to the webcam
ser.write('N'.encode('utf_8'))
ms = ser.readline()
ser.close()
video_capture.release()
cv2.destroyAllWindows()
