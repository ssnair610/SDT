from flask import Flask ,redirect,render_template,request,json
import subprocess
import os

__home__ = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fileupload',methods=['POST'])
def fileupload():
    uploaded_file = request.files['file']
    uploaded_file.save(os.path.join(f'{__home__}/client-side/outbound/container', str(uploaded_file.filename)))
    data = request.form

    with open(f'{__home__}/client-side/outbound/algorithm contract.json', 'w') as alg_contract_file:
        json.dump(data, alg_contract_file, indent=4)

    subprocess.call(("python", "-u", f"{__home__}/client-side/talk.py"))

    return redirect('/summary')

@app.route('/summary')
def summary():
    summaryHTML = ''
    with open(f'{__home__}/templates/summary.html', 'rt') as source_file:
        summaryHTML = '\r\n'.join(source_file.readlines())
    return summaryHTML


if __name__ == "__main__":
    app.run(debug=False)