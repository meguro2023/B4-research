# Mikel Broström 🔥 Yolo Tracking 🧾 AGPL-3.0 license

import numpy as np
#import torch
import cv2
#from PIL import Image
import math
import matplotlib.pyplot as plt


# カウント数を描画
def write_count_text(img, total):
    # img = cv2.imread(image_path)
    # 黒塗りの背景を加える
    cv2.rectangle(img, (0, 0), (310, 80), color=(0, 0, 0), thickness=-1)
    moji = 'total:'+str(total)
    cv2.putText(img,
        text=moji,
        org=(10, 60),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=2.0,
        color=(0, 0, 255),
        thickness=5,
        lineType=cv2.LINE_4)
    # cv2.imwrite('./output_image/bytetrack/神宮橋/'+str(frame_idx)+'.jpg', img)
    return img


# カウント数を描画
def write_count_text_big(img, total):
    # img = cv2.imread(image_path)
    # 黒塗りの背景を加える
    cv2.rectangle(img, (0, 0), (490, 140), color=(0, 0, 0), thickness=-1)
    moji = 'total:'+str(total)
    cv2.putText(img,
        text=moji,
        org=(30, 110),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=3.5,
        color=(0, 0, 255),
        thickness=8,
        lineType=cv2.LINE_4)
    # cv2.imwrite('./output_image/bytetrack/神宮橋/'+str(frame_idx)+'.jpg', img)
    return img

def write_count_text_big2(img, total):
    # img = cv2.imread(image_path)
    # 黒塗りの背景を加える
    cv2.rectangle(img, (0, 0), (220, 80), color=(0, 0, 0), thickness=-1)
    moji = 'total:'+str(total)
    cv2.putText(img,
        text=moji,
        org=(12, 60),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=2,
        color=(0, 0, 255),
        thickness=6,
        lineType=cv2.LINE_4)
    # cv2.imwrite('./output_image/bytetrack/神宮橋/'+str(frame_idx)+'.jpg', img)
    return img


def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

# bboxの中心を描画
def write_bbox_center(img, x, y, in_out):
    # 赤色のBGR値を指定 (OpenCVではBGRの順序)
    if (in_out==1 or in_out==0): # エリア内
        point_color = (0, 255, 0)
        in_out = 1
    else: # エリア外
        point_color = (0, 0, 255)
        in_out = -1
    # 指定した座標に赤い点を描画
    cv2.circle(img, (int(x), int(y)), 10, point_color, -1)  # 5は円の半径、-1は塗りつぶしを意味します
    return img, in_out


# 指定したパスに描画した画像を保存
def save_image(img, output_path, frame_idx):
    num = str(frame_idx)
    cv2.imwrite(output_path+num.zfill(5)+'.jpg', img)


# 検出の範囲を設定・描画（その領域にbboxの中心が来たら検出する）
def detection_area_draw(img, area, lane_head):
    # 多角形の頂点を定義 (ここでは三角形を例に取ります)
    # pts = np.array([[600, 300], [800, 850], [1800, 650], [1300, 250]], dtype=np.int32)
    # # 多角形を描画
    #cv2.polylines(img, [area], isClosed=True, color=(24, 235, 249), thickness=5)

    # 車線をすべて描画
    for lane in area:
        cv2.polylines(img, [lane], isClosed=True, color=(24, 235, 249), thickness=5)

    # # 車線の先頭の基準点を描画
    # for head in lane_head:
    #     img = cv2.circle(img, (head[0], head[1]), radius=10, color=(255, 200, 0), thickness=-1)

    return img

# 検出の範囲を設定・描画（その領域にbboxの中心が来たら検出する）
def detection_area_draw2(img, area):
    # 多角形の頂点を定義 (ここでは三角形を例に取ります)
    # pts = np.array([[600, 300], [800, 850], [1800, 650], [1300, 250]], dtype=np.int32)
    # # 多角形を描画
    img = cv2.polylines(img, [area], isClosed=True, color=(24, 235, 249), thickness=5)

    # # 車線をすべて描画
    # for lane in area:
    #     cv2.polylines(img, [lane], isClosed=True, color=(24, 235, 249), thickness=5)

    # # 車線の先頭の基準点を描画
    # for head in lane_head:
    #     img = cv2.circle(img, (head[0], head[1]), radius=10, color=(255, 200, 0), thickness=-1)

    return img

# 検出の範囲を設定・描画
# real_laneは射影変換するときに使用したエリア，DETECTION_AREAは検出エリア（鳥瞰画像から逆変換したもの）
def detection_area_draw3(img, real_lane, DETECTION_AREA):
    # 黄色い領域
    img = cv2.polylines(img, [real_lane.astype(int)], isClosed=True, color=(24, 235, 249), thickness=15)
    # 検出範囲を描画
    img = cv2.polylines(img, [DETECTION_AREA], isClosed=True, color=(255,0,255), thickness=3)
    return img

def detection_area_draw4(img, real_lane):
    # 黄色い領域
    img = cv2.polylines(img, [real_lane.astype(int)], isClosed=True, color=(24, 235, 249), thickness=7)
    # # 検出範囲を描画
    # img = cv2.polylines(img, [DETECTION_AREA], isClosed=True, color=(255,0,255), thickness=3)
    return img


# bboxの中心が検出領域に入っているかを判定し，入っているなら緑，入っていないなら赤の点を打つ
# pt1:bboxの左上，pt2:bboxの右下
def object_in_the_area(lane_area, trajectory_point, id_posi, pt1, pt2):
    # 多角形の頂点を定義 (ここでは三角形を例に取ります)
    # pts = np.array([[600, 300], [800, 850], [1800, 650], [1300, 250]], dtype=np.int32)
    # 判定したい点を定義
    if trajectory_point=='BOTTOM_LEFT':
        x = pt1[0]
        y = pt2[1]
    elif trajectory_point=='BOTTOM_RIGHT':
        x = pt2[0]
        y = pt2[1]
    elif trajectory_point=='CENTER':
        x = int((pt1[0]+pt2[0])/2)
        y = int((pt1[1]+pt2[1])/2)
    elif trajectory_point=='BOTTOM_CENTER':
        x = int((pt1[0]+pt2[0])/2)
        y = pt2[1]

    point_to_check = (int(x), int(y))
    # 多角形内に点があるかどうかを判定
    in_out = -1
    for i, lane in enumerate(lane_area):
        point_inside_polygon = cv2.pointPolygonTest(lane, point_to_check, measureDist=False)
        if point_inside_polygon == 1 or point_inside_polygon == 0:
            in_out = i
            id_posi[i].append([x, y])

    #point_inside_polygon = cv2.pointPolygonTest(area, point_to_check, measureDist=False)
    # 判定結果
    # if point_inside_polygon == 1:
    #     print("点は多角形の内部にあります。")
    # elif point_inside_polygon == 0:
    #     print("点は多角形の境界上にあります。")
    # else:
    #     print("点は多角形の外部にあります。")
    # img, in_out = write_bbox_center(img, x, y, point_inside_polygon) # bboxの中心を描画（エリア内:緑，エリア外:赤）
    return in_out, id_posi

# これは車線用
# 入力された点(基準点)がどの車線内にいるのか，入っていないのかを判定
# 出力は, エリア外:in_out=-1, 車線内:inout=車線の番号
def object_in_the_area2(lane_area, x, y):
    point_to_check = (int(x), int(y))
    # 多角形内に点があるかどうかを判定
    in_out = -1
    for i, lane in enumerate(lane_area):
        point_inside_polygon = cv2.pointPolygonTest(lane, point_to_check, measureDist=False)
        if point_inside_polygon == 1 or point_inside_polygon == 0:
            in_out = i
            break
    return in_out

# こっちはエリア用
# 入力された点(基準点)が指定したエリアに入っているか，入っていないのかを判定
# 出力は, エリア外:in_out=-1, 車線内:inout=0
def object_in_the_area3(area, x, y):
    point_to_check = (int(x), int(y))
    # 多角形内に点があるかどうかを判定
    in_out = -1
    point_inside_polygon = cv2.pointPolygonTest(area, point_to_check, measureDist=False)
    if point_inside_polygon == 1 or point_inside_polygon == 0:
        in_out = 0
    
    return in_out


# 入力された点(基準点)が指定したエリアに入っているか，入っていないのかを判定
# xとyは，trajectory_xとtrajectory_y
# 出力は, エリア外:in_out=-1, 車線内:inout=車線のindex
def object_in_the_area_svm(up_down_model, lane_model, count_lane, id_posi, x, y):
    z = np.array([[x,y]])

    in_out=0
    # 上り，下りのどちらかだけカウントする場合
    # 下りのクラスが0，上りのクラスが1である
    if count_lane=='up':
        up_or_down = up_down_model.predict(z)
        if up_or_down[0]==1:
            in_out=0
        else:
            in_out=-1
    elif count_lane=='down':
        up_or_down = up_down_model.predict(z)
        if up_or_down[0]==0:
            in_out=0
        else:
            in_out=-1

    if in_out>=0:
        # predict関数で、車線を予測
        in_out = lane_model.predict(z)
        in_out = in_out[0]
        id_posi[in_out].append([x, y])

    return in_out, id_posi

# 入力された点(基準点)が指定したエリアに入っているか，入っていないのかを判定
# xとyは，trajectory_xとtrajectory_y
# 出力は, エリア外:in_out=-1, 車線内:inout=0
def object_in_the_area_svm2(up_down_model, lane_model, count_lane, x, y):
    z = np.array([[x,y]])

    in_out=0
    # 上り，下りのどちらかだけカウントする場合
    # 下りのクラスが0，上りのクラスが1である
    if count_lane=='up':
        up_or_down = up_down_model.predict(z)
        if up_or_down[0]==1:
            in_out=0
        else:
            in_out=-1
    elif count_lane=='down':
        up_or_down = up_down_model.predict(z)
        if up_or_down[0]==0:
            in_out=0
        else:
            in_out=-1

    if in_out>=0:
        # predict関数で、車線を予測
        in_out = lane_model.predict(z)
        in_out = in_out[0]

    return in_out



# エリア内にある物体のbboxを描画
def write_bbox_frame_id_class(img, id, class_name, conf, pt1, pt2):
    # 物体がエリア内にあるならid, class, bboxを描画
    cv2.rectangle(img,
        pt1,
        pt2,
        color=(0, 255, 0),
        thickness=5,
        lineType=cv2.LINE_4,
        shift=0)
    # bboxの上に背景を加える
    if class_name=='car':
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-40), (pt1[0]+340, pt1[1]), color=(0, 255, 0), thickness=-1)
    elif class_name=='truck':
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-40), (pt1[0]+380, pt1[1]), color=(0, 255, 0), thickness=-1)
    
    moji = 'id:'+str(id)+' '+class_name+' '+str(round(conf, 2))
    cv2.putText(img,
        text=moji,
        org=(pt1[0], pt1[1]-3),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1.5,
        color=(255, 255, 255),
        thickness=5,
        lineType=cv2.LINE_4)
    return img

def write_bbox_frame_id(img, id, pt1, pt2):
    if id>0:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=(0, 255, 0),
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)
        # bboxの上に背景を加える
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-25), (pt1[0]+100, pt1[1]), color=(0, 255, 0), thickness=-1)
    else:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=(0, 0, 255),
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)
        # bboxの上に背景を加える
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-25), (pt1[0]+100, pt1[1]), color=(0, 0, 255), thickness=-1)

    moji = 'id:'+str(id)
    cv2.putText(img,
        text=moji,
        org=(pt1[0], pt1[1]-3),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.7,
        color=(0, 0, 0),
        thickness=3,
        lineType=cv2.LINE_4)
    return img

def write_bbox_frame_id_free_big(img, id, pt1, pt2):
    # 物体がエリア内にあるならid, class, bboxを描画
    cv2.rectangle(img,
        pt1,
        pt2,
        color=(50, 205, 154),
        thickness=5,
        lineType=cv2.LINE_4,
        shift=0)
    # bboxの上に背景を加える
    # cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+205, pt1[1]), color=(50, 205, 154), thickness=-1)
    cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+165, pt1[1]), color=(50, 205, 154), thickness=-1)
    # bboxの上に文字を加える
    moji = 'id:'+str(id)
    cv2.putText(img,
        text=moji,
        org=(pt1[0]+3, pt1[1]-8),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=2,
        color=(0, 0, 0),
        thickness=8,
        lineType=cv2.LINE_4)
    
    # if id>0:
    #     # 物体がエリア内にあるならid, class, bboxを描画
    #     cv2.rectangle(img,
    #         pt1,
    #         pt2,
    #         color=(0, 255, 0),
    #         thickness=5,
    #         lineType=cv2.LINE_4,
    #         shift=0)
    #     # bboxの上に背景を加える
    #     cv2.rectangle(img, (pt1[0]-3, pt1[1]-25), (pt1[0]+100, pt1[1]), color=(0, 255, 0), thickness=-1)
    # else:
    #     # 物体がエリア内にあるならid, class, bboxを描画
    #     cv2.rectangle(img,
    #         pt1,
    #         pt2,
    #         color=(0, 0, 255),
    #         thickness=5,
    #         lineType=cv2.LINE_4,
    #         shift=0)
    #     # bboxの上に背景を加える
    #     cv2.rectangle(img, (pt1[0]-3, pt1[1]-25), (pt1[0]+100, pt1[1]), color=(0, 0, 255), thickness=-1)

    # moji = 'id:'+str(id)
    # cv2.putText(img,
    #     text=moji,
    #     org=(pt1[0], pt1[1]-3),
    #     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    #     fontScale=0.7,
    #     color=(0, 0, 0),
    #     thickness=3,
    #     lineType=cv2.LINE_4)
    return img


# track_trans.py用
def write_bbox_frame_id2(img, id, inverse_M, posi, prevented_switch_id, pt1, pt2):
    if id>0:
        if id not in prevented_switch_id:
            # 物体がエリア内にあるならid, class, bboxを描画
            cv2.rectangle(img,
                pt1,
                pt2,
                color=(50, 205, 154),
                thickness=5,
                lineType=cv2.LINE_4,
                shift=0)
            # bboxの上に背景を加える
            cv2.rectangle(img, (pt1[0]-3, pt1[1]-25), (pt1[0]+85, pt1[1]), color=(50, 205, 154), thickness=-1)
            # bboxの上に文字を加える
            moji = 'id:'+str(id)
            cv2.putText(img,
                text=moji,
                org=(pt1[0], pt1[1]-3),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.7,
                color=(0, 0, 0),
                thickness=3,
                lineType=cv2.LINE_4)
        else:
            # 物体がエリア内にあるならid, class, bboxを描画
            cv2.rectangle(img,
                pt1,
                pt2,
                color=(255, 191, 0),
                thickness=5,
                lineType=cv2.LINE_4,
                shift=0)
            # bboxの上に背景を加える
            cv2.rectangle(img, (pt1[0]-3, pt1[1]-25), (pt1[0]+85, pt1[1]), color=(255, 191, 0), thickness=-1)
            # bboxの上に文字を加える
            moji = 'id:'+str(id)
            cv2.putText(img,
                text=moji,
                org=(pt1[0], pt1[1]-3),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.7,
                color=(0, 0, 0),
                thickness=3,
                lineType=cv2.LINE_4)


    # マイナスidの場合は基準点のみ打つ
    else:
        a = transform_pt((posi[0],posi[1]), inverse_M)
        #cv2.circle(img, a, 10, (0,0,255), -1)  # 5は円の半径、-1は塗りつぶしを意味します
        cv2.rectangle(img, (a[0]-15, a[1]-15), (a[0]+15, a[1]+15), (0,0,255), thickness=5)
        # bboxの上に背景を加える
        cv2.rectangle(img, (a[0]-18, a[1]-45), (a[0]+88, a[1]-15), color=(0,0,255), thickness=-1)
        # bboxの上に文字を加える
        moji = 'id:'+str(id)
        cv2.putText(img,
            text=moji,
            org=(a[0]-10, a[1]-20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.7,
            color=(0, 0, 0),
            thickness=3,
            lineType=cv2.LINE_4)

    return img


# track_trans.py用
def write_bbox_frame_id3_big(img, id, inverse_M, posi, prevented_switch_id, pt1, pt2, a=0, b=0, c=0, d=0):
    if id>0:
        if id not in prevented_switch_id or id==4:
            if id>=10 and id<100:
                # 物体がエリア内にあるならid, class, bboxを描画
                cv2.rectangle(img,
                    pt1,
                    pt2,
                    color=(50, 205, 154),
                    thickness=5,
                    lineType=cv2.LINE_4,
                    shift=0)
                # # bboxの上に背景を加える
                # cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+165, pt1[1]), color=(50, 205, 154), thickness=-1)
                # # bboxの上に文字を加える
                # moji = 'id:'+str(id)
                # cv2.putText(img,
                #     text=moji,
                #     org=(pt1[0]+3, pt1[1]-8),
                #     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                #     fontScale=2,
                #     color=(0, 0, 0),
                #     thickness=8,
                #     lineType=cv2.LINE_4)
            elif id>=100:
                # 物体がエリア内にあるならid, class, bboxを描画
                cv2.rectangle(img,
                    pt1,
                    pt2,
                    color=(50, 205, 154),
                    thickness=5,
                    lineType=cv2.LINE_4,
                    shift=0)
                # bboxの上に背景を加える
                cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+205, pt1[1]), color=(50, 205, 154), thickness=-1)
                # bboxの上に文字を加える
                moji = 'id:'+str(id)
                cv2.putText(img,
                    text=moji,
                    org=(pt1[0]+3, pt1[1]-8),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=2,
                    color=(0, 0, 0),
                    thickness=8,
                    lineType=cv2.LINE_4)
            else:
                if id==3:
                    # 物体がエリア内にあるならid, class, bboxを描画
                    cv2.rectangle(img,
                        pt1,
                        (pt2[0], pt2[1]+15),
                        color=(50, 205, 154),
                        thickness=5,
                        lineType=cv2.LINE_4,
                        shift=0)
                    # # bboxの上に背景を加える
                    # cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+128, pt1[1]), color=(50, 205, 154), thickness=-1)
                    # # bboxの上に文字を加える
                    # moji = 'id:'+str(id)
                    # cv2.putText(img,
                    #     text=moji,
                    #     org=(pt1[0]+3, pt1[1]-8),
                    #     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    #     fontScale=2,
                    #     color=(0, 0, 0),
                    #     thickness=8,
                    #     lineType=cv2.LINE_4)
                else:
                    # 物体がエリア内にあるならid, class, bboxを描画
                    cv2.rectangle(img,
                        pt1,
                        pt2,
                        color=(50, 205, 154),
                        thickness=5,
                        lineType=cv2.LINE_4,
                        shift=0)
                    # # bboxの上に背景を加える
                    # cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+128, pt1[1]), color=(50, 205, 154), thickness=-1)
                    # # bboxの上に文字を加える
                    # moji = 'id:'+str(id)
                    # cv2.putText(img,
                    #     text=moji,
                    #     org=(pt1[0]+3, pt1[1]-8),
                    #     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    #     fontScale=2,
                    #     color=(0, 0, 0),
                    #     thickness=8,
                    #     lineType=cv2.LINE_4)
    return img



# track_trans.py用
def write_bbox_frame_id2_big(img, id, inverse_M, posi, prevented_switch_id, pt1, pt2, a=0, b=0, c=0, d=0, e=0, f=0, g=0, h=0):    
    if id>0:
        if id not in prevented_switch_id or id==4 or id==8:
            if id>=10 and id<100:
                # 物体がエリア内にあるならid, class, bboxを描画
                cv2.rectangle(img,
                    pt1,
                    pt2,
                    color=(50, 205, 154),
                    thickness=5,
                    lineType=cv2.LINE_4,
                    shift=0)
                # bboxの上に背景を加える
                cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+165, pt1[1]), color=(50, 205, 154), thickness=-1)
                # bboxの上に文字を加える
                moji = 'id:'+str(id)
                cv2.putText(img,
                    text=moji,
                    org=(pt1[0]+3, pt1[1]-8),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=2,
                    color=(0, 0, 0),
                    thickness=8,
                    lineType=cv2.LINE_4)
            elif id>=100:
                # 物体がエリア内にあるならid, class, bboxを描画
                cv2.rectangle(img,
                    pt1,
                    pt2,
                    color=(50, 205, 154),
                    thickness=5,
                    lineType=cv2.LINE_4,
                    shift=0)
                # bboxの上に背景を加える
                cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+205, pt1[1]), color=(50, 205, 154), thickness=-1)
                # bboxの上に文字を加える
                moji = 'id:'+str(id)
                cv2.putText(img,
                    text=moji,
                    org=(pt1[0]+3, pt1[1]-8),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=2,
                    color=(0, 0, 0),
                    thickness=8,
                    lineType=cv2.LINE_4)
            else:
                if id==3:
                    # 物体がエリア内にあるならid, class, bboxを描画
                    cv2.rectangle(img,
                        pt1,
                        (pt2[0], pt2[1]+15),
                        color=(50, 205, 154),
                        thickness=5,
                        lineType=cv2.LINE_4,
                        shift=0)
                    # bboxの上に背景を加える
                    cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+128, pt1[1]), color=(50, 205, 154), thickness=-1)
                    # bboxの上に文字を加える
                    moji = 'id:'+str(id)
                    cv2.putText(img,
                        text=moji,
                        org=(pt1[0]+3, pt1[1]-8),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=2,
                        color=(0, 0, 0),
                        thickness=8,
                        lineType=cv2.LINE_4)
                else:
                    # 物体がエリア内にあるならid, class, bboxを描画
                    cv2.rectangle(img,
                        pt1,
                        pt2,
                        color=(50, 205, 154),
                        thickness=5,
                        lineType=cv2.LINE_4,
                        shift=0)
                    # bboxの上に背景を加える
                    cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+128, pt1[1]), color=(50, 205, 154), thickness=-1)
                    # bboxの上に文字を加える
                    moji = 'id:'+str(id)
                    cv2.putText(img,
                        text=moji,
                        org=(pt1[0]+3, pt1[1]-8),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=2,
                        color=(0, 0, 0),
                        thickness=8,
                        lineType=cv2.LINE_4)

        else:
            if id>=100:
                # 物体がエリア内にあるならid, class, bboxを描画
                cv2.rectangle(img,
                    pt1,
                    pt2,
                    color=(255, 191, 0),
                    thickness=5,
                    lineType=cv2.LINE_4,
                    shift=0)
                # bboxの上に背景を加える
                cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+205, pt1[1]), color=(255, 191, 0), thickness=-1)
                # bboxの上に文字を加える
                moji = 'id:'+str(id)
                cv2.putText(img,
                    text=moji,
                    org=(pt1[0]+3, pt1[1]-8),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=2,
                    color=(0, 0, 0),
                    thickness=8,
                    lineType=cv2.LINE_4)
            else:
                # 物体がエリア内にあるならid, class, bboxを描画
                cv2.rectangle(img,
                    pt1,
                    pt2,
                    color=(255, 191, 0),
                    thickness=5,
                    lineType=cv2.LINE_4,
                    shift=0)
                # bboxの上に背景を加える
                cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+165, pt1[1]), color=(255, 191, 0), thickness=-1)
                # bboxの上に文字を加える
                moji = 'id:'+str(id)
                cv2.putText(img,
                    text=moji,
                    org=(pt1[0]+3, pt1[1]-8),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=2,
                    color=(0, 0, 0),
                    thickness=8,
                    lineType=cv2.LINE_4)


    # マイナスidの場合は基準点のみ打つ
    else:
        # if id==-10:
        #     # 物体がエリア内にあるならid, class, bboxを描画
        #     cv2.rectangle(img,
        #         a,
        #         b,
        #         color=(0, 0, 255),
        #         thickness=5,
        #         lineType=cv2.LINE_4,
        #         shift=0)
        #     # bboxの上に背景を加える
        #     cv2.rectangle(img, (a[0]-3, a[1]-45), (a[0]+162, a[1]), color=(0, 0, 255), thickness=-1)
        #     # bboxの上に文字を加える
        #     moji = 'id:'+str(id)
        #     cv2.putText(img,
        #         text=moji,
        #         org=(a[0]+3, a[1]-5),
        #         fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #         fontScale=1.5,
        #         color=(0, 0, 0),
        #         thickness=5,
        #         lineType=cv2.LINE_4)
        # elif id==-16:
        #     # 物体がエリア内にあるならid, class, bboxを描画
        #     cv2.rectangle(img,
        #         c,
        #         d,
        #         color=(0, 0, 255),
        #         thickness=5,
        #         lineType=cv2.LINE_4,
        #         shift=0)
        #     # bboxの上に背景を加える
        #     cv2.rectangle(img, (c[0]-3, c[1]-45), (c[0]+162, c[1]), color=(0, 0, 255), thickness=-1)
        #     # bboxの上に文字を加える
        #     moji = 'id:'+str(id)
        #     cv2.putText(img,
        #         text=moji,
        #         org=(c[0]+3, c[1]-5),
        #         fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #         fontScale=1.5,
        #         color=(0, 0, 0),
        #         thickness=5,
        #         lineType=cv2.LINE_4)
        # elif id==-14:
        #     # 物体がエリア内にあるならid, class, bboxを描画
        #     cv2.rectangle(img,
        #         e,
        #         f,
        #         color=(0, 0, 255),
        #         thickness=5,
        #         lineType=cv2.LINE_4,
        #         shift=0)
        #     # bboxの上に背景を加える
        #     cv2.rectangle(img, (e[0]-3, e[1]-45), (e[0]+162, e[1]), color=(0, 0, 255), thickness=-1)
        #     # bboxの上に文字を加える
        #     moji = 'id:'+str(id)
        #     cv2.putText(img,
        #         text=moji,
        #         org=(e[0]+3, e[1]-5),
        #         fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #         fontScale=1.5,
        #         color=(0, 0, 0),
        #         thickness=5,
        #         lineType=cv2.LINE_4)
        # elif id==-22:
        #     # 物体がエリア内にあるならid, class, bboxを描画
        #     cv2.rectangle(img,
        #         g,
        #         h,
        #         color=(0, 0, 255),
        #         thickness=5,
        #         lineType=cv2.LINE_4,
        #         shift=0)
        #     # bboxの上に背景を加える
        #     cv2.rectangle(img, (g[0]-3, g[1]-45), (g[0]+162, g[1]), color=(0, 0, 255), thickness=-1)
        #     # bboxの上に文字を加える
        #     moji = 'id:'+str(id)
        #     cv2.putText(img,
        #         text=moji,
        #         org=(g[0]+3, g[1]-5),
        #         fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #         fontScale=1.5,
        #         color=(0, 0, 0),
        #         thickness=5,
        #         lineType=cv2.LINE_4)
        
        a = transform_pt((posi[0],posi[1]), inverse_M)
        #cv2.circle(img, a, 10, (0,0,255), -1)  # 5は円の半径、-1は塗りつぶしを意味します
        cv2.rectangle(img, (a[0]-15, a[1]-15), (a[0]+15, a[1]+15), (0,0,255), thickness=5)
        # bboxの上に背景を加える
        cv2.rectangle(img, (a[0]-18, a[1]-45), (a[0]+88, a[1]-15), color=(0,0,255), thickness=-1)
        # bboxの上に文字を加える
        moji = 'id:'+str(id)
        cv2.putText(img,
            text=moji,
            org=(a[0]-10, a[1]-20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.7,
            color=(0, 0, 0),
            thickness=3,
            lineType=cv2.LINE_4)

    return img



def write_bbox_frame_id2_big_huhu(img, id, pt1, pt2):
    
    # # 中心座標に点を描画
    # x = int((pt1[0]+pt2[0])/2)
    # y = int((pt1[1]+pt2[1])/2)
    # point_color = (255, 0, 255)
    # cv2.circle(img, (x, y), 8, point_color, -1)  # 5は円の半径、-1は塗りつぶしを意味します

    if id>=10 and id<100:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=(50, 205, 154),
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)
        # bboxの上に背景を加える
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+165, pt1[1]), color=(50, 205, 154), thickness=-1)
        # bboxの上に文字を加える
        moji = 'id:'+str(id)
        cv2.putText(img,
            text=moji,
            org=(pt1[0]+3, pt1[1]-8),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=2,
            color=(0, 0, 0),
            thickness=8,
            lineType=cv2.LINE_4)
    elif id>=100:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=(50, 205, 154),
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)
        # bboxの上に背景を加える
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+205, pt1[1]), color=(50, 205, 154), thickness=-1)
        # bboxの上に文字を加える
        moji = 'id:'+str(id)
        cv2.putText(img,
            text=moji,
            org=(pt1[0]+3, pt1[1]-8),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=2,
            color=(0, 0, 0),
            thickness=8,
            lineType=cv2.LINE_4)
    else:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=(50, 205, 154),
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)
        # bboxの上に背景を加える
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+128, pt1[1]), color=(50, 205, 154), thickness=-1)
        # bboxの上に文字を加える
        moji = 'id:'+str(id)
        cv2.putText(img,
            text=moji,
            org=(pt1[0]+3, pt1[1]-8),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=2,
            color=(0, 0, 0),
            thickness=8,
            lineType=cv2.LINE_4)

        

    return img

def write_bbox_frame_id3_big_huhu(img, id, pt1, pt2):
    
    # # 中心座標に点を描画
    # x = int((pt1[0]+pt2[0])/2)
    # y = int((pt1[1]+pt2[1])/2)
    # point_color = (255, 0, 255)
    # cv2.circle(img, (x, y), 8, point_color, -1)  # 5は円の半径、-1は塗りつぶしを意味します

    if id>=10 and id<100:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=(50, 205, 154),
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)
    elif id>=100:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=(50, 205, 154),
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)
        # bboxの上に背景を加える
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+205, pt1[1]), color=(50, 205, 154), thickness=-1)
        # bboxの上に文字を加える
        moji = 'id:'+str(id)
        cv2.putText(img,
            text=moji,
            org=(pt1[0]+3, pt1[1]-8),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=2,
            color=(0, 0, 0),
            thickness=8,
            lineType=cv2.LINE_4)
    else:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=(50, 205, 154),
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)    

    return img


# 車線ごとにbboxの色を変えて描画
def write_bbox_frame_id_lane_color(img, id, pt1, pt2, lane_color):
    if id>0:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=lane_color,
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)
        # bboxの上に背景を加える
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-25), (pt1[0]+100, pt1[1]), color=lane_color, thickness=-1)
    else:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=(0, 0, 255),
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)
        # bboxの上に背景を加える
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-25), (pt1[0]+100, pt1[1]), color=(0, 0, 255), thickness=-1)

    moji = 'id:'+str(id)
    # bboxの色が黒っぽいなら白，bboxの色が白っぽいなら黒でIDを描画
    blue, green, red = lane_color
    luminance = 0.299 * red + 0.587 * green + 0.114 * blue
    if luminance > 128:
        text_color=(0, 0, 0)
    else:
        text_color=(255,255,255)
    cv2.putText(img,
        text=moji,
        org=(pt1[0], pt1[1]-3),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.7,
        color=text_color,
        thickness=3,
        lineType=cv2.LINE_4)
    return img


# 車線ごとにbboxの色を変えて描画
def write_bbox_frame_id_huhu_big(img, id, pt1, pt2):
    if id!=52:
        # 物体がエリア内にあるならid, class, bboxを描画
        cv2.rectangle(img,
            pt1,
            pt2,
            color=(50, 205, 154),
            thickness=5,
            lineType=cv2.LINE_4,
            shift=0)
        # bboxの上に背景を加える
        cv2.rectangle(img, (pt1[0]-3, pt1[1]-65), (pt1[0]+165, pt1[1]), color=(50, 205, 154), thickness=-1)
        # bboxの上に文字を加える
        moji = 'id:'+str(id)
        cv2.putText(img,
            text=moji,
            org=(pt1[0]+3, pt1[1]-8),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=2,
            color=(0, 0, 0),
            thickness=8,
            lineType=cv2.LINE_4)
    
    return img




def write_bbox_frame(img, pt1, pt2):
    # 物体がエリア外ならbboxのみ描画
    cv2.rectangle(img,
        pt1,
        pt2,
        color=(0, 0, 255),
        thickness=5,
        lineType=cv2.LINE_4,
        shift=0)
    return img

# 軌跡を描画(bboxの指定した位置に点を打つ)
# pt1:bboxの左上，pt2:bboxの右下
def write_trajectory_point(img, trajectory_point, pt1, pt2):
    if trajectory_point=='BOTTOM_LEFT':
        x = pt1[0]
        y = pt2[1]
    elif trajectory_point=='BOTTOM_RIGHT':
        x = pt2[0]
        y = pt2[1]
    elif trajectory_point=='CENTER':
        x = int((pt1[0]+pt2[0])/2)
        y = int((pt1[1]+pt2[1])/2)
    elif trajectory_point=='BOTTOM_CENTER':
        x = int((pt1[0]+pt2[0])/2)
        y = pt2[1]
    # 紫色のBGR値を指定 (OpenCVではBGRの順序)
    point_color = (255, 0, 255)
    # 指定した座標に点を描画
    cv2.circle(img, (x, y), 5, point_color, -1)  # 5は円の半径、-1は塗りつぶしを意味します

    return img

# [[上りの軌跡の基準点], [下りの軌跡の基準点]]が与えられ，上りは赤，下りは青で描画
def write_trajectory_point2(img, histry_bbox_trajectory_point):
    for i, k in enumerate(histry_bbox_trajectory_point):
        if i==0:
            # 赤色のBGR値を指定 (OpenCVではBGRの順序)
            point_color = (0, 0, 255)
        else:
            # 青色のBGR値を指定 (OpenCVではBGRの順序)
            point_color = (255, 0, 0)
        # 指定した座標に点を描画
        for l in k:
            # cv2.circle(img, (l[0], l[1]), 5, point_color, -1)  # 5は円の半径、-1は塗りつぶしを意味します
            cv2.circle(img, l, 5, point_color, -1)  # 5は円の半径、-1は塗りつぶしを意味します

    return img

def write_rotate_bbox(image, pt1, pt3):
    r = 135
    
    x1=pt1[0]
    y1=pt1[1]
    x2=pt1[0]
    y2=pt3[1]
    x3=pt3[0]
    y3=pt3[1]
    x4=pt3[0]
    y4=pt1[1]
    center_x=(pt1[0]+pt3[0])//2
    center_y=(pt1[1]+pt3[1])//2
    r = math.radians(r)

    x5=int((x1-center_x)*math.cos(r)-(y1-center_y)*math.sin(r)+center_x)
    y5=int((x1-center_x)*math.sin(r)+(y1-center_y)*math.cos(r)+center_y)

    x6=int((x2-center_x)*math.cos(r)-(y2-center_y)*math.sin(r)+center_x)
    y6=int((x2-center_x)*math.sin(r)+(y2-center_y)*math.cos(r)+center_y)

    x7=int((x3-center_x)*math.cos(r)-(y3-center_y)*math.sin(r)+center_x)
    y7=int((x3-center_x)*math.sin(r)+(y3-center_y)*math.cos(r)+center_y)

    x8=int((x4-center_x)*math.cos(r)-(y4-center_y)*math.sin(r)+center_x)
    y8=int((x4-center_x)*math.sin(r)+(y4-center_y)*math.cos(r)+center_y)

    area = np.array([[x5, y5], [x6, y6], [x7, y7], [x8, y8]], dtype=np.int32)
    cv2.polylines(image, [area], isClosed=True, color=(255, 0, 0), thickness=5)
    
    return image

# 指定したところにマスクする
# area=[[top_left, bottom_right],[top_left, bottom_right],...]
def write_mask(image, masked_area):
    for m in masked_area:
        masked_image = cv2.rectangle(image, m[0], m[1], (0, 0, 0), thickness=-1)
        image = cv2.bitwise_and(image, masked_image)
    return image

# マスクエリアのリストを改造する関数
def conversion_mask_area(old_mask_area):
    mask_area = []
    for i, k in enumerate(old_mask_area):
        mask_area.append([])
        for j in range(4):
            if j==0:
                mask_area[i].append(k[0])
            elif j==1:
                mask_area[i].append((k[0][0], k[1][1]))
            elif j==2:
                mask_area[i].append(k[1])
            else:
                mask_area[i].append((k[1][0], k[0][1]))
    mask_area = np.array(mask_area)
    return mask_area

# 車線にどのidの車がいるのかを描画
def write_id_lane(image, id_lane):
    # 描画するテキストを指定
    texts = []
    for i, id in enumerate(id_lane):
        t = "lane"+str(i+1)+": "+str(id)
        texts.append(t)

    # フォント、スケール、色、太さを指定
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (255, 255, 255)  # テキストの色
    line_type = 2

    # テキストを描画する位置を指定（右上から下方向に描画）
    text_x = image.shape[1] - 700  # テキストの横方向の位置
    text_y = 40  # 最初のテキストの縦方向の位置

    # 画像にテキストを描画
    for text in texts:
        image = cv2.putText(image, text, (text_x, text_y), font, font_scale, font_color, line_type)
        text_y += 50  # 次のテキストの縦方向の位置を調整
    
    return image


# 車線にどのidの車がいるのかを描画
def write_id_lane_big(image, id_lane):
    # 黒塗りの背景を加える
    cv2.rectangle(image, (0, 0), (1920, 220), color=(0, 0, 0), thickness=-1)
    # 描画するテキストを指定
    texts = []
    for i, id in enumerate(id_lane):
        t = "lane"+str(i+1)+": "+str(id)
        texts.append(t)

    # フォント、スケール、色、太さを指定
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_color = (255, 255, 255)  # テキストの色
    # line_type = 2
    thickness = 5

    # テキストを描画する位置を指定（右上から下方向に描画）
    text_x = image.shape[1] - 600  # テキストの横方向の位置
    text_y = 80  # 最初のテキストの縦方向の位置

    # 画像にテキストを描画
    for text in texts:
        image = cv2.putText(image, text, (text_x, text_y), font, font_scale, font_color, thickness)
        text_y += 95  # 次のテキストの縦方向の位置を調整
    
    return image

    
# 車線ごとに，idを先頭順に並べる
def id_lane_sort(id_lane, lane_head, id_posi):
    new_id_lane = []
    new_id_lane_index = []
    for _ in lane_head:
        new_id_lane_index.append([])
        new_id_lane.append([])
    np_id_posi = np.array(id_posi)
    for i, head in enumerate(lane_head):
        # [[ユークリッド距離, 0(index番号)],[ユークリッド距離, 1],...]
        distance_index = []
        for j, posi in enumerate(id_posi[i]):
            dist = np.linalg.norm(head - posi)
            distance_index.append([dist, j])
        distance_index.sort()
        for k in distance_index:
            new_id_lane_index[i].append(k[1])
    
    for i, j in enumerate(new_id_lane_index):
        for index in j:
            new_id_lane[i].append(id_lane[i][index])
    return new_id_lane

# 車線ごとに，idを先頭順に並べる，id_laneとid_lane_xyxyとid_trajectory_posiのsortをする
def id_lane_sort2(id_lane, lane_head, id_lane_xyxy, id_posi):
    new_id_lane = []
    new_id_lane_xyxy = []
    new_id_trajectory_posi = []
    new_id_lane_index = []
    for _ in lane_head:
        new_id_lane_index.append([])
        new_id_lane.append([])
        new_id_lane_xyxy.append([])
        new_id_trajectory_posi.append([])
    #np_id_posi = np.array(id_posi)
    for i, head in enumerate(lane_head):
        # [[ユークリッド距離, 0(index番号)],[ユークリッド距離, 1],...]
        distance_index = []
        for j, posi in enumerate(id_posi[i]):
            dist = np.linalg.norm(head - posi)
            distance_index.append([dist, j])
        distance_index.sort()
        for k in distance_index:
            new_id_lane_index[i].append(k[1])
    
    for i, j in enumerate(new_id_lane_index):
        for index in j:
            new_id_lane[i].append(id_lane[i][index])
            new_id_lane_xyxy[i].append(id_lane_xyxy[i][index])
            new_id_trajectory_posi[i].append(id_posi[i][index])

    return new_id_lane, new_id_lane_xyxy, new_id_trajectory_posi

# 車線ごとに，idを先頭順に並べる，id_laneとid_lane_xyxyとid_trajectory_posiのsortをする
# 補正画像を考慮した簡易ver
# 射影変換後の車線は縦に流れるのか，横に流れるのか
# car_flow = 0: 車は縦に流れる，1: 車は横に流れる
def id_lane_sort3(head_direction, id_lane, id_lane_xyxy, id_posi):
    new_id_lane = []
    new_id_lane_xyxy = []
    new_id_trajectory_posi = []
    new_id_lane_index = []
    for _ in range(len(id_lane)):
        new_id_lane_index.append([])
        new_id_lane.append([])
        new_id_lane_xyxy.append([])
        new_id_trajectory_posi.append([])
    for i, lane_posi in enumerate(id_posi):
        # [[ユークリッド距離, 0(index番号)],[ユークリッド距離, 1],...]
        distance_index = []
        # 車が下に流れる場合はy座標を逆順にソートすることで先頭順になる
        if head_direction=='down':
            for j, posi in enumerate(lane_posi):
                distance_index.append([posi[1], j])
            distance_index.sort(reverse=True)
        elif head_direction=='up':
            for j, posi in enumerate(lane_posi):
                distance_index.append([posi[1], j])
            distance_index.sort()
        elif head_direction=='right':
            for j, posi in enumerate(lane_posi):
                distance_index.append([posi[0], j])
            distance_index.sort(reverse=True)
        else:
            for j, posi in enumerate(lane_posi):
                distance_index.append([posi[0], j])
            distance_index.sort()
        for k in distance_index:
            new_id_lane_index[i].append(k[1])
    for i, j in enumerate(new_id_lane_index):
        for index in j:
            new_id_lane[i].append(id_lane[i][index])
            new_id_lane_xyxy[i].append(id_lane_xyxy[i][index])
            new_id_trajectory_posi[i].append(id_posi[i][index])
    return new_id_lane, new_id_lane_xyxy, new_id_trajectory_posi


# bbox(a)とbbox(b)のiouを計算する
# a = [a_top_left, a_bottom_right], b = [b_top_left, b_bottom_right]
def calculation_iou(a, b):
    # a, bは矩形を表すリストで、a=[xmin, ymin, xmax, ymax]
    ax_mn, ay_mn, ax_mx, ay_mx = a[0], a[1], a[2], a[3]
    bx_mn, by_mn, bx_mx, by_mx = b[0], b[1], b[2], b[3]

    a_area = (ax_mx - ax_mn + 1) * (ay_mx - ay_mn + 1)
    b_area = (bx_mx - bx_mn + 1) * (by_mx - by_mn + 1)

    abx_mn = max(ax_mn, bx_mn)
    aby_mn = max(ay_mn, by_mn)
    abx_mx = min(ax_mx, bx_mx)
    aby_mx = min(ay_mx, by_mx)
    w = max(0, abx_mx - abx_mn + 1)
    h = max(0, aby_mx - aby_mn + 1)
    intersect = w*h

    iou = intersect / (a_area + b_area - intersect)
    return iou


# 基準点(bboxの左下や右下など)を計算
# pt1:bboxの左上，pt2:bboxの右下
def trajectory_calculation(trajectory_point, pt1, pt2):
    if trajectory_point=='BOTTOM_LEFT':
        x = pt1[0]
        y = pt2[1]
    elif trajectory_point=='BOTTOM_RIGHT':
        x = pt2[0]
        y = pt2[1]
    elif trajectory_point=='CENTER':
        x = int((pt1[0]+pt2[0])/2)
        y = int((pt1[1]+pt2[1])/2)
    elif trajectory_point=='BOTTOM_CENTER':
        x = int((pt1[0]+pt2[0])/2)
        y = pt2[1]
    # # 紫色のBGR値を指定 (OpenCVではBGRの順序)
    # point_color = (255, 0, 255)
    # # 指定した座標に点を描画
    # cv2.circle(img, (x, y), 5, point_color, -1)  # 5は円の半径、-1は塗りつぶしを意味します
    return x, y

# 基準点がマスクエリア内かを判定
# in_out=-1なら範囲外なのでok, in_out=1ならマスク範囲内なので検出しない
def in_out_mask_check(masked_area, x, y):
    in_out = -1
    point_to_check = (int(x), int(y))
    for k in masked_area:
        point_inside_polygon = cv2.pointPolygonTest(k, point_to_check, measureDist=False)
        # 判定結果
        # if point_inside_polygon == 1:
        #     print("点は多角形の内部にあります。")
        # elif point_inside_polygon == 0:
        #     print("点は多角形の境界上にあります。")
        # else:
        #     print("点は多角形の外部にあります。")
        if point_inside_polygon == 1 or point_inside_polygon == 0:
            in_out = 1
            break
    
    return in_out


# ベクトルのなす角を計算（入力はどちらもnumpy形式で）
#ベクトルx1, x2から角度を計算する関数を定義
def angle_calc(x1, x2):
    cos_theta = np.dot(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))
    theta = np.arccos(cos_theta) * 180 / np.pi
    return theta


# 座標ptを変換行列Mで変換
def transform_pt(pt, M):
    if isinstance(pt, (list, tuple)):
        pt = np.array(pt, dtype=np.float32)
    assert pt.ndim == 1 and pt.shape[0] == 2 # 1次元のx,y2要素を前提
    pt = np.append(pt, 1.0)
    pt = np.dot(M, pt) # 射影行列で座標変換
    pt = pt / pt[2] # 第3要素が１となるよう按分
    pt = pt[:2] # x,y要素
    return tuple(pt.astype(int).tolist()) # 後でdrawMarkerで使うのでtupleにしておく



# 補正画像を使って，どの車線に属しているかを判定
def trans_lane_judgment(trans_pt, lane_border, car_flow):
    if car_flow==0:
        frag=0
        t0 = 0
        for j, k in enumerate(lane_border):
            t1 = k
            if t0<=trans_pt[0] and trans_pt[0]<=t1:
                in_out = j
                frag=1
                break
            t0 = k
        if frag==0:
            in_out = j+1
    else:
        frag=0
        t0 = 0
        for j, k in enumerate(lane_border):
            t1 = k
            if t0<=trans_pt[1] and trans_pt[1]<=t1:
                in_out = j
                frag=1
                break
            t0 = k
        if frag==0:
            in_out = j+1
    return in_out


# 補正画像を使って，どの車線に属しているかを判定
def trans_lane_judgment2(trans_pt, trans_lane_look, car_flow):
    in_out = -1
    point_inside_polygon = cv2.pointPolygonTest(trans_lane_look, trans_pt, measureDist=False)
    if point_inside_polygon == 1:    
        # 車が縦に動いているなら，x座標に注目すれば，車線がわかる
        if car_flow==0:
            in_out = trans_pt[0]//300
        else:
            in_out = trans_pt[1]//300
    return in_out



# 車線内の一番近いマイナスidを探してくる
# returnはインデックス値
def find_the_nearest_minus_id(id_lane, id_posi, new_ii, car_flow, matching_range):
    # [[ユークリッド距離, 0(index番号)],[ユークリッド距離, 1],...]
    distance_index = []
    for minus_idx, minus_id in enumerate(id_lane):
        if minus_id<0:
            #dist = np.linalg.norm(np.array(id_posi[new_ii]) - np.array(id_posi[minus_idx]))
            if car_flow==0:
                dist = abs(id_posi[minus_idx][1]-id_posi[new_ii][1])
            else:
                dist = abs(id_posi[minus_idx][0]-id_posi[new_ii][0])
            distance_index.append([dist, minus_idx])
    if len(distance_index)>0:
        distance_index.sort()
        #print(distance_index)
        if distance_index[0][0]<matching_range:
            nearest_minus_idx = distance_index[0][1]
        else:
            nearest_minus_idx = -1
        # この範囲内なら対応付ける
        # 範囲は一次元で判定
        # 車が縦に流れていたらy座標のみ注目
        # if car_flow==0:
        #     if abs(id_posi[new_ii][1] - id_posi[nearest_minus_idx][1])<matching_range:
        #         pass
        #     else:
        #         nearest_minus_idx = -1
        # else:
        #     if abs(id_posi[new_ii][0] - id_posi[nearest_minus_idx][0])<matching_range:
        #         pass
        #     else:
        #         nearest_minus_idx = -1
    else:
        nearest_minus_idx = -1

    return nearest_minus_idx

    


# 補正画像を作成し，出力画像とマージする
def merging_trans_image(frame_idx, img, id_lane, id_posi, prevented_switch_id, max_x, max_y, car_flow, lane_border, forward_back_car, head_direction, axis_visualization=False, trans_img_path='trans_img'):
    # 補正画像の元を作る
    trans_img = np.ones((int(max_y), int(max_x)), dtype=np.uint8)
    trans_img = cv2.cvtColor(trans_img, cv2.COLOR_BGR2RGB)

    # 車線に線を引く
    if car_flow==0:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(i, 0),
                pt2=(i, int(max_y)),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
    else:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(0, i),
                pt2=(int(max_x), i),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
            
    # 枠線を作る
    cv2.rectangle(trans_img, (10,10), (int(max_x)-10,int(max_y)-10), (255, 255, 255), thickness=30, lineType=cv2.LINE_8, shift=0)

    #cv2.imwrite('trans_img.jpg', trans_img)

    # 元画像での畳四隅座標を射影変換し鳥瞰画像にマーキング
    # for src_pt in pts1:
    #     dst_pt = transform_pt(src_pt, M)
    #     cv2.drawMarker(img3, dst_pt, (0, 255, 0), markerSize=20)
        
    # 補正画像に位置をマーキング
    # その上にidを表示
    # bbox作った時の位置を保存（車が縦に動く場合(car_flow=0)はtopとbottom, 車が横に動く場合(car_flow=1)はrightとleftを保存）
    # {id: [topまたはleft, bottomまたはright]}
    bbox_posi = {}
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
            # idが正なら緑，ただし，bbox補完で付け替えたidは水色
            if id_lane[i][j]>0:
                if id_lane[i][j] not in prevented_switch_id:
                    color_num = (50, 205, 154)
                else:
                    #color_num = (255,204,0)
                    color_num = (255, 191, 0)
            # マイナスidなら赤
            else:
                color_num = (0,0,255)
            # trans_img = cv2.circle(trans_img, (int(posi[0]),int(posi[1])), 100, color_num, -1)
            # 正方形を描画
            x, y = int(posi[0]), int(posi[1])
            square_size = 340
            a = x - square_size // 2
            b = y - square_size // 2
            c = x + square_size // 2
            d = y + square_size // 2
            top_left = (a, b)
            bottom_right = (c, d)
            if car_flow==0:
                bbox_posi[id_lane[i][j]] = [(x, b), (x, d)]
            else:
                bbox_posi[id_lane[i][j]] = [(a, y), (c, y)]
            cv2.rectangle(trans_img, top_left, bottom_right, color=color_num, thickness=30)
            # trans_img = cv2.circle(trans_img, (posi[0],posi[1]), 140, color_num, -1)
            cv2.putText(trans_img,
                text=str(id_lane[i][j]),
                org=(int(posi[0])-90,int(posi[1])+50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=3.5,
                color=(255,255,255),
                thickness=14,
                lineType=cv2.LINE_4)
        

    # マイナスidについて，前後の車に矢印を引く
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
            # 位置予測する時に参考にした前後の車がわかるように前後のidのbboxに矢印を描画
            if id_lane[i][j]<0:
                forward_car = forward_back_car[id_lane[i][j]][0]
                back_car = forward_back_car[id_lane[i][j]][1]
                # 前の車に引く矢印
                if forward_car:
                    if head_direction=='down':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[forward_car][0], (255,211,51), thickness=30, tipLength=0.1)
                    elif head_direction=='up':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[forward_car][1], (255,211,51), thickness=30, tipLength=0.1)
                    elif head_direction=='right':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[forward_car][0], (255,211,51), thickness=30, tipLength=0.1)
                    else:
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[forward_car][1], (255,211,51), thickness=30, tipLength=0.1)
                if back_car:
                    if head_direction=='down':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[back_car][1], (51,197,255), thickness=30, tipLength=0.1)
                    elif head_direction=='up':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[back_car][0], (51,197,255), thickness=30, tipLength=0.1)
                    elif head_direction=='right':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[back_car][1], (51,197,255), thickness=30, tipLength=0.1)
                    else:
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[back_car][0], (51,197,255), thickness=30, tipLength=0.1)


    # plt.figure(figsize=(10,10), facecolor='w', dpi=150)
    # plt.imshow(trans_img)
    # plt.savefig(trans_img_path,bbox_inches="tight")
    # plt.clf()
    if axis_visualization=='True':
        plt.figure(figsize=(8,8), facecolor='w')
        plt.imshow(trans_img)
        trans_img_path = trans_img_path+'/'+str(frame_idx)+'.jpg'
        plt.savefig(trans_img_path,bbox_inches="tight")
        plt.clf()

    # 補正画像と出力画像をマージ
    # 車が縦に流れる場合は，出力画像の右にマージする
    #img1 = cv2.imread('00460.jpg') # 出力画像
    #img2 = cv2.imread(trans_img_path) # 補正画像
    
    h1, w1, _ = img.shape # 出力画像
    h2, w2, _ = trans_img.shape # 補正画像

    new_h = h1
    aspect_ratio = float(w2) / float(h2)
    new_w = int(new_h * aspect_ratio)

    resized_bird_img = cv2.resize(trans_img, (new_w, new_h))

    #cv2.imwrite('resized_bird_img.jpg', resized_bird_img)

    # 画像を横に結合
    merged_image = np.hstack((img, resized_bird_img))

    # 画像の表示
    # plt.imshow(merged_image)
    # plt.show()
    # 保存はここでやらなくていい
    # cv2.imwrite('merged_image2.png', merged_image)
    return merged_image


# 縦移動・横移動共に制限
# 補正画像を作成し，出力画像とマージする
def merging_trans_image2(img, id_lane, id_posi, prevented_switch_id, max_x, max_y, car_flow, lane_border, forward_back_car, head_direction, lane_width, axis_visualization=False, trans_img_path='trans_image.jpg'):

    lane_num = len(id_lane)

    # 補正画像の元を作る
    # 1車線を500pixとする
    if car_flow==0:
        trans_img = np.ones((int(max_y), lane_width*lane_num), dtype=np.uint8)
    else:
        trans_img = np.ones((lane_width*lane_num, int(max_x)), dtype=np.uint8)
    trans_img = cv2.cvtColor(trans_img, cv2.COLOR_BGR2RGB)

    # 車線に線を引く
    if car_flow==0:
        for i in range(lane_num):
            cv2.line(trans_img,
                pt1=(lane_width*i, 0),
                pt2=(lane_width*i, int(max_y)),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
    else:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(0, lane_width*i),
                pt2=(int(max_x), lane_width*i),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
            
    # 枠線を作る
    if car_flow==0:
        cv2.rectangle(trans_img, (10,10), (lane_width*lane_num-10,int(max_y)-10), (255, 255, 255), thickness=30, lineType=cv2.LINE_8, shift=0)

    #cv2.imwrite('trans_img.jpg', trans_img)

    # 元画像での畳四隅座標を射影変換し鳥瞰画像にマーキング
    # for src_pt in pts1:
    #     dst_pt = transform_pt(src_pt, M)
    #     cv2.drawMarker(img3, dst_pt, (0, 255, 0), markerSize=20)
        
    # 補正画像に位置をマーキング
    # その上にidを表示
    # bbox作った時の位置を保存（車が縦に動く場合(car_flow=0)はtopとbottom, 車が横に動く場合(car_flow=1)はrightとleftを保存）
    # {id: [topまたはleft, bottomまたはright]}
    bbox_posi = {}
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
            # idが正なら緑，ただし，bbox補完で付け替えたidは水色
            if id_lane[i][j]>0:
                if id_lane[i][j] not in prevented_switch_id:
                    color_num = (50, 205, 154)
                else:
                    #color_num = (255,204,0)
                    color_num = (255, 191, 0)
            # マイナスidなら赤
            else:
                color_num = (0,0,255)
            # trans_img = cv2.circle(trans_img, (int(posi[0]),int(posi[1])), 100, color_num, -1)
            # 正方形を描画
            # その前に，
            # 車が縦に流れる場合，x軸の位置も固定してしまう（y軸に関しては逆走不可の制約をかける）
            # 車が横に流れる場合，y軸の位置も固定してしまう
            if car_flow==0:
                x, y = lane_width//2 + (lane_width*i), int(posi[1])
            else:
                x, y = int(posi[0]), lane_width//2 + (lane_width*i)


            square_size = 340
            a = x - square_size // 2
            b = y - square_size // 2
            c = x + square_size // 2
            d = y + square_size // 2
            top_left = (a, b)
            bottom_right = (c, d)
            if car_flow==0:
                bbox_posi[id_lane[i][j]] = [(x, b), (x, d)]
            else:
                bbox_posi[id_lane[i][j]] = [(a, y), (c, y)]
            cv2.rectangle(trans_img, top_left, bottom_right, color=color_num, thickness=30)
            # trans_img = cv2.circle(trans_img, (posi[0],posi[1]), 140, color_num, -1)
            if car_flow==0:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(lane_width//2+(lane_width*i)-90,int(posi[1])+50),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=3.5,
                    color=(255,255,255),
                    thickness=14,
                    lineType=cv2.LINE_4)
            else:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])-90,lane_width//2+(lane_width*i)+50),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=3.5,
                    color=(255,255,255),
                    thickness=14,
                    lineType=cv2.LINE_4)   
        

    # マイナスidについて，前後の車に矢印を引く
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
            # 位置予測する時に参考にした前後の車がわかるように前後のidのbboxに矢印を描画
            if id_lane[i][j]<0:
                forward_car = forward_back_car[id_lane[i][j]][0]
                back_car = forward_back_car[id_lane[i][j]][1]
                # 前の車に引く矢印
                if forward_car:
                    if head_direction=='down':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[forward_car][0], (255,211,51), thickness=30, tipLength=0.1)
                    elif head_direction=='up':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[forward_car][1], (255,211,51), thickness=30, tipLength=0.1)
                    elif head_direction=='right':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[forward_car][0], (255,211,51), thickness=30, tipLength=0.1)
                    else:
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[forward_car][1], (255,211,51), thickness=30, tipLength=0.1)
                if back_car:
                    if head_direction=='down':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[back_car][1], (51,197,255), thickness=30, tipLength=0.1)
                    elif head_direction=='up':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[back_car][0], (51,197,255), thickness=30, tipLength=0.1)
                    elif head_direction=='right':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[back_car][1], (51,197,255), thickness=30, tipLength=0.1)
                    else:
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[back_car][0], (51,197,255), thickness=30, tipLength=0.1)


    # plt.figure(figsize=(10,10), facecolor='w', dpi=150)
    # plt.imshow(trans_img)
    # plt.savefig(trans_img_path,bbox_inches="tight")
    # plt.clf()
    if axis_visualization=='True':
        plt.figure(figsize=(8,8), facecolor='w')
        plt.imshow(trans_img)
        plt.savefig(trans_img_path,bbox_inches="tight")
        plt.clf()

    # 補正画像と出力画像をマージ
    # 車が縦に流れる場合は，出力画像の右にマージする
    #img1 = cv2.imread('00460.jpg') # 出力画像
    #img2 = cv2.imread(trans_img_path) # 補正画像
    
    h1, w1, _ = img.shape # 出力画像
    h2, w2, _ = trans_img.shape # 補正画像

    new_h = h1
    aspect_ratio = float(w2) / float(h2)
    new_w = int(new_h * aspect_ratio)

    resized_bird_img = cv2.resize(trans_img, (new_w, new_h))

    #cv2.imwrite('resized_bird_img.jpg', resized_bird_img)

    # 画像を横に結合
    merged_image = np.hstack((img, resized_bird_img))

    # 画像の表示
    # plt.imshow(merged_image)
    # plt.show()
    # 保存はここでやらなくていい
    # cv2.imwrite('merged_image2.png', merged_image)
    return merged_image


# 補正画像と，何も検出されなかった出力画像をマージする
def merging_trans_image_0(img, id_lane, max_x, max_y, car_flow, lane_border, head_direction, lane_width, axis_visualization=False, trans_img_path='trans_image.jpg'):

    lane_num = len(id_lane)

    # 補正画像の元を作る
    # 1車線を500pixとする
    if car_flow==0:
        trans_img = np.ones((int(max_y), lane_width*lane_num), dtype=np.uint8)
    else:
        trans_img = np.ones((lane_width*lane_num, int(max_x)), dtype=np.uint8)
    trans_img = cv2.cvtColor(trans_img, cv2.COLOR_BGR2RGB)

    # 車線に線を引く
    if car_flow==0:
        for i in range(lane_num):
            cv2.line(trans_img,
                pt1=(lane_width*i, 0),
                pt2=(lane_width*i, int(max_y)),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
    else:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(0, lane_width*i),
                pt2=(int(max_x), lane_width*i),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
            
    # 枠線を作る
    if car_flow==0:
        cv2.rectangle(trans_img, (10,10), (lane_width*lane_num-10,int(max_y)-10), (255, 255, 255), thickness=30, lineType=cv2.LINE_8, shift=0)

    #cv2.imwrite('trans_img.jpg', trans_img)

    # 元画像での畳四隅座標を射影変換し鳥瞰画像にマーキング
    # for src_pt in pts1:
    #     dst_pt = transform_pt(src_pt, M)
    #     cv2.drawMarker(img3, dst_pt, (0, 255, 0), markerSize=20)

    # 補正画像と出力画像をマージ
    # 車が縦に流れる場合は，出力画像の右にマージする
    #img1 = cv2.imread('00460.jpg') # 出力画像
    #img2 = cv2.imread(trans_img_path) # 補正画像
    
    h1, w1, _ = img.shape # 出力画像
    h2, w2, _ = trans_img.shape # 補正画像

    new_h = h1
    aspect_ratio = float(w2) / float(h2)
    new_w = int(new_h * aspect_ratio)

    resized_bird_img = cv2.resize(trans_img, (new_w, new_h))

    #cv2.imwrite('resized_bird_img.jpg', resized_bird_img)

    # 画像を横に結合
    merged_image = np.hstack((img, resized_bird_img))

    # 画像の表示
    # plt.imshow(merged_image)
    # plt.show()
    # 保存はここでやらなくていい
    # cv2.imwrite('merged_image2.png', merged_image)
    return merged_image

# 補正画像を作成し，出力画像とマージする
def merging_trans_image3(img, id_lane, id_posi, prevented_switch_id, max_x, max_y, car_flow, lane_border, forward_back_car, head_direction, trans_lane, trans_lane_look):
    # 補正画像の元を作る
    trans_img = np.ones((int(max_y), int(max_x)), dtype=np.uint8)
    trans_img = cv2.cvtColor(trans_img, cv2.COLOR_BGR2RGB)

    # 車線に線を引く
    if car_flow==0:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(i, 0),
                pt2=(i, int(max_y)),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
    else:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(0, i),
                pt2=(int(max_x), i),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
            
    # 枠線を作る
    cv2.rectangle(trans_img, (10,10), (int(max_x)-10,int(max_y)-10), (255, 255, 255), thickness=30, lineType=cv2.LINE_8, shift=0)

    # 射影変換する際に用いた鳥瞰画像における黄色いエリア
    cv2.rectangle(trans_img, trans_lane[0].astype(int)-5, trans_lane[2].astype(int)-5, (24, 235, 249), thickness=20, lineType=cv2.LINE_8, shift=0)
    # 全体の検出エリア
    cv2.polylines(trans_img, [trans_lane_look.astype(int)], isClosed=True, color=(255,0,255), thickness=20)


    #cv2.imwrite('trans_img.jpg', trans_img)

    # 元画像での畳四隅座標を射影変換し鳥瞰画像にマーキング
    # for src_pt in pts1:
    #     dst_pt = transform_pt(src_pt, M)
    #     cv2.drawMarker(img3, dst_pt, (0, 255, 0), markerSize=20)
        
    # 補正画像に位置をマーキング
    # その上にidを表示
    # bbox作った時の位置を保存（車が縦に動く場合(car_flow=0)はtopとbottom, 車が横に動く場合(car_flow=1)はrightとleftを保存）
    # {id: [topまたはleft, bottomまたはright]}
    bbox_posi = {}
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
            # idが正なら緑，ただし，bbox補完で付け替えたidは水色
            if id_lane[i][j]>0:
                if id_lane[i][j] not in prevented_switch_id:
                    color_num = (50, 205, 154)
                else:
                    #color_num = (255,204,0)
                    color_num = (255, 191, 0)
            # マイナスidなら赤
            else:
                color_num = (0,0,255)
            # trans_img = cv2.circle(trans_img, (int(posi[0]),int(posi[1])), 100, color_num, -1)
            # 正方形を描画
            x, y = int(posi[0]), int(posi[1])
            square_size = 340
            a = x - square_size // 2
            b = y - square_size // 2
            c = x + square_size // 2
            d = y + square_size // 2
            top_left = (a, b)
            bottom_right = (c, d)
            if car_flow==0:
                bbox_posi[id_lane[i][j]] = [(x, b), (x, d)]
            else:
                bbox_posi[id_lane[i][j]] = [(a, y), (c, y)]
            cv2.rectangle(trans_img, top_left, bottom_right, color=color_num, thickness=30)
            # trans_img = cv2.circle(trans_img, (posi[0],posi[1]), 140, color_num, -1)
            cv2.putText(trans_img,
                text=str(id_lane[i][j]),
                org=(int(posi[0])-90,int(posi[1])+50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=3.5,
                color=(255,255,255),
                thickness=14,
                lineType=cv2.LINE_4)
        

    # マイナスidについて，前後の車に矢印を引く
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
            # 位置予測する時に参考にした前後の車がわかるように前後のidのbboxに矢印を描画
            if id_lane[i][j]<0:
                forward_car = forward_back_car[id_lane[i][j]][0]
                back_car = forward_back_car[id_lane[i][j]][1]
                # 前の車に引く矢印
                if forward_car:
                    if head_direction=='down':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[forward_car][0], (255,211,51), thickness=30, tipLength=0.1)
                    elif head_direction=='up':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[forward_car][1], (255,211,51), thickness=30, tipLength=0.1)
                    elif head_direction=='right':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[forward_car][0], (255,211,51), thickness=30, tipLength=0.1)
                    else:
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[forward_car][1], (255,211,51), thickness=30, tipLength=0.1)
                if back_car:
                    if head_direction=='down':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[back_car][1], (51,197,255), thickness=30, tipLength=0.1)
                    elif head_direction=='up':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[back_car][0], (51,197,255), thickness=30, tipLength=0.1)
                    elif head_direction=='right':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[back_car][1], (51,197,255), thickness=30, tipLength=0.1)
                    else:
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[back_car][0], (51,197,255), thickness=30, tipLength=0.1)

    # 補正画像と出力画像をマージ
    # 車が縦に流れる場合は，出力画像の右にマージする
    #img1 = cv2.imread('00460.jpg') # 出力画像
    #img2 = cv2.imread(trans_img_path) # 補正画像
    
    h1, w1, _ = img.shape # 出力画像
    h2, w2, _ = trans_img.shape # 補正画像

    new_h = h1
    aspect_ratio = float(w2) / float(h2)
    new_w = int(new_h * aspect_ratio)

    resized_bird_img = cv2.resize(trans_img, (new_w, new_h))

    #cv2.imwrite('resized_bird_img.jpg', resized_bird_img)

    # 画像を横に結合
    merged_image = np.hstack((img, resized_bird_img))

    # 画像の表示
    # plt.imshow(merged_image)
    # plt.show()
    # 保存はここでやらなくていい
    # cv2.imwrite('merged_image2.png', merged_image)
    return merged_image



# 補正画像を作成し，出力画像とマージする
def merging_trans_image4(frame_idx, img, id_lane, id_posi, prevented_switch_id, max_x, max_y, car_flow, lane_border, forward_back_car, head_direction, trans_lane, trans_lane_look):
    # 補正画像の元を作る
    trans_img = np.ones((int(max_y), int(max_x)*2), dtype=np.uint8)
    trans_img = cv2.cvtColor(trans_img, cv2.COLOR_BGR2RGB)

    # 車線に線を引く
    if car_flow==0:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(i*2, 0),
                pt2=(i*2, int(max_y)),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
    else:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(0, i),
                pt2=(int(max_x), i),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
            
    # 枠線を作る
    cv2.rectangle(trans_img, (10,10), (int(max_x)*2-10,int(max_y)-10), (255, 255, 255), thickness=30, lineType=cv2.LINE_8, shift=0)

    # 射影変換する際に用いた鳥瞰画像における黄色いエリア
    #cv2.rectangle(trans_img, trans_lane[0].astype(int)-5, trans_lane[2].astype(int)-5, (24, 235, 249), thickness=20, lineType=cv2.LINE_8, shift=0)
    # 全体の検出エリア
    #cv2.polylines(trans_img, [trans_lane_look.astype(int)], isClosed=True, color=(255,0,255), thickness=20)


    #cv2.imwrite('trans_img.jpg', trans_img)

    # 元画像での畳四隅座標を射影変換し鳥瞰画像にマーキング
    # for src_pt in pts1:
    #     dst_pt = transform_pt(src_pt, M)
    #     cv2.drawMarker(img3, dst_pt, (0, 255, 0), markerSize=20)
        
    # 補正画像に位置をマーキング
    # その上にidを表示
    # bbox作った時の位置を保存（車が縦に動く場合(car_flow=0)はtopとbottom, 車が横に動く場合(car_flow=1)はrightとleftを保存）
    # {id: [topまたはleft, bottomまたはright]}
    bbox_posi = {}
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
            if id_lane[i][j]==-4:
                continue
            # idが正なら緑，ただし，bbox補完で付け替えたidは水色
            if id_lane[i][j]>0:
                if id_lane[i][j] not in prevented_switch_id or id_lane[i][j]==4 or id_lane[i][j]==8:
                    color_num = (50, 205, 154)
                else:
                    #color_num = (255,204,0)
                    color_num = (255, 191, 0)
            # マイナスidなら赤
            else:
                color_num = (0,0,255)
            # trans_img = cv2.circle(trans_img, (int(posi[0]),int(posi[1])), 100, color_num, -1)
            # 正方形を描画
            if id_lane[i][j]==2:
                x, y = int(posi[0])*2-70, int(posi[1])
            # elif id_lane[i][j]==-14:
            #     x, y = int(posi[0])*2+50, int(posi[1])
            else:
                x, y = int(posi[0])*2, int(posi[1])
            square_size = 340
            a = x - square_size // 2
            b = y - square_size // 2
            c = x + square_size // 2
            d = y + square_size // 2
            top_left = (a, b)
            bottom_right = (c, d)
            if car_flow==0:
                bbox_posi[id_lane[i][j]] = [(x, b), (x, d)]
            else:
                bbox_posi[id_lane[i][j]] = [(a, y), (c, y)]
            cv2.rectangle(trans_img, top_left, bottom_right, color=color_num, thickness=30)
            # trans_img = cv2.circle(trans_img, (posi[0],posi[1]), 140, color_num, -1)
            if id_lane[i][j]==2:
                cv2.putText(trans_img,
                    text=str(3),
                    org=(int(posi[0])*2-140,int(posi[1])+70),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=7,
                    color=(255,255,255),
                    thickness=24,
                    lineType=cv2.LINE_4)
            elif id_lane[i][j]==3:
                cv2.putText(trans_img,
                    text=str(2),
                    org=(int(posi[0])*2-70,int(posi[1])+70),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=7,
                    color=(255,255,255),
                    thickness=24,
                    lineType=cv2.LINE_4)
            elif 0<id_lane[i][j] and id_lane[i][j]<10:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-70,int(posi[1])+70),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=7,
                    color=(255,255,255),
                    thickness=24,
                    lineType=cv2.LINE_4)
            elif id_lane[i][j]==-14:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-145,int(posi[1])+55),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=4.5,
                    color=(255,255,255),
                    thickness=22,
                    lineType=cv2.LINE_4)
            elif id_lane[i][j]==-16:
                cv2.putText(trans_img,
                    text=str(-16),
                    org=(int(posi[0])*2-145,int(posi[1])+55),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=4.5,
                    color=(255,255,255),
                    thickness=22,
                    lineType=cv2.LINE_4)
            elif id_lane[i][j]==-10:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-145,int(posi[1])+55),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=4.5,
                    color=(255,255,255),
                    thickness=22,
                    lineType=cv2.LINE_4)
            elif id_lane[i][j]==-22:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-145,int(posi[1])+55),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=4.5,
                    color=(255,255,255),
                    thickness=22,
                    lineType=cv2.LINE_4)
            elif id_lane[i][j]==11:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-140,int(posi[1])+70),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=7,
                    color=(255,255,255),
                    thickness=24,
                    lineType=cv2.LINE_4)
            elif id_lane[i][j]==14:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-140,int(posi[1])+70),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=7,
                    color=(255,255,255),
                    thickness=24,
                    lineType=cv2.LINE_4)
            else:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-145,int(posi[1])+70),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=7,
                    color=(255,255,255),
                    thickness=24,
                    lineType=cv2.LINE_4)
        

    # マイナスidについて，前後の車に矢印を引く
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
            if id_lane[i][j]==-4:
                continue
            # 位置予測する時に参考にした前後の車がわかるように前後のidのbboxに矢印を描画
            if id_lane[i][j]<0:
                forward_car = forward_back_car[id_lane[i][j]][0]
                back_car = forward_back_car[id_lane[i][j]][1]
                # 前の車に引く矢印
                if forward_car:
                    if head_direction=='down':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[forward_car][0], (255,211,51), thickness=30, tipLength=0.1)
                    elif head_direction=='up':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[forward_car][1], (255,211,51), thickness=30, tipLength=0.1)
                    elif head_direction=='right':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[forward_car][0], (255,211,51), thickness=30, tipLength=0.1)
                    else:
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[forward_car][1], (255,211,51), thickness=30, tipLength=0.1)
                if back_car:
                    if head_direction=='down':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[back_car][1], (51,197,255), thickness=30, tipLength=0.1)
                    elif head_direction=='up':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[back_car][0], (51,197,255), thickness=30, tipLength=0.1)
                    elif head_direction=='right':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[back_car][1], (51,197,255), thickness=30, tipLength=0.1)
                    else:
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[back_car][0], (51,197,255), thickness=30, tipLength=0.1)

    # 補正画像と出力画像をマージ
    # 車が縦に流れる場合は，出力画像の右にマージする
    #img1 = cv2.imread('00460.jpg') # 出力画像
    #img2 = cv2.imread(trans_img_path) # 補正画像
                        
    if frame_idx==1:
        cv2.imwrite('trans_img1.jpg', trans_img)
        cv2.imwrite('img1.jpg', img)
    if frame_idx==2:
        cv2.imwrite('trans_img2.jpg', trans_img)
        cv2.imwrite('img2.jpg', img)
    # if frame_idx==816:
    #     cv2.imwrite('trans_img816.jpg', trans_img)
    #     cv2.imwrite('img816.jpg', img)

    h1, w1, _ = img.shape # 出力画像
    h2, w2, _ = trans_img.shape # 補正画像

    new_h = h1
    aspect_ratio = float(w2) / float(h2)
    new_w = int(new_h * aspect_ratio)

    resized_bird_img = cv2.resize(trans_img, (new_w, new_h))

    #cv2.imwrite('resized_bird_img.jpg', resized_bird_img)

    # 画像を横に結合
    merged_image = np.hstack((img, resized_bird_img))

    # if frame_idx==276:
    #     cv2.imwrite('merged_image276.jpg', merged_image)
    # if frame_idx==285:
    #     cv2.imwrite('merged_image285.jpg', merged_image)

    # 画像の表示
    # plt.imshow(merged_image)
    # plt.show()
    # 保存はここでやらなくていい
    # cv2.imwrite('merged_image2.png', merged_image)
    return merged_image


# 補正画像を作成し，出力画像とマージする
# id指定なし
def merging_trans_image5(frame_idx, img, id_lane, id_posi, prevented_switch_id, max_x, max_y, car_flow, lane_border, forward_back_car, head_direction, trans_lane, trans_lane_look):
    # 補正画像の元を作る
    trans_img = np.ones((int(max_y), int(max_x)*2), dtype=np.uint8)
    trans_img = cv2.cvtColor(trans_img, cv2.COLOR_BGR2RGB)

    # 車線に線を引く
    if car_flow==0:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(i*2, 0),
                pt2=(i*2, int(max_y)),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
    else:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(0, i),
                pt2=(int(max_x), i),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
            
    # 枠線を作る
    cv2.rectangle(trans_img, (10,10), (int(max_x)*2-10,int(max_y)-10), (255, 255, 255), thickness=30, lineType=cv2.LINE_8, shift=0)

    # 射影変換する際に用いた鳥瞰画像における黄色いエリア
    #cv2.rectangle(trans_img, trans_lane[0].astype(int)-5, trans_lane[2].astype(int)-5, (24, 235, 249), thickness=20, lineType=cv2.LINE_8, shift=0)
    # 全体の検出エリア
    #cv2.polylines(trans_img, [trans_lane_look.astype(int)], isClosed=True, color=(255,0,255), thickness=20)


    #cv2.imwrite('trans_img.jpg', trans_img)

    # 元画像での畳四隅座標を射影変換し鳥瞰画像にマーキング
    # for src_pt in pts1:
    #     dst_pt = transform_pt(src_pt, M)
    #     cv2.drawMarker(img3, dst_pt, (0, 255, 0), markerSize=20)
        
    # 補正画像に位置をマーキング
    # その上にidを表示
    # bbox作った時の位置を保存（車が縦に動く場合(car_flow=0)はtopとbottom, 車が横に動く場合(car_flow=1)はrightとleftを保存）
    # {id: [topまたはleft, bottomまたはright]}
    bbox_posi = {}
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
            # idが正なら緑，ただし，bbox補完で付け替えたidは水色
            if id_lane[i][j]>0:
                if id_lane[i][j] not in prevented_switch_id or id_lane[i][j]==4 or id_lane[i][j]==8:
                    color_num = (50, 205, 154)
                else:
                    #color_num = (255,204,0)
                    color_num = (255, 191, 0)
            # マイナスidなら赤
            else:
                color_num = (0,0,255)
            # trans_img = cv2.circle(trans_img, (int(posi[0]),int(posi[1])), 100, color_num, -1)
            # 正方形を描画
            x, y = int(posi[0])*2, int(posi[1])
            
            square_size = 340
            a = x - square_size // 2
            b = y - square_size // 2
            c = x + square_size // 2
            d = y + square_size // 2
            top_left = (a, b)
            bottom_right = (c, d)
            if car_flow==0:
                bbox_posi[id_lane[i][j]] = [(x, b), (x, d)]
            else:
                bbox_posi[id_lane[i][j]] = [(a, y), (c, y)]
            cv2.rectangle(trans_img, top_left, bottom_right, color=color_num, thickness=30)
            # trans_img = cv2.circle(trans_img, (posi[0],posi[1]), 140, color_num, -1)
            
            if 0<id_lane[i][j] and id_lane[i][j]<10:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-70,int(posi[1])+70),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=7,
                    color=(255,255,255),
                    thickness=24,
                    lineType=cv2.LINE_4)
            else:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-145,int(posi[1])+70),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=7,
                    color=(255,255,255),
                    thickness=24,
                    lineType=cv2.LINE_4)
        

    # マイナスidについて，前後の車に矢印を引く
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
    
            # 位置予測する時に参考にした前後の車がわかるように前後のidのbboxに矢印を描画
            if id_lane[i][j]<0:
                forward_car = forward_back_car[id_lane[i][j]][0]
                back_car = forward_back_car[id_lane[i][j]][1]
                # 前の車に引く矢印
                if forward_car:
                    if head_direction=='down':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[forward_car][0], (255,211,51), thickness=30, tipLength=0.1)
                    elif head_direction=='up':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[forward_car][1], (255,211,51), thickness=30, tipLength=0.1)
                    elif head_direction=='right':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[forward_car][0], (255,211,51), thickness=30, tipLength=0.1)
                    else:
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[forward_car][1], (255,211,51), thickness=30, tipLength=0.1)
                if back_car:
                    if head_direction=='down':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[back_car][1], (51,197,255), thickness=30, tipLength=0.1)
                    elif head_direction=='up':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[back_car][0], (51,197,255), thickness=30, tipLength=0.1)
                    elif head_direction=='right':
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][0], bbox_posi[back_car][1], (51,197,255), thickness=30, tipLength=0.1)
                    else:
                        cv2.arrowedLine(trans_img, bbox_posi[id_lane[i][j]][1], bbox_posi[back_car][0], (51,197,255), thickness=30, tipLength=0.1)

    # 補正画像と出力画像をマージ
    # 車が縦に流れる場合は，出力画像の右にマージする
    #img1 = cv2.imread('00460.jpg') # 出力画像
    #img2 = cv2.imread(trans_img_path) # 補正画像

    # if frame_idx==816:
    #     cv2.imwrite('trans_img816.jpg', trans_img)
    #     cv2.imwrite('img816.jpg', img)

    h1, w1, _ = img.shape # 出力画像
    h2, w2, _ = trans_img.shape # 補正画像

    new_h = h1
    aspect_ratio = float(w2) / float(h2)
    new_w = int(new_h * aspect_ratio)

    resized_bird_img = cv2.resize(trans_img, (new_w, new_h))

    #cv2.imwrite('resized_bird_img.jpg', resized_bird_img)

    # 画像を横に結合
    merged_image = np.hstack((img, resized_bird_img))

    # if frame_idx==276:
    #     cv2.imwrite('merged_image276.jpg', merged_image)
    # if frame_idx==285:
    #     cv2.imwrite('merged_image285.jpg', merged_image)

    # 画像の表示
    # plt.imshow(merged_image)
    # plt.show()
    # 保存はここでやらなくていい
    # cv2.imwrite('merged_image2.png', merged_image)
    return merged_image


# 補正画像を作成し，出力画像とマージする
# これは鳥瞰画像に矢印つけないver
def merging_trans_image6(frame_idx, img, id_lane, id_posi, prevented_switch_id, max_x, max_y, car_flow, lane_border, forward_back_car, head_direction, trans_lane, trans_lane_look):
    # 補正画像の元を作る
    trans_img = np.ones((int(max_y), int(max_x)*2), dtype=np.uint8)
    trans_img = cv2.cvtColor(trans_img, cv2.COLOR_BGR2RGB)

    # 車線に線を引く
    if car_flow==0:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(i*2, 0),
                pt2=(i*2, int(max_y)),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
    else:
        for i in lane_border:
            cv2.line(trans_img,
                pt1=(0, i),
                pt2=(int(max_x), i),
                color=(255, 255, 255),
                thickness=30,
                lineType=cv2.LINE_4,
                shift=0)
            
    # 枠線を作る
    cv2.rectangle(trans_img, (10,10), (int(max_x)*2-10,int(max_y)-10), (255, 255, 255), thickness=30, lineType=cv2.LINE_8, shift=0)

    # 射影変換する際に用いた鳥瞰画像における黄色いエリア
    #cv2.rectangle(trans_img, trans_lane[0].astype(int)-5, trans_lane[2].astype(int)-5, (24, 235, 249), thickness=20, lineType=cv2.LINE_8, shift=0)
    # 全体の検出エリア
    #cv2.polylines(trans_img, [trans_lane_look.astype(int)], isClosed=True, color=(255,0,255), thickness=20)


    #cv2.imwrite('trans_img.jpg', trans_img)

    # 元画像での畳四隅座標を射影変換し鳥瞰画像にマーキング
    # for src_pt in pts1:
    #     dst_pt = transform_pt(src_pt, M)
    #     cv2.drawMarker(img3, dst_pt, (0, 255, 0), markerSize=20)
        
    # 補正画像に位置をマーキング
    # その上にidを表示
    # bbox作った時の位置を保存（車が縦に動く場合(car_flow=0)はtopとbottom, 車が横に動く場合(car_flow=1)はrightとleftを保存）
    # {id: [topまたはleft, bottomまたはright]}
    bbox_posi = {}
    for i, trans_posi in enumerate(id_posi):
        for j, posi in enumerate(trans_posi):
            # idが正なら緑，ただし，bbox補完で付け替えたidは水色
            if id_lane[i][j]>0:
                if id_lane[i][j] not in prevented_switch_id or id_lane[i][j]==4 or id_lane[i][j]==8:
                    color_num = (50, 205, 154)
                else:
                    #color_num = (255,204,0)
                    color_num = (255, 191, 0)
            # マイナスidなら赤
            else:
                color_num = (0,0,255)
            # trans_img = cv2.circle(trans_img, (int(posi[0]),int(posi[1])), 100, color_num, -1)
            # 正方形を描画
            x, y = int(posi[0])*2, int(posi[1])
            
            square_size = 340
            a = x - square_size // 2
            b = y - square_size // 2
            c = x + square_size // 2
            d = y + square_size // 2
            top_left = (a, b)
            bottom_right = (c, d)
            if car_flow==0:
                bbox_posi[id_lane[i][j]] = [(x, b), (x, d)]
            else:
                bbox_posi[id_lane[i][j]] = [(a, y), (c, y)]
            cv2.rectangle(trans_img, top_left, bottom_right, color=color_num, thickness=30)
            # trans_img = cv2.circle(trans_img, (posi[0],posi[1]), 140, color_num, -1)
            
            if 0<id_lane[i][j] and id_lane[i][j]<10:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-70,int(posi[1])+70),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=7,
                    color=(255,255,255),
                    thickness=24,
                    lineType=cv2.LINE_4)
            else:
                cv2.putText(trans_img,
                    text=str(id_lane[i][j]),
                    org=(int(posi[0])*2-145,int(posi[1])+70),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=7,
                    color=(255,255,255),
                    thickness=24,
                    lineType=cv2.LINE_4)

    h1, w1, _ = img.shape # 出力画像
    h2, w2, _ = trans_img.shape # 補正画像

    new_h = h1
    aspect_ratio = float(w2) / float(h2)
    new_w = int(new_h * aspect_ratio)

    resized_bird_img = cv2.resize(trans_img, (new_w, new_h))

    #cv2.imwrite('resized_bird_img.jpg', resized_bird_img)

    # 画像を横に結合
    merged_image = np.hstack((img, resized_bird_img))

    # if frame_idx==276:
    #     cv2.imwrite('merged_image276.jpg', merged_image)
    # if frame_idx==285:
    #     cv2.imwrite('merged_image285.jpg', merged_image)

    # 画像の表示
    # plt.imshow(merged_image)
    # plt.show()
    # 保存はここでやらなくていい
    # cv2.imwrite('merged_image2.png', merged_image)
    return merged_image





def point_slide_to_center(trans_pt, class_name, car_flow, trajectory_point):
    if car_flow==0 and trajectory_point=='BOTTOM_RIGHT':
        trans_pt = list(trans_pt)
        if class_name=='car':
            trans_pt[0]-=85
        else:
            trans_pt[0]-=105
    elif car_flow==0 and trajectory_point=='BOTTOM_LEFT':
        trans_pt = list(trans_pt)
        if class_name=='car':
            trans_pt[0]+=150
        else:
            trans_pt[0]+=120
    
    trans_pt = tuple(trans_pt)

    return trans_pt

def point_slide_to_center2(trans_pt, class_name, car_flow, trajectory_point, id):
    if car_flow==0 and trajectory_point=='BOTTOM_RIGHT':
        trans_pt = list(trans_pt)
        # if class_name=='car':
        #     trans_pt[0]-=85
        # else:
        #     trans_pt[0]-=105
        if class_name=='car':
            trans_pt[0]-=85
        else:
            trans_pt[0]-=125
        # if id==3:
        #     trans_pt[0]=599
        # if id==15:
        #     trans_pt[0]-=20
        
    elif car_flow==0 and trajectory_point=='BOTTOM_LEFT':
        trans_pt = list(trans_pt)
        if class_name=='car':
            trans_pt[0]+=100
        else:
            trans_pt[0]+=100
        if id==4:
            trans_pt[0]+=20
    
    trans_pt = tuple(trans_pt)

    return trans_pt


