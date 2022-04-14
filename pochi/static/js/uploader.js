window.addEventListener("load", async function () {
    // アップロードエリアの取得
    var fileArea = document.getElementById("uploadHere")
    // HSDファイルのinput用
    var fileInput = document.getElementById('uploadFile');
    // アップロード前画像
    var imgArea = document.getElementById("ImgBeforeUpload")
    // 送信用
    var file
    // ドラッグ中
    fileArea.addEventListener('dragover', (event) => {
        event.preventDefault();
    })
    // マウスがドラッグ＆ドロップ領域外に出たとき
    fileArea.addEventListener('dragleave', (event) => {
        event.preventDefault();
    })
    // ドロップ後
    fileArea.addEventListener('drop', function (e) {
        e.preventDefault();
        var files = e.dataTransfer.files;
        if (typeof files[0] !== 'undefined') { //ファイルのチェック
            console.log('file accepted')
            // 取得したファイルをinput[type=file]へ
            fileInput.files = files;
            fileInput.dispatchEvent(new Event('change', { bubbles: true }))
        } else {
            console.log('file not accepted')
            return
        }
    })
    // ファイルエリアのクリック時
    imgArea.addEventListener('click', function (e) {
        fileInput.click()
    })

    fileInput.addEventListener('change', function (e) {
        file = e.target.files[0];
        console.log(file)
        if (typeof e.target.files[0] !== undefined) {
            sendHSD(file);
        } else {
            alert('エラー')
        }
    })

})


function sendHSD(file) {

    var params = new FormData()
    params.append('file', file)
    console.log(params)

    if (confirm('こちらのファイルをアップロードしますか？') != true) {
        return
    }
    // TODO: Djangoから取得したCSRF-TOKENを設定
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

    axios.interceptors.request.use(request => {
        console.log(request)
        return request
    })

    axios.post(
        window.location.href,
        params,
        {
            headers:
            {
                'Content-Type': 'multipart/form-data'
            },
            responseType: 'json'
        }
    ).then((response) => {
        if (response.data.status == 'success') {
            console.log('成功しました')
            window.location.href = window.location.href.replace('upload', 'annotation')
        }
        else {
            alert('送信されたデータに誤りがあります')
        }
    }
    ).catch((error) => {
        console.log(error)
        alert('通信中に何らかのエラーが発生しました')
    })
}

