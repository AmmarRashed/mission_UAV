import os, argparse
from xml.dom import minidom

ap = argparse.ArgumentParser()

ap.add_argument("-lp", "--load_path", type=str,
                help="loading path")
ap.add_argument("-sp", "--save_path", type=str,
                help="saving path")

args = vars(ap.parse_args())
load_path = args["load_path"]
save_path = args["save_path"]

def parse_boundary_box_params(file_path, save_path):
    mydoc = minidom.parse(file_path)
    element_text = lambda element: mydoc.getElementsByTagName(element)[0].childNodes[0].data
    filename = element_text('filename').split(".")[0]
    assert filename == os.path.basename(file_path).split(".")[0]

    xmin = int(element_text("xmin"))
    xmax = int(element_text("xmax"))

    ymin = int(element_text("ymin"))
    ymax = int(element_text("ymax"))

    params = xmin, ymin, xmax - xmin, ymax - ymin

    with open(os.path.join(save_path, filename) + ".txt", 'w') as f:
        f.write(str(params))


for file in os.listdir(load_path):
    parse_boundary_box_params(os.path.join(load_path, file), save_path)

