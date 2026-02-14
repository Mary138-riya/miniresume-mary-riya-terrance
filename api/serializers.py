from rest_framework import serializers
import re
from datetime import datetime

class ResumeSerializer(serializers.Serializer):
    # Input fields
    full_name = serializers.CharField(max_length=100)
    dob = serializers.DateField()
    contact_number = serializers.CharField(max_length=15)
    contact_address = serializers.CharField(max_length=500)
    education_qualification = serializers.CharField(max_length=200)
    graduation_year = serializers.IntegerField(min_value=1950, max_value=2030)
    years_of_experience = serializers.IntegerField(min_value=0, max_value=50)
    skill_set = serializers.ListField(child=serializers.CharField())
    
    # Output only fields (read_only)
    id = serializers.CharField(read_only=True)
    resume_file_path = serializers.CharField(read_only=True, required=False)
    technology_category = serializers.CharField(read_only=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    
    # Write only fields (for file upload)
    resume_file = serializers.FileField(write_only=True, required=False)
    
    # Custom validation for phone number
    def validate_contact_number(self, value):
        # Remove spaces, dashes, etc.
        cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
        if not cleaned.isdigit():
            raise serializers.ValidationError("Phone number should contain only digits")
        if len(cleaned) < 10:
            raise serializers.ValidationError("Phone number must have at least 10 digits")
        return value
    
    # Custom validation for DOB and graduation year
    def validate(self, data):
        if 'dob' in data and 'graduation_year' in data:
            dob_year = data['dob'].year
            current_year = datetime.now().year
            if data['graduation_year'] < dob_year + 15:
                raise serializers.ValidationError({
                    "graduation_year": "Graduation year too early based on date of birth"
                })
            if data['graduation_year'] > current_year + 1:
                raise serializers.ValidationError({
                    "graduation_year": "Graduation year cannot be in the distant future"
                })
        return data
