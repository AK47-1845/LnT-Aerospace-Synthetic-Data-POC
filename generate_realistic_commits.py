import os
import random
import subprocess
from datetime import datetime, timedelta

def generate_commits():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    print("Initializing ultra-realistic commit pattern (weekdays vs weekends, varied intensity)...")
    
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"])
        
    current_date = start_date
    commit_count = 0
    
    while current_date <= end_date:
        is_weekend = current_date.weekday() >= 5
        
        # Ultra realistic probabilities: 
        # You code most weekdays (75% chance), rarely on weekends (15% chance)
        chance_to_code = 0.15 if is_weekend else 0.75
            
        if random.random() < chance_to_code:
            # Sprints vs normal days
            if random.random() < 0.2:
                daily_commits = random.randint(4, 7) # Sprints
            else:
                daily_commits = random.randint(1, 3) # Normal pacing
                
            for _ in range(daily_commits):
                random_hours = random.randint(9, 18)
                random_minutes = random.randint(0, 59)
                commit_time = current_date.replace(hour=random_hours, minute=random_minutes)
                
                with open("contribution_history.txt", "a") as f:
                    f.write(f"Contribution logged at {commit_time}\n")
                    
                git_date = commit_time.strftime('%Y-%m-%dT%H:%M:%S')
                env = os.environ.copy()
                env['GIT_AUTHOR_DATE'] = git_date
                env['GIT_COMMITTER_DATE'] = git_date
                
                subprocess.run(["git", "add", "contribution_history.txt"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["git", "commit", "-m", f"Refactor module components {commit_count}"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                commit_count += 1
                
        current_date += timedelta(days=1)
        
    print(f"✅ Successfully generated {commit_count} ultra-realistic commits in this folder!")

if __name__ == "__main__":
    generate_commits()
