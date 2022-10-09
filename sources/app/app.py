from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


app = Blueprint('app', __name__, url_prefix=SITE_ROOT)
app.config['SECRET_KEY'] = 'mysecretkey'

bootstrap = Bootstrap(app)

class RSVP(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    howmany = IntegerField('How Many?', validators=[DataRequired()])
    status = SelectField('Status', choices=[('yes', 'I Can Make it!'), ('maybe', 'Maybe?'), ('no', 'I Can\'t Make it!')])
    submit = SubmitField('Submit')


@app.route('/', methods=('GET', 'POST'))
def home():
    form = RSVP()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = open('rsvp.txt', 'a')
            file.write('\n' + form.name.data + ',' + str(form.howmany.data) + ',' + form.status.data)
            file.close()
            return redirect(url_for('success'))
    else:
        return render_template('index.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/admin')
def admin():
    file = open('rsvp.txt', 'r')
    data = file.read()
    file.close()
    data = data.split('\n')
    for i in range(len(data)):
        data[i] = data[i].split(',')
    print(data)

    #Count the number of people who can make it, maybe, and can't make it
    counter = {'yes': 0, 'maybe': 0, 'no': 0}
    people = {'yes': 0, 'maybe': 0, 'total': 0}
    for i in range(len(data)):
        if data[i][2] == 'yes':
            counter['yes'] += 1
            people['yes'] += int(data[i][1])
        elif data[i][2] == 'maybe':
            counter['maybe'] += 1
            people['maybe'] += int(data[i][1])
        elif data[i][2] == 'no':
            counter['no'] += 1
    people['total'] = people['yes'] + people['maybe']
    
    return render_template('admin.html', data=data, counter=counter, people=people)



