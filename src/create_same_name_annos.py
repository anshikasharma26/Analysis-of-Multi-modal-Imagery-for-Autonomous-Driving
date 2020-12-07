import os
import os.path
from os.path import join
import cv2
import numpy as np

NAMES_TO_LABELS = {'person': 0, 'people': 1, 'cyclist': 2, 'person?': 3}


def get_visible_anno_file_paths(dir, result):
    a = os.listdir(dir)
    for item in a:
        path = dir + "/"+item
        if os.path.isdir(path):
            get_visible_anno_file_paths(path, result)
        elif os.path.isfile(path) and ".txt":
            result.append(path)


if __name__ == "__main__":
    # get all anno files
    result = []
    get_visible_anno_file_paths('annotations', result)

    np.random.shuffle(result)
    print(result)
    print(len(result))

    # for each anno file, create new anno file that follow Yolo anno format
    count = 0
    for old_path in result:
        octets = old_path.split("/", maxsplit=40)
        new_anno_path = octets[1] + "/" + octets[2] + "/visible/" + octets[3]

        image_path = new_anno_path[:-3] + "jpg"
        image = cv2.imread(image_path)
        im_height = image.shape[0]
        im_width = image.shape[1]

        # read old file and write to new file
        file = open(old_path, "r")
        lines = file.readlines()[1:]  # exclude the first row
        a = 1
        bboxes = []
        for line in lines:
            items = line.split(sep=" ", maxsplit=20)
            className = items[0]
            classLabel = NAMES_TO_LABELS[className]
            xMin = int(items[1])
            yMin = int(items[2])
            width = int(items[3])
            height = int(items[4])
            xMax = xMin + width
            yMax = yMin + height
            xCenter = (xMax - xMin) // 2 + xMin
            yCenter = (yMax - yMin) // 2 + yMin

            bbox = str(classLabel) + " " + str(xCenter/ im_width) + " " + str(yCenter/ im_height) + " " + str(width / im_width) + " " + str(height / im_height)
            bboxes.append(bbox)
        bboxesStr = ""
        for bbox in bboxes:
            bboxesStr += bbox + "\n"
        print(str(count) + "create file "+new_anno_path+" and write "+bboxesStr)
        count +=1
        file = open(new_anno_path, "w+")
        file.write(bboxesStr)
        file.close()
