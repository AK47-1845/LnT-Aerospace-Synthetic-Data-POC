import os
import random
import subprocess
from datetime import datetime, timedelta

def generate_commits():
    end_date = datetime.now()
    # User requested starting from March or April 2026 to align with actual repo creation
    start_date = datetime(2026, 4, 1) # April 1, 2026
    
    print(f"Initializing ultra-realistic commit pattern starting strictly from {start_date.strftime('%B %Y')} to avoid timeline ambiguity...")
    
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"])
        
    current_date = start_date
    commit_count = 0
    
    # We need to distribute ~350 commits over ~166 days (April to mid-September). 
    
    while current_date <= end_date:
        is_weekend = current_date.weekday() >= 5
        
        # High intensity since we are packing a year's worth of work into 5.5 months
        chance_to_code = 0.35 if is_weekend else 0.85
            
        if random.random() < chance_to_code:
            # Sprints vs normal days
            if random.random() < 0.25:
                daily_commits = random.randint(5, 8) # Heavy Sprints
            else:
                daily_commits = random.randint(1, 4) # Normal pacing
                
            for _ in range(daily_commits):
                random_hours = random.randint(9, 19)
                random_minutes = random.randint(0, 59)
                commit_time = current_date.replace(hour=random_hours, minute=random_minutes)
                
                with open("contribution_history.txt", "a") as f:
                    f.write(f"Contribution logged at {commit_time}\n")
                    
                git_date = commit_time.strftime('%Y-%m-%dT%H:%M:%S')
                env = os.environ.copy()
                env['GIT_AUTHOR_DATE'] = git_date
                env['GIT_COMMITTER_DATE'] = git_date
                
                subprocess.run(["git", "add", "contribution_history.txt"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["git", "commit", "-m", f"Implement core physical AI features {commit_count}"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                commit_count += 1
                
        current_date += timedelta(days=1)
        
    print(f"Successfully generated {commit_count} ultra-realistic commits starting from April 2026!")

if __name__ == "__main__":
    generate_commits()
