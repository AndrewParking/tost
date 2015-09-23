var jQuery = require('jquery');

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getBaseUrl() {
    var prev = window.location.hostname;
    if (prev == '127.0.0.1') {
        return 'http://' + prev + ':8000';
    } else {
        return prev;
    }
}

function getQuestionId() {
	let arr = window.location.toString().split('/');
    console.log(arr[arr.length-2]);
	return arr[arr.length-2];
}

function getAccountId() {
    return getQuestionId();
}

module.exports = {
	baseUrl: getBaseUrl(),
	csrftoken: getCookie('csrftoken'),
	questionId: getQuestionId(),
    accountId: getAccountId(),
}
