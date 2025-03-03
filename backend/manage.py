
import os
import sys
import json
import time
import requests
import threading

sys.path.append('..')
from model.model import FishDetectionModel
from scipy.stats import mode


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wsp.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def start_model():
    # for production
    # rtsp_url = "rtsp://pool250:_250_pool@45.152.168.61:52037"

    # To test the model's operation, we use a prepared video
    rtsp_url = '../model/utils/test_data/output1.avi'
    url = "http://127.0.0.1:8000/api/post_data/"

    model = FishDetectionModel("../model/weights/best.pt", rtsp_url)
    population_10 = []
    while True:
        result = model.rtsp_predict()
        if result is not None:
            frame_with_boxes, population_size = result
            population_10.append(population_size)

            if len(population_10) > 10:
                population_10.pop(0)

            requests.post(url, json.dumps({
                "frame_with_boxes": frame_with_boxes,
                "population_size": str(mode(population_10).mode),
            }))


if __name__ == '__main__':
    threading.Thread(target=start_model, daemon=True).start()
    main()



