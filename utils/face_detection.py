import cv2
import os 
def get_face_bbox(frame, mp_face_detection, thereisface):

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        frame.flags.writeable = False
        results = face_detection.process(frame)
        frame.flags.writeable = True

        h, w, _ = frame.shape
        if results.detections:
            
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                xmin = int(bbox.xmin * w * 0.9)
                ymin = int(bbox.ymin * h * 0.9)
                width = int(bbox.width * w * 1.1)
                height = int(bbox.height * h * 1.1)
                
                top_left = (xmin, ymin)
                bottom_right = (xmin + width, ymin + height)

                # 바운딩 박스 그리기
                cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)

    return frame, thereisface


import face_recognition


faceDB = './faceDB'
os.makedirs(faceDB, exist_ok=True)

def get_faces(faceDB_folder):
    known_face_encodings = []
    known_face_names = []
    images = os.listdir(faceDB_folder)
    for image in images:
        load_image = face_recognition.load_image_file(f"{faceDB_folder}/" + image)
        load_image_encoding = face_recognition.face_encodings(load_image)[0]
        known_face_encodings.append(load_image_encoding)
        known_face_names.append(image.split(".")[0])
        
    return known_face_encodings, known_face_names


known_face_encodings, known_face_names = get_faces(faceDB)

def get_face_bbox2(frame, mp_face_detection, thereisface):

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        frame.flags.writeable = False
        results = face_detection.process(frame)
        frame.flags.writeable = True

        h, w, _ = frame.shape
        if results.detections:
            
            face_locations = []
            
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                xmin = int(bbox.xmin * w * 0.9)
                ymin = int(bbox.ymin * h * 0.9)
                width = int(bbox.width * w * 1.1)
                height = int(bbox.height * h * 1.1)
                xmax = xmin + width
                ymax = ymin + height
                
                face_locations.append([ymin, xmax, ymax, xmin])

                
            
            face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            for idx, [ymin, xmax, ymax, xmin] in enumerate(face_locations):
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
                
                matches = face_recognition.compare_faces(known_face_encodings, face_encodings[idx], 0.4)
                name = "Unknown"
                
                # 인식할 사람에 속한다면 이름을 가져옵니다.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                cv2.putText(frame, name, (xmin + 10, ymax - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)    

    return frame, thereisface


def get_face_bbox3(frame, mp_face_detection, thereisface):

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        frame.flags.writeable = False
        results = face_detection.process(frame)
        frame.flags.writeable = True

        h, w, _ = frame.shape
        
        if results.detections:
            
            face_locations = []
            
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                xmin = int(bbox.xmin * w * 0.9)
                ymin = int(bbox.ymin * h * 0.9)
                width = int(bbox.width * w * 1.1)
                height = int(bbox.height * h * 1.1)
                xmax = xmin + width
                ymax = ymin + height
                
                if not thereisface:
                    face_encodings = face_recognition.face_encodings(frame, [[ymin, xmax, ymax, xmin]])

                    matches = face_recognition.compare_faces(known_face_encodings, face_encodings[0], 0.4)

                    # 인식할 사람에 속한다면 이름을 가져옵니다.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]
                        thereisface = name
                    
                    # else:
                    #     known_face_encodings, known_face_names = get_faces(faceDB)
                    #     name = "a{:08}".format(len(known_face_names))
                    
                    
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
                if thereisface:
                    cv2.putText(frame, thereisface, (xmin + 10, ymax - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)    

        else:
            thereisface = None
        
    return frame, thereisface