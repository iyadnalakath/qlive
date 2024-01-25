from rest_framework import serializers
from .models import Subject,Teachers

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]


class TeacherSerializer(serializers.ModelSerializer):
    total_rating = serializers.SerializerMethodField()
    subject_name = serializers.StringRelatedField(source="subject", many=True, read_only=True)
    # roll_no = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = Teachers
        fields = [
            "id",
            "teacher_name",
            "roll_no",
            "subject",
            "subject_name", 
            "whatsapp_no",
            "email",
            "experience",
            "date",
            "remuneration_min",
            "remuneration_max",
            "video_link",
            "bank_acc_holder_name",
            "bank_name",
            "branch",
            "ifsc_code",
            "about",
            "remark",
            "qualification",
            "demo_rating",
            "english_fluency",
            "interview_rating",
            "total_rating",
        ]
    

    def get_total_rating(self, obj):

        experience_rating = obj.experience
        english_fluency_rating = obj.english_fluency
        interview_rating = obj.interview_rating

 
        rating_mapping = {
            '5+ Year': 5,
            '3+ Year': 4.5,
            '1+ Year': 4,
            '<1 Year': 3,
            '100%': 5,
            '90%': 4.5,
            '80%': 4,
            'Below 80%': 3,
        }

        total_rating = (
            rating_mapping.get(experience_rating, 0) +
            rating_mapping.get(english_fluency_rating, 0) +
            rating_mapping.get(interview_rating, 0)
        ) / 3

        return total_rating
    
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['subject_name'] = [subject.name for subject in instance.subject.all()]
        return ret
    

class SimpleTeacherSerializer(serializers.ModelSerializer):
    total_rating = serializers.SerializerMethodField()

    class Meta:
        model = Teachers
        fields = [
            "id",
            "teacher_name",
            "roll_no",
            "total_rating",
            "about",
        ]


    def get_total_rating(self, obj):

        experience_rating = obj.experience
        english_fluency_rating = obj.english_fluency
        interview_rating = obj.interview_rating

 
        rating_mapping = {
            '5+ Year': 5,
            '3+ Year': 4.5,
            '1+ Year': 4,
            '<1 Year': 3,
            '100%': 5,
            '90%': 4.5,
            '80%': 4,
            'Below 80%': 3,
        }

        total_rating = (
            rating_mapping.get(experience_rating, 0) +
            rating_mapping.get(english_fluency_rating, 0) +
            rating_mapping.get(interview_rating, 0)
        ) / 3

        return total_rating