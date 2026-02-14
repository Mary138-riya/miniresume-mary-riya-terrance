from django.core.cache import cache
import uuid
from datetime import datetime
import os

# Cache keys
RESUME_LIST_KEY = 'resume_list'
RESUME_PREFIX = 'resume_'

def get_all_resumes():
    """Get all resumes from cache"""
    resume_ids = cache.get(RESUME_LIST_KEY, [])
    resumes = []
    for resume_id in resume_ids:
        resume = cache.get(f"{RESUME_PREFIX}{resume_id}")
        if resume:
            resumes.append(resume)
    return resumes

def get_resume_by_id(resume_id):
    """Get single resume by ID"""
    return cache.get(f"{RESUME_PREFIX}{resume_id}")

def create_resume(resume_data):
    """Create new resume in cache"""
    resume_id = str(uuid.uuid4())
    resume_data['id'] = resume_id
    resume_data['created_at'] = datetime.now().isoformat()
    
    # Store in cache
    cache.set(f"{RESUME_PREFIX}{resume_id}", resume_data, timeout=None)
    
    # Add to list
    resume_ids = cache.get(RESUME_LIST_KEY, [])
    resume_ids.append(resume_id)
    cache.set(RESUME_LIST_KEY, resume_ids, timeout=None)
    
    print(f"✅ Created resume with ID: {resume_id}")  # For debugging
    return resume_data

def delete_resume(resume_id):
    """Delete resume from cache"""
    # Remove from list
    resume_ids = cache.get(RESUME_LIST_KEY, [])
    if resume_id in resume_ids:
        resume_ids.remove(resume_id)
        cache.set(RESUME_LIST_KEY, resume_ids, timeout=None)
    
    # Delete from cache
    cache.delete(f"{RESUME_PREFIX}{resume_id}")
    print(f"✅ Deleted resume: {resume_id}")  # For debugging
    return True

def categorize_by_skills(skills):
    """Categorize candidate based on skills"""
    skills_lower = [s.lower() for s in skills]
    
    categories = {
        "Python Developer": ["python", "django", "flask", "fastapi"],
        "Java Developer": ["java", "spring", "j2ee"],
        "Frontend Developer": ["javascript", "react", "angular", "vue", "html", "css"],
        "DevOps Engineer": ["docker", "kubernetes", "jenkins", "aws", "cloud", "devops", "pcf", "cloud foundry"],
        "Data Engineer": ["sql", "database", "etl", "data", "pandas"],
        "Full Stack Developer": ["python", "javascript", "react", "node", "fullstack", "html", "css"]
    }
    
    for category, keywords in categories.items():
        if any(keyword in skills_lower for keyword in keywords):
            return category
    
    return "Other"
