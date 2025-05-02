from flask import Flask, render_template
import math

app = Flask(__name__)

@app.route('/factorial/<int:num>')
def factorial(num):
    result = math.factorial(num)
    return render_template('result.html', number=num, result=result)

if __name__ == '__main__':
    app.run(debug=True)
