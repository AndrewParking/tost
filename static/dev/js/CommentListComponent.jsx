var React = require('react'),
	baseUrl = require('./utils').baseUrl,
	CommentComponent = require('./CommentComponent'),
	sendCommentXHR = require('./XHR').sendCommentXHR,
	deleteCommentXHR = require('./XHR').deleteCommentXHR;


class CommentListComponent extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			comments: this.props.data,
			shown: false,
			targetUrl: this.props.targetUrl,
		};
		this.openComments = this.openComments.bind(this);
		this.closeComments = this.closeComments.bind(this);
		this.postComment = this.postComment.bind(this);
		this.deleteComment = this.deleteComment.bind(this);
	}

	openComments() {
		this.setState(prev => {
			return {
				comments: prev.comments,
				shown: true
			};
		});
	}

	closeComments() {
		this.setState(prev => {
			return {
				comments: prev.comments,
				shown: false
			};
		});
	}

	postComment() {
		let self = this,
			elem = document.getElementById('comment-content'),
			data = {
				content: elem.value
			};
		sendCommentXHR(this.state.targetUrl, data)
			.then(result => {
				self.setState(prev => {
					let oldComments = prev.comments;
					oldComments.push(result);
					return {
						comments: oldComments,
						shown: true
					};
				});
				elem.value = '';
			});
	}

	deleteComment(e) {
		let id = e.target.id,
			self = this;
		deleteCommentXHR(id)
			.then(result => {
				let arr = this.state.comments;
				for (let i=0, len=arr.length; i<len; i++) {
					console.log(arr[i].id, id);
					if (arr[i].id == id) {
						arr.splice(i, 1);
						break;
					}
				}
				self.setState(prev => {
					return {
						comments: arr,
						shown: true
					};
				});
			});
	}

	render() {
		if (this.state.shown) {
			let comments = this.state.comments.map(comment => {
				let removeButton = comment.my ? <span onClick={this.deleteComment} className='comment-delete' id={comment.id}>remove</span> : '';
				return (
					<div className='comment' key={comment.id}>
						<div className='comment-heading'>
							<img src={comment.author.photo} />
							<a href={baseUrl + '/account/' + comment.author.id + '/'}>
								{comment.author.username}
							</a>
							{removeButton}
						</div>
						<div className='comment-content'>{comment.content}</div>
					</div>
				);
			});
			return (
				<div>
					<div className='comments-container'>{comments}</div>
					<div className='comment-form'>
						<textarea id='comment-content' placeholder='Type your comment here...'></textarea>
						<button onClick={this.postComment} className='btn btn-primary'>Leave comment</button>
					</div>
					<p className='comments-toggle' onClick={this.closeComments}>Hide comments</p>
				</div>
			);
		} else {
			return (
				<p className='comments-toggle' onClick={this.openComments}>Show comments</p>
			);
		}
	}

}



module.exports = CommentListComponent;


