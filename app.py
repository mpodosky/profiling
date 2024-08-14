from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load data from the JSON file
with open('data/adjustments.json', 'r') as f:
    data = json.load(f)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/profile')
def index():
    return render_template('index.html', data=data)

@app.route('/profile', methods=['POST'])
def profile():
    # Print statements for debugging
    print(request.form)  # Print the entire form data

    selected_strengths = request.form.getlist('Speech,-Language,-and-Communication-strengths') + \
                         request.form.getlist('Social,-Emotional,-and-Adaptive-Skills-strengths') + \
                         request.form.getlist('Cognitive-Processing-strengths') + \
                         request.form.getlist('Physical-and-Sensory-Needs-strengths') + \
                         request.form.getlist('Restrictive-and-Repetitive-Behaviors-strengths') + \
                         request.form.getlist('Academic-and-Learning-Supports-strengths')
    
    selected_needs = request.form.getlist('Speech,-Language,-and-Communication-needs') + \
                     request.form.getlist('Social,-Emotional,-and-Adaptive-Skills-needs') + \
                     request.form.getlist('Cognitive-Processing-needs') + \
                     request.form.getlist('Physical-and-Sensory-Needs-needs') + \
                     request.form.getlist('Restrictive-and-Repetitive-Behaviors-needs') + \
                     request.form.getlist('Academic-and-Learning-Supports-needs')

    # Print statements for debugging
    print("Selected Strengths:", selected_strengths)
    print("Selected Needs:", selected_needs)

    adjustments = []

    # Logic to find adjustments based on selected strengths and needs
    for category, details in data.items():
        for strength in selected_strengths:
            if strength in details['adjustments']:
                adjustments.extend(details['adjustments'][strength])
        for need in selected_needs:
            if need in details['adjustments']:
                adjustments.extend(details['adjustments'][need])

    # Remove duplicates
    adjustments = list(set(adjustments))

    # Pass data to the results page
    return render_template('results.html', strengths=selected_strengths, needs=selected_needs, adjustments=adjustments, data=data)

if __name__ == '__main__':
    app.run(debug=True)
