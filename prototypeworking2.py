import cv2 as cv
from os import listdir
from datetime import datetime
from random import randint


def get_vid_data(video_capture):
    return [int(video_capture.get(3)), int(video_capture.get(4)), int(video_capture.get(7)), int(video_capture.get(5))]  # width, height, total frames, fps


def get_all_frames(video_capture):
    frames = []
    while True:
        ret, frame = video_capture.read()
        if not ret:  # if not frame returned:
            break
        frames.append(frame)
    video_capture.release()
    return frames


def merge_frames(frames, DELAY_F, vid_data, bbox, file_save_name, outline_boxes):
    width, height, _, fps = vid_data
    save_path = f"./output_videos/outputs/{file_save_name}.mp4"
    out = cv.VideoWriter(save_path, cv.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    x, y, w, h = bbox
    current_index = 0
    print(f"processing {len(frames)} frames...")
    for frame in frames:
        if outline_boxes:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # drawing 2px green rectangle around bbox
        frm = frame.copy()
        frm[y:(y+h), x:(x+w)] = DELAY_F[current_index][y:(y+h), x:(x+w)]
        current_index += 1
        out.write(frm)
    out.release()
    print('complete')
    return save_path


def create_delaybox(vid_path, bbox, file_save_name, delay=20, outline_boxes=True):
    video_capture = cv.VideoCapture(vid_path)
    vid_data = get_vid_data(video_capture)  # width, height, total frames, fps
    frames = get_all_frames(video_capture)
    delay %= len(frames)  # this is to stop delay being larger than number of frames while maintaining ratio of delay.
    DELAY_F = frames[delay:] + frames[:delay]  # order of delayed frames
    return merge_frames(frames, DELAY_F, vid_data, bbox, file_save_name, outline_boxes)


def gen_random_settings(width, height, total_frames):
    xs = (randint(0, width), randint(0, width))
    ys = (randint(0, height), randint(0, height))
    x = min(xs)
    w = max(xs) - x
    y = min(ys)
    h = max(ys) - y
    delay = randint(1, total_frames - 1)  # randint is inclusive, and i want a minimum of a 1 frame delay ratio.
    return (x, y, w, h), delay


def run_program():
    print('\n')
    vid_dir_path = "./test_videos"
    c = 1
    files = listdir(vid_dir_path)
    for file in files:
        print(f"{c}. {file}")
        c += 1
    choice = int(input('\nChoose a file (enter number): '))
    vid_path = vid_dir_path + "/" + files[choice-1]
    outline_boxes = (input("Enter 'o' to include an outline of each box, or enter 'n' for no outlines: ") == 'o')
    video_capture = cv.VideoCapture(vid_path)
    width, height, total_frames, _ = get_vid_data(video_capture)
    print(f"\nVideo Dimensions: Width {width}, Height {height}.\n")
    bbox_number = 0
    while bbox_number < 1:
        bbox_number = int(input("Number of delay boxes (>=1): "))
    randomise_box_coords = (input("Enter 'r' to randomise all settings, or enter 'm' to choose manually: ") == 'r')
    file_save_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if randomise_box_coords:
        for i in range(bbox_number):
            bbox, delay = gen_random_settings(width, height, total_frames)  # x, y, w, h
            print('\n')
            print(f"Box {i+1}/{bbox_number}: random coords (x, y, width, height): {bbox}")
            print(f"Delay: {delay} frames")
            vid_path = create_delaybox(vid_path, bbox, file_save_name, delay, outline_boxes)
    else:
        for i in range(bbox_number):
            bbox = (max(0, int(input("Box start x: "))), 
                    max(0, int(input("Box start y: "))),
                    min(width, int(input("Box width: "))),
                    min(height, int(input("Box height: "))))
            delay = int(input(f"Frame delay in box {i+1}/{bbox_number}: "))
            vid_path = create_delaybox(vid_path, bbox, file_save_name, delay, outline_boxes)
    print(f"Video saved at {vid_path}")


if __name__ == '__main__':
    run_program()
