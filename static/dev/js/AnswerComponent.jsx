var React = require('react'),
	baseUrl = require('./utils').baseUrl,
	questionId = require('./utils').questionId,
	LikeComponent = require('./LikeComponent'),
	markAsSolutionXHR = require('./XHR').markAsSolutionXHR,
	removeSolutionMarkXHR = require('./XHR').removeSolutionMarkXHR,
	CommentListComponent = require('./CommentListComponent');


class AnswerComponent extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			solution: this.props.data.solution,
		};
		this.getMarkBtn = this.getMarkBtn.bind(this);
		this.markAsSolution = this.markAsSolution.bind(this);
		this.removeSolutionMark = this.removeSolutionMark.bind(this);
	}

	markAsSolution() {
		let self = this;
		markAsSolutionXHR(this.props.qid, this.props.data.id)
			.then(result => {
				self.setState({
					solution: true
				});
			});
	}

	removeSolutionMark() {
		let self = this;
		removeSolutionMarkXHR(this.props.qid, this.props.data.id)
			.then(result => {
				self.setState({
					solution: false
				});
			});
	}

	getMarkBtn() {
		console.log(this.props.qid);
		if (this.props.qid) {
			if (this.state.solution) {
				return <button className='btn btn-warning mark' onClick={this.removeSolutionMark}>Remove solution mark</button>;
			} else {
				return <button className='btn btn-success mark' onClick={this.markAsSolution}>Mark as solution</button>
			}
		}
	}

	render() {
		let account = this.props.data.author,
			likeUrl = baseUrl + '/questions/' + questionId + '/answers/' + this.props.data.id + '/',
			commentUrl = baseUrl + '/questions/' + questionId + '/answers/' + this.props.data.id + '/comment_it/',
			likeData = {
				likes: this.props.data.likes_count,
				liked: this.props.data.already_liked
			},
			markBtn = this.getMarkBtn(),
			solutionSpan = this.state.solution ? <span className='label label-success'>solution</span> : '';
		return (
			<div>
				<div className='answer-header'>
					<img src={account.photo} />
					<a href={baseUrl + '/account/' + account.id + '/'}>{account.username}</a>
					{solutionSpan}
				</div>
				<div className='answer-content'>{this.props.data.content}</div>
				<div>
					<LikeComponent targetUrl={likeUrl} data={likeData} />
					{markBtn}
				</div>
				<div><CommentListComponent targetUrl={commentUrl} data={this.props.data.comments} /></div>
			</div>
		);
	}

}

module.exports = AnswerComponent;

