#!/usr/bin/env python3
"""
Test script for Resume Management API
Run this in a separate terminal while Django server is running
"""

import requests
import json
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api"

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}📌 {text}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ️ {text}{RESET}")

# Create a test resume file
def create_test_file():
    filename = "test_resume.txt"
    content = """MARY RIYA TERRANCE
Full-stack Developer | Cloud & DevOps Engineer

Skills: Python, Django, Docker, AWS, Linux, HTML, CSS
Experience: Fresher
Education: B.Tech Computer Science
"""
    with open(filename, 'w') as f:
        f.write(content)
    print_info(f"Created test file: {filename}")
    return filename

print_header("🚀 TESTING RESUME MANAGEMENT API ON UBUNTU")
print_info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print_info(f"Platform: Ubuntu Linux")

# Test 1: Health Check
print_header("1️⃣ TESTING HEALTH ENDPOINT")
try:
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print_success(f"Health check passed! Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print_error(f"Health check failed! Status: {response.status_code}")
except Exception as e:
    print_error(f"Connection failed: {e}")
    print_info("Make sure Django server is running: python manage.py runserver")
    exit(1)

# Test 2: Create Resume
print_header("2️⃣ TESTING RESUME CREATION WITH FILE UPLOAD")

test_file = create_test_file()

url = f"{BASE_URL}/resumes"
files = {
    'resume_file': ('resume.txt', open(test_file, 'rb'), 'text/plain')
}
data = {
    'full_name': 'Mary Riya Terrance',
    'dob': '2002-05-15',
    'contact_number': '9876543210',
    'contact_address': 'Kollam, Kerala, India - 691012',
    'education_qualification': 'B.Tech Computer Science and Engineering',
    'graduation_year': '2025',
    'years_of_experience': '0',
    'skill_set': 'Python,Django,Docker,AWS,Linux,HTML,CSS,JavaScript'
}

try:
    response = requests.post(url, data=data, files=files)
    if response.status_code == 201:
        print_success("Resume created successfully!")
        result = response.json()
        print(f"📋 Resume Data:")
        print(f"   ID: {GREEN}{result['id']}{RESET}")
        print(f"   Name: {result['full_name']}")
        print(f"   Category: {YELLOW}{result['technology_category']}{RESET}")
        print(f"   Skills: {', '.join(result['skill_set'])}")
        
        # Save ID for later tests
        resume_id = result['id']
    else:
        print_error(f"Creation failed! Status: {response.status_code}")
        print(f"Error: {response.json()}")
        exit(1)
except Exception as e:
    print_error(f"Error: {e}")
    exit(1)

# Test 3: Get All Resumes
print_header("3️⃣ TESTING GET ALL RESUMES")
try:
    response = requests.get(f"{BASE_URL}/resumes/")
    if response.status_code == 200:
        resumes = response.json()
        print_success(f"Found {len(resumes)} resumes")
        for i, resume in enumerate(resumes, 1):
            print(f"   {i}. {resume['full_name']} - {resume['technology_category']}")
    else:
        print_error(f"Failed! Status: {response.status_code}")
except Exception as e:
    print_error(f"Error: {e}")

# Test 4: Filter by Skill
print_header("4️⃣ TESTING FILTER BY SKILL")
try:
    response = requests.get(f"{BASE_URL}/resumes/?skill=python")
    if response.status_code == 200:
        resumes = response.json()
        print_success(f"Found {len(resumes)} resumes with Python skill")
    else:
        print_error(f"Failed! Status: {response.status_code}")
except Exception as e:
    print_error(f"Error: {e}")

# Test 5: Get Specific Resume
print_header("5️⃣ TESTING GET RESUME BY ID")
try:
    response = requests.get(f"{BASE_URL}/resumes/{resume_id}")
    if response.status_code == 200:
        print_success(f"Found resume with ID: {resume_id}")
    else:
        print_error(f"Resume not found!")
except Exception as e:
    print_error(f"Error: {e}")

# Test 6: Delete Resume
print_header("6️⃣ TESTING DELETE RESUME")
try:
    response = requests.delete(f"{BASE_URL}/resumes/{resume_id}/delete")
    if response.status_code == 204:
        print_success(f"Resume deleted successfully!")
    else:
        print_error(f"Delete failed! Status: {response.status_code}")
except Exception as e:
    print_error(f"Error: {e}")

# Test 7: Verify Deletion
print_header("7️⃣ VERIFYING DELETION")
try:
    response = requests.get(f"{BASE_URL}/resumes/{resume_id}")
    if response.status_code == 404:
        print_success("Confirmed: Resume no longer exists (404 Not Found)")
    else:
        print_error(f"Unexpected response: {response.status_code}")
except Exception as e:
    print_error(f"Error: {e}")

# Cleanup
if os.path.exists(test_file):
    os.remove(test_file)

print_header("🏁 TESTING COMPLETE")
print_success("All tests passed!")

