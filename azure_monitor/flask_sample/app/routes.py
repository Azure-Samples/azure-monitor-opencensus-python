import json
import requests

from flask import flash, make_response, redirect, render_template, request, url_for

from app import app, db, logger
from app.forms import ToDoForm
from app.metrics import mmap, request_measure, tmap
from app.models import Todo

# Hitting any endpoint will track an incoming request (requests)


@app.route('/')
@app.route('/error')
def index():
    form = ToDoForm()
    # Queries to the data base will track an outgoing request (dependencies)
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    path = request.url_rule
    if path and 'error' in path.rule:
        flash('ERROR: String must be less than 11 characters.')
    return render_template(
        'index.html',
        title='Home',
        form=form,
        complete=complete,
        incomplete=incomplete
    )


@app.route('/save', methods=['POST'])
def save():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    incomplete.extend(complete)
    url = "http://localhost:5001/api/save"
    entries = ["Id: " + str(entry.id) + " Task: " + entry.text + " Complete: " + str(entry.complete) \
        for entry in incomplete]
    response = requests.post(url=url, data=json.dumps(entries))
    if response.ok:
        flash("Todo saved to file.")
    else:
        logger.error(response.reason)
        flash("Exception occurred while saving")
    return redirect('/')


@app.route('/blacklist')
def blacklist():
    return render_template('blacklist.html')


@app.route('/add', methods=['POST'])
def add():
    add_input = request.form['add_input']
    # Fail if string greater than 10 characters
    try:
        if len(add_input) > 10:
            raise Exception
        todo = Todo(text=add_input, complete=False)
        db.session.add(todo)
        db.session.commit()
        # Logging with the logger will be tracked as logging telemetry (traces)
        logger.warn("Added entry: " + todo.text)
        # Records a measure metric to be sent as telemetry (customMetrics)
        mmap.measure_int_put(request_measure, 1)
        mmap.record(tmap)
    except Exception:
        logger.exception("ERROR: Input length too long.")
        return redirect('/error')
    return redirect('/')


@app.route('/complete/<id>', methods=['POST'])
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    logger.warn("Marked complete: " + todo.text)
    return redirect('/')

### Endpoints for CLI demo ###


@app.route('/get/incomplete')
def get_incomplete():
    incomplete = Todo.query.filter_by(complete=False).all()
    return json.dumps([(task.id, task.text) for task in incomplete])


@app.route('/get/complete')
def get_complete():
    complete = Todo.query.filter_by(complete=True).all()
    return json.dumps([(task.id, task.text) for task in complete])


@app.route('/add/<task>', methods=['POST'])
def add_task(task):
    try:
        print("Task Received: " + task)
        if len(task) > 10:
            raise Exception
        todo = Todo(text=task, complete=False)
        db.session.add(todo)
        db.session.commit()
        # Logging with the logger will be tracked as logging telemetry (traces)
        logger.warn("Added entry: " + todo.text)
        # Records a measure metric to be sent as telemetry (customMetrics)
        mmap.measure_int_put(request_measure, 1)
        mmap.record(tmap)
    except Exception:
        logger.exception("ERROR: Input length too long.")
        return make_response("ERROR: Input length too long.", 500)
    return make_response("Successfully added task.", 200)


@app.route('/complete/task/<id>', methods=['POST'])
def complete_task(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    logger.warn("Marked complete: " + todo.text)
    return make_response("Success", 200)


@app.route('/save/tasks', methods=['POST'])
def save_tasks():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    incomplete.extend(complete)
    url = "http://localhost:5001/api/save"
    entries = ["Id: " + str(entry.id) + " Task: " + entry.text + " Complete: " + str(entry.complete) \
        for entry in incomplete]
    response = requests.post(url=url, data=json.dumps(entries))
    if response.ok:
        logger.warn("Todo saved to file.")
        return make_response("Todo saved to file.", 200)
    else:
        logger.error(response.reason)
        return make_response("Exception occurred while saving.", 500)
    return redirect('/')