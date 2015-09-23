var React = require('react'),
	baseUrl = require('./utils').baseUrl,
	questionId = require('./utils').questionId,
	AnswerListComponent = require('./AnswerListComponent'),
	CommentListComponent = require('./CommentListComponent'),
	LikeComponent = require('./LikeComponent');


class QuestionComponent extends React.Component {

	constructor(props) {
		super(props);
	}

	render() {
		let likeUrl = baseUrl + '/questions/' + questionId + '/',
			commentUrl = baseUrl + '/questions/' + questionId + '/comment_it/',
			qid = this.props.data.my ? this.props.data.id : 0,
			likeData = {
				liked: this.props.data.already_liked,
				likes: this.props.data.likes_count
			};
		return (
			<div>
				<div><LikeComponent targetUrl={likeUrl} data={likeData} /></div>
				<div><CommentListComponent targetUrl={commentUrl} data={this.props.data.comments} /></div>
				<div><AnswerListComponent qid={qid} data={this.props.data.answers} /></div>
			</div>
		);
	}

}


module.exports = QuestionComponent;
