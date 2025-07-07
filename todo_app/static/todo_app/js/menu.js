document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.querySelector('.logout-button');
    const reloadButton = document.querySelector('.reload-button');

    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            // ログアウト処理へのリダイレクトや AJAX リクエスト
            window.location.href = '/login/'; // 例: ログアウトURLへのリダイレクト
        });
    }

    if (reloadButton) {
        reloadButton.addEventListener('click', function() {
            // 画面のリロード
            window.location.reload();
        });
    }
});