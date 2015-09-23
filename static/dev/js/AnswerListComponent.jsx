var React = require('react'),
	sendAnswerXHR = require('./XHR').sendAnswerXHR,
	AnswerComponent = require('./AnswerComponent');


class AnswerListComponent extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			answers: this.props.data,
		};
		this.sendAnswer = this.sendAnswer.bind(this);
	}

	sendAnswer() {
		let elem = document.getElementById('answer-content'),
			self = this,
			data = {
				content: elem.value
			};
		sendAnswerXHR(data)
			.then(result => {
				self.setState(prev => {
					let oldAnswers = prev.answers;
					oldAnswers.push(result);
					return {
						answers: oldAnswers
					};
				});
				elem.value = '';
			});
	}

	render() {
		let answers = this.state.answers.map(answer => {
			return <AnswerComponent qid={this.props.qid} key={answer.id} data={answer} />;
		});
		return (
			<div className='answers'>
				<div className='answer-form'>
					<textarea id='answer-content' placeholder='Type your answer here...'></textarea>
					<button className='btn btn-primary' onClick={this.sendAnswer}>Post answer</button>
				</div>
				<div>{answers}</div>
			</div>
		);
	}

}


module.exports = AnswerListComponent;