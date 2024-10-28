import cv2

# 동영상 파일 열기
cap = cv2.VideoCapture("videoplayback.mp4")
# cap = cv2.VideoCapture(0) 웹캠열기
edge_bool = False
cartoon_bool = False

def cartoon_effect(frame):
    # 색상 단순화
    img_color = cv2.pyrDown(frame)
    img_color = cv2.pyrDown(img_color)
    img_color = cv2.pyrUp(img_color)
    img_color = cv2.pyrUp(img_color)

    # 경계선 강조
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, 9, 9)

    # 카툰 효과 이미지 생성
    cartoon = cv2.bitwise_and(img_color, img_color, mask=edges)
    return cartoon

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 그레이스케일 변환
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Canny edge detection 적용
    edges = cv2.Canny(image=gray_img, threshold1=100, threshold2=200)

    if edge_bool:
        image = edges
    elif cartoon_bool:
        image = cartoon_effect(frame)
    else:
        image = frame
        
    cv2.imshow("Video", image)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("b"):
        edge_bool = not edge_bool
    elif key == ord("c"):
        cartoon_bool = not cartoon_bool

# 외부 자원은 반환
cap.release()
cv2.destroyAllWindows()