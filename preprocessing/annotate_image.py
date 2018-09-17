import cv2, argparse, os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str,
                help="image path")

args = vars(ap.parse_args())
image_path = args["image"]
image = cv2.imread(image_path)
initBB = cv2.selectROI("Image", image, fromCenter=False,
                               showCrosshair=True)

with open("Data/annotations/"+os.path.basename(image_path).split(".")[0]+".txt", 'w') as f:
    f.write(str(initBB))