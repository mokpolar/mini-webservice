from flask import Flask, Blueprint, request, render_template

page_abtest = Blueprint('page', __name__)

@page_abtest.route('/test')
def test():
    return render_template('page_a.html')