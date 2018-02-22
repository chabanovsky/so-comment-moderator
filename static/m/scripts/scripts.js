
function loadHelper(url, onSuccess, onError) {
    $.ajax({
        url: url,
        method: 'GET',
        success: onSuccess,
        error: onError
    });
}