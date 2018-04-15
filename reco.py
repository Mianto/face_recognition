import cv2
import face_recognition
import glob

'''
    This is a demo of running face recognition on live video using webcam.
    It includes some basic performance tweaks to make things run a lot faster:
    1. Process each video frame at 1/2 resolution
    2. Only detect faces in every other frame of video.
'''


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


def load_images(path, known_face_encodings, known_face_names):
    '''
    Function to get face encoding and name of the person
    from the image file name

    Parameters
    ----------
    path: String
        containing the path of Image Folder
    known_face_encodings: List
        Stores face Encoding
    known_face_names: List
        Stores name of the persons

    Returns
    -------
    known_face_encodings: List
    known_face_names: List
        updated list of the data
    '''
    files = glob.glob(path)
    for imag in files:
        name = imag[65:-4]
        load_image = face_recognition.load_image_file(imag)
        known_face_encodings.append(
            face_recognition.face_encodings(load_image)[0])
        known_face_names.append(name)
    return known_face_encodings, known_face_names


def recognise(known_face_encodings, known_face_names):
    '''
    Function to open webcam and recognise faces

    Parameters
    ----------
    known_face_encodings: List
        Stores face Encoding
    known_face_names: List
        Stores name of the persons

    Returns
    -------
    None

    '''
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    unique = []
    i = 0

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size
        # for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses)
        # to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = list(face_recognition.face_distance(
                    known_face_encodings, face_encoding))
                name = "Unknown"

                # If a match was found in known_face_encodings,
                # just use the first one.
                if len(matches) != 0:
                    if min(matches) <= 0.6:
                        match_index = matches.index(min(matches))
                        name = known_face_names[match_index]

                if name == 'Unknown':
                    i += 1
                    known_face_encodings.append(face_encoding)
                    name = 'Unknown' + str(i)
                    known_face_names.append(name)

                face_names.append(name)
        process_this_frame = not process_this_frame

        for name in face_names:
            if name not in unique:
                unique.append(name)
        count = len(unique)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame
            # we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top),
                          (right, bottom), (255, 0, 255), 1)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 30),
                          (right, bottom), (255, 0, 255), -1)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 0.75, (0, 255, 0), 1)

            # to show the count of people
            cv2.rectangle(frame, (0, 0), (30, 30), (255, 0, 255), -1)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, str(count), (6, 24), font, 0.75, (0, 255, 0), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print known_face_names
            print unique
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    known_face_encodings = []
    known_face_names = []
    path = '//home//prashant//Documents//Face_reco//face_recognition//Images//*.jpg'
    known_face_encodings, known_face_names = load_images(
        path, known_face_encodings, known_face_names)
    recognise(known_face_encodings, known_face_names)
