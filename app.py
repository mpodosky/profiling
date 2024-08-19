from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load data from the JSON file
with open('data/adjustments.json', 'r') as f:
    data = json.load(f)

# List of Strengths/Interests and Hobbies
strengths_list = [
    "Creative thinking", "Problem-solving", "Empathy", "Resilience", "Curiosity", "Teamwork", "Leadership", 
    "Listening", "Public speaking", "Critical thinking", "Innovation", "Kindness", "Honesty", "Responsibility",
    "Adaptability", "Independence", "Determination", "Fairness", "Respectfulness", "Collaboration", "Compassion",
    "Cultural awareness", "Patience", "Enthusiasm", "Organizational skills", "Attention to detail",
    "Enthusiasm for learning", "Self-discipline", "Time management", "Resourcefulness", "Sense of humor", 
    "Optimism", "Self-awareness", "Emotional intelligence", "Artistic skills", "Musical talent", "Physical fitness",
    "Sportsmanship", "Environmental awareness", "Reading comprehension", "Writing ability", "Mathematical thinking",
    "Scientific curiosity", "Technological literacy", "Digital creativity", "Practical skills", 
    "Cultural heritage knowledge", "Problem identification", "Conflict resolution", "Social skills"
]

hobbies_list = [
    "Drawing", "Painting", "Playing a musical instrument", "Singing", "Dancing", "Writing stories", "Reading books",
    "Acting/Drama", "Gardening", "Cooking/Baking", "Playing sports (e.g., soccer, cricket)", "Cycling", 
    "Skateboarding", "Playing video games", "Coding", "Building with LEGO", "Photography", "Birdwatching", 
    "Fishing", "Camping", "Hiking", "Collecting (e.g., stamps, coins)", "Model building", "Woodworking", "Origami",
    "Crafting", "Knitting", "Sewing", "Astronomy", "Puzzle solving (e.g., jigsaw puzzles)", "Playing chess", 
    "Playing board games", "Swimming", "Surfing", "Snorkeling", "Playing with pets", "Volunteering", "Nature walks",
    "Beachcombing", "Exploring rock pools", "Bushwalking", "Birdwatching", "Playing in a band", "Acting in school plays",
    "Participating in school clubs", "Rollerblading", "Participating in scouts/guides", "Making YouTube videos",
    "Blogging or journaling", "Practicing martial arts (e.g., karate, judo)"
]

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/selection', methods=['GET', 'POST'])
def selection():
    if request.method == 'POST':
        strengths = request.form.getlist('strengths')
        hobbies = request.form.getlist('hobbies')
        
        other_strength = request.form.get('other_strength')
        if 'other-strength' in strengths and other_strength:
            strengths.remove('other-strength')
            strengths.append(other_strength)

        other_hobby = request.form.get('other_hobby')
        if 'other-hobby' in hobbies and other_hobby:
            hobbies.remove('other-hobby')
            hobbies.append(other_hobby)
        
        return redirect(url_for('generate_profile', strengths=strengths, hobbies=hobbies))
    
    return render_template('selection.html', strengths=strengths_list, hobbies=hobbies_list)

@app.route('/profile', methods=['GET', 'POST'])
def generate_profile():
    if request.method == 'POST':
        strengths = request.form.getlist('strengths')
        hobbies = request.form.getlist('hobbies')
        return redirect(url_for('index', strengths=strengths, hobbies=hobbies))
    else:
        strengths = request.args.getlist('strengths')
        hobbies = request.args.getlist('hobbies')
        return render_template('profile.html', strengths=strengths, hobbies=hobbies)

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_strengths = request.form.getlist('strengths')
        selected_needs = request.form.getlist('needs')

        adjustments = []
        for category, details in data.items():
            for strength in selected_strengths:
                if strength in details['adjustments']:
                    adjustments.extend(details['adjustments'][strength])
            for need in selected_needs:
                if need in details['adjustments']:
                    adjustments.extend(details['adjustments'][need])

        adjustments = list(set(adjustments))

        return render_template('results.html', strengths=selected_strengths, needs=selected_needs, adjustments=adjustments, data=data)
    else:
        strengths = request.args.getlist('strengths')
        hobbies = request.args.getlist('hobbies')
        return render_template('index.html', strengths=strengths, hobbies=hobbies, data=data)

@app.route('/adjustments_needs', methods=['POST'])
def adjustments_needs():
    selected_strengths = request.form.getlist('strengths')
    selected_needs = request.form.getlist('needs')

    adjustments = []
    for category, details in data.items():
        for strength in selected_strengths:
            if strength in details['adjustments']:
                adjustments.extend(details['adjustments'][strength])
        for need in selected_needs:
            if need in details['adjustments']:
                adjustments.extend(details['adjustments'][need])

    adjustments = list(set(adjustments))

    return render_template('results.html', strengths=selected_strengths, needs=selected_needs, adjustments=adjustments, data=data)

if __name__ == '__main__':
    app.run(debug=True)
