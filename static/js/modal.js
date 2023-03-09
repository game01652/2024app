const modalBtns = document.querySelectorAll(".modal-toggle");
modalBtns.forEach(function (btn) {
    btn.onclick = function () {
        var modal = btn.getAttribute('data-modal');
        document.getElementById(modal).style.display = "block";
    };
});

const closeBtns = document.querySelectorAll(".modal-close");
closeBtns.forEach(function (btn) {
    btn.onclick = function () {
        var modal = btn.closest('.modal');
        modal.style.display = "none";
    };
});

window.onclick = function (event) {
    if (event.target.className === "modal") {
        event.target.style.display = "none";
    }
};


/* 参照ページ */
/* 動くWebデザイン アイデア帳 スライドショー -リンクをクリックすると、背景が暗くなり動画や画像やテキストを表示-
https://coco-factory.jp/ugokuweb/move01/9-6-3/*/