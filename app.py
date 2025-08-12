import datetime
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  completed = db.Column(db.Boolean, default=False)
  date_created = db.Column(db.DateTime, default=datetime.datetime.now)

  def __repr__(self) -> str:
    return '<Task %r>' % self.id
  def to_dict(self):
      return {
          'id': self.id,
          'content': self.content,
          'completed': self.completed,
          'date_created': self.date_created.isoformat()
      }

@app.route('/')
def index(): 
  return "Hello world"

@app.route('/t')
def index1(): 
  return render_template('index.html')

@app.route('/todos', methods=['POST', 'GET'])
def f(): 
  if request.method == 'GET':
    todos = Todo.query.all()
    json_todos = []
    for todo in todos:
      json_todos.append(todo.to_dict())
    return json_todos
  if request.method == 'POST':
    data = request.json
    new_todo = Todo(content=data['content'])
    try: 
      db.session.add(new_todo)
      db.session.commit()
      print(new_todo)
      return "created"
    except:
      return "Creation failed"
  return render_template('index.html')

@app.route('/todos/<int:id>')
def getById(id):
  return Todo.query.get(id).to_dict()

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5555)
