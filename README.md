1. This program allows the user to specify a number of bounding boxes, the coordinates of said bboxes, delay time in frames, and whether to show an outline for the bboxes or not. There is also the option to randomise bbox position and scale as well as delay time. Within these bboxes, the video playback is offset by a number of frames specified by the `delay` input, and the region outside the boxes is as usual. Once the last frame is reached within the bboxes, the region within the bbox loops back to the first frame. Due to the structure of the algorithm, bboxes can be layered, which then applies the delay effect twice; one for each layered bbox in a given region.

2. All code written by me, Levin Rainey. Obviously I read and copied sections of the opencv-python (https://pypi.org/project/opencv-python/) in doing so.
   
3. Setup requires:
        a) A directory titled `output_videos` to be created in the same directory as the program file.
        b) A directory titled `outputs` to be created in the `output_videos` directory.
        c) A directory titled `test_images` to be created in the same directory as the program file.

4. Clearly this setup is strange and irritating, but I'm uploading this program more to back it up for myself than for public use. If you want to change this directory system, see the following lines in the Python file: `24`, `63`.

5. Finally, you may notice that in the included pre-set-up directories here on GitHub, there contains a `.txt` file in both `outputs` and `test_images`. This was for me to create these directories on GitHub, as I did it via the website. Feel free to delete them after download, since they obviously provide no use to the program.
