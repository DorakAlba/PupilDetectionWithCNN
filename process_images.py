import os
import json
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import ImageDraw
from PIL import Image
import numpy as np
from src.utils.imgutils import searchInnerBound, searchOuterBound



def image_work(folder, file):
    eye_img = f'CASIA1/{folder}/{file}'
    eye_img_s = f'CASIAsolution/{file}'
    img = Image.open(eye_img).convert("L")

    np_img = np.clip(np.array(img) * 1, 0, 255)
    img = Image.fromarray(np_img)

    y, x, r = searchInnerBound(np_img)
    y_o, x_o, r_o = searchOuterBound(np_img, y, x, r)

    draw = ImageDraw.Draw(img)

    def draw_ellise_by_points(x, y, r):
        leftUpPoint = (x - r, y - r)
        rightDownPoint = (x + r, y + r)

        twoPointList = [leftUpPoint, rightDownPoint]
        draw.ellipse(twoPointList, width=2, outline=(255,))

    draw_ellise_by_points(x,y,r)
    draw_ellise_by_points(x_o,y_o,r_o)


    img.save(eye_img_s)
    return [int(x),int(y),int(r), int(x_o),int(y_o), int(r_o)]


directory = "CASIA1"

expansion = {}
test_expansion = {}
counter = 0
with open("CASIAsolution/labels.json","w") as file:

    # data = json.load(file)
    for filename in os.listdir("CASIA1"):
        counter+=1
        for filename2 in os.listdir(directory+"/"+filename):
            if counter<85:
                expansion[f"{filename}/{filename2}"] = image_work(filename, filename2)
            else:
                test_expansion[f"{filename}/{filename2}"] = image_work(filename, filename2)


    # data.update(expansion)
    # file.seek(0)
    # print(expansion)
    json.dump(expansion,file,indent=2)
with open("CASIAsolution/test.json","w") as file_test:
    json.dump(test_expansion,file_test,indent=2)
