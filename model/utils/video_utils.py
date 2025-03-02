import os
import json
import cv2 # type: ignore

from datetime import datetime


def get_name_frames(annotation_path: str) -> set[int]:
    '''
    Returns the frame numbers to extract from the video.
    
    Args:
        annotation_path (str): path to the file with annotations in COCO format.
      
    Returns:
        set[int]: integer value of all frames used in the annotation.
    '''

    frames = set()
    with open(annotation_path, 'r') as json_file:
        annotation = json.load(json_file)
  
    for img in annotation["images"]:
        img_name = img["file_name"]
        frame = img_name[img_name.index('_') + 1 : img_name.index('.')]
        frames.add(int(frame))

    return frames


def save_annotated_frames(video_path: str, 
                          annotation_path: str,
                          save_dir_path: str = "./",
                          file_type: str = "png",
                          discharge: int = 6) -> None:
    '''
    Saves the specified frames to a folder.
    
    Args:
        video_path (str):      path to video.
        annotation_path (str): path to the file with annotations in COCO format corresponding to the video index in the video_path.
        save_dir_path (str):        path to the directory where the videos will be saved.
        file_type (str):       the type in which the frames will be saved.
        discharge (int):       the number of digits that will represent the number (zeros are added to the beginning).
    
    Returns:
        None
    '''
    
    if not os.path.exists(save_dir_path):
        os.mkdir(save_dir_path)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Failed to read video. Make sure you specified it correctly `video_path`.")
        return None
    
    frames = get_name_frames(annotation_path)
    num_frame, ret = 1, False
    
    while cap.isOpened():
        ret, image = cap.read()
        
        if not ret: break
        elif num_frame in frames:
            cv2.imwrite(f'{save_dir_path}/frame_{num_frame:0{discharge}d}.{file_type}', image)
        
        num_frame += 1
  
    cap.release()
    cv2.destroyAllWindows()
    
    return None


def get_annotation_frame(frame_path: str,
                         annotation_path: str) -> list[tuple[tuple[int]]]:
    '''
    Returns a list of bonding boxes for the given frame.
    
    Args:
        image_path (str):      path to the frame that needs to be drawn.
        annotation_path (str): path to the annotation of the specified frame.
    
    Returns:
        list[tuple[tuple[int]]]: list(tuple(tuple(x_min, y_min), tuple(x_max, y_max)), ...).
    '''
    
    with open(annotation_path, 'r') as json_file:
        annotation = json.load(json_file)
        
    frame_name = frame_path.split("/")[-1].split(".")[0]
        
    for image_info in annotation["images"]: 
        if frame_name in image_info["file_name"]:
            image_id = image_info["id"]
            break
    else:
        return []

    coordinates = []
    for annotate in annotation["annotations"]:
        if annotate["image_id"] == image_id:
            bbox = annotate["bbox"]
            coordinates.append(
                ((int(bbox[0]), int(bbox[1])), 
                (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])))  
            ) 
            
    return coordinates


def draw_annotation_frame(frame_path: str, 
                          annotation_path: str) -> None:
    '''
    Renders a frame with its annotations.
    
    Args:
        image_path (str):      path to the frame that needs to be drawn.
        annotation_path (str): path to the annotation of the specified frame.
    
    Returns:
        None
    '''

    image = cv2.imread(frame_path)
    coordinates = get_annotation_frame(frame_path, annotation_path)

    for rect in coordinates:
        cv2.rectangle(image, rect[0], rect[1], (0, 255, 0), 2)

    cv2.imshow("Frame", image) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return None


def write_rtsp_stream(rtsp_url: str,
                      output_path: str,
                      fourcc_type: list[str] | tuple[str] = ['D', 'I', 'V', 'X'],
                      recording_time: int = 30) -> None:
    '''
    Writes the stream to a file.
    
    Args:
        rtsp_url (str): url rtsp stream.
        output_path (str): path to the output file.
        fourcc_type (list[str] | tuple[str]): type VideoWriter_fourcc.
        recording_time (int): time in seconds to record the stream.
        
    Retruns:
        None
    '''
    
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

    cap = cv2.VideoCapture(rtsp_url)    
    if not cap.isOpened():
        print("Failed to read rtsp stream. Make sure you specified it correctly `rtshp_url`.")
        return None
    else:
        print("Recording has started!")

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = cap.get(cv2.CAP_PROP_FPS)

    fourcc =  cv2.VideoWriter_fourcc(*fourcc_type)
    out = cv2.VideoWriter(output_path, fourcc, frame_count, (frame_width, frame_height))

    start_time = datetime.now()
    while cap.isOpened() and (datetime.now() - start_time).seconds < recording_time:
        ret, frame = cap.read()

        if not ret:
            print("Failed to get frame. Terminating...")
            break
        
        out.write(frame)

        # To exit, press 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Recording finished!")

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    return None


if __name__ == "__main__":
    # test functions  
    # save_annotated_frames("./test_data/output1.avi", 
    #                         "./test_data/output1.json",
    #                         save_dir_path="frames")
    
    draw_annotation_frame("./frames/frame_000107.png", 
                          "./test_data/output1.json")
    