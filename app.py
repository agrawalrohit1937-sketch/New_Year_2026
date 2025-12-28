from flask import Flask, render_template, request
import pickle
import numpy as np
import random

app = Flask(__name__)

with open('resolution_model.pkl', 'rb') as file:
    model = pickle.load(file)

resolution_mapping = {
    'Gym/Fitness': 0, 'Learn Coding': 1, 'Save Money': 2, 'Quit Smoking': 3,
    'Read More Books': 4, 'Healthy Diet': 5, 'Find a Relationship': 6,
    'Start a Business': 7, 'Stop Procrastination': 8, 'Academic Comeback': 9, 'Stop Stalking Ex': 10
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Inputs
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

            res_type_num = resolution_mapping[res_type_str]
            features = np.array([[gender, age, res_type_num, relationship, attendance, stress, willpower, laziness, social_media, friends, distance]])
            prediction = model.predict(features)
            days = int(prediction[0])

            # --- 😂 FUNNY HINGLISH VERDICTS ---
            cause = "Bas mann nahi kiya."
            tip = "Soja bhai."
            color = "#ff4757" # Red

            # --- 1. Find a Relationship (Special Request) ---
            if res_type_str == 'Find a Relationship':
                if days < 10:
                    cause = "Tumhari shakal aur harkatein match nahi kar rahi."
                    tip = "Pehle nahana shuru kar, phir ladki/ladka dhund."
                elif friends == 0:
                    cause = "Tumhare dost hi tumhara katwa rahe hain (Toxic Friends)."
                    tip = "Dost badal, kismat badal jayegi."
                elif relationship == 1:
                    cause = "Pehle wo 'Situationship' wale trauma se toh nikal ja."
                    tip = "Kabir Singh banna band kar."
                else:
                    cause = "Shabash! Mummy bahu/damaad dhundne hi wali thi."
                    tip = "Tinder delete kar aur confidence rakh."

            # --- 2. Stop Stalking Ex ---
            elif res_type_str == 'Stop Stalking Ex':
                if social_media > 3:
                    cause = "Tu phir se uski ID search kar raha hai, jhooth mat bol."
                    tip = "Block button use kar, decoration ke liye nahi hai."
                    days = 0 # Force fail
                else:
                    cause = "Lagta hai self-respect wapas aa gayi."

            # --- 3. Academic Comeback ---
            elif res_type_str == 'Academic Comeback':
                if attendance < 60:
                    cause = f"Attendance {attendance}% hai. HOD tumhara 'Moye Moye' kar dega."
                    tip = "Teacher ke pair pakad le, shayad pass ho jaye."
                else:
                    cause = "Padhne baitha par 5 min baad Reel scroll karne laga."

            # --- 4. Gym/Fitness ---
            elif res_type_str == 'Gym/Fitness':
                if laziness > 7:
                    cause = "Tujhse kambal nahi uthta, dumbbell kya uthega?"
                    tip = "Gym ki fees donation samajh ke bhool ja."
                elif distance > 8:
                    cause = "Gym door hai, aur tu aalsi hai. Khatam, Tata, Bye Bye."

            # --- 5. Start Business ---
            elif res_type_str == 'Start a Business':
                if laziness > 5:
                    cause = "Shark Tank dekh ke Josh aaya tha, ab thanda ho gaya."
                    tip = "Job hi karle, business tere bas ka nahi."

            # --- 6. Generic Roasts ---
            elif social_media > 6:
                cause = "Screen Time: 8 Hours. Future: Andhera."
                tip = "Phone phek de, shayad life ban jaye."
            
            elif stress > 8:
                cause = "Itna stress lega to ganja ho jayega."
                tip = "Chai pi, chill kar."

            # --- Verdict Titles (Funny) ---
            if days < 5: verdict = "Tumse Na Ho Payega 💀"
            elif days < 20: verdict = "Koshish Achi Thi 🤡"
            else: verdict = "System Faad Denge 🔥"

            if days > 25: color = "#2ed573" # Green
            elif days > 7: color = "#ffa502" # Orange

            return render_template('result.html', days=days, verdict=verdict, cause=cause, tip=tip, color=color)

        except Exception as e:
            return str(e)

if __name__ == '__main__':
    app.run(debug=True)