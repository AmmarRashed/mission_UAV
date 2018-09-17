from imutils.video import VideoStream
from imutils.video import FPS

import argparse
import imutils
import cv2
import time

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")

args = vars(ap.parse_args())

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}
tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

initBB = None

vs = cv2.VideoCapture(args["video"])
fps = None
i = 0
while True:
    frame = vs.read()[1]
    if frame is None:
        break
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]

    if initBB is not None:  # we are currently tracking an object
        # gran the new bounding boxes of the object
        (success, box) = tracker.update(frame)

        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # update fps counter
        fps.update()
        fps.stop()

        # set of info to display
        info = [
            ("Tracker", "KCF"),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2F}".format(fps.fps()))
        ]

        # draw the info on the frame
        for (i, (k, v)) in enumerate(info):
            text = "{}:{}".format(k, v)
            cv2.putText(frame, text, (10, H - i * 20 - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    else:
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                               showCrosshair=True)  # TODO get the bounding box
        tracker.init(frame, initBB)
        fps = FPS().start()

vs.release()
cv2.destroyAllWindows()