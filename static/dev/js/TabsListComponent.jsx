var React = require('react'),
	baseUrl = require('./utils').baseUrl;


class TabsListComponent extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			currentTab: 'questions'
		};
		this.chooseQuestions = this.chooseQuestions.bind(this);
		this.chooseAnswers = this.chooseAnswers.bind(this);
		this.getData = this.getData.bind(this);
	}

	chooseQuestions() {
		this.setState({
			currentTab: 'questions'
		});
	}

	chooseAnswers() {
		this.setState({
			currentTab: 'answers'
		});
	}

	getData() {
		if (this.state.currentTab === 'questions') {
			console.log('props', this.props.data);
			return this.props.data.own_questions.map(question => {
				return (
					<div className='question' key={question.id}>
		                <h5>
		                	<a href={baseUrl + '/' + question.id + '/'}>
		                		{question.summary}
		                	</a>
		                </h5>
		                <p className='question-date'>{question.created_at}</p>
		                <p>
		                    <span className='label label-primary question-answers-count'>
		                        {question.answers_count} answers
		                    </span>
		                    <span className='label label-success question-comments-count'>
		                        {question.comments_count} comments
		                    </span>
		                    <span className='label label-warning question-likes-count'>
		                        {question.likes_count} likes
		                    </span>
		                </p>
		            </div>
				);
			});
		} else {
			return this.props.data.own_answers.map(answer => {
				return (
					<div className='question' key={answer.id}>
						<h5>{answer.content}</h5>
						<p className='question-date'>{answer.created_at}</p>
						<p>
		                    <span className='label label-primary question-answers-count'>
		                        {answer.answers_count} answers
		                    </span>
		                    <span className='label label-success question-comments-count'>
		                        {answer.comments_count} comments
		                    </span>
		                    <span className='label label-warning question-likes-count'>
		                        {answer.likes_count} likes
		                    </span>
		                </p>
					</div>
				);
			})
		}
	}

	render() {
		let data = this.getData(),
			qClass = this.state.currentTab == 'questions' ? 'label-primary' : 'label-default',
			aClass = this.state.currentTab == 'answers' ? 'label-primary' : 'label-default';
		return (
			<div>
				<div className='profile-tabs'>
					<span className={'label ' + qClass} onClick={this.chooseQuestions}>Questions</span>
					<span className={'label ' + aClass} onClick={this.chooseAnswers}>Answers</span>
				</div>
				<div className='question-wrapper question-profile-wrapper'>{data}</div>
			</div>
		);
	}

}


module.exports = TabsListComponent;