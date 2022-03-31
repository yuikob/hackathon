// カラーリスト（上限10個？）
const COLOR_LIST = ['red', 'yellow', 'green', 'blue', 'black', 'purple', 'orange', 'lime', 'aqua', 'pink']

atn = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            // start_points: [],
            // end_points: [],
            separated_xy: [],
            all_xy: [],
            rect_MousedownFlg: true,
            color_list: [],
            graph_src: '',
            annotation_src: '',
        }
    },
    methods: {
        sendResult() {
            if (confirm('こちらでよろしいですか？') != true) {
                return
            }
            // canvasのsrc情報を登録
            atn.annotation_src = document.getElementById("canvas").toDataURL("image/jpeg")

            // vueインスタンスに保存したデータをjson化
            json_data = data2Json()

            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

            axios.interceptors.request.use(request => {
                return request
            })

            axios({
                method: 'POST',
                url: window.location.href,
                data: json_data, // jsonデータ. request.bodyに格納
            }).then((response) => {
                if (response.data.status == 'success') {
                    alert('送信が完了しました')

                    // グラフの表示
                    var graphImage = document.getElementById("graph")
                    graphImage.src = "data:image/jpeg;base64," + response.data.graph

                    // グラフのsrc情報を登録
                    atn.graph_src = graphImage.src
                }
                else {
                    alert('送信されたデータに誤りがあります')
                }
            }
            ).catch((error) => {
                console.log(error)
                alert('送信中に何らかのエラーが発生しました')
            })
        },
        downloadImages() {  // 一括ダウンロード
            downloadImg('image.jpeg', atn.annotation_src)
            downloadImg('spectrum.jpeg', atn.graph_src)
        }
    },
    mounted() {
        initFunction()
    }
}).mount('#atn')


async function initFunction() {
    await axios({
        method: 'GET',
        url: window.location.href.replace('annotation', 'info'),
    }).then((response) => {
        if (response.data.status == 'success') {
            var rgbImg = new Image();
            rgbImg.src = "data:image/jpeg;base64," + response.data.rgb_image;

            const cs = document.getElementById('canvas');
            const ctx = cs.getContext('2d');

            // 画像の描画
            rgbImg.onload = function () {
                ctx.drawImage(rgbImg, 0, 0, 640, 480)
            }

            cs.onmousedown = function (event) {
                if (!atn.rect_MousedownFlg) {
                    alert('これ以上入力はできません')
                }
                // 初期化
                atn.separated_xy = []

                atn.separated_xy.push(event.offsetX);
                atn.separated_xy.push(event.offsetY);
            }

            cs.onmousemove = function (event) {
                event.preventDefault();
            }

            cs.onmouseup = function (event) {
                atn.separated_xy.push(event.offsetX);
                atn.separated_xy.push(event.offsetY);

                console.log(atn.separated_xy)

                // 画像上に範囲を描画する
                ctx.strokeStyle = COLOR_LIST[atn.all_xy.length]
                ctx.strokeRect(atn.separated_xy[0], atn.separated_xy[1], atn.separated_xy[2] - atn.separated_xy[0], atn.separated_xy[3] - atn.separated_xy[1])
                
                atn.color_list.push(COLOR_LIST[atn.all_xy.length])  // 色の登録
                atn.all_xy.push(atn.separated_xy)  // 全体の座標の登録

                // 10個入力したらこれ以上入力できなくする  ←消去する場合はあとで直さないといけない！！
                if (atn.all_xy.length == 10) {
                    atn.rect_MousedownFlg = false;
                }
            }
        }
    })
}

function data2Json() {
    let json_data = {
        all_xy: [],
        color_list: [],
    };
    atn.all_xy.forEach(element => {
        json_data.all_xy.push(element)
    });
    atn.color_list.forEach(element => {
        json_data.color_list.push(element)
    });
    console.log(json_data)
    return json_data
}

function downloadImg(fileName, fileSrc) {
    // ファイルのsrc情報
    const url = fileSrc;

    // リンクを生成
    let link = document.createElement('a');
    link.href= url;
    link.download = fileName;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

}
