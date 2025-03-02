import base64
import os
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
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
         
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(rtsp_url)

    def predict(self, input_data: np.ndarray) -> list:
        '''
        Returns predictions in YOLO format.
      
        Args:
          input_data (np.ndarray): frame for which predictions need to be obtained.
        '''

        return self.model(input_data) 

    def rtsp_predict(self) -> tuple[str, int]:
        '''Returns the current frame predictions of the stream and the population size.'''

        if not self.cap.isOpened():
            print("Failed to read rtsp stream. Make sure you specified it correctly `rtshp_url`.")
            return None

        ret, frame = self.cap.read()

        if not ret:
            print("Failed to get frame. Terminating")
            return None
        
        predict = self.predict(frame)[0].boxes.xywh
        frame_with_boxes = self.add_bounding_box(frame, predict)

        _, buffer = cv2.imencode('.jpg', frame_with_boxes)
        jpeg_bytes = buffer.tobytes()
        jpeg_base64 = base64.b64encode(jpeg_bytes).decode('utf-8')

        return jpeg_base64, len(predict)

    def set_rtsp_stream(self, new_rtsp_url: str) -> None:
        '''Change of rtsp stream'''

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
    rtsp_url = "rtsp://pool250:_250_pool@45.152.168.61:52037"
    model = FishDetectionModel("best.pt", rtsp_url)
    result = model.rtsp_predict()

    if result is not None:
        frame_with_boxes, population_size = result

        if isinstance(frame_with_boxes, str):
            jpeg_bytes = base64.b64decode(frame_with_boxes)
            jpeg_array = np.frombuffer(jpeg_bytes, dtype=np.uint8)
            image = cv2.imdecode(jpeg_array, cv2.IMREAD_COLOR)
        else:
            image = frame_with_boxes

        cv2.imshow(image)
        print(f"Population size: {population_size}")

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    