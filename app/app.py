from flask import Flask, request, render_template_string, redirect, url_for
import pymysql
import os

app = Flask(__name__)

db_host = os.getenv('DB_HOST', 'db')
db_user = os.getenv('DB_USER', 'task_user')
db_password = os.getenv('DB_PASSWORD', 'task_pass')
db_name = os.getenv('DB_NAME', 'tasks_db')

def get_db():
    return pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

@app.route('/', methods=['GET'])
def show_tasks():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT name FROM tasks ORDER BY id")
    tasks = cur.fetchall()
    db.close()
    
    html = '''
    <form method="post">
        <input name="task" placeholder="Название задачи" required>
        <button type="submit">Add</button>
    </form>
    <ul>
    {% for t in tasks %}
        <li>{{ t[0] }}</li>
    {% endfor %}
    </ul>
    '''
    return render_template_string(html, tasks=tasks)

@app.route('/', methods=['POST'])
def add_task():
    task = request.form.get('task', '').strip()
    if task:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO tasks (name) VALUES (%s)", (task,))
        db.commit()
        db.close()
    return redirect(url_for('show_tasks'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
