from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
import uuid
from datetime import datetime
from .serializers import ResumeSerializer
from .utils import (
    get_all_resumes, get_resume_by_id, 
    create_resume, delete_resume, categorize_by_skills
)

# Health check endpoint
@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Resume Management API',
        'server': 'Django on Ubuntu'
    }, status=status.HTTP_200_OK)

# Create resume with file upload
@api_view(['POST'])
def create_resume_api(request):
    try:
        print("📥 Received resume creation request")  # Debug
        
        # Handle file upload
        resume_file = request.FILES.get('resume_file')
        
        # Get other data from request
        data = request.data.dict() if hasattr(request.data, 'dict') else request.data
        
        # Parse skill_set (comma-separated string to list)
        if 'skill_set' in data and isinstance(data['skill_set'], str):
            data['skill_set'] = [s.strip() for s in data['skill_set'].split(',')]
            print(f"📋 Parsed skills: {data['skill_set']}")
        
        # Validate data
        serializer = ResumeSerializer(data=data)
        if serializer.is_valid():
            print("✅ Validation passed")
            
            # Save file if provided
            file_path = None
            if resume_file:
                # Generate unique filename
                file_extension = os.path.splitext(resume_file.name)[1]
                file_name = f"{uuid.uuid4()}{file_extension}"
                file_path = os.path.join('media/resumes', file_name)
                
                # Save file
                with open(file_path, 'wb+') as destination:
                    for chunk in resume_file.chunks():
                        destination.write(chunk)
                print(f"📄 File saved: {file_path}")
            
            # Prepare resume data
            resume_data = serializer.validated_data
            resume_data['skill_set'] = data['skill_set']  # Use parsed list
            resume_data['technology_category'] = categorize_by_skills(resume_data['skill_set'])
            resume_data['resume_file_path'] = file_path if file_path else None
            
            print(f"🏷️ Category: {resume_data['technology_category']}")
            
            # Store in cache
            created_resume = create_resume(resume_data)
            
            return Response(created_resume, status=status.HTTP_201_CREATED)
        else:
            print(f"❌ Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# List all resumes with filters
@api_view(['GET'])
def list_resumes(request):
    resumes = get_all_resumes()
    print(f"📋 Found {len(resumes)} total resumes")
    
    # Get filter parameters
    skill = request.query_params.get('skill')
    experience = request.query_params.get('experience')
    graduation_year = request.query_params.get('graduation_year')
    technology = request.query_params.get('technology')
    
    # Apply filters
    filtered = []
    for resume in resumes:
        include = True
        
        if skill and include:
            skill_lower = skill.lower()
            resume_skills = [s.lower() for s in resume.get('skill_set', [])]
            if not any(skill_lower in s for s in resume_skills):
                include = False
        
        if experience and include:
            try:
                if resume.get('years_of_experience') != int(experience):
                    include = False
            except:
                pass
        
        if graduation_year and include:
            try:
                if resume.get('graduation_year') != int(graduation_year):
                    include = False
            except:
                pass
        
        if technology and include:
            if resume.get('technology_category', '').lower() != technology.lower():
                include = False
        
        if include:
            filtered.append(resume)
    
    print(f"🔍 After filters: {len(filtered)} resumes")
    return Response(filtered)

# Get single resume
@api_view(['GET'])
def get_resume(request, resume_id):
    print(f"🔍 Looking for resume: {resume_id}")
    resume = get_resume_by_id(resume_id)
    if not resume:
        return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(resume)

# Delete resume
@api_view(['DELETE'])
def delete_resume_api(request, resume_id):
    print(f"🗑️ Deleting resume: {resume_id}")
    resume = get_resume_by_id(resume_id)
    if not resume:
        return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Delete file if exists
    file_path = resume.get('resume_file_path')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
        print(f"📄 Deleted file: {file_path}")
    
    # Delete from cache
    delete_resume(resume_id)
    
    return Response(status=status.HTTP_204_NO_CONTENT)

# Root endpoint
@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Resume Management API',
        'author': 'Mary Riya Terrance',
        'server': 'Ubuntu Linux',
        'endpoints': {
            'GET /api/health': 'Health check',
            'POST /api/resumes': 'Upload resume with details',
            'GET /api/resumes/': 'List all resumes',
            'GET /api/resumes/{id}': 'Get resume by ID',
            'DELETE /api/resumes/{id}/delete': 'Delete resume',
            'GET /api/resumes/?skill=python': 'Filter resumes'
        }
    })
