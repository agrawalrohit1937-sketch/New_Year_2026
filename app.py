from flask import Flask, render_template, request
import pickle
import numpy as np
import os
import random

app = Flask(__name__)

# --- LOAD MODEL ---
model_path = 'resolution_model.pkl'
model = None

if os.path.exists(model_path):
    with open(model_path, 'rb') as file:
        data = pickle.load(file)
        model = data['model']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            name = request.form.get('name', 'User')
            gender = int(request.form['gender']) # 0=Female, 1=Male
            res_type_raw = request.form['resolution'] 
            
            willpower = int(request.form['willpower'])
            laziness = int(request.form['laziness'])
            social_media = float(request.form['social_media'])
            friends = int(request.form['friends_support'])

            # --- SCORE GENERATION (Fake it to make them happy!) ---
            # Hum random use karenge taaki score hamesha alag aaye, par high rahe.
            base_score = random.randint(70, 95)
            
            # Boost logic
            if willpower > 7: base_score += 5
            if laziness < 4: base_score += 5

            score = min(99, base_score) # Cap at 99%

            # --- 🔮 GENDER SPECIFIC RESULTS 🔮 ---
            
            title = ""
            msg = ""
            tip = ""
            icon = ""
            theme_color = "" # CSS Background for result

            # ====== 🎀 GIRL WORLD (Female) ======
            if gender == 0:
                theme_color = "linear-gradient(135deg, #ffdde1 0%, #ee9ca7 100%)" # Soft Pink Gradient
                
                # 💘 LOVE
                if 'Relationship' in res_type_raw or 'Ex' in res_type_raw:
                    icon = "💖"
                    title = "Future Wifey Energy 💍"
                    msg = "OMG! Your aura is radiating pure LOVE right now. You don't chase, you attract! 💅"
                    tip = "💡 Tip: Wear pink tomorrow. Someone is going to confess their feelings. 🤫"
                    score = max(85, score) # Girls ko love mein high score chahiye

                # 💸 MONEY
                elif 'Business' in res_type_raw or 'Money' in res_type_raw:
                    icon = "🥂"
                    title = "Rich Mom Energy 💸"
                    msg = "You are entering your 'Lucky Girl' era. Money is literally flowing towards you!"
                    tip = "💡 Tip: Start visualizing your dream car. It's closer than you think. 🚗"

                # 💪 FITNESS
                else:
                    icon = "🧘‍♀️"
                    title = "Pilates Princess 🎀"
                    msg = "Glowing skin, toned body, and peace of mind. You are becoming THAT girl."
                    tip = "💡 Tip: Drink your water and take a cute mirror selfie. You look good! 📸"


            # ====== ⚡ BOY WORLD (Male) ======
            else:
                theme_color = "linear-gradient(135deg, #141E30 0%, #243B55 100%)" # Dark Blue/Black Gradient
                
                # 💘 LOVE
                if 'Relationship' in res_type_raw or 'Ex' in res_type_raw:
                    icon = "👑"
                    title = "The King 🗿"
                    msg = "Stop worrying about her. Build your empire and she will come running."
                    tip = "💡 Tip: Focus on your purpose. Women follow success, not desperation. 🚀"

                # 💸 MONEY
                elif 'Business' in res_type_raw or 'Money' in res_type_raw:
                    icon = "🦁"
                    title = "Top G Mindset 🏆"
                    msg = "You are dangerous right now. The matrix cannot stop you. Pure dominance."
                    tip = "💡 Tip: Work in silence today. Let your Lamborghini make the noise later. 🏎️"
                    score = max(88, score) # Boys ko money mein high score chahiye

                # 💪 FITNESS
                else:
                    icon = "🦍"
                    title = "Demon Back Loading... 💪"
                    msg = "Light weight, baby! You are turning into a beast. Respect is earned in the gym."
                    tip = "💡 Tip: Add 5kg more to your lift today. You are stronger than you think. 🔥"

            return render_template('result.html', name=name, score=score, title=title, msg=msg, tip=tip, color_bg=theme_color, icon=icon, gender=gender)

        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
