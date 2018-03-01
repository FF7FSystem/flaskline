from flask import render_template, url_for, redirect, abort
from app import app, db
from termcolor import colored

@app.errorhandler(404)
def not_found_error(error):
    print(colored('Запуск функции not_found_error','red', attrs=['bold']))
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    print(colored('Запуск функции internal_error','red', attrs=['bold']))
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    print(colored('Запуск функции request_entity_too_large','red', attrs=['bold']))
    print(error.name, error.code)
    return render_template('413.html'), 413