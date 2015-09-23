var React = require('react'),
	QuestionComponent = require('./QuestionComponent'),
	TabsListComponent = require('./TabsListComponent'),
	detailContainer = document.getElementById('question-app-container'),
	profileContainer = document.getElementById('profile-container'),
	getDataXHR = require('./XHR').getDataXHR,
	getProfileDataXHR = require('./XHR').getProfileDataXHR;


if (detailContainer !== null) {
	getDataXHR()
		.then(result => {
			console.log('success');
			React.render(
				<QuestionComponent data={result} />,
				detailContainer
			);
		}, error => {
			console.log('fail');
		});
}


if (profileContainer !== null) {
	getProfileDataXHR()
		.then(result => {
			React.render(
				<TabsListComponent data={result} />,
				profileContainer
			);
		});
}

