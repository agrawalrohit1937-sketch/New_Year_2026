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
            gender = int(request.form['gender'])
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

            # Prediction
            if model:
                res_type_num = resolution_mapping.get(res_type_str, 0)
                features = np.array([[gender, age, res_type_num, relationship, attendance, stress, willpower, laziness, social_media, friends, distance]])
                prediction = model.predict(features)
                days = int(prediction[0])
            else:
                days = random.randint(10, 365)
            
            days = max(5, min(365, days))

            # --- 🎀 FAIRYCORE RESULT LOGIC 🎀 ---
            
            # Default
            title = "Dreamy Vibes ✨"
            msg = "Your energy is shifting. Good things are coming."
            # Gradient: Soft Pink to Lavender
            color_bg = "linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #a18cd1 100%)"
            # Text Color for Emphasis
            text_accent = "#ff6b6b"
            icon = "🔮"

            # 1. Love & Relationship
            if res_type_str == 'Find a Relationship':
                if days < 30:
                    title = "Self-Love Era 🩰"
                    msg = "You are the prize. Focus on your glow up, not a relationship!"
                    color_bg = "linear-gradient(135deg, #fad0c4 0%, #ffd1ff 100%)" # Peach Pink
                    text_accent = "#ff9f43"
                    icon = "🎀"
                elif days < 90:
                    title = "Lucky Girl Syndrome 🍀"
                    msg = "Manifesting a cute text back? The universe says YES."
                    color_bg = "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)" # Purple Pink
                    text_accent = "#9b59b6"
                    icon = "💌"
                else:
                    title = "Main Character Energy 👑"
                    msg = "Your aura is pink and glowing. Love is literally around the corner."
                    color_bg = "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)" # Mint Blue
                    text_accent = "#00b894"
                    icon = "💍"

            # 2. Gym / Diet
            elif res_type_str in ['Gym/Fitness', 'Healthy Diet']:
                if laziness > 6:
                    title = "Sleeping Beauty 😴"
                    msg = "Rest is productive too! But try to move your body a little."
                    color_bg = "linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)" # Periwinkle
                    text_accent = "#6c5ce7"
                    icon = "🧸"
                else:
                    title = "Pilates Princess 🧘‍♀️"
                    msg = "Drinking water, minding my business, and glowing up."
                    color_bg = "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)" # Sky Blue
                    text_accent = "#0984e3"
                    icon = "✨"

            # 3. Money / Career
            elif res_type_str in ['Save Money', 'Start a Business', 'Academic Comeback']:
                title = "That Girl 💅"
                msg = "Organized, wealthy, and successful. Your vision board is real."
                color_bg = "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)" # Mint Green
                text_accent = "#00b894"
                icon = "💸"

            # 4. Ex / Healing
            elif res_type_str == 'Stop Stalking Ex':
                title = "Unbothered Queen 💅"
                msg = "Blocking negativity and attracting peace. You are doing amazing."
                color_bg = "linear-gradient(to top, #fff1eb 0%, #ace0f9 100%)" # Soft White Blue
                text_accent = "#74b9ff"
                icon = "🕊️"

            return render_template('result.html', days=days, name=name, title=title, msg=msg, color_bg=color_bg, text_accent=text_accent, icon=icon)

        except Exception as e:
            return str(e)

if __name__ == '__main__':
    app.run(debug=True)
