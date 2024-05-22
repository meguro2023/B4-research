import glob

import cv2

import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

img_array = []
for filename in sorted(glob.glob("/Users/meguro/Documents/谷口研/修士卒研/particlefiller/data/田野倉/output_frame2/*.jpg")):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)
    break
    #img_array.append(img)
    # i+=1
    # if i%100==0:
    #     print(i)
    # if i>=15000:
    #     break
i = 0
for filename in sorted(glob.glob("/Users/meguro/Documents/谷口研/修士卒研/particlefiller/data/田野倉/output_frame2/*.jpg"), key=natural_keys):
    img = cv2.imread(filename)
    # height, width, layers = img.shape
    # size = (width, height)
    img_array.append(img)
    i+=1
    if i%100==0:
        print(i)
    # if i>=15000:
    #     break

name = '/Users/meguro/Documents/谷口研/修士卒研/particlefiller/data/田野倉/output_frame2/particle_video.mp4'
out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), 30.0, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()




# img_array = []
# i = 0
# for filename in sorted(glob.glob("/home/meguro/mydatasets/boxmot2/上江橋/*.jpg")):
#     img = cv2.imread(filename)
#     height, width, layers = img.shape
#     size = (width, height)
#     break
#     #img_array.append(img)
    

# for filename in sorted(glob.glob("/home/meguro/mydatasets/boxmot2/上江橋/*.jpg")):
#     # if i<15000:
#     #     continue
#     img = cv2.imread(filename)
#     # height, width, layers = img.shape
#     # size = (width, height)
#     img_array.append(img)
#     i+=1
#     if i%100==0:
#         print(i)
#     # if i>=30000:
#     #     break

# name = '/home/meguro/mydatasets/cctv2/実験用データ/結果動画/上江橋_auto.mp4'
# out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), 30.0, size)

# for i in range(len(img_array)):
#     out.write(img_array[i])
# out.release()




# img_array = []
# i = 0
# for filename in sorted(glob.glob("/home/meguro/mydatasets/boxmot/botsort/仲町二丁目_30分/*.jpg")):
#     img = cv2.imread(filename)
#     height, width, layers = img.shape
#     size = (width, height)
#     break
#     #img_array.append(img)
#     # i+=1
#     # if i%100==0:
#     #     print(i)
#     # if i>=15000:
#     #     break

# for filename in sorted(glob.glob("/home/meguro/mydatasets/boxmot/botsort/仲町二丁目_30分/*.jpg")):
#     if i<30000:
#         continue
#     img = cv2.imread(filename)
#     # height, width, layers = img.shape
#     # size = (width, height)
#     img_array.append(img)
#     i+=1
#     if i%1000==0:
#         print(i)
#     if i>=45000:
#         break

# name = '/home/meguro/mydatasets/boxmot/bbox_video/仲町二丁目_30分_3.mp4'
# out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), 30.0, size)

# for i in range(len(img_array)):
#     out.write(img_array[i])
# out.release()




# img_array = []
# i = 0
# for filename in sorted(glob.glob("/home/meguro/mydatasets/boxmot/botsort/仲町二丁目_30分/*.jpg")):
#     img = cv2.imread(filename)
#     height, width, layers = img.shape
#     size = (width, height)
#     break
#     #img_array.append(img)
#     # i+=1
#     # if i%100==0:
#     #     print(i)
#     # if i>=15000:
#     #     break

# for filename in sorted(glob.glob("/home/meguro/mydatasets/boxmot/botsort/仲町二丁目_30分/*.jpg")):
#     if i<45000:
#         continue
#     img = cv2.imread(filename)
#     # height, width, layers = img.shape
#     # size = (width, height)
#     img_array.append(img)
#     i+=1
#     if i%1000==0:
#         print(i)
#     # if i>=45000:
#     #     break

# name = '/home/meguro/mydatasets/boxmot/bbox_video/仲町二丁目_30分_4.mp4'
# out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), 30.0, size)

# for i in range(len(img_array)):
#     out.write(img_array[i])
# out.release()

