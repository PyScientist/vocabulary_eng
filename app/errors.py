from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    print('error 400')
    app.logger.info('Error 400 occurred')
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.info('Error 500 occurred')
    return render_template('500.html'), 500
