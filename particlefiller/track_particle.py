import sys
sys.path.append('/Users/meguro/Documents/谷口研/修士卒研/particlefiller/')

import numpy as np
import configs.config_mix_new as config
import utils_back as my_function
import cv2
from ast import literal_eval


### config #######################################################################################
### pathの最後には/を入れること
# OUTPUT_PATH = '/home/meguro/tracking/yolo_tracking/output_image/bytetrack/神宮橋/'
#OUTPUT_PATH = '/home/meguro/mydatasets/boxmot/bytetrack/神宮橋_雨_DA/'
#OUTPUT_PATH = '/home/meguro/mydatasets/boxmot/bytetrack/小倉2/'
#OUTPUT_PATH = '/home/meguro/mydatasets/boxmot/botsort/南千住_30分/'
#OUTPUT_PATH = '/home/meguro/mydatasets/boxmot2/手動_補完/上江橋/'
#OUTPUT_PATH = '/home/meguro/mydatasets/boxmot/botsort/仲町二丁目_30分/'

OUTPUT_PATH = config.OUTPUT_PATH

DETECTION_FILE_NAME = config.DETECTION_FILE_NAME

FRAME_PATH = config.FRAME_PATH


# マスクの場所を指定
# 現在マスク内の車も検出しちゃっているので，ここを修正するように
# 南千住
#masked_area = [[(0, 944),(1920, 1080)], [(0, 0),(1920, 160)]]
#masked_area = [[(0, 0),(1920, 300)]]
masked_area = config.masked_area

output_image_space = config.output_image_space

# 仲町二丁目
#masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)]]

# マスク内にいる車は検出したくないので，ここで使用するリストを作る
#mask_area = np.array(masked_area)
# mask_area = []
# for i, k in enumerate(masked_area):
#     mask_area.append([])
#     for j in range(4):
#         if j==0:
#             mask_area[i].append(k[0])
#         elif j==1:
#             mask_area[i].append((k[0][0], k[1][1]))
#         elif j==2:
#             mask_area[i].append(k[1])
#         else:
#             mask_area[i].append((k[1][0], k[0][1]))
# mask_area = np.array(mask_area)






### 検出範囲の設定
# 神宮橋
#DETECTION_AREA = np.array([[630, 346], [825, 865], [1919, 670], [1118, 283]], dtype=np.int32)
# 山南
#DETECTION_AREA = np.array([[630, 600], [1580, 909], [1670, 613], [935, 418]], dtype=np.int32)
# 小倉
#DETECTION_AREA = np.array([[355, 751], [1580, 909], [1650, 538], [795, 538]], dtype=np.int32)
#
#DETECTION_AREA = np.array([[1550, 713], [1692, 235], [1021, 141], [819, 361]], dtype=np.int32)
#DETECTION_AREA = np.array([[1550, 713], [1692, 235], [1021, 141], [819, 361]], dtype=np.int32)
#全体
#DETECTION_AREA = np.array([[120, 510], [1650, 1060], [1580, 440], [870, 390]], dtype=np.int32)

# 車線エリア
# 南千住
#lane_AREA = config.lane_AREA
# lane_AREA = np.array([[(805, 302), (1907, 750), (1900, 605), (1016, 308)], 
#                 [(1900, 605), (1016, 308), (1178, 307), (1904, 485)]
#                 ],
#                 dtype=np.int32)
# 仲町二丁目
# lane_AREA = np.array([[(417, 455), (568, 457), (1803, 929), (1489, 997)], 
#                 [(568, 457), (841, 438), (1852, 785), (1803, 929)]
#                 ],
#                 dtype=np.int32)

# 車線の先頭の座標
# 南千住
# lane_head = np.array([[62, 868],[375, 963],[1134, 937]],dtype=np.int32)
# 仲町二丁目
#lane_head = np.array([[1696, 963],[1828, 857]],dtype=np.int32)
# 上江橋
#lane_head = config.lane_head
#lane_head = np.array([[1920, 660],[1920, 660]],dtype=np.int32)

# bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
#trajectory_point = 'BOTTOM_RIGHT'
trajectory_point = config.trajectory_point

trans_lane = config.trans_lane

car_flow = config.car_flow


#lane_num = len(lane_border)+1
lane_num = config.lane_num

lane_border = []
for i in range(lane_num-1):
    lane_border.append(300*(i+1))

head_direction = config.head_direction
matching_range = config.matching_range
axis_visualization = config.axis_visualization
trans_img_path = config.trans_img_path
horizontal_limit_pixel = config.horizontal_limit_pixel
lane_width = config.lane_width
save_frame_num = config.save_frame_num
# 鳥瞰画像における検出範囲
trans_lane_look = config.trans_lane_look
# x座標の最大値とy座標の最大値を抽出
max_x = np.max(trans_lane_look[:, 0])
max_y = np.max(trans_lane_look[:, 1])
# trans_imgのサイズ
trans_lane_final = np.array([(0,0),(max_x,0),(max_x, max_y),(0, max_y)], dtype=np.float32)
DETECTION_AREA = config.DETECTION_AREA
output_do_or_not = config.output_do_or_not
save_trajectory = config.save_trajectory
particle_num = config.particle_num


### クラス名とクラス番号の紐付け
#class_num_list = [2, 3, 7]
#class_name_list = ['car', 'motorcycle', 'truck']

#class_num_list = [0, 1, 2, 3]
#class_name_list = ['car', 'truck', 'motorcycle', 'bus']

class_num_list = [2, 5, 7]
class_name_list = ['car', 'bus', 'truck']

# 車両が検出される際，同じ車両なのにbboxが二重に重なってしまうことがあるので，それを防ぐためのiouの閾値
# この閾値以上のiouが計算されたら，重なった一方のidを廃棄する
IOU_LIMIT = 0.8
# 新規idとマイナスidのiouが，この閾値以上なら，マッチング成功とし，新規idにマイナスidを割り当てる
NEW_IOU_LIMIT = 0


# 射影変換行列を求める
# 基準とする畳四隅の写真上の座標（単位px）
real_lane = config.real_lane
# DETECTION_AREA = config.real_lane.astype(int)
# 基準とする畳四隅の実際の座標（単位cm）
trans_lane = config.trans_lane
# 射影行列の取得
M = cv2.getPerspectiveTransform(real_lane, trans_lane) 
inverse_M = np.linalg.inv(M)



total_id=[]
vehicle_type=[]
removed_id = [] # 廃棄したidはここに入れておく
# histry_id=[]
# histry_bbox_center=[]
histry_bbox_trajectory_point=[]

# 1フレーム前のid_laneを保存しておく
id_lane_before = []
# 2フレーム前のid_laneを保存しておく
id_lane_before_more = []
# 1フレーム前のid_lane_xyxyを保存しておく
id_lane_xyxy_before = []
# 2フレーム前のid_lane_xyxyを保存しておく
id_lane_xyxy_before_more = []
# 1フレーム前のid_trajectory_posiを保存しておく
id_trajectory_posi_before = []
# 2フレーム前のid_trajectory_posiを保存しておく
id_trajectory_posi_before_more = []
# 1フレーム前のlost_vehicle_particleを保存
lost_vehicle_particle_before = []

for _ in range(lane_num):
    id_lane_before.append([])
    id_lane_before_more.append([])
    id_lane_xyxy_before.append([])
    id_lane_xyxy_before_more.append([])
    id_trajectory_posi_before.append([])
    id_trajectory_posi_before_more.append([])

# 3フレーム前から10フレーム前のid_laneを保存しておく
id_lane_before_more_10 = []
# 3フレーム前から10フレーム前のid_lane_xyxyを保存しておく
id_lane_xyxy_before_more_10 = []
# 3フレーム前から10フレーム前のid_trajectory_posiを保存しておく
id_trajectory_posi_before_more_10 = []
for _ in range(save_frame_num):
    id_lane_before_more_10.append([])
    id_lane_xyxy_before_more_10.append([])
    id_trajectory_posi_before_more_10.append([])

# mask_areaの変形
mask_area = my_function.conversion_mask_area(masked_area)
# id_switchを仮bboxで修正できた場合は色を変えるために作成
# id switchを防いだidを保存
prevented_switch_id = []
# 検出できたフレームを保存
detection_bigin_frame = 0
a = 0
b = 0
a2 = 0
b2 = 0
a3=0
b3=0
a4=0
b4=0



# for frame_idx, r in enumerate(results):        
with open(DETECTION_FILE_NAME, 'r') as file:
    
    for line in file:
        # 改行文字を取り除いてリストに追加
        data_list = line.strip()
        # 改行文字を取り除き、カンマで分割
        values = line.strip().split('!')
        # print(values)
        # 各変数に代入
        be,frame_idx,id_num,class_num,bbox_center,bbox_frame,conf_list = values
        be = int(be)
        frame_idx = int(frame_idx)
        id_num = literal_eval(id_num)
        class_num = literal_eval(class_num)
        bbox_center = literal_eval(bbox_center)
        bbox_frame = literal_eval(bbox_frame)
        conf_list = literal_eval(conf_list)


        if frame_idx%10==0:
            print(str(frame_idx) + 'フレーム目')
        # print(frame_idx)
        # 物体検出できた時，r.boxes.dataには「725 281 108 94 0 2 -1」このようなlistとなり，サイズが7になる
        # このうち，2はクラスを指しており，現在クラス2はcarである．
        # [frame_idx: 現在調べているフレーム数(何フレームにその物体がいたか),
        # results.boxes.id.unsqueeze(1).to('cpu'): その物体のid,
        # ops.xyxy2ltwh(results.boxes.xyxy).to('cpu'): bboxの４つの座標,
        # results.boxes.conf.unsqueeze(1).to('cpu'): クラス判定の閾値指定(らしい),
        # results.boxes.cls.unsqueeze(1).to('cpu'),: その物体のクラス
        # dont_care]: ?
        #print(r)

        # processed_img = r.orig_img.copy()
        # #im = cv2.imread(processed_img)
        # cv2.imwrite('./image_sample/'+str(frame_idx)+'.jpg', processed_img)

        # 毎フレームごとに見ていく
        # どの車線にどのidがいるのかを記録する
        id_lane = []
        # 同時に，そのidのbbox_frame(左上，右下)の情報を保存
        id_lane_xyxy = []
        # 同時に，現フレームでの各idのbboxの基準点の座標を保存しておく（先頭順にsortするため）
        # こっちにはパーティクルの中心の値を格納する
        id_trajectory_posi = []
        for _ in range(lane_num):
            id_lane.append([])
            id_lane_xyxy.append([])
            id_trajectory_posi.append([])

        # 失跡車両が発生したら，決められた数のパーティクルをまく
        # {マイナスid: np.array(2, パーティクルの数)}
        lost_vehicle_particle = {}


        # 移動予測した時に参考にした前後の車を保存
        # {マイナスid:[参考にした前の車のid(無ければNone), 参考にした後ろの車のid(無ければNone)]},...]
        forward_back_car = {}

        if be==0:

            detection_bigin_frame+=1

            # そのフレーム内にいるオブジェクトのid
            id_num = np.array(id_num)
            # print(id_num) # [[1],[2],[3]]のような形で，そのフレームに写っているidが格納されている
            # そのフレーム内にいるオブジェクトのクラス
            class_num = np.array(class_num)
            # print(class_num)
            # そのフレーム内にいるオブジェクトのbboxの中心の集合
            bbox_center = np.array(bbox_center)
            bbox_frame = np.array(bbox_frame)
            # print(bbox_center)
            conf_list = np.array(conf_list)
            # print(conf_list)

            # 推論結果の出力
            # im_array = r.plot()  # plot a BGR numpy array of predictions
            # img = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            # img = my_function.pil2cv(img)
            if output_do_or_not:
                frame_name = FRAME_PATH + str(frame_idx) + '.jpg'
                img = cv2.imread(frame_name)

                # 地点の文字が書かれているところはマスクする
                #img = my_function.write_mask(img, masked_area)
                #img = my_function.write_mask(img, [[(0, 0), (1920, 300)]])

                # 検出範囲を描画
                img = my_function.detection_area_draw4(img, real_lane)
                #img = my_function.detection_area_draw(img, lane_AREA, lane_head)

                #img = my_function.detection_area_draw4(img, np.array([(20, 277), (303, 169), (766, 249), (430, 540)], dtype=np.float32))


            # 検出されたIDの数だけ回す
            for i, id in enumerate(id_num):

                # if int(id[0])==46 or int(id[0])==55 or int(id[0])==26 or int(id[0])==60:
                #     continue
                # if int(id[0])==27:
                #     id[0] = 4
                # 基準点の座標を取得
                trajectory_x, trajectory_y = my_function.trajectory_calculation(trajectory_point, [int(bbox_frame[i][0]),int(bbox_frame[i][1])], [int(bbox_frame[i][2]),int(bbox_frame[i][3])])
                # 基準点がマスクエリア内なら軌跡はとらない
                # in_out_mask=-1なら範囲外なのでok, in_out_mask=1ならマスク範囲内なので検出しない
                in_out_mask = my_function.in_out_mask_check(mask_area, trajectory_x, trajectory_y)
                if in_out_mask==1:
                    continue


                # もし，過去に対応付けidを扱う場合は，対応付けしたidの中で一番小さいidとして扱う
                # id対応付けの対象は，同じ車体にほぼ同じbboxを付けた場合
                # まずは，removed_id=[[7, 9], [10, 7]]のような状態を[[7, 9, 10]]のようにする
                result_dict = {}
                for sublist in removed_id:
                    sublist.sort()
                    key = sublist[0]
                    if key in result_dict:
                        result_dict[key].extend(sublist[1:])
                    else:
                        result_dict[key] = sublist
                removed_id = list(result_dict.values())
                # 次に今見ているidが対応付けしたidなのかどうかを確かめ，removed_idに入っていた場合は，そのidは対応付けで一番小さいidとして扱う
                for sublist in removed_id:
                    if int(id[0]) in sublist:
                        out = sublist[0]
                        id[0] = out
                        break
                # もし，今見ているidがすでに車線内にいるならパス
                frag=0
                for lanes in id_lane:
                    if int(id[0]) in lanes:
                        frag=1
                        break
                if frag==1:
                    continue

                # bbox_center_x = bbox_center[i][0]
                # bbox_center_y = bbox_center[i][1]
                # bbox_center = [bbox_center[i][0], bbox_center[i][1]]

                #bbox_top_left = [int(bbox_frame[i][0]), int(bbox_frame[i][1])]
                #bbox_bottom_right = [int(bbox_frame[i][2]), int(bbox_frame[i][3])]

                # 車体の基準点(trajectory_point)が車線内に入っているかを判定
                # 同時に，その車がどの車線にいるかを調べる
                # in_out: 車線内ならその車がいる車線数(0,1,...)，車線エリア外なら-1
                #in_out, id_trajectory_posi = my_function.object_in_the_area(lane_AREA, trajectory_point, id_trajectory_posi, (bbox_top_left[0],bbox_top_left[1]), (bbox_bottom_right[0],bbox_bottom_right[1]))
                # in_out: 1:範囲内 -1:範囲外
                # img, in_out = my_function.object_in_the_area(img, DETECTION_AREA, bbox_center_x, bbox_center_y)

                # 基準点の射影変換を行い，鳥瞰画像内の検出エリアに入っているかを判定する
                trans_pt = my_function.transform_pt((trajectory_x, trajectory_y), M)

                # 鳥瞰画像にマッピングする前に，基準点を車の先頭の真ん中(逆方向の場合は車の後ろの真ん中)に移す作業を行う
                class_index = class_num_list.index(int(class_num[i][0]))
                class_name = class_name_list[class_index]
                #trans_pt = my_function.point_slide_to_center(trans_pt, class_name, car_flow, trajectory_point)

                trans_pt = my_function.point_slide_to_center2(trans_pt, class_name, car_flow, trajectory_point, int(id[0]))

                # appendする前に，逆走を防ぐため，前フレームに同じidがあったらそのid_posiを参照し，逆走していたらその前フレームのid_posiを用いる（down,upの場合はy軸，left,rightの場合はx軸に注目）
                # 同時に横移動を抑制したい


                for ii, k in enumerate(id_lane_before):
                    if int(id[0]) in k:
                        trans_pt = list(trans_pt)
                        idx = k.index(int(id[0]))
                        if head_direction=='down': # 車が下に行く場合は，y軸に注目．横の抑制はx軸に注目
                            yy = id_trajectory_posi_before[ii][idx][1]
                            if trans_pt[1]<yy:
                                trans_pt[1]=yy
                            xx = id_trajectory_posi_before[ii][idx][0]
                            s = trans_pt[0]-xx
                            if abs(s)>horizontal_limit_pixel:
                                if s>0:
                                    trans_pt[0] = xx + horizontal_limit_pixel
                                else:
                                    trans_pt[0] = xx - horizontal_limit_pixel
                        elif head_direction=='up':
                            yy = id_trajectory_posi_before[ii][idx][1]
                            if trans_pt[1]>yy:
                                trans_pt[1]=yy
                            xx = id_trajectory_posi_before[ii][idx][0]
                            s = trans_pt[0]-xx
                            if abs(s)>horizontal_limit_pixel:
                                if s>0:
                                    trans_pt[0] = xx + horizontal_limit_pixel
                                else:
                                    trans_pt[0] = xx - horizontal_limit_pixel
                        elif head_direction=='left':
                            xx = id_trajectory_posi_before[ii][idx][0]
                            if trans_pt[0]>xx:
                                trans_pt[0]=xx
                        else:
                            xx = id_trajectory_posi_before[ii][idx][0]
                            if trans_pt[0]<xx:
                                trans_pt[0]=xx
                        trans_pt = tuple(trans_pt)
                        break

                # 修正した座標を用いて，車線判定を行う
                # 車線内（0, 1, ...）, 車線エリア外（-1）
                in_out = my_function.trans_lane_judgment2(trans_pt, trans_lane_look, car_flow)

                # bboxの基準点がエリア内ならbboxを描画
                if in_out>=0:
                    id_trajectory_posi[in_out].append([trans_pt[0], trans_pt[1]])

                    # 同じ車両に2つのbboxを重ねてしまうことがあるので，iouを計算し，重なりすぎていた場合，その二つのidを対応付ける(表示するのは小さい方のid)
                    # 変数xyxy: すでに車線に属している，かつ，独立していると判断されたidのbboxのxyxy, xyxy=[[左上x],[左上y],[右下x],[右下y]]
                    # 変数bbox_frame[i]: 現在注目しているidのbboxのxyxy(小数), bbox_frame[i]=[[左上x],[左上y],[右下x],[右下y]]
                    c = id_lane_xyxy.copy()
                    for t, xyxy in enumerate(c[in_out]):
                        iou_num = my_function.calculation_iou(xyxy, bbox_frame[i])
                        # すでに車線上にあるidのbboxとほぼピッタリ重なってしまった場合には一方のidと対応付ける
                        if iou_num>IOU_LIMIT:
                            frag=0
                            for ii in removed_id:
                                if ii[0]==int(id[0]):
                                    frag=1
                                    break
                            if frag==1:
                                continue
                            removed_id.append([id_lane[in_out][t], int(id[0])])
                            #print('removed_id:', removed_id)
                            continue
                    # IOUの試練を突破したidの左上と右下の位置を保存
                    id_lane_xyxy[in_out].append(bbox_frame[i])
                    # どの車線に属しているのかを記録
                    id_lane[in_out].append(int(id[0]))
                    # クラス名を調べる
                    # class_index = class_num_list.index(int(class_num[i][0]))
                    # class_name = class_name_list[class_index]
                    # bboxを描画
                    ### img = my_function.write_bbox_frame_id_class(img, int(id[0]), class_name, conf_list[i], (int(bbox_frame[i][0]),int(bbox_frame[i][1])), (int(bbox_frame[i][2]),int(bbox_frame[i][3])))
                    #img = my_function.write_bbox_frame_id(img, int(id[0]), (bbox_top_left[0],bbox_top_left[1]), (bbox_bottom_right[0],bbox_bottom_right[1]))                    
                    # 回転したbboxを描画
                    # img = my_function.write_rotate_bbox(img, (int(bbox_frame[i][0]),int(bbox_frame[i][1])), (int(bbox_frame[i][2]),int(bbox_frame[i][3])))
                    # bboxの基準点に点を打つ
                    #img = my_function.write_trajectory_point(img, trajectory_point, (bbox_top_left[0],bbox_top_left[1]), (bbox_bottom_right[0],bbox_bottom_right[1]))
                    # 新IDがある場合，追加する
                    # ここでtotal_idに追加してしまうと，付け替えれる新idもすべてカウントしてしまうので，カウントは最後に行う
                    # if (int(id[0]) in total_id)==False:
                    #     total_id.append(int(id[0]))
                    #     vehicle_type.append(int(class_num[i][0]))

                # 物体がエリア外ならbboxのフレームのみ描画
                else:
                    pass
                    # img = my_function.write_bbox_frame(img, (int(bbox_frame[i][0]),int(bbox_frame[i][1])), (int(bbox_frame[i][2]),int(bbox_frame[i][3])))
                    # 回転したbboxを描画
                    # img = my_function.write_rotate_bbox(img, (int(bbox_frame[i][0]),int(bbox_frame[i][1])), (int(bbox_frame[i][2]),int(bbox_frame[i][3])))

                # これまで検出されたbboxのxyxyを保存(軌跡を打つため)
                # histry_bbox_trajectory_point += [[(int(bbox_frame[i][0]),int(bbox_frame[i][1])), (int(bbox_frame[i][2]),int(bbox_frame[i][3]))]]


            # 検出された物体の軌跡を描画(bboxの指定された位置に点を打つだけ)
            # for ii in histry_bbox_trajectory_point:
            #     img = my_function.write_trajectory_point(img, trajectory_point, ii[0], ii[1])

            #print(id_lane_xyxy)
            
            # aaa = id_lane[1][0]

            # ccc = []
            # for iii in id_lane_xyxy[1]:
            #     aaa = iii[0]
            #     bbb = iii[3]
            #     ccc.append([aaa, bbb])
            # print(ccc)
            # print(id_lane[1])

            # 車線ごとに，idを先頭順に並べる
            id_lane, id_lane_xyxy, id_trajectory_posi= my_function.id_lane_sort3(head_direction, id_lane, id_lane_xyxy, id_trajectory_posi)


            ###################################################################################
            # 大型アップデート
            # bbox補完が車線とかからはみ出た場合の処理をまだしていないので注意
            # 前と後ろの車の平均のやつをまだやっていない

            # id_lane_beforeのマイナスのidのbboxを動かす処理
            # 動かした後は，今の車線のid_laneにid_lane_beforeのマイナスidを追加する
            # まずは，マイナスのidを動かすために前の車と後ろの車を見つける
            # 「id_lane_beforeでマイナスidの前にいる正のid」「そのidが今の車線にいる」を両方満たすidを見つける
            # ない場合は後ろの情報だけでマイナスのidを動かす
            # 「id_lane_beforeでマイナスidの前にいる正のid」「そのidが今の車線にいる」を両方満たすidを見つける
            # ない場合は後ろの情報だけでマイナスのidを動かす
            # 前と後ろ両方にいる車が得られなかったら過去の自分の情報だけでbboxを保管する
            # 横移動はさせないようにする（上下に移動しているときはx座標に注目，左右に動いている場合はy座標に注目する）
            remove_minus_id = []
            for jj, lane in enumerate(id_lane_before):
                for ii, minus_id in enumerate(lane):
                    # id_lane_beforeの中のマイナスidを発見
                    if minus_id<0:
                        # そのマイナスidの前方の車を発見
                        k = ii-1
                        while k>=0:
                            if lane[k]>0 and (lane[k] in id_lane[jj]):
                                forward_car = lane[k]
                                break
                            k-=1
                        if k==-1:
                            forward_car = None
                        # そのマイナスidの後方の車を発見
                        k = ii+1
                        while k<len(lane):
                            if lane[k]>0 and (lane[k] in id_lane[jj]):
                                back_car = lane[k]
                                break
                            k+=1
                        if k==len(lane):
                            back_car = None
                        # 前と後ろの車が両方見つからなかった場合は，t-2フレームとt-1フレームの自分の移動量を見て動かす
                        if forward_car==None and back_car == None:
                            # 修正
                            # 位置予測の赤いbboxが動かなくなる時があるので，10フレーム前とかの情報を使って頑張って動かす
                            # 10フレーム前から見ていって，なるべく古い情報を持ってくる
                            # 2フレーム前には必ずある
                            frag = 0
                            for iii, k in enumerate(reversed(id_lane_before_more_10)):
                                f = save_frame_num-iii-1 # 後ろから見ていく 9, 8, 7, 6...
                                for jjj, kk in enumerate(k):
                                    if minus_id in kk:
                                        idx = kk.index(minus_id)
                                        t_2 = id_trajectory_posi_before_more_10[f][jjj][idx]
                                        frag = 1
                                        break
                                    elif minus_id*(-1) in kk:
                                        idx = kk.index(minus_id*(-1))
                                        t_2 = id_trajectory_posi_before_more_10[f][jjj][idx]
                                        frag = 1
                                        break
                                if frag==1:
                                    break
                            
                            # id_lane_before_more内は必ずminus_idか-1*minus_idが存在する
                            # t-2フレーム時の基準点の座標を持ってくる
                            # if minus_id in id_lane_before_more[jj]:    
                            #     idx = id_lane_before_more[jj].index(minus_id)
                            #     t_2 = id_trajectory_posi_before_more[jj][idx]
                            # else:
                            #     idx = id_lane_before_more[jj].index(-1*minus_id)
                            #     t_2 = id_trajectory_posi_before_more[jj][idx]
                            # t-1フレーム時の基準点の座標を持ってくる
                            if minus_id in id_lane_before[jj]:    
                                idx = id_lane_before[jj].index(minus_id)
                                t_1 = id_trajectory_posi_before[jj][idx]
                            else:
                                idx = id_lane_before[jj].index(-1*minus_id)
                                t_1 = id_trajectory_posi_before[jj][idx]
                            # 移動量を計算
                            # dx = t_1[0] - t_2[0]
                            # dy = t_1[1] - t_2[1]
                            dx = round((t_1[0] - t_2[0])/f)
                            dy = round((t_1[1] - t_2[1])/f)
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                                if head_direction=='down':
                                    dy = abs(dy)
                                else:
                                    dy = -1*abs(dy)
                            else:
                                dy=0
                                if head_direction=='right':
                                    dx = abs(dx)
                                else:
                                    dx = -1*abs(dx)
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 前の車のみ見つかった場合は，前の車の移動量のみを参考にしてマイナスidを動かす
                        elif back_car == None:
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(forward_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(forward_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx = t[0] - t_1[0]
                            dy = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                            else:
                                dy=0
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 後ろの車のみ見つかった場合は，後ろの車の移動量のみを参考にしてマイナスidを動かす
                        elif forward_car == None:
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(back_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(back_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx = t[0] - t_1[0]
                            dy = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                            else:
                                dy=0
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 前と後ろ両方の車が見つかった場合は，前と後ろの移動量の平均を基にして動かす
                        else:
                            # 前の車
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(forward_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(forward_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx_f = t[0] - t_1[0]
                            dy_f = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx_f=0
                            else:
                                dy_f=0
                            # 後ろの車
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(back_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(back_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx_b = t[0] - t_1[0]
                            dy_b = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx_b=0
                            else:
                                dy_b=0
                            xx = id_trajectory_posi_before[jj][ii][0]+((dx_f+dx_b)/2)
                            yy = id_trajectory_posi_before[jj][ii][1]+((dy_f+dy_b)/2)

                        # 現在は，エリア外に行ったマイナスidは無視する
                        if 0<=xx and xx<=max_x and 0<=yy and yy<=max_y:
                            # [xx, yy]が同じ車線内に入っているかを判定
                            #in_out = my_function.object_in_the_area2(lane_AREA, xx, yy)
                            in_out = my_function.trans_lane_judgment((xx, yy), lane_border, car_flow)
                            # 入っていたらid_lane[ii]にマイナスidをappend
                            if in_out>=0:
                                if in_out==jj:
                                    id_lane[jj].append(minus_id)
                                    id_trajectory_posi[jj].append([xx, yy])
                                    # マイナスidのbboxを動かすため，t-1フレーム時のマイナスidのbbox座標を持ってくる
                                    if minus_id in id_lane_before[jj]:    
                                        idx = id_lane_before[jj].index(minus_id)
                                        t_1_frame = id_lane_xyxy_before[jj][idx]
                                    else:
                                        idx = id_lane_before[jj].index(-1*minus_id)
                                        t_1_frame = id_lane_xyxy_before[jj][idx]
                                    id_lane_xyxy[jj].append([t_1_frame[0], t_1_frame[1], t_1_frame[2], t_1_frame[3]])
                                    #id_lane_xyxy[jj].append([t_1_frame[0]+dx, t_1_frame[1]+dy, t_1_frame[2]+dx, t_1_frame[3]+dy])
                                    forward_back_car[minus_id] = [forward_car, back_car]
                        # 仮bboxを動かして，それが枠外だった場合，それは廃棄する
                        else:
                            remove_minus_id.append(minus_id)
                        
                        # エリア外，または，別の車線に入ってしまった場合は，そのbbox補完は諦める（車線の中心を定めてそれを沿うようにすれば回避できる）

            # remove_minus_idのidを廃棄する（マッチング成功したマイナスid,お役御免）
            id_lane_c = id_lane.copy()
            for del_id in remove_minus_id:
                for jj, lane in enumerate(id_lane_c):
                    if del_id in lane:
                        idx = id_lane[jj].index(del_id)
                        id_lane[jj].pop(idx)
                        id_lane_xyxy[jj].pop(idx)
                        id_trajectory_posi[jj].pop(idx)


            # 車線ごとに，idを先頭順に並べる
            #id_lane, id_lane_xyxy, id_trajectory_posi= my_function.id_lane_sort2(id_lane, lane_head, id_lane_xyxy, id_trajectory_posi)
            id_lane, id_lane_xyxy, id_trajectory_posi= my_function.id_lane_sort3(head_direction, id_lane, id_lane_xyxy, id_trajectory_posi)


            # 前フレームにいなくて，今のフレームにいるid(新id)を探す
            # まずは，その新idが突如id_switchしただけの可能性があるので，前フレームの同じ車線内の情報をみて，あまりにも重なっているようなら，id同士を対応付ける
            # 前の処理(iou>0.9)でやったのは，同じ車体に二つのbboxが重なった時の対応
            # 新idを見つけたら，id_lane内のbbox補完とマッチングし，id_switchを防ぐ
            id_lane_c = id_lane.copy()
            remove_minus_id = [] # id_lane内のマイナスidと新規idがマッチングできたら，そのマイナスidは廃棄する
            for jj, lane in enumerate(id_lane_c):
                for new_ii, new_id in enumerate(lane):
                    if new_id<0:
                        continue
                    # 前フレームにいなくて，今のフレームにいるid(新id)を探す
                    if new_id not in id_lane_before[jj]:
                        # print(id, ': 新id')
                        # その新idのbbox補完が見つかったら，そのまま(マイナスのidがある，(例)新id:10, -10の補完がある)
                        for lane2 in id_lane:
                            if -1*new_id in lane2:
                                remove_minus_id.append(-1*new_id)
                                break
                        else:
                            # 前フレームの同じ車線内の情報をみて，新idのbboxと前フレームのbboxがあまりにも重なっているようなら，id同士を対応付ける
                            frag=0
                            for before_ii, before_bbox in enumerate(id_lane_xyxy_before[jj]):
                                if id_lane_before[jj][before_ii]<0:
                                    continue
                                iou_num = my_function.calculation_iou(id_lane_xyxy[jj][new_ii], before_bbox)
                                if iou_num>IOU_LIMIT:
                                    removed_id.append([id_lane_before[jj][before_ii], new_id])
                                    # 新idをid_lane_before[jj][before_ii]に切り替えたいが，すでにそのidが今のフレームにいるなら新idに関わるbboxの情報などは廃棄する．
                                    if id_lane_before[jj][before_ii] in id_lane[jj]:
                                        # id_lane[jj].pop(new_ii)
                                        # id_lane_xyxy[jj].pop(new_ii)
                                        # id_trajectory_posi[jj].pop(new_ii)
                                        remove_minus_id.append(new_id)
                                        # id_lane[jj][new_ii] = id_lane_before[jj][before_ii]
                                    else:
                                        id_lane[jj][new_ii] = id_lane_before[jj][before_ii]
                                    frag=1
                                    break
                            if frag==0:
                                # 新規idとbbox補完のiouを測って，成功した場合はマッチングしてidの対応付けをする
                                # 本当は，一番iouが高いマイナスidを新idに割り当てたいが，時間がないのでとりあえず片っ端からやっていく
                                # for minus_ii, minus_id in enumerate(lane):
                                #     if minus_id<0:
                                #         iou_num = my_function.calculation_iou(id_lane_xyxy[jj][new_ii], id_lane_xyxy[jj][minus_ii])
                                #         if iou_num>NEW_IOU_LIMIT:
                                #             removed_id.append([-1*minus_id, new_id])
                                #             id_lane[jj][new_ii] = -1*minus_id
                                #             remove_minus_id.append(minus_id)
                                #             break

                                # 補正画像を見て，新idの指定した範囲内にマイナスidがいた場合は，付け替える
                                # 縦に車が流れている道路であれば，y座標の値に注目して，車線内の一番近くマイナスidがmatching_range内であれば，付け替える作業を行う
                                # new_iiの前後のインデックスを見るだけでも良さそうだが，とりあえず車線内のマイナスidをすべて調べて一番近いマイナスidを探す
                                # 出力:条件を満たした候補のマイナスidのインデックス，見つからなかった場合は-1を出力
                                #print('ok')
                                nearest_minus_idx = my_function.find_the_nearest_minus_id(id_lane[jj], id_trajectory_posi[jj], new_ii, car_flow, matching_range)
                                

                                if nearest_minus_idx>=0:
                                    removed_id.append([-1*id_lane[jj][nearest_minus_idx], new_id])
                                    id_lane[jj][new_ii] = -1*id_lane[jj][nearest_minus_idx]
                                    remove_minus_id.append(id_lane[jj][nearest_minus_idx])
                                    prevented_switch_id.append(-1*id_lane[jj][nearest_minus_idx])


            #print(prevented_switch_id)


            # 前フレームにあって，今のフレームにいないidを探す(つまり追跡が途切れたid)
            # そのidは仮bboxをid_laneのフレームに配置する
            # 仮bboxの位置は，前と後ろの車の情報を用いて保管する
            # ただし，前と後ろの車が両方見つからない，かつ，そのidが，t-1フレームにいたが，t-2フレームにはいない場合(つまり1フレームにだけ登場した場合)は仕方がないので無視する
            # 修正
            # 今までは，今フレームと前フレームの同じ車線しか見ていなかったが，車線全体を見る
            # じゃないと車が車線変更した時に元いた車線に位置予測の赤いbboxが残ってしまう
            for jj, lane in enumerate(id_lane_before):
                for ii, old_id in enumerate(lane):
                    if old_id<0:
                        continue
                    # 追跡が途切れたidを発見
                    frag=0
                    for k in id_lane:
                        if old_id in k:
                            frag=1
                    if frag==0:
                    #if old_id not in id_lane[jj]:
                        # そのマイナスidの前方の車を発見
                        k = ii-1
                        while k>=0:
                            if lane[k]>0 and (lane[k] in id_lane[jj]):
                                forward_car = lane[k]
                                break
                            k-=1
                        if k==-1:
                            forward_car = None
                        # そのマイナスidの後方の車を発見
                        k = ii+1
                        while k<len(lane):
                            if lane[k]>0 and (lane[k] in id_lane[jj]):
                                back_car = lane[k]
                                break
                            k+=1
                        if k==len(lane):
                            back_car = None
                        # 前と後ろの車が両方見つからなかった場合は，2フレーム前と1フレーム前の情報を使って仮bboxを作成
                        # ここを修正
                        # 前後の車がない場合は，なるべく後ろのフレームから
                        if forward_car==None and back_car == None:
                            # 修正
                            # 位置予測の赤いbboxが動かなくなる時があるので，10フレーム前とかの情報を使って頑張って動かす
                            # 10フレーム前から見ていって，なるべく古い情報を持ってくる
                            # 2フレーム前には必ずある
                            frag = 0
                            for iii, k in enumerate(reversed(id_lane_before_more_10)):
                                f = save_frame_num-iii-1 # 後ろから見ていく 9, 8, 7, 6...
                                for jjj, kk in enumerate(k):
                                    if old_id in kk:
                                        idx = kk.index(old_id)
                                        t_2 = id_trajectory_posi_before_more_10[f][jjj][idx]
                                        frag = 1
                                        break
                                if frag==1:
                                    break
                                if f==1:
                                    break
                            if frag==0:
                                continue

                            # 2フレーム前にそのold_idがいない場合は諦める
                            # ここの例が実際ある
                            # if old_id not in id_lane_before_more[jj]:
                            #     continue
                            # # t-2フレーム時の基準点の座標を持ってくる
                            # idx = id_lane_before_more[jj].index(old_id)
                            # t_2 = id_trajectory_posi_before_more[jj][idx]
                            # t-1フレーム時の基準点の座標を持ってくる 
                            # これは絶対ある
                            idx = id_lane_before[jj].index(old_id)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            # 移動量を計算
                            # dx = t_1[0] - t_2[0]
                            # dy = t_1[1] - t_2[1]
                            dx = round((t_1[0] - t_2[0])/f)
                            dy = round((t_1[1] - t_2[1])/f)
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                                if head_direction=='down':
                                    dy = abs(dy)
                                else:
                                    dy = -1*abs(dy)
                            else:
                                dy=0
                                if head_direction=='right':
                                    dx = abs(dx)
                                else:
                                    dx = -1*abs(dx)
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 前の車のみ見つかった場合は，前の車の移動量のみを参考にしてマイナスidを動かす
                        elif back_car == None:
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(forward_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(forward_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx = t[0] - t_1[0]
                            dy = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                            else:
                                dy=0
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 後ろの車のみ見つかった場合は，後ろの車の移動量のみを参考にしてマイナスidを動かす
                        elif forward_car == None:
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(back_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(back_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx = t[0] - t_1[0]
                            dy = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                            else:
                                dy=0
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 前と後ろ両方の車が見つかった場合は，前と後ろの移動量の平均を基にして動かす
                        else:
                            # 前の車
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(forward_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(forward_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx_f = t[0] - t_1[0]
                            dy_f = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx_f=0
                            else:
                                dy_f=0
                            # 後ろの車
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(back_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(back_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx_b = t[0] - t_1[0]
                            dy_b = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx_b=0
                            else:
                                dy_b=0
                            xx = id_trajectory_posi_before[jj][ii][0]+((dx_f+dx_b)/2)
                            yy = id_trajectory_posi_before[jj][ii][1]+((dy_f+dy_b)/2)

                        # [xx, yy]が同じ車線内に入っているかを判定
                        #in_out = my_function.object_in_the_area2(lane_AREA, xx, yy)
                        # 現在は，エリア外に行ったマイナスidは無視する
                        if 0<=xx and xx<=max_x and 0<=yy and yy<=max_y:
                        
                            in_out = my_function.trans_lane_judgment((xx, yy), lane_border, car_flow)
                            # 入っていたらid_lane[ii]にマイナスidをappend
                            if in_out>=0:
                                if in_out==jj:
                                    id_lane[jj].append(-1*old_id)
                                    id_trajectory_posi[jj].append([xx, yy])
                                    # マイナスidのbboxを動かすため，t-1フレーム時のマイナスidのbbox座標を持ってくる  
                                    idx = id_lane_before[jj].index(old_id)
                                    t_1_frame = id_lane_xyxy_before[jj][idx]
                                    id_lane_xyxy[jj].append([t_1_frame[0], t_1_frame[1], t_1_frame[2], t_1_frame[3]])
                                    # id_lane_xyxy[jj].append([t_1_frame[0]+dx, t_1_frame[1]+dy, t_1_frame[2]+dx, t_1_frame[3]+dy])
                                    forward_back_car[-1*old_id] = [forward_car, back_car]
                                    # # パーティクルを生成
                                    # if car_flow==0:
                                    #     lost_vehicle_particle[-1*old_id] = np.
                                    
                                    

                        # エリア外，または，別の車線に入ってしまった場合は，そのbbox補完は諦める（車線の中心を定めてそれを沿うようにすれば回避できる）


            # remove_minus_idのidを廃棄する（マッチング成功したマイナスid,お役御免）
            id_lane_c = id_lane.copy()
            for del_id in remove_minus_id:
                for jj, lane in enumerate(id_lane_c):
                    if del_id in lane:
                        idx = id_lane[jj].index(del_id)
                        id_lane[jj].pop(idx)
                        id_lane_xyxy[jj].pop(idx)
                        id_trajectory_posi[jj].pop(idx)


            # 車線ごとに，idを先頭順に並べる
            #id_lane, id_lane_xyxy, id_trajectory_posi= my_function.id_lane_sort2(id_lane, lane_head, id_lane_xyxy, id_trajectory_posi)
            id_lane, id_lane_xyxy, id_trajectory_posi= my_function.id_lane_sort3(head_direction, id_lane, id_lane_xyxy, id_trajectory_posi)


            # t-2フレームの情報，t-1フレームの情報を記録
            if detection_bigin_frame==1:
                id_lane_before = id_lane.copy()
                id_lane_before_more = id_lane.copy()
                id_lane_xyxy_before = id_lane_xyxy.copy()
                id_lane_xyxy_before_more = id_lane_xyxy.copy()
                id_trajectory_posi_before = id_trajectory_posi.copy()
                id_trajectory_posi_before_more = id_trajectory_posi.copy()
            elif detection_bigin_frame==2:
                id_lane_before = id_lane.copy()
                id_lane_xyxy_before = id_lane_xyxy.copy()
                id_trajectory_posi_before = id_trajectory_posi.copy()
            else:
                id_lane_before_more = id_lane_before.copy()
                id_lane_before = id_lane.copy()
                id_lane_xyxy_before_more = id_lane_xyxy_before.copy()
                id_lane_xyxy_before = id_lane_xyxy.copy()
                id_trajectory_posi_before_more = id_trajectory_posi_before.copy()
                id_trajectory_posi_before = id_trajectory_posi.copy()

            id_lane_before_more_10.insert(0, id_lane)
            id_lane_xyxy_before_more_10.insert(0, id_lane_xyxy)
            id_trajectory_posi_before_more_10.insert(0, id_trajectory_posi)
            id_lane_before_more_10.pop(-1)
            id_lane_xyxy_before_more_10.pop(-1)
            id_trajectory_posi_before_more_10.pop(-1)

            # # id:15の情報を保管
            # for jj, lane in enumerate(id_lane):
            #     for ii, id2 in enumerate(lane):
            #         if id2==10:
            #             a = (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1]))
            #             b = (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3]))
            # for jj, lane in enumerate(id_lane):
            #     for ii, id2 in enumerate(lane):
            #         if id2==16:
            #             a2 = (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1]))
            #             b2 = (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3]))
            # for jj, lane in enumerate(id_lane):
            #     for ii, id2 in enumerate(lane):
            #         if id2==14:
            #             a3 = (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1]))
            #             b3 = (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3]))
            # for jj, lane in enumerate(id_lane):
            #     for ii, id2 in enumerate(lane):
            #         if id2==22:
            #             a4 = (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1]))
            #             b4 = (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3]))


            # if output_do_or_not:
            #     for jj, lane in enumerate(id_lane):
            #         if jj==0:
            #             continue
            #         for ii, id2 in enumerate(lane):
            #             # bbox描画し
            #             img = my_function.write_bbox_frame_id3_big(img, id2, inverse_M, id_trajectory_posi[jj][ii], prevented_switch_id, (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1])), (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3])), a, b, a2, b2)
            #         break
            
            # bboxを描画
            if output_do_or_not:
                for jj, lane in enumerate(id_lane):
                    for ii, id2 in enumerate(lane):
                        # bbox描画し
                        img = my_function.write_bbox_frame_id2_big(img, id2, inverse_M, id_trajectory_posi[jj][ii], prevented_switch_id, (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1])), (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3])), a, b, a2, b2, a3, b3, a4, b4)
                        #img = my_function.write_bbox_frame_id2_big(img, id2, inverse_M, id_trajectory_posi[jj][ii], prevented_switch_id, (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1])), (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3])))
                        # #正のidなら基準点を打つ
                        #img = my_function.write_trajectory_point(img, trajectory_point, (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1])), (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3])))
                        # if id2>0 and id2!=2:
                        #     img = my_function.write_trajectory_point(img, trajectory_point, (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1])), (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3])))
        
        

            # bboxを描画
            # if output_do_or_not:
            #     for jj, lane in enumerate(id_lane):
            #         for ii, id2 in enumerate(lane):
            #             if id2==-15:
            #                 img = my_function.write_bbox_frame_id2_big(img, id2, inverse_M, id_trajectory_posi[jj][ii], prevented_switch_id, (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1])), (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3])), a, b)
            #                 #正のidなら基準点を打つ
            #                 # if id2>0 and id2!=2:
            #                 #     img = my_function.write_trajectory_point(img, trajectory_point, (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1])), (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3])))

            
            
            # # bboxを描画
            # if output_do_or_not:
            #     for jj, lane in enumerate(id_lane):
            #         for ii, id2 in enumerate(lane):
            #             if id2==5 or id2==10:
            #                 img = my_function.write_bbox_frame_id2_big(img, id2, inverse_M, id_trajectory_posi[jj][ii], prevented_switch_id, (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1])), (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3])), a, b)
            #                 # #正のidなら基準点を打つ
            #                 # if id2>0 and id2!=2:
            #                 #     img = my_function.write_trajectory_point(img, trajectory_point, (int(id_lane_xyxy[jj][ii][0]),int(id_lane_xyxy[jj][ii][1])), (int(id_lane_xyxy[jj][ii][2]),int(id_lane_xyxy[jj][ii][3])))
            #     # 検出範囲を描画
            #     #img = my_function.detection_area_draw4(img, real_lane)


            # print(id_lane)

            # カウントを行う
            for _, lane in enumerate(id_lane):
                for _, new_id in enumerate(lane):
                    if new_id>0:
                        if (new_id in total_id)==False:
                            total_id.append(new_id)
                            #vehicle_type.append(int(class_num[i][0]))

            ###################################################################################
            # print(len(id_lane[0]))
            # # 同時に，そのidのbbox_frame(左上，右下)の情報を保存
            # print(len(id_lane_xyxy[0]))
            # # 同時に，現フレームでの各idのbboxの基準点の座標を保存しておく（先頭順にsortするため）
            # print(len(id_trajectory_posi[0]))


            # 現在の車線状況を描画
            if output_do_or_not:
                #img = my_function.write_id_lane_big(img, id_lane)
                # 現在のカウント数を描画
                img = my_function.write_count_text_big(img, len(total_id))
                #img = my_function.write_count_text_big2(img, len(total_id))



                # print(id_lane)
                # print(id_trajectory_posi)
                # 補正画像の作成し，出力画像とマージ
                img = my_function.merging_trans_image5(frame_idx, img, id_lane, id_trajectory_posi, prevented_switch_id, max_x, max_y, car_flow, lane_border, forward_back_car, head_direction, trans_lane, trans_lane_look)
                
                # これまでの結果を反映した画像を保存
                if frame_idx%output_image_space==0:
                    my_function.save_image(img, OUTPUT_PATH, frame_idx)


            if save_trajectory:
                with open('to_trans3.txt', 'a') as output:
                    for ii, lane in enumerate(id_lane):
                        for jj, id in enumerate(lane):
                            if id>0:
                                w = id_lane_xyxy[ii][jj][2] - id_lane_xyxy[ii][jj][0]
                                h = id_lane_xyxy[ii][jj][3] - id_lane_xyxy[ii][jj][1]
                                data_list = str(frame_idx)+','+str(id)+','+str(id_lane_xyxy[ii][jj][0])+','+str(id_lane_xyxy[ii][jj][1])+','+str(w)+','+str(h)+',1,-1,-1,-1'
                                # データをファイルに書き込む
                                output.write(f"{data_list}\n")




            # id_num = r.boxes.id.unsqueeze(1).numpy()
            # print(int(id_num[0][0]))
            # class_num = r.boxes.cls.unsqueeze(1).numpy()
            # print(int(class_num[0][0]))
            
            # print(total_id)
            # print(vehicle_type)

            # 推論結果の出力
            # im_array = r.plot()  # plot a BGR numpy array of predictions
            # im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            # # im.show()  # show image
            # im = my_function.pil2cv(im)
            # my_function.write_count_text(im, len(total_id))
            # im.save('/home/meguro/tracking/yolo_tracking/image_sample/results2.jpg')  # save image



        # 何も検出できなかった場合はオリジナルimageを保存
        else:
            # マイナスIDがある場合は動かしたい
            # 失跡ID検出もする
            remove_minus_id = []
            for jj, lane in enumerate(id_lane_before):
                for ii, minus_id in enumerate(lane):
                    # id_lane_beforeの中のマイナスidを発見
                    if minus_id<0:
                        # そのマイナスidの前方の車を発見
                        k = ii-1
                        while k>=0:
                            if lane[k]>0 and (lane[k] in id_lane[jj]):
                                forward_car = lane[k]
                                break
                            k-=1
                        if k==-1:
                            forward_car = None
                        # そのマイナスidの後方の車を発見
                        k = ii+1
                        while k<len(lane):
                            if lane[k]>0 and (lane[k] in id_lane[jj]):
                                back_car = lane[k]
                                break
                            k+=1
                        if k==len(lane):
                            back_car = None
                        # 前と後ろの車が両方見つからなかった場合は，t-2フレームとt-1フレームの自分の移動量を見て動かす
                        if forward_car==None and back_car == None:
                            # 修正
                            # 位置予測の赤いbboxが動かなくなる時があるので，10フレーム前とかの情報を使って頑張って動かす
                            # 10フレーム前から見ていって，なるべく古い情報を持ってくる
                            # 2フレーム前には必ずある
                            frag = 0
                            for iii, k in enumerate(reversed(id_lane_before_more_10)):
                                f = save_frame_num-iii-1 # 後ろから見ていく 9, 8, 7, 6...
                                for jjj, kk in enumerate(k):
                                    if minus_id in kk:
                                        idx = kk.index(minus_id)
                                        t_2 = id_trajectory_posi_before_more_10[f][jjj][idx]
                                        frag = 1
                                        break
                                    elif minus_id*(-1) in kk:
                                        idx = kk.index(minus_id*(-1))
                                        t_2 = id_trajectory_posi_before_more_10[f][jjj][idx]
                                        frag = 1
                                        break
                                if frag==1:
                                    break
                            
                            # id_lane_before_more内は必ずminus_idか-1*minus_idが存在する
                            # t-2フレーム時の基準点の座標を持ってくる
                            # if minus_id in id_lane_before_more[jj]:    
                            #     idx = id_lane_before_more[jj].index(minus_id)
                            #     t_2 = id_trajectory_posi_before_more[jj][idx]
                            # else:
                            #     idx = id_lane_before_more[jj].index(-1*minus_id)
                            #     t_2 = id_trajectory_posi_before_more[jj][idx]
                            # t-1フレーム時の基準点の座標を持ってくる
                            if minus_id in id_lane_before[jj]:    
                                idx = id_lane_before[jj].index(minus_id)
                                t_1 = id_trajectory_posi_before[jj][idx]
                            else:
                                idx = id_lane_before[jj].index(-1*minus_id)
                                t_1 = id_trajectory_posi_before[jj][idx]
                            # 移動量を計算
                            # dx = t_1[0] - t_2[0]
                            # dy = t_1[1] - t_2[1]
                            dx = round((t_1[0] - t_2[0])/f)
                            dy = round((t_1[1] - t_2[1])/f)
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                                if head_direction=='down':
                                    dy = abs(dy)
                                else:
                                    dy = -1*abs(dy)
                            else:
                                dy=0
                                if head_direction=='right':
                                    dx = abs(dx)
                                else:
                                    dx = -1*abs(dx)
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 前の車のみ見つかった場合は，前の車の移動量のみを参考にしてマイナスidを動かす
                        elif back_car == None:
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(forward_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(forward_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx = t[0] - t_1[0]
                            dy = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                            else:
                                dy=0
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 後ろの車のみ見つかった場合は，後ろの車の移動量のみを参考にしてマイナスidを動かす
                        elif forward_car == None:
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(back_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(back_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx = t[0] - t_1[0]
                            dy = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                            else:
                                dy=0
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 前と後ろ両方の車が見つかった場合は，前と後ろの移動量の平均を基にして動かす
                        else:
                            # 前の車
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(forward_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(forward_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx_f = t[0] - t_1[0]
                            dy_f = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx_f=0
                            else:
                                dy_f=0
                            # 後ろの車
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(back_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(back_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx_b = t[0] - t_1[0]
                            dy_b = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx_b=0
                            else:
                                dy_b=0
                            xx = id_trajectory_posi_before[jj][ii][0]+((dx_f+dx_b)/2)
                            yy = id_trajectory_posi_before[jj][ii][1]+((dy_f+dy_b)/2)

                        # 現在は，エリア外に行ったマイナスidは無視する
                        if 0<=xx and xx<=max_x and 0<=yy and yy<=max_y:
                            # [xx, yy]が同じ車線内に入っているかを判定
                            #in_out = my_function.object_in_the_area2(lane_AREA, xx, yy)
                            in_out = my_function.trans_lane_judgment((xx, yy), lane_border, car_flow)
                            # 入っていたらid_lane[ii]にマイナスidをappend
                            if in_out>=0:
                                if in_out==jj:
                                    id_lane[jj].append(minus_id)
                                    id_trajectory_posi[jj].append([xx, yy])
                                    # マイナスidのbboxを動かすため，t-1フレーム時のマイナスidのbbox座標を持ってくる
                                    if minus_id in id_lane_before[jj]:    
                                        idx = id_lane_before[jj].index(minus_id)
                                        t_1_frame = id_lane_xyxy_before[jj][idx]
                                    else:
                                        idx = id_lane_before[jj].index(-1*minus_id)
                                        t_1_frame = id_lane_xyxy_before[jj][idx]
                                    id_lane_xyxy[jj].append([t_1_frame[0], t_1_frame[1], t_1_frame[2], t_1_frame[3]])
                                    #id_lane_xyxy[jj].append([t_1_frame[0]+dx, t_1_frame[1]+dy, t_1_frame[2]+dx, t_1_frame[3]+dy])
                                    forward_back_car[minus_id] = [forward_car, back_car]
                        # 仮bboxを動かして，それが枠外だった場合，それは廃棄する
                        else:
                            remove_minus_id.append(minus_id)
                        
                        # エリア外，または，別の車線に入ってしまった場合は，そのbbox補完は諦める（車線の中心を定めてそれを沿うようにすれば回避できる）

            # remove_minus_idのidを廃棄する（マッチング成功したマイナスid,お役御免）
            id_lane_c = id_lane.copy()
            for del_id in remove_minus_id:
                for jj, lane in enumerate(id_lane_c):
                    if del_id in lane:
                        idx = id_lane[jj].index(del_id)
                        id_lane[jj].pop(idx)
                        id_lane_xyxy[jj].pop(idx)
                        id_trajectory_posi[jj].pop(idx)


            # 車線ごとに，idを先頭順に並べる
            #id_lane, id_lane_xyxy, id_trajectory_posi= my_function.id_lane_sort2(id_lane, lane_head, id_lane_xyxy, id_trajectory_posi)
            id_lane, id_lane_xyxy, id_trajectory_posi= my_function.id_lane_sort3(head_direction, id_lane, id_lane_xyxy, id_trajectory_posi)

            # 前フレームにあって，今のフレームにいないidを探す(つまり追跡が途切れたid)
            # そのidは仮bboxをid_laneのフレームに配置する
            # 仮bboxの位置は，前と後ろの車の情報を用いて保管する
            # ただし，前と後ろの車が両方見つからない，かつ，そのidが，t-1フレームにいたが，t-2フレームにはいない場合(つまり1フレームにだけ登場した場合)は仕方がないので無視する
            # 修正
            # 今までは，今フレームと前フレームの同じ車線しか見ていなかったが，車線全体を見る
            # じゃないと車が車線変更した時に元いた車線に位置予測の赤いbboxが残ってしまう
            for jj, lane in enumerate(id_lane_before):
                for ii, old_id in enumerate(lane):
                    if old_id<0:
                        continue
                    # 追跡が途切れたidを発見
                    frag=0
                    for k in id_lane:
                        if old_id in k:
                            frag=1
                    if frag==0:
                    #if old_id not in id_lane[jj]:
                        # そのマイナスidの前方の車を発見
                        k = ii-1
                        while k>=0:
                            if lane[k]>0 and (lane[k] in id_lane[jj]):
                                forward_car = lane[k]
                                break
                            k-=1
                        if k==-1:
                            forward_car = None
                        # そのマイナスidの後方の車を発見
                        k = ii+1
                        while k<len(lane):
                            if lane[k]>0 and (lane[k] in id_lane[jj]):
                                back_car = lane[k]
                                break
                            k+=1
                        if k==len(lane):
                            back_car = None
                        # 前と後ろの車が両方見つからなかった場合は，2フレーム前と1フレーム前の情報を使って仮bboxを作成
                        # ここを修正
                        # 前後の車がない場合は，なるべく後ろのフレームから
                        if forward_car==None and back_car == None:
                            # 修正
                            # 位置予測の赤いbboxが動かなくなる時があるので，10フレーム前とかの情報を使って頑張って動かす
                            # 10フレーム前から見ていって，なるべく古い情報を持ってくる
                            # 2フレーム前には必ずある
                            frag = 0
                            for iii, k in enumerate(reversed(id_lane_before_more_10)):
                                f = save_frame_num-iii-1 # 後ろから見ていく 9, 8, 7, 6...
                                for jjj, kk in enumerate(k):
                                    if old_id in kk:
                                        idx = kk.index(old_id)
                                        t_2 = id_trajectory_posi_before_more_10[f][jjj][idx]
                                        frag = 1
                                        break
                                if frag==1:
                                    break
                                if f==1:
                                    break
                            if frag==0:
                                continue

                            # 2フレーム前にそのold_idがいない場合は諦める
                            # ここの例が実際ある
                            # if old_id not in id_lane_before_more[jj]:
                            #     continue
                            # # t-2フレーム時の基準点の座標を持ってくる
                            # idx = id_lane_before_more[jj].index(old_id)
                            # t_2 = id_trajectory_posi_before_more[jj][idx]
                            # t-1フレーム時の基準点の座標を持ってくる 
                            # これは絶対ある
                            idx = id_lane_before[jj].index(old_id)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            # 移動量を計算
                            # dx = t_1[0] - t_2[0]
                            # dy = t_1[1] - t_2[1]
                            dx = round((t_1[0] - t_2[0])/f)
                            dy = round((t_1[1] - t_2[1])/f)
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                                if head_direction=='down':
                                    dy = abs(dy)
                                else:
                                    dy = -1*abs(dy)
                            else:
                                dy=0
                                if head_direction=='right':
                                    dx = abs(dx)
                                else:
                                    dx = -1*abs(dx)
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 前の車のみ見つかった場合は，前の車の移動量のみを参考にしてマイナスidを動かす
                        elif back_car == None:
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(forward_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(forward_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx = t[0] - t_1[0]
                            dy = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                            else:
                                dy=0
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 後ろの車のみ見つかった場合は，後ろの車の移動量のみを参考にしてマイナスidを動かす
                        elif forward_car == None:
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(back_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(back_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx = t[0] - t_1[0]
                            dy = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx=0
                            else:
                                dy=0
                            xx = id_trajectory_posi_before[jj][ii][0]+dx
                            yy = id_trajectory_posi_before[jj][ii][1]+dy
                        # 前と後ろ両方の車が見つかった場合は，前と後ろの移動量の平均を基にして動かす
                        else:
                            # 前の車
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(forward_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(forward_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx_f = t[0] - t_1[0]
                            dy_f = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx_f=0
                            else:
                                dy_f=0
                            # 後ろの車
                            # t-1フレーム時の前の車の基準点の座標を持ってくる
                            idx = id_lane_before[jj].index(back_car)
                            t_1 = id_trajectory_posi_before[jj][idx]
                            t_1_frame = id_lane_xyxy_before[jj][idx]
                            # 今のフレームの前の車の基準点の座標を持ってくる
                            idx = id_lane[jj].index(back_car)
                            t = id_trajectory_posi[jj][idx]
                            t_frame = id_lane_xyxy[jj][idx]
                            # 移動量を計算
                            dx_b = t[0] - t_1[0]
                            dy_b = t[1] - t_1[1]
                            # 横移動は考慮しないようにする
                            if car_flow==0:
                                dx_b=0
                            else:
                                dy_b=0
                            xx = id_trajectory_posi_before[jj][ii][0]+((dx_f+dx_b)/2)
                            yy = id_trajectory_posi_before[jj][ii][1]+((dy_f+dy_b)/2)

                        # [xx, yy]が同じ車線内に入っているかを判定
                        #in_out = my_function.object_in_the_area2(lane_AREA, xx, yy)
                        # 現在は，エリア外に行ったマイナスidは無視する
                        if 0<=xx and xx<=max_x and 0<=yy and yy<=max_y:
                        
                            in_out = my_function.trans_lane_judgment((xx, yy), lane_border, car_flow)
                            # 入っていたらid_lane[ii]にマイナスidをappend
                            if in_out>=0:
                                if in_out==jj:
                                    id_lane[jj].append(-1*old_id)
                                    id_trajectory_posi[jj].append([xx, yy])
                                    # マイナスidのbboxを動かすため，t-1フレーム時のマイナスidのbbox座標を持ってくる  
                                    idx = id_lane_before[jj].index(old_id)
                                    t_1_frame = id_lane_xyxy_before[jj][idx]
                                    id_lane_xyxy[jj].append([t_1_frame[0], t_1_frame[1], t_1_frame[2], t_1_frame[3]])
                                    # id_lane_xyxy[jj].append([t_1_frame[0]+dx, t_1_frame[1]+dy, t_1_frame[2]+dx, t_1_frame[3]+dy])
                                    forward_back_car[-1*old_id] = [forward_car, back_car]
                                    

                        # エリア外，または，別の車線に入ってしまった場合は，そのbbox補完は諦める（車線の中心を定めてそれを沿うようにすれば回避できる）


            # remove_minus_idのidを廃棄する（マッチング成功したマイナスid,お役御免）
            id_lane_c = id_lane.copy()
            for del_id in remove_minus_id:
                for jj, lane in enumerate(id_lane_c):
                    if del_id in lane:
                        idx = id_lane[jj].index(del_id)
                        id_lane[jj].pop(idx)
                        id_lane_xyxy[jj].pop(idx)
                        id_trajectory_posi[jj].pop(idx)


            # 車線ごとに，idを先頭順に並べる
            #id_lane, id_lane_xyxy, id_trajectory_posi= my_function.id_lane_sort2(id_lane, lane_head, id_lane_xyxy, id_trajectory_posi)
            id_lane, id_lane_xyxy, id_trajectory_posi= my_function.id_lane_sort3(head_direction, id_lane, id_lane_xyxy, id_trajectory_posi)



            # t-2フレームの情報，t-1フレームの情報を記録
            if detection_bigin_frame==1:
                id_lane_before = id_lane.copy()
                id_lane_before_more = id_lane.copy()
                id_lane_xyxy_before = id_lane_xyxy.copy()
                id_lane_xyxy_before_more = id_lane_xyxy.copy()
                id_trajectory_posi_before = id_trajectory_posi.copy()
                id_trajectory_posi_before_more = id_trajectory_posi.copy()
                lost_vehicle_particle_before = lost_vehicle_particle.copy()
            elif detection_bigin_frame==2:
                id_lane_before = id_lane.copy()
                id_lane_xyxy_before = id_lane_xyxy.copy()
                id_trajectory_posi_before = id_trajectory_posi.copy()
                lost_vehicle_particle_before = lost_vehicle_particle.copy()
            else:
                id_lane_before_more = id_lane_before.copy()
                id_lane_before = id_lane.copy()
                id_lane_xyxy_before_more = id_lane_xyxy_before.copy()
                id_lane_xyxy_before = id_lane_xyxy.copy()
                id_trajectory_posi_before_more = id_trajectory_posi_before.copy()
                id_trajectory_posi_before = id_trajectory_posi.copy()
                lost_vehicle_particle_before = lost_vehicle_particle.copy()

            id_lane_before_more_10.insert(0, id_lane)
            id_lane_xyxy_before_more_10.insert(0, id_lane_xyxy)
            id_trajectory_posi_before_more_10.insert(0, id_trajectory_posi)
            id_lane_before_more_10.pop(-1)
            id_lane_xyxy_before_more_10.pop(-1)
            id_trajectory_posi_before_more_10.pop(-1)


            if output_do_or_not:
                frame_name = 'data/仲町二丁目/frame/' + str(frame_idx) + '.jpg'
                img = cv2.imread(frame_name)
                # 検出範囲を描画
                #img = my_function.detection_area_draw(img, DETECTION_AREA)
                # # 車線ごとに，idを先頭順に並べる
                # id_lane = my_function.id_lane_sort(id_lane, lane_head, id_trajectory_posi)
                # # 現在の車線状況を描画
                # img = my_function.write_id_lane(img, id_lane)
                # 地点の文字が書かれているところはマスクする
                img = my_function.write_mask(img, masked_area)
                # 検出範囲を描画
                img = my_function.detection_area_draw4(img, real_lane)
                # 現在のカウント数を描画
                img = my_function.write_count_text(img, len(total_id))
                img = my_function.merging_trans_image_0(img, id_lane, max_x, max_y, car_flow, lane_border, head_direction, lane_width, axis_visualization, trans_img_path)
                # フレームを保存
                my_function.save_image(img, OUTPUT_PATH, frame_idx)

        # 小倉20分はおそらく36000フレーム
        # if frame_idx>=36500:
        #     break
        # if frame_idx>=4000:
        #     break
print('total_count: '+str(len(total_id)))


