import os, cv2, argparse

ap = argparse.ArgumentParser()

ap.add_argument("-lp", "--load_path", type=str,
                help="loading path")
ap.add_argument("-sp", "--save_path", type=str,
                help="saving path")

ap.add_argument("--w", "--width", type=str, default=100,
                help="width")

ap.add_argument("--h", "--height", type=str, default=100,
                help="height")
args = vars(ap.parse_args())
load_path = args["load_path"]
save_path = args["save_path"]

if not os.path.isdir(save_path):
    os.makedirs(save_path)

for img in os.listdir(load_path): # can be modified according to number of pictures
    image = cv2.imread(os.path.join(load_path, img), 3)  # 3 for RGB
    try:
        resized_image = cv2.resize(image, (100, 100))
    except cv2.error:
        continue
    cv2.imwrite(os.path.join(save_path,img), resized_image)