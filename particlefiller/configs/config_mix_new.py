import numpy as np
#import cv2
import os


### config #######################################################################################

# # 車線を生成する場所
count_place = '仲町二丁目_下り_big'
#count_place = '仲町二丁目_下り_big'

# ファイルの保存先（あらかじめ作っておく）
# パスの最後にスラッシュ/をつけること

# track_trans3.py用のpath
# BATH_PATH = '/home/meguro/mydatasets/track_trans/'
# OUTPUT_PATH = BATH_PATH+count_place+'/'
# OUTPUT_PATH = '/home/meguro/mydatasets/track_trans/仲町二丁目_big3/'
# OUTPUT_PATH = '/home/meguro/mydatasets/track_trans/仲町二丁目_trans5/'

# track_free.py用のpath
# BATH_PATH = '/home/meguro/mydatasets/track_free/'
# OUTPUT_PATH = BATH_PATH+count_place+'/'
# OUTPUT_PATH = '/home/meguro/mydatasets/track_free/MVI_40863_big/'

# # track_huhu.py用のpath
# BATH_PATH = '/home/meguro/mydatasets/track_huhu/'
# OUTPUT_PATH = BATH_PATH+count_place+'/'

# track_particle.py用のpath
# BATH_PATH = '/home/meguro/mydatasets/track_particle/仲町二丁目/'
# OUTPUT_PATH = BATH_PATH+count_place+'/'
OUTPUT_PATH = '/Users/meguro/Documents/谷口研/修士卒研/particlefiller/data/仲町二丁目/output/'

# track_memory.py用のpath
# detection.txtの名前変更忘れずに
# BATH_PATH = '/home/meguro/mydatasets/track_memory/'
# OUTPUT_PATH = BATH_PATH+count_place+'/'
# OUTPUT_PATH = '/home/meguro/mydatasets/track_memory/minami500/'
# OUTPUT_PATH = '/home/meguro/mydatasets/track_memory/strongsort/仲町二丁目/'


#作成しようとしているディレクトリが存在するかどうかを判定する
if os.path.isdir(OUTPUT_PATH):
    #既にディレクトリが存在する場合は何もしない
    pass
else:
    #ディレクトリが存在しない場合のみ作成する
    os.makedirs(OUTPUT_PATH)





if count_place=='仲町二丁目':
    source = "/home/meguro/mydatasets/cctv2/実験用データ/仲町二丁目/仲町二丁目_0120_1001_1101.mov"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'nakacho.txt'


elif count_place=='仲町二丁目_渋滞':
    source = "/home/meguro/mydatasets/MLIT/survey/仲町二丁目_渋滞.mov"
    # テストの検出の際のconf(default=0.5)
    conf = 0.5
    OUTPUT_FILE_NAME = 'nakacho_jutai.txt'


elif count_place=='上江橋':
    source = "/home/meguro/mydatasets/cctv2/実験用データ/上江橋/上江橋_0120_0901-1001.mov"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'track_buffer_1000.txt'

elif count_place=='可搬型カメラ_昼':
    source = "/home/meguro/mydatasets/cctv2/実験用データ/20190416_可搬型カメラ/可搬型カメラ_昼.AVI"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'detection100_0_6.txt'

elif count_place=='可搬型カメラ_夜':
    source = "/home/meguro/mydatasets/cctv2/実験用データ/20190416_可搬型カメラ/可搬型カメラ_夜.AVI"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'detection100_0_6.txt'

elif count_place=='山南':
    source = "/home/meguro/mydatasets/cctv2/実験用データ/山南/10.240.8.12C00783-20220309142707.mpeg"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'detection100_0_6.txt'

elif count_place=='神宮橋':
    source = "/home/meguro/mydatasets/cctv2/実験用データ/神宮橋/神宮橋_0120_1100_1200.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'detection100_0_6.txt'

elif count_place=='南千住':
    source = "/home/meguro/mydatasets/cctv2/実験用データ/南千住/南千住_10.160.15.241C04749-20220510072812.mpeg"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'track_buffer_500.txt'

elif count_place=='MVI_40742_memo':
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/test/MVI_40742.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'detection100_0_6.txt'

elif count_place=='MVI_40743_memo':
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/test/MVI_40743.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'detection100_0_6.txt'

elif count_place=='MVI_40863_memo':
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/test/MVI_40863.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'detection100_0_6.txt'

elif count_place=='MVI_40864_memo':
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/test/MVI_40864.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'detection100_0_6.txt'

elif count_place=='MVI_63544_memo':
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/train/MVI_63544.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'detection100_0_6.txt'

elif count_place=='MVI_40152_memo':
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/train/MVI_40152.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    OUTPUT_FILE_NAME = 'detection100_0_6.txt'

elif count_place=='田野倉':
    source = "/home/meguro/mydatasets/cctv2/実験用データ/田野倉/particle_test.mov"
    # テストの検出の際のconf(default=0.5)
    conf = 0.5
    OUTPUT_FILE_NAME = 'particle_test.txt'


elif count_place=='MVI_40743_big':
    # test用
    # テスト動画のパス
    source = "/home/meguro/mydatasets/UA-DETRAC_video/test/MVI_40743.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.5
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = True
    
    # track_trans.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(20, 277), (322, 160), (754, 260), (430, 540)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (1800,0), (1800,2250), (0,2250)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0), (1800,0), (1800,2250), (0,2250)], dtype=np.float32)
    DETECTION_AREA = np.array([(20, 277), (322, 160), (754, 260), (430, 540)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 6
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'down'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    # lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_RIGHT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = []


    # track_huhu.py用
    # 車線
    # lane_AREA = np.array([[(20,277),(97,238),(576,462),(430,540)],
    #     [(97,238),(149,221),(666,397),(576,462)],
    #     [(149,221),(200,203),(796,367),(666,397)],
    #     [(200,203),(252,191),(808,336),(796,367)],
    #     [(252,191),(287,180),(861,295),(808,336)],
    #     [(287,180),(322,147),(835,241),(861,295)],], dtype=np.int32)
    lane_AREA = np.array([[(20,277),(109,243),(541,446),(430,540)],
        [(109,243),(163,222),(617,380),(541,446)],
        [(163,222),(209,205),(672,332),(617,380)],
        [(209,205),(249,190),(708,301),(672,332)],
        [(249,190),(293,175),(744,270),(708,301)],
        [(293,175),(349,153),(788,233),(744,270)],], dtype=np.int32)
    lane_head = np.array([[960, 414],[960, 414],[960, 414],[960, 414],[960, 414],[960, 414]],dtype=np.int32)
    lane_head2 = np.array([[150, 2250],[450, 2250],[750, 2250],[1050, 2250],[1350, 2250],[1650, 2250]],dtype=np.int32)

    # track_free.py用
    DETECTION_AREA_free = np.array([(20, 277), (322, 160), (754, 260), (430, 540)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = False
    save_trajectory_path = 'to_huhu_743.txt'


elif count_place=='南千住_big':
    #DETECTION_FILE_NAME = '/Users/meguro/Documents/谷口研/カウント/カウント場所_cctv/南千住/detection_0_6.txt'

    # test用
    # テスト動画のパス
    #source = "/home/meguro/mydatasets/cctv2/実験用データ/実験用/仲町二丁目_1分.mov"
    #source = "/home/meguro/mydatasets/MLIT/survey/minami.mov"
    #source = "/home/meguro/mydatasets/MLIT/survey/minami_jutai.mov"
    # source = "/home/meguro/mydatasets/MLIT/survey/発表用.mov"
    source = "/home/meguro/mydatasets/cctv2/実験用データ/南千住/南千住_10.160.15.241C04749-20220510072812.mpeg"
    # テストの検出の際のconf(default=0.5)
    conf = 0.5
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = True
    
    # track_huhu.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    # real_lane = np.array([(1152,451), (1336,480), (718, 900), (80, 800)], dtype=np.float32)
    real_lane = np.array([(1152,451), (1336,480), (676, 926), (39, 817)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (600,0), (600,3450), (0,3450)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0),(600,0),(600, 3450),(0,3450)], dtype=np.float32)
    # DETECTION_AREA = np.array([(1152,451), (1336,480), (718, 900), (80, 800)], dtype=np.int32)
    DETECTION_AREA = np.array([(1152,451), (1336,480), (676, 926), (39, 817)], dtype=np.float32)


    # 車線の数を指定
    lane_num = 2
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'down'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'CENTER'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = []

    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(1011,426), (1170,460), (347, 804), (22, 686)],
                        [(1170,460), (1336,480), (718, 900), (347, 804)]
            ],
            dtype=np.int32)
    lane_head = np.array([[266, 912],[266, 912]],dtype=np.int32)

    # track_free.py用
    DETECTION_AREA_free = np.array([(1073,442), (1336,480), (718, 900), (39, 730)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = False





elif count_place=='仲町二丁目_下り_big':
    DETECTION_FILE_NAME = '/Users/meguro/Documents/谷口研/修士卒研/particlefiller/data/仲町二丁目/nakacho_jutai.txt'
    FRAME_PATH = 'data/仲町二丁目/frame/'
    # test用
    # テスト動画のパス
    # source = "/home/meguro/mydatasets/MLIT/survey/仲町二丁目_ID_Switch.mov"
    # source = "/home/meguro/mydatasets/cctv2/実験用データ/実験用/仲町二丁目_zure.mov"
    # source = "/home/meguro/mydatasets/cctv2/実験用データ/仲町二丁目/仲町二丁目_0120_1001_1101.mov"
    # source = "/home/meguro/mydatasets/MLIT/survey/交通流.mov"
    source = "/home/meguro/mydatasets/MLIT/survey/仲町二丁目_渋滞.mov"

    # テストの検出の際のconf(default=0.5)
    conf = 0.6
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = True
 
    # track_huhu.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(530,526), (880,526), (1897, 884), (1150, 884)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (600,0), (600,3400), (0,3400)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0), (600,0), (600,3400), (0,3400)], dtype=np.float32)
    DETECTION_AREA = np.array([(530,526), (880,526), (1897, 884), (1150, 884)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 2
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'down'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_RIGHT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    # パーティクルの数を設定
    particle_num = 50


    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(417, 455), (664, 457), (1890, 913), (1489, 997)], 
        [(664, 457), (1046, 414), (1898, 555), (1890, 913)]
        ],
        dtype=np.int32)
    # 車線の先頭
    lane_head = np.array([[1696, 963],[1828, 857]],dtype=np.int32)

    # track_free.py用
    DETECTION_AREA_free = np.array([(537, 533),(1146, 533),(1893, 754),(1360, 1036)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = False



elif count_place=='仲町二丁目_下り':
    # test用
    # テスト動画のパス
    source = "/home/meguro/mydatasets/cctv2/実験用データ/実験用/仲町二丁目_1分.mov"
    #source = "/home/meguro/mydatasets/cctv2/実験用データ/仲町二丁目/仲町二丁目_1101-1201.mov"
    # テストの検出の際のconf(default=0.5)
    conf = 0.7
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = False
    
    # track_huhu.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(537, 533), (914, 533), (1516, 752), (895, 752)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (600,0), (600,1950), (0,1950)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0),(600,0),(600, 2465),(0,2969)], dtype=np.float32)
    DETECTION_AREA = np.array([(537, 533),(914, 533),(1831, 866),(1360, 1036)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 2
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'down'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_RIGHT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]


    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(417, 455), (664, 457), (1890, 913), (1489, 997)], 
        [(664, 457), (1046, 414), (1898, 555), (1890, 913)]
        ],
        dtype=np.int32)
    # 車線の先頭
    lane_head = np.array([[1696, 963],[1828, 857]],dtype=np.int32)

    # track_free.py用
    DETECTION_AREA_free = np.array([(537, 533),(1146, 533),(1893, 754),(1360, 1036)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = False



elif count_place=='上江橋_下り':
    # test用
    # テスト動画のパス
    source = "/home/meguro/mydatasets/cctv2/実験用データ/訓練用/上江橋（下り）202101200931-1001.mpeg"
    # テストの検出の際のconf(default=0.5)
    conf = 0.7
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = False
    
    # track_trans.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(927, 363), (1208, 363), (1585, 467), (1176, 467)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (600,0), (600,1200), (0,1200)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0),(600,0),(600, 1669),(0,2336)], dtype=np.float32)
    DETECTION_AREA = np.array([(927, 363),(1208, 363),(1845, 538),(1779, 718)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 2
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'down'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_RIGHT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = [[(0, 0), (1920, 280)]]


    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(888, 347), (1167, 347), (1859, 596), (1720, 704)], 
        [(1167, 347), (1476, 347), (1920, 418), (1859, 596)]
        ],
        dtype=np.int32)
    # 車線の先頭
    lane_head = np.array([[1920, 639],[1920, 639]],dtype=np.int32)

    # track_free.py用
    DETECTION_AREA_free = np.array([(888, 347), (1476, 347), (1920, 418), (1720, 704)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = True


elif count_place=='ua-detrac':
    # test用
    # テスト動画のパス
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/MVI_40992.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.7
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = True
    
    # track_trans.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(143, 200), (435, 202), (622, 253), (273, 253)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (600,0), (600,700), (0,700)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0),(600,0),(600, 1415),(0,2107)], dtype=np.float32)
    DETECTION_AREA = np.array([(143, 199),(435, 201),(919, 334),(859, 492)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 2
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'up'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_RIGHT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = []


    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(158, 213), (232, 175), (908, 375), (855, 490)], 
        [(232, 175), (319, 153), (956, 253), (908, 375)]
        ],
        dtype=np.int32)
    # 車線の先頭
    lane_head = np.array([[180, 123],[180, 123]],dtype=np.int32)


    # track_free.py用
    DETECTION_AREA_free = np.array([(158, 213), (319, 153), (956, 253), (855, 490)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = True


elif count_place=='MVI_40742':
    # test用
    # テスト動画のパス
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/test/MVI_40742.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.5
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = True
    
    # track_trans.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(20, 277), (322, 160), (754, 260), (430, 540)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (1800,0), (1800,2250), (0,2250)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0), (1800,0), (1800,2250), (0,2250)], dtype=np.float32)
    DETECTION_AREA = np.array([(20, 277), (322, 160), (754, 260), (430, 540)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 6
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'down'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    # lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_RIGHT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = []


    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(20,277),(97,238),(576,462),(430,540)],
        [(97,238),(149,221),(666,397),(576,462)],
        [(149,221),(200,203),(796,367),(666,397)],
        [(200,203),(252,191),(808,336),(796,367)],
        [(252,191),(287,180),(861,295),(808,336)],
        [(287,180),(322,147),(835,241),(861,295)],], dtype=np.int32)
    lane_head = np.array([[960, 414],[960, 414],[960, 414],[960, 414],[960, 414],[960, 414]],dtype=np.int32)
    lane_head2 = np.array([[150, 2250],[450, 2250],[750, 2250],[1050, 2250],[1350, 2250],[1650, 2250]],dtype=np.int32)

    # track_free.py用
    DETECTION_AREA_free = np.array([(20, 277), (322, 160), (754, 260), (430, 540)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = True
    save_trajectory_path = 'to_huhu_742.txt'


elif count_place=='MVI_40743':
    # test用
    # テスト動画のパス
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/test/MVI_40743.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.5
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = False
    
    # track_trans.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(20, 277), (322, 160), (754, 260), (430, 540)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (1800,0), (1800,2250), (0,2250)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0), (1800,0), (1800,2250), (0,2250)], dtype=np.float32)
    DETECTION_AREA = np.array([(20, 277), (322, 160), (754, 260), (430, 540)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 6
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'down'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    # lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_RIGHT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = []


    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(20,277),(97,238),(576,462),(430,540)],
        [(97,238),(149,221),(666,397),(576,462)],
        [(149,221),(200,203),(796,367),(666,397)],
        [(200,203),(252,191),(808,336),(796,367)],
        [(252,191),(287,180),(861,295),(808,336)],
        [(287,180),(322,147),(835,241),(861,295)],], dtype=np.int32)
    lane_head = np.array([[960, 414],[960, 414],[960, 414],[960, 414],[960, 414],[960, 414]],dtype=np.int32)
    lane_head2 = np.array([[150, 2250],[450, 2250],[750, 2250],[1050, 2250],[1350, 2250],[1650, 2250]],dtype=np.int32)

    # track_free.py用
    DETECTION_AREA_free = np.array([(20, 277), (322, 160), (754, 260), (430, 540)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = True
    save_trajectory_path = 'to_huhu_743.txt'


elif count_place=='MVI_40863':
    # test用
    # テスト動画のパス
    source = "/home/meguro/mydatasets/UA-DETRAC_video/test/MVI_40863.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.5
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = True
    
    # track_trans.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(7,263), (341, 113), (871, 159), (615, 539)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (1800,0), (1800,2250), (0,2250)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0), (1800,0), (1800,2250), (0,2250)], dtype=np.float32)
    DETECTION_AREA = np.array([(7,263), (341, 113), (871, 159), (615, 539)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 6
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'down'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    # lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_RIGHT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = []


    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(7,263),(53,203),(803,450),(615,539)],
        [(53,203),(76,169),(869,348),(803,450)],
        [(76,169),(86,136),(903,276),(869,348)],
        [(86,136),(138,125),(913,224),(903,276)],
        [(138,125),(227,115),(906,188),(913,224)],
        [(227,115),(225,94),(915,147),(906,188)],], dtype=np.int32)
    lane_head = np.array([[960, 338],[960, 338],[960, 338],[960, 338],[960, 338],[960, 338]],dtype=np.int32)
    lane_head2 = np.array([[150, 2250],[450, 2250],[750, 2250],[1050, 2250],[1350, 2250],[1650, 2250]],dtype=np.int32)

    # track_free.py用
    DETECTION_AREA_free = np.array([(7,263), (341, 113), (871, 159), (615, 539)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = True
    save_trajectory_path = 'to_huhu_863.txt'


elif count_place=='MVI_40864':
    # test用
    # テスト動画のパス
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/test/MVI_40864.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.5
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = False
    
    # track_trans.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(7,263), (341, 113), (871, 159), (615, 539)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (1800,0), (1800,2250), (0,2250)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0), (1800,0), (1800,2250), (0,2250)], dtype=np.float32)
    DETECTION_AREA = np.array([(7,263), (341, 113), (871, 159), (615, 539)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 6
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'down'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    # lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_RIGHT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = []


    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(7,263),(53,203),(803,450),(615,539)],
        [(53,203),(76,169),(869,348),(803,450)],
        [(76,169),(86,136),(903,276),(869,348)],
        [(86,136),(138,125),(913,224),(903,276)],
        [(138,125),(227,115),(906,188),(913,224)],
        [(227,115),(225,94),(915,147),(906,188)],], dtype=np.int32)
    lane_head = np.array([[960, 338],[960, 338],[960, 338],[960, 338],[960, 338],[960, 338]],dtype=np.int32)
    lane_head2 = np.array([[150, 2250],[450, 2250],[750, 2250],[1050, 2250],[1350, 2250],[1650, 2250]],dtype=np.int32)


    # track_free.py用
    DETECTION_AREA_free = np.array([(7,263), (341, 113), (871, 159), (615, 539)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = True
    save_trajectory_path = 'to_huhu2.txt'



elif count_place=='MVI_40152':
    # test用
    # テスト動画のパス
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/train/MVI_40152.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.77
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = True
    
    # track_trans.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(806,163), (942, 194), (764, 540), (408, 363)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (900,0), (900,2250), (0,2250)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0), (900,0), (900,2250), (0,2250)], dtype=np.float32)
    DETECTION_AREA = np.array([(806,163), (942, 194), (764, 540), (408, 363)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 3
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'up'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    # lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_LEFT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = []


    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(7,263),(53,203),(803,450),(615,539)],
        [(53,203),(76,169),(869,348),(803,450)],
        [(76,169),(86,136),(903,276),(869,348)],
        [(86,136),(138,125),(913,224),(903,276)],
        [(138,125),(227,115),(906,188),(913,224)],
        [(227,115),(225,94),(915,147),(906,188)],], dtype=np.int32)
    lane_head = np.array([[960, 338],[960, 338],[960, 338],[960, 338],[960, 338],[960, 338]],dtype=np.int32)
    lane_head2 = np.array([[150, 0],[450, 0],[750, 0]],dtype=np.int32)


    # track_free.py用
    DETECTION_AREA_free = np.array([(806,163), (942, 194), (764, 540), (408, 363)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = False
    save_trajectory_path = 'to_huhu.txt'


elif count_place=='MVI_63544':
    # test用
    # テスト動画のパス
    source = "/home/meguro/mydatasets/UA-DETRAC_mask/train/MVI_63544.mp4"
    # テストの検出の際のconf(default=0.5)
    conf = 0.7
    # カウント結果の出力画像を何フレームに一回取るか
    output_image_space = 1
    # ファイル出力を行わない場合はFalse
    output_do_or_not = True
    
    # track_trans.py用
    # ここの4エリアはあらかじめ求めておく
    # 平行化の処理に使う座標（検出画像の座標）
    real_lane = np.array([(481,101), (700, 101), (378, 282), (45, 282)], dtype=np.float32)
    # 平行化の処理に使う座標（鳥瞰画像の座標）
    trans_lane = np.array([(0,0), (900,0), (900,2250), (0,2250)], dtype=np.float32)

    # 鳥瞰画像における検出範囲
    trans_lane_look = np.array([(0,0), (900,0), (900,2250), (0,2250)], dtype=np.float32)
    DETECTION_AREA = np.array([(481,101), (700, 101), (378, 282), (45, 282)], dtype=np.int32)


    # 車線の数を指定
    lane_num = 3
    # track_trans2.pyで用いる，表示用のレーンの道幅の設定(1車線分の長さ)
    lane_width = 800
    # 車線を分ける（lane_borderを定める）ために，軸をつけたものを可視化するモード
    # True: 軸を表示（ファイル出力をする），False: 軸を非表示（カウントするときはFalseにする）
    axis_visualization='False'
    # 軸をつけたグラフのファイル名
    trans_img_path = 'trans_image.jpg'
    # 射影変換後の車線は縦に流れるのか，横に流れるのか
    # 0: 車は縦に流れる，1: 車は横に流れる
    car_flow = 0
    # 車線の先頭は上下左右のどれか「up down left right」
    head_direction = 'down'
    # 車線の中間の座標
    # 縦に流れる2車線道路の場合，1車線目はx軸の0~500, 2車線目は500~1000のようなイメージ
    #lane_border = [800]
    # lane_border = [300]
    # 新idは，この値の範囲内にマイナスidがある場合は，マイナスidが割り当てられる
    matching_range = 800
    # 一度に移動する横の移動を何ピクセルまで許すか
    horizontal_limit_pixel = 1
    # 何フレーム分の記録を残し，それを使って移動予測をするか．10フレーム分保存しておく
    save_frame_num = 10
    # bboxのどこに軌跡を打つか: 'TOP_LEFT' 'TOP_RIGHT' 'BOTTOM_LEFT' 'BOTTOM_RIGHT' 'CENTER' 'BOTTOM_CENTER' 'BOTTOM_RIGHT'
    trajectory_point = 'BOTTOM_LEFT'
    # マスクの場所を指定
    # masked_area = [[(0, 0), (1920, 400)],[(1683, 193), (222, 335)],[(950,373), (1101,521)],[(1240,396),(1616,617)]]
    masked_area = []


    # track_huhu.py用
    # 車線
    lane_AREA = np.array([[(7,263),(53,203),(803,450),(615,539)],
        [(53,203),(76,169),(869,348),(803,450)],
        [(76,169),(86,136),(903,276),(869,348)],
        [(86,136),(138,125),(913,224),(903,276)],
        [(138,125),(227,115),(906,188),(913,224)],
        [(227,115),(225,94),(915,147),(906,188)],], dtype=np.int32)
    lane_head = np.array([[960, 338],[960, 338],[960, 338],[960, 338],[960, 338],[960, 338]],dtype=np.int32)
    lane_head2 = np.array([[150, 2250],[450, 2250],[750, 2250]],dtype=np.int32)


    # track_free.py用
    DETECTION_AREA_free = np.array([(481,101), (700, 101), (378, 282), (45, 282)], dtype=np.int32)

    # ua-detrac用
    # 軌跡の情報を保存するかどうか
    # 保存する場合は，まずファイルの中身を削除すること
    save_trajectory = True
    save_trajectory_path = 'to_huhu.txt'