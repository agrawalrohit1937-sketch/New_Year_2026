from flask import Flask, render_template, request
import pickle
import numpy as np
import os
import random

app = Flask(__name__)

# Load Model
model_path = 'resolution_model.pkl'
if os.path.exists(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
else:
    model = None

resolution_mapping = {
    'Find a Relationship': 6, 'Gym/Fitness': 0, 'Learn Coding': 1, 
    'Save Money': 2, 'Quit Smoking': 3, 'Read More Books': 4, 
    'Healthy Diet': 5, 'Start a Business': 7, 'Stop Procrastination': 8, 
    'Academic Comeback': 9, 'Stop Stalking Ex': 10
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            name = request.form.get('name', 'Bestie')
            gender = int(request.form['gender']) # 1 = Male, 0 = Female
            age = int(request.form['age'])
            res_type_str = request.form['resolution_type']
            relationship = int(request.form['relationship'])
            attendance = int(request.form['attendance'])
            stress = int(request.form['stress'])
            willpower = int(request.form['willpower'])
            laziness = int(request.form['laziness'])
            social_media = float(request.form['social_media'])
            friends = int(request.form['friends'])
            distance = float(request.form['distance'])

            # ML Prediction
            if model:
                res_type_num = resolution_mapping.get(res_type_str, 0)
                features = np.array([[gender, age, res_type_num, relationship, attendance, stress, willpower, laziness, social_media, friends, distance]])
                prediction = model.predict(features)
                days = int(prediction[0])
            else:
                days = random.randint(10, 365)
            
            days = max(5, min(365, days))

            # --- 🔮 GENDER SPECIFIC RESULT LOGIC 🔮 ---
            
            # Default
            title = "Dreamy Vibes ✨"
            msg = "Your energy is shifting. Good things are coming."
            color_bg = "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)"
            text_accent = "#9b59b6"
            icon = "🔮"

            # 1. Love & Relationship
            if res_type_str == 'Find a Relationship':
                if days < 30:
                    title = "Lone Wolf Era 🐺" if gender == 1 else "Self-Love Era 🩰"
                    msg = "Focus on your empire right now." if gender == 1 else "You are the prize. Focus on your glow up!"
                    color_bg = "linear-gradient(135deg, #2c3e50 0%, #bdc3c7 100%)" if gender == 1 else "linear-gradient(135deg, #fad0c4 0%, #ffd1ff 100%)"
                    text_accent = "#34495e" if gender == 1 else "#ff9f43"
                    icon = "🔥" if gender == 1 else "🎀"
                elif days < 90:
                    title = "Lover Boy Arc 🌹" if gender == 1 else "Lucky Girl Syndrome 🍀"
                    msg = "Someone is crushing on you hard." if gender == 1 else "Manifesting a cute text back? Universe says YES."
                    color_bg = "linear-gradient(135deg, #16a085 0%, #f4d03f 100%)" if gender == 1 else "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)"
                    text_accent = "#27ae60" if gender == 1 else "#9b59b6"
                    icon = "💌"
                else:
                    title = "King Energy 👑" if gender == 1 else "Main Character Energy 👑"
                    msg = "You attract, you don't chase."
                    color_bg = "linear-gradient(135deg, #00c6ff 0%, #0072ff 100%)" if gender == 1 else "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)"
                    text_accent = "#2980b9" if gender == 1 else "#00b894"
                    icon = "💍"

            # 2. Gym / Diet
            elif res_type_str in ['Gym/Fitness', 'Healthy Diet']:
                if laziness > 6:
                    title = "Rest & Recover 😴"
                    msg = "Even Kings need sleep." if gender == 1 else "Rest is productive too, Queen."
                    color_bg = "linear-gradient(135deg, #bdc3c7 0%, #2c3e50 100%)" if gender == 1 else "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)"
                    text_accent = "#7f8c8d" if gender == 1 else "#6c5ce7"
                    icon = "💤"
                else:
                    title = "Beast Mode 🦁" if gender == 1 else "Pilates Princess 🧘‍♀️"
                    msg = "They ain't ready for your transformation." if gender == 1 else "Drinking water, minding business, glowing up."
                    color_bg = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)" if gender == 1 else "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
                    text_accent = "#16a085" if gender == 1 else "#0984e3"
                    icon = "💪" if gender == 1 else "✨"

            # 3. Money / Career
            elif res_type_str in ['Save Money', 'Start a Business', 'Academic Comeback']:
                title = "Future Millionaire 💸" if gender == 1 else "That Girl 💅"
                msg = "Forbes list is calling your name." if gender == 1 else "Organized, wealthy, and successful."
                color_bg = "linear-gradient(135deg, #f7971e 0%, #ffd200 100%)" if gender == 1 else "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)"
                text_accent = "#d35400" if gender == 1 else "#00b894"
                icon = "🚀" if gender == 1 else "👜"

            # 4. Ex / Healing
            elif res_type_str == 'Stop Stalking Ex':
                title = "GigaChad Mindset 🗿" if gender == 1 else "Unbothered Queen 💅"
                msg = "Focus on the grind, not the past." if gender == 1 else "Blocking negativity and attracting peace."
                color_bg = "linear-gradient(to top, #cfd9df 0%, #e2ebf0 100%)"
                text_accent = "#34495e" if gender == 1 else "#74b9ff"
                icon = "🚫"

            return render_template('result.html', days=days, name=name, title=title, msg=msg, color_bg=color_bg, text_accent=text_accent, icon=icon)

        except Exception as e:
            return str(e)

if __name__ == '__main__':
    app.run(debug=True)
