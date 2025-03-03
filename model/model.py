import base64
import json
import os

import requests
import torch
import cv2
import numpy as np

from ultralytics import YOLO


class FishDetectionModel():
    '''
    Model for detecting fish on video.

    Methods:
      predict(input_data)
        Returns the model's predictions.
      
      rtsp_predict()
        Returns the current frame predictions of the stream and the population size.

      set_rtsp_stream(new_rtsp_url)
        Change of rtsp stream.

      add_bounding_box(image, predictions)
        Adding Bounding Boxes to an Image.
    '''

    def __init__(self, model_path: str,
                 rtsp_url: str | None = None):
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
         
        self.model = YOLO(model_path)
        self.rtsp_url = rtsp_url
        self.cap = cv2.VideoCapture(rtsp_url)

    def predict(self, input_data: np.ndarray) -> list:
        '''
        Returns predictions in YOLO format.
      
        Args:
          input_data (np.ndarray): frame for which predictions need to be obtained.
        '''

        return self.model(input_data, verbose=False) 

    def rtsp_predict(self, max_retries=3) -> tuple[str, int]:
        '''Returns the current frame predictions of the stream and the population size.'''

        retries = 0
        while retries < max_retries:
            if not self.cap.isOpened():
                print("Failed to read RTSP stream. Retrying...")
                self.cap = cv2.VideoCapture(self.rtsp_url)
                retries += 1
                continue

            ret, frame = self.cap.read()

            if ret:
                predict = self.predict(frame)[0].boxes.xywh
                frame_with_boxes = self.add_bounding_box(frame, predict)

                _, buffer = cv2.imencode('.jpg', frame_with_boxes)
                jpeg_bytes = buffer.tobytes()
                jpeg_base64 = base64.b64encode(jpeg_bytes).decode('utf-8')

                return jpeg_base64, len(predict)

            print("Failed to get frame. Retrying...")
            retries += 1

        print("Max retries reached. Terminating.")
        return None

    def set_rtsp_stream(self, new_rtsp_url: str) -> None:
        '''Change of rtsp stream'''

        self.rtsp_url = new_rtsp_url
        self.cap = cv2.VideoCapture(new_rtsp_url)
        return None

    @classmethod
    def add_bounding_box(cls, image: np.ndarray, 
                         predictions: torch.Tensor | list):
        '''
        Adding Bounding Boxes to an Image.
      
        Args:
          image (np.ndarray): frame or picture.

        predictions (torch.Tensor | list): corresponding pictures of predictions in XYWH format.
        '''

        coordinates = []
        for bbox in predictions:
            x_center, y_center = bbox[0], bbox[1]
            width, height = bbox[2], bbox[3]

            xmin = int((x_center - width / 2))
            ymin = int((y_center - height / 2))
            xmax = int((x_center + width / 2))
            ymax = int((y_center + height / 2))
            coordinates.append(
                ((xmin, ymin), 
                (xmax, ymax))
            ) 

        for rect in coordinates:
            cv2.rectangle(image, rect[0], rect[1], (0, 255, 0), 2)

        return image


if __name__ == "__main__":
    # url = "http://127.0.0.1:8000/api/post_data/"
    #
    # ans = requests.post(url, json.dumps({
    #     "state1": "qwe",
    #     "state2": False,
    # }))
    #
    # print(ans.text)

    url = "http://127.0.0.1:8000/api/post_data/"

    ans = requests.post(url, json.dumps({
        "state1": "qwe",
        "state2": False,
    }))
    rtsp_url = './utils/test_data/output1.avi'
    # rtsp_url = "rtsp://pool250:_250_pool@45.152.168.61:52037/Streaming/Channels/101?tcp"
    model = FishDetectionModel("weights/best.pt", rtsp_url)
    while True:
        result = model.rtsp_predict()

        if result is not None:
            frame_with_boxes, population_size = result

            ans = requests.post(url, json.dumps({
                "frame_with_boxes": frame_with_boxes,
                "population_size": population_size,
            }))

            print(ans.text)
