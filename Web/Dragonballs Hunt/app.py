from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/robots.txt')
def robots():
    robots_content = """User-agent: *
Disallow: /characters/dragonball6/
# Part 5: 3lC0mE_"""
    response = make_response(robots_content)
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.route('/characters/dragonball6/')
def dragonball6():
    return render_template('dragonball6.html')

@app.route('/characters/dragonball6/vegeta/')
def vegeta():
    response = make_response(render_template('vegeta.html'))
    response.set_cookie('part7🟠⭐⭐⭐⭐⭐⭐⭐', 'TEaM!}')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20001, debug=False)
