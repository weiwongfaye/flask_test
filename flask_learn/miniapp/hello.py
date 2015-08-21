from flask import Flask, render_template, request,redirect, url_for
from flask_wtf import Form
from wtforms.fields import RadioField, SubmitField
from guess import Guess, GuessError

app = Flask(__name__)
questions = ['Is it comiled?','Does it run on a VM']
guesses = ['Python', 'Java', 'C++']
app.config['SECRET_KEY'] = 'test1'


game = Guess('Python')
game.expand('Python', 'C++', 'Is it interpreted?', False)
game.expand('C++', 'Java', 'Does it run on a VM?', True)

class YesNoQuestion(Form):
	answer = RadioField('your answer', choices = [('yes','Yes'),('no','No')])
	submit = SubmitField('Submit')


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/question/<int:id>', methods = ['GET','POST'])
def question(id):
	question = game.get_question(id)
	if question is None:
		return redirect(url_for('guess',id = id))

	form = YesNoQuestion()
	if form.validate_on_submit():
	# 	if form.answer.data == 'yes':
	# 		return redirect(url_for('question',id = id + 1))
	# 	else:
	# 		return redirect(url_for('question',id = id))
	# if request.method == 'POST':
	# 	if request.form['answer'] == 'yes':
	# 		return redirect(url_for('question',id=id+1))
		new_id = game.answer_question(form.answer.data == 'yes', id)
		return redirect(url_for('question',id = new_id))

	return render_template('question.html',question=question, form = form)


@app.route('/guess/<int:id>')
def guess(id):
	form = YesNoQuestion()
	if form.validate_on_submit():
		if form.answer.data == 'yes':
			return redirect(url_for('index'))
		return redirect(url_for('learn',id = id))
	return render_template('guess.html', guess=game.get_guess[id],form = form)


@app.route('/learn/<int: id>', methods=['GET','POST'])
def learn(id):
	guess = game.get_guess(id)
	form = LearnForm()
	if form.validate_on_submit():
		game.expand(guess, form.language.data, form )



if __name__ == '__main__':
	app.run(host = '0.0.0.0', port = 5000, debug = True)