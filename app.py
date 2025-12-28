from flask import Flask, render_template, request
import pickle
import numpy as np
import random

app = Flask(__name__)

# Load Model
with open('resolution_model.pkl', 'rb') as file:
    model = pickle.load(file)

# --- 1. Final Mapping (Must match Training) ---
resolution_mapping = {
    'Gym/Fitness': 0,
    'Learn Coding': 1,
    'Save Money': 2,
    'Quit Smoking': 3,
    'Read More Books': 4,
    'Healthy Diet': 5,
    'Find a Relationship': 6,
    'Start a Business': 7,
    'Stop Procrastination': 8,
    'Academic Comeback': 9,
    'Stop Stalking Ex': 10
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # --- 1. Get All Inputs (Including New Ones) ---
            gender = int(request.form['gender']) # 1=Male, 0=Female
            age = int(request.form['age'])
            res_type_str = request.form['resolution_type']
            relationship = int(request.form['relationship'])
            attendance = int(request.form['attendance'])
            stress = int(request.form['stress']) # NEW INPUT
            willpower = int(request.form['willpower'])
            laziness = int(request.form['laziness'])
            social_media = float(request.form['social_media'])
            friends = int(request.form['friends'])
            distance = float(request.form['distance'])

            # --- 2. Predict ---
            res_type_num = resolution_mapping[res_type_str]
            
            # Feature Array (Order MUST match the CSV/Training Data exactly)
            # Order: Gender, Age, Res, Rel, Attend, Stress, Will, Lazy, Social, Friends, Dist
            features = np.array([[gender, age, res_type_num, relationship, attendance, stress, willpower, laziness, social_media, friends, distance]])
            
            prediction = model.predict(features)
            days = int(prediction[0])

            # --- 3. SAVAGE ROAST LOGIC ---
            cause = "Unknown reason."
            tip = "Try harder."
            color = "#ff4757" # Red default

            # --- Stress Logic (New) ---
            if stress > 8:
                cause = f"Your stress level is {stress}/10. You need therapy, not a resolution."
                tip = "Go sleep. Just go sleep."
                days = min(days, 5) # High stress kills resolutions fast

            # --- Goal Specific Roasts ---
            
            elif res_type_str == 'Stop Stalking Ex':
                if days < 5:
                    cause = "You checked his/her 'Last Seen' while filling this form."
                    tip = "Block button exists for a reason."
                else:
                    cause = "You created a fake account to stalk. Technically still stalking."

            elif res_type_str == 'Academic Comeback':
                if attendance < 65:
                    cause = f"Your attendance is {attendance}%. Even God cannot save you."
                    tip = "Beg the HOD for mercy."
                else:
                    cause = "You opened the book and posted a story immediately."

            elif res_type_str == 'Start a Business':
                cause = "Watching Shark Tank doesn't make you an Entrepreneur."
                tip = "First finish your assignment, CEO sahab."

            elif res_type_str == 'Find a Relationship':
                if relationship == 1:
                    cause = "You are stuck in a Situationship. You are cooked."
                else:
                    cause = "Your standards are too high for your social skills."

            elif res_type_str in ['Gym/Fitness', 'Healthy Diet']:
                if laziness > 7:
                    cause = "You treat 'Rest Day' as 'Rest Month'."
                    tip = "Walking to the fridge is not cardio."

            elif res_type_str == 'Learn Coding':
                cause = "You spent 3 days setting up VS Code themes and 0 days coding."

            # Verdicts
            if days < 7: verdict = "Cooked Immediately 💀"
            elif days < 21: verdict = "Mid Effort 😐"
            else: verdict = "Main Character Energy ✨"
            
            if days > 20: color = "#2ed573" # Green
            elif days > 7: color = "#ffa502" # Orange

            return render_template('result.html', days=days, verdict=verdict, cause=cause, tip=tip, color=color)

        except Exception as e:
            return str(e)

if __name__ == '__main__':
    app.run(debug=True)
