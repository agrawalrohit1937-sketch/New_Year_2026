import pandas as pd
import numpy as np

# --- BIG DATASET (15,000 Rows) ---
num_rows = 15000 
np.random.seed(42)

# Categories
resolutions = [
    'Gym/Fitness', 'Learn Coding', 'Save Money', 'Quit Smoking', 
    'Read More Books', 'Healthy Diet', 'Find a Relationship', 
    'Start a Business', 'Stop Procrastination', 'Academic Comeback', 'Stop Stalking Ex'
]

# --- Generate Data ---
gender = np.random.choice(['Male', 'Female'], num_rows) # NEW COLUMN
age = np.random.randint(18, 28, num_rows)
resolution_type = np.random.choice(resolutions, num_rows)
willpower = np.random.randint(1, 11, num_rows)
laziness = np.random.randint(1, 11, num_rows)
social_media = np.round(np.random.uniform(1, 14, num_rows), 1)
friends = np.random.choice([0, 1, 2], num_rows, p=[0.3, 0.5, 0.2]) # 0=Toxic, 1=Neutral, 2=Good
distance = np.round(np.random.uniform(0.5, 20, num_rows), 1)
relationship_status = np.random.choice([0, 1, 2], num_rows) 
attendance = np.random.randint(10, 100, num_rows)
stress_level = np.random.randint(1, 11, num_rows) # NEW COLUMN

# --- Complex Logic for Days Lasted ---
days_lasted = []

for i in range(num_rows):
    res = resolution_type[i]
    
    # Base Calculation
    score = (willpower[i] * 3) - (laziness[i] * 2) - (social_media[i] * 1.5) - (stress_level[i] * 1)
    
    # Gender Logic (Stereotypes for Data Patterns)
    if gender[i] == 'Male' and res == 'Gym/Fitness':
        score += 5 # Boys often stick to gym longer
    if gender[i] == 'Female' and res == 'Healthy Diet':
        score += 5 # Girls often stick to diet longer
        
    # Stress Logic
    if stress_level[i] > 8 and res in ['Quit Smoking', 'Stop Procrastination']:
        score -= 15 # High stress breaks these habits instantly
        
    # Academic Comeback
    if res == 'Academic Comeback':
        if attendance[i] < 50: score -= 25
        elif attendance[i] > 90: score += 15
        
    # Stop Stalking Ex
    if res == 'Stop Stalking Ex':
        if social_media[i] > 6: score -= 20
        if relationship_status[i] == 0: score -= 5
        
    # Start Business
    if res == 'Start a Business':
        if laziness[i] > 4: score -= 20
        
    # Find Relationship
    if res == 'Find a Relationship' and friends[i] == 0:
        score -= 10
        
    # Gym Distance
    if res == 'Gym/Fitness' and distance[i] > 10:
        score -= 12

    # Final Calculation with Noise
    final_days = int(score + np.random.randint(-5, 10))
    final_days = max(0, min(90, final_days)) # 0 to 90 days range
    days_lasted.append(final_days)

# Create DataFrame
df = pd.DataFrame({
    'Gender': gender,                # NEW
    'Age': age,
    'Resolution_Type': resolution_type,
    'Relationship_Status': relationship_status,
    'Attendance_Perc': attendance,
    'Stress_Level': stress_level,    # NEW
    'Willpower': willpower,
    'Laziness': laziness,
    'Social_Media': social_media,
    'Friends': friends,
    'Distance': distance,
    'Days_Lasted': days_lasted
})

df.to_csv('resolution_data.csv', index=False)
print(f"✅ BIG DATASET CREATED: {num_rows} Rows & 12 Columns.")