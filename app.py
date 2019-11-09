from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import requests
import json
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'


"""
Test send POST request

Requirement:
* header add
* send json content

"""
@app.route('/test-post')
def test_post():
    r = request.post('http://localhost:5000/send-post',
                     params={'q': 'flask is so amazing'}, headers)
    return 'Result'

@app.route('/bokeh')
def bokeh():

    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    fig = figure(plot_width=600, plot_height=600)
    fig.vbar(
        x=[1, 2, 3, 4],
        width=0.5,
        bottom=0,
        top=[1.7, 2.2, 4.6, 3.9],
        color='navy'
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

@app.route("/check")
def check():
    url = 'http://localhost:5000/api/check'
    headers = {'Content-Type': 'application/json', 'Authorization': 'test'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    response = json.dumps(response.text, sort_keys = True,
                          indent = 4, separators = (',', ': '))
    return render_template(
        'index.html',
        response=response,
    )

if __name__ == '__main__':
    app.run(debug=True)