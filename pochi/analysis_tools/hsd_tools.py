import base64
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# TODO: 基本的にバッファから読み込むようにHSD系のツールを改変する


def read_HSD_from_buffer(
    buffer: bytes,
    size_y: int,
    size_x: int,
    file_extension: str,
    band: int = 141,
    bit_depth: int = 8,
) -> int:
    """
    この関数について:
        size_y, size_xで指定したサイズの.datもしくは.hsd形式(file_extensionで指定)のHSDを読み込む関数.

    引数argument:
        file_path('str'):読み込みたい.dat,.hsdのファイルパス

    戻り値return:
        shape(縦480,横640,バンド141)のnumpy_uint8
    """
    # バッファからnp配列へ変換
    DAT = np.frombuffer(buffer, dtype=np.uint16)

    if file_extension == "hsd":  # .hsdの場合_ヘッダー情報を消去後にuint16->uint8に変換
        DAT = np.delete(DAT, slice(0, 500000))
        if bit_depth == 10:  # ビット深度が10の場合
            DAT = DAT >> 2
        DAT = DAT.astype(np.uint8)  # uint8への変換
        HSData = np.reshape(DAT, (size_y, band, size_x))

    else:  # .datの場合_縦,bandを反転
        HSData = np.reshape(DAT, (size_y, band, size_x))
        HSData = HSData[::-1, ::-1, :]

    return HSData.transpose(0, 2, 1)


def HSD_to_RGB(
    HSD: np.ndarray,
    use_range: int = 3,
    R_band: int = 55,
    G_band: int = 35,
    B_band: int = 23,
    gamma: float = 2.2,
) -> None:
    """
    この関数について:
    引数argument:
        HSD(numpy_array): (shpae(480,640,141)のnumpy_array_uint8)
        file_name(str): 画像保存時のファイル名
        use_range(int): RGB_bandのbandを中心に+-use_rangeにて指定したバンドを平均する(0は入れないで)
        R_band,G_band,B_band(int): RGBに使用する3bandを指定


    戻り値return:
    """

    # RGB配列に変換(Buleに係数２をかけて底上げ)
    RGB_array = np.zeros((HSD.shape[0], HSD.shape[1], 3), dtype="uint8")
    RGB_array[:, :, 0] = np.mean(
        HSD[:, :, R_band - use_range : R_band + use_range], axis=2
    )
    RGB_array[:, :, 1] = np.mean(
        HSD[:, :, G_band - use_range : G_band + use_range], axis=2
    )
    RGB_array[:, :, 2] = np.mean(
        HSD[:, :, B_band - use_range : B_band + use_range], axis=2
    )

    # 画素値の最大値
    imax = np.max(RGB_array)
    # ガンマ補正
    RGB_array[:, :, :] = imax * (RGB_array[:, :, :] / imax) ** (1 / gamma)

    return RGB_array


def RGB_to_PIL(RGB_array: np.ndarray):
    return Image.fromarray(RGB_array)


def PIL_to_b64(PILImage: Image, format="jpeg"):
    buffer = BytesIO()
    PILImage.save(buffer, format)
    return base64.b64encode(buffer.getvalue()).decode("ascii")

def GetBoxSpectrum(HSD,x1,y1,x2,y2):
    """
    HSDから指定されたボックス内の平均波形を出力します
    Parameters
    ----------
    x1,y1(int):選択した座標の左上
    x2,y2(int):選択した座標の右下
    HSD:ハイパースペクトルデータ(np.array)
    
    Return
    ----------
    mean_spectrum:平均波形(mp.array141band)
    """
    #2点のxy座標を大小で入れ替え
    if x1>x2:
          x1,x2 = x2,x1
    if y1>y2:
          y1,y2 = y2,y1
    #ボックス内でトリミングして平均波形を取得
    mean_spctrum=HSD[y1:y2,:x1:x2,:].reshape(-1,141).mean(axis=0)
    return mean_spctrum

def get_spectrum_PIL(HSD,coordinate_list,color_list):
    """ 
    param
    -------------
    coordinate_list: [[x1,y1,x2,y2],[x1,y1,x2,y2],[x1,y1,x2,y2].....]
                    座標リストのリスト
    Return
    --------------
    PIL_img : PIL形式の波形画像を返します

    """
    
    fig = plt.figure(figsize = (20,10))
    j = 0
    for i in coordinate_list:
        plt.plot(GetBoxSpectrum(HSD,i[0],i[1],i[2],i[3]), color=color_list[j])
        j += 1

    fig.canvas.draw()
    # 画像をバイト列で取得する。
    data = fig.canvas.tostring_rgb()
    # 画像の大きさを取得する。
    w, h = fig.canvas.get_width_height()
    c = len(data) // (w * h)
    print(w,h)
    # PIL.Image に変換する
    PIL_img = Image.frombytes("RGB", (w, h), data, "raw")
    plt.close()
    return PIL_img 