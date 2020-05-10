# Dependecies
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

# General Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            # print('POST REQ')
            return redirect('/')
        except Exception as err:
            return f'There was an issue adding your task. {err}'

    else:
        # print('GET REQ')
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:uid>')
def delete(uid):
    task_to_delete = Todo.query.get_or_404(uid)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        # print('POST REQ')
        return redirect('/')
    except Exception as err:
        return f'There was an issue deleting your task. {err}'


@app.route('/update/<int:uid>', methods=['POST', 'GET'])
def update(uid):
    task = Todo.query.get_or_404(uid)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as err:
            return f'There was an issue updating your task. {err}'
    else :
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
