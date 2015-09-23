var React = require('react'),
	likeXHR = require('./XHR').likeXHR,
	dislikeXHR = require('./XHR').dislikeXHR;


class LikeComponent extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			likes: this.props.data.likes,
			liked: this.props.data.liked,
			targetUrl: this.props.targetUrl,
		};
		this.sendLikeXHR = this.sendLikeXHR.bind(this);
		this.sendDislikeXHR = this.sendDislikeXHR.bind(this);
	}

	sendLikeXHR() {
		let self = this;
		likeXHR(this.state.targetUrl)
			.then(result => {
				self.setState(prev => {
					return {
						likes: prev.likes + 1,
						liked: true
					};
				});
			}, error => {
				console.log(error);
			});
	}

	sendDislikeXHR() {
		let self = this;
		dislikeXHR(this.state.targetUrl)
			.then(result => {
				self.setState(prev => {
					return {
						likes: prev.likes - 1,
						liked: false
					};
				});
			})
	}

	render() {
		let clickFunc = this.state.liked ? this.sendDislikeXHR : this.sendLikeXHR,
			buttonText = this.state.liked ? 'You like it' : 'Like',
			buttonClass = 'btn ' + (this.state.liked ? ' btn-warning ' : ' btn-success ') + 'like-button';
		return (
			<button onClick={clickFunc} className={buttonClass}>
				{buttonText}<span className='counter'>{this.state.likes}</span>
			</button>
		);
	}

}


module.exports = LikeComponent;