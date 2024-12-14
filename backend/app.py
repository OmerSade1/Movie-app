import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{db_password}@db/{db_name}"
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    app.logger.info('Fetched todos: %s', todos)
    return jsonify([{'id': todo.id, 'text': todo.text} for todo in todos])

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_todo = Todo(text=data['text'])
    db.session.add(new_todo)
    try:
        db.session.commit()
        app.logger.info('Added new todo: %s', new_todo)
        print(f"Added new todo: {new_todo.text}")
        return '', 201
    except Exception as e:
        print(f"Failed to add new todo: {new_todo.text}. Error: {str(e)}")
        return str(e), 500
    
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
	todo = Todo.query.get(id)
	if todo is None:
		return '', 404
	db.session.delete(todo)
	db.session.commit()
	app.logger.info('Deleted todo: %s', todo)
	return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)