import face_recognition
from picamera import PiCamera
import picamera
from time import sleep
import cv2
import numpy as np

known_image = face_recognition.load_image_file("/home/pi/Desktop/cac_facial_recognition/user_cac_image.jpeg")
user_encoding = [face_recognition.face_encodings(known_image)[0]]
camera = picamera.PiCamera()
camera.resolution = (1024, 720)
output = np.empty((720, 1024, 3), dtype=np.uint8)

if __name__ == "__main__":

    
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        print("Capturing image.")
        camera.capture(output, format="rgb")
        frame = output
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(user_encoding, face_encoding)
                name = "Unknown"
                if True in matches:
                    name = "Match!"
                    #first_match_index = matches.index(True)
                    #name = known_face_names[first_match_index]
                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

