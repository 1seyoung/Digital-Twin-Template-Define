import cv2
import numpy as np
import datetime
# Haar Cascades를 사용한 객체 검출 함수
def detect_object(img, cascade_file):
    # 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Cascade 분류기 로드
    cascade = cv2.CascadeClassifier(cascade_file)
    # 객체 검출
    objects = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # 검출된 객체 좌표 반환
    return objects


def cap():
    # 카메라로부터 이미지 한 장 가져오기
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera")
        return

    ret, frame = cap.read()

    # Haar Cascades 파일 경로 설정
    cascade_file = "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(cascade_file)
    # 객체 검출 수행
    objects = detect_object(frame, cascade_file)

    # 검출된 객체 표시
    for (x, y, w, h) in objects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 검출된 객체 수 출력
    time= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    num_objects = len(objects)
    text =f"{time}\nNumber of objects detected: {num_objects}"

    # 이미지 파일로 저장하기
    img_path = "captured_image.jpg"
    cv2.imwrite(img_path, frame)

    # 종료
    cap.release()
    cv2.destroyAllWindows()

    return text