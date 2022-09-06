from crypt import methods
import unittest
from flask import request, make_response, redirect, escape, render_template, session, url_for, flash
from flask_login import login_required, current_user

from app.firestore_service import delete_todo, get_todos, put_todo, update_todo
from app import create_app
from app.forms import DeleteTodoForm, TodoForm, UpdateTodoForm

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

# Si no se encuentra la ruta usa esta función
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr # Detecta la ip desde donce se hace la petición

    response = make_response(redirect('/hello'))
    # response.set_cookie('user_ip', user_ip)
    session['user_ip'] = user_ip

    # Disparar error 500 para probar el manejador del error
    # No olvidar cambiar el modo debug a false app.run(debug=False)
    # raise(Exception('500 error'))
    return response

@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    # user_ip = request.cookies.get('user_ip')
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_todo_form = DeleteTodoForm()
    update_todo_form = UpdateTodoForm()

    # Por recomendación de otra persona para evitar la vulnerabilidad a XSS hacer lo siguiente 
    # user_ip = escape(user_ip)
    
    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
        'delete_todo_form': delete_todo_form,
        'update_todo_form': update_todo_form
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)

        flash('Tarea creada con éxito')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id
    
    update_todo(user_id=user_id, todo_id=todo_id, done=done)
    return redirect(url_for('hello'))

# if __name__ == '__main__':
#     app.run('localhost', 5000, debug=True)

