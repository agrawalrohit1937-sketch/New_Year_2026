import pandas as pd
import numpy as np

# Rows
num_rows = 15000 
np.random.seed(42)

resolutions = [
    'Gym/Fitness', 'Learn Coding', 'Save Money', 'Quit Smoking', 
    'Read More Books', 'Healthy Diet', 'Find a Relationship', 
    'Start a Business', 'Stop Procrastination', 'Academic Comeback', 'Stop Stalking Ex'
]

# Random Inputs
gender = np.random.choice([0, 1], num_rows) # 0=Female, 1=Male
age = np.random.randint(18, 30, num_rows)
resolution_type = np.random.choice(resolutions, num_rows)
willpower = np.random.randint(1, 11, num_rows)
laziness = np.random.randint(1, 11, num_rows)
social_media = np.round(np.random.uniform(1, 12, num_rows), 1)
friends = np.random.choice([0, 1, 2], num_rows) # 0=Toxic, 1=Normal, 2=Besties
distance = np.round(np.random.uniform(1, 15, num_rows), 1)
relationship_status = np.random.choice([0, 1, 2], num_rows) 
attendance = np.random.randint(20, 100, num_rows)
stress = np.random.randint(1, 11, num_rows)

# --- STRICT LOGIC FOR HIGH ACCURACY ---
days_lasted = []

for i in range(num_rows):
    res = resolution_type[i]
    days = 0 # Start
    
    # 1. Base Score (Willpower vs Laziness)
    days = (willpower[i] * 5) - (laziness[i] * 3)
    
    # 2. Category Specific Logic (Strong Patterns)
    
    # RELATIONSHIP: Social Media doesn't hurt much, Friends matter
    if res == 'Find a Relationship':
        if friends[i] == 2: days += 20 # Friends help set you up
        elif friends[i] == 0: days -= 10 # Toxic friends block you
        if social_media[i] > 5: days += 5 # Sliding into DMs helps
        
    # ACADEMIC / CODING: Attendance & Social Media matter
    elif res in ['Academic Comeback', 'Learn Coding']:
        if attendance[i] < 75: days -= 30 # Detained likely
        if social_media[i] > 4: days -= 15 # Distraction
        
    # GYM: Distance & Laziness matter
    elif res == 'Gym/Fitness':
        if distance[i] > 8: days -= 20 # Too far
        if laziness[i] > 7: days = 2 # Lazy people quit fast
        
    # STALKING EX: Social Media is enemy
    elif res == 'Stop Stalking Ex':
        if social_media[i] > 3: days -= 25 # Insta = Relapse
        if relationship_status[i] == 0: days -= 10 # Single = Stalking
        
    # BUSINESS: Laziness kills it
    elif res == 'Start a Business':
        if laziness[i] > 4: days = 5 # Business hard hai
        
    # 3. Add randomness (Noise)
    days += np.random.randint(-3, 5)
    
    # Clamp (0 to 100 days)
    days = max(0, min(100, int(days)))
    days_lasted.append(days)

# Save
df = pd.DataFrame({
    'Gender': gender,
    'Age': age,
    'Resolution_Type': resolution_type,
    'Relationship_Status': relationship_status,
    'Attendance_Perc': attendance,
    'Stress_Level': stress,
    'Willpower': willpower,
    'Laziness': laziness,
    'Social_Media': social_media,
    'Friends': friends,
    'Distance': distance,
    'Days_Lasted': days_lasted
})

df.to_csv('resolution_data.csv', index=False)
print("✅ HIGH ACCURACY Dataset Created.")