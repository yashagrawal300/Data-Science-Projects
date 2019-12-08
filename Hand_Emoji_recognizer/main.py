import tensorflow.keras
import numpy as np
import cv2

np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model("keras_model.h5")


# classes = ["Thumbs_up", "Stop", "Ok", "Fist", "Two_fingers", "Vulcan_salute",
#           "Yo"]

s = ["1.png", "2.png", "3(1).png", "4.jfif", "5.png", "6.jfif", "7.png"]

img = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

while True:
    ret, frame = img.read()

    frame = cv2.rectangle(frame, (90, 90), (324, 324), (0, 0, 255), 3)

    frame2 = frame[90:324, 90:324]
    image = cv2.resize(frame2, (224, 224))

    image_array = np.asarray(image)

    normalized = (image_array.astype(np.float32) / 127.0) - 1

    data[0] = normalized

    pre = model.predict(data)

    result = cv2.imread(s[np.argmax(pre[0])])

    cv2.imshow("img", frame)
    cv2.imshow("result", result)
    if cv2.waitKey(1) & 0xff == ord('q'):
        cv2.imwrite("frame.jpg", frame)
        break
