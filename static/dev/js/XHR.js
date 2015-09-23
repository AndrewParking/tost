var baseUrl = require('./utils').baseUrl,
	csrftoken = require('./utils').csrftoken,
	accountId = require('./utils').accountId,
	questionId = require('./utils').questionId;


module.exports = {

	getDataXHR() {
		return new Promise(function(resolve, reject) {
			var request = new XMLHttpRequest(),
				url = baseUrl + '/questions/' + questionId + '/';

			request.onload = function() {
				let response = JSON.parse(this.responseText);
				if (this.status == 200) {
					resolve(response);
				} else {
					reject(response);
				}
			}

			request.open('GET', url, true);
			request.send(null);
		});
	},

	getProfileDataXHR() {
		return new Promise(function(resolve, reject) {
			var request = new XMLHttpRequest(),
				url = baseUrl + '/account/accounts/' + accountId + '/';

			request.onload = function() {
				let response = JSON.parse(this.responseText);
				if (this.status == 200) {
					resolve(response);
				} else {
					reject(response);
				}
			}

			request.open('GET', url, true);
			request.send(null);
		});
	},

	likeXHR(url) {
		return new Promise(function(resolve, reject) {
			var request = new XMLHttpRequest();

			request.onload = function() {
				if (this.status == 201) {
					resolve(this.responseText);
				} else {
					reject(this.responseText);
				}
			}

			request.open('POST', url + 'like_it/', true);
			request.setRequestHeader('X-CSRFToken', csrftoken);
			request.setRequestHeader('Content-Type', 'application/json');
			request.send(JSON.stringify({}));
		});
	},

	dislikeXHR(url) {
		return new Promise(function(resolve, reject) {
			var request = new XMLHttpRequest();

			request.onload = function() {
				if (this.status == 204) {
					resolve(this.responseText);
				} else {
					reject(this.responseText);
				}
			}

			request.open('DELETE', url + 'dislike_it/', true);
			request.setRequestHeader('X-CSRFToken', csrftoken);
			request.setRequestHeader('Content-Type', 'application/json');
			request.send(null);
		});
	},

	sendCommentXHR(url, data) {
		return new Promise(function(resolve, reject) {
			var request = new XMLHttpRequest();

			request.onload = function() {
				let response = JSON.parse(this.responseText);
				console.log(response);
				if (this.status == 201) {
					resolve(response);
				} else {
					reject(response);
				}
			}

			request.open('POST', url, true);
			request.setRequestHeader('X-CSRFToken', csrftoken);
			request.setRequestHeader('Content-Type', 'application/json');
			request.send(JSON.stringify(data));
		});
	},

	sendAnswerXHR(data) {
		return new Promise(function(resolve, reject) {
			var request = new XMLHttpRequest(),
				url = baseUrl + '/questions/' + questionId + '/answers/';

			request.onload = function() {
				let response = JSON.parse(this.responseText);
				if (this.status == 201) {
					resolve(response);
				} else {
					reject(response);
				}
			}

			request.open('POST', url, true);
			request.setRequestHeader('X-CSRFToken', csrftoken);
			request.setRequestHeader('Content-Type', 'application/json');
			request.send(JSON.stringify(data));
		});
	},

	deleteCommentXHR(id) {
		return new Promise(function(resolve, reject) {
			var request = new XMLHttpRequest(),
				url = baseUrl + '/comments/' + id + '/';

			request.onload = function() {
				if (this.status == 204) {
					resolve(this.responseText);
				} else {
					reject(this.responseText);
				}
			}

			request.open('DELETE', url, true);
			request.setRequestHeader('X-CSRFToken', csrftoken);
			request.send(null);
		});
	},

	markAsSolutionXHR(qid, id) {
		return new Promise(function(resolve, reject) {
			var request = new XMLHttpRequest(),
				url = baseUrl + '/questions/' + qid + '/answers/' + id + '/mark_as_solution/';

			request.onload = function() {
				if (this.status == 200) {
					resolve(this.responseText);
				} else {
					reject(this.responseText);
				}
			}

			request.open('PATCH', url, true);
			request.setRequestHeader('X-CSRFToken', csrftoken);
			request.send(null);
		});
	},

	removeSolutionMarkXHR(qid, id) {
		return new Promise(function(resolve, reject) {
			var request = new XMLHttpRequest(),
				url = baseUrl + '/questions/' + qid + '/answers/' + id + '/remove_solution_mark/';

			request.onload = function() {
				if (this.status == 200) {
					resolve(this.responseText);
				} else {
					reject(this.responseText);
				}
			}

			request.open('PATCH', url, true);
			request.setRequestHeader('X-CSRFToken', csrftoken);
			request.send(null);
		});
	},

}
