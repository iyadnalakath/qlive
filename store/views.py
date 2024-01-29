from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializer import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.core.exceptions import PermissionDenied
from .filters import TeacherFilter

# Create your views here.


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin", "staff"]:
            subjects = Subject.objects.all()
            subject_count = Subject.objects.count()

            serializer = SubjectListSerializer({
                'subject_count': subject_count,
                'subjects': subjects
            })
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view subjects.")
        
    def retrieve(self, request, *args, **kwargs):
        subject = self.get_object()
        if request.user.role in ["admin", "staff"]:
            serializer = SubjectSerializer(subject)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("You are not allowed to view this object.")

    def create(self, request, *args, **kwargs):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            # print (self.request.user.role
            #     )
            if self.request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        subject = self.get_object()

        try:
            # Trigger pre_delete signal to check association with teachers
            protect_subject_delete(sender=Subject, instance=subject)

            if request.user.role == "admin":
                subject.delete()
                return Response({'response': 'Subject deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                raise PermissionDenied("You are not allowed to delete this object.")
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        subjetct = self.get_object()
        serializer = SubjectSerializer(subjetct, data=request.data)
        if serializer.is_valid():
            if request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to update this object.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherViewSet(ModelViewSet):
    queryset = Teachers.objects.prefetch_related('subject').all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = ['subject', 'experience', 'english_fluency']
    filterset_class = TeacherFilter
    search_fields = ["teacher_name","roll_no"]

    
    def list(self, request, *args, **kwargs):
        if request.user.role in ["admin", "staff"]:
            queryset = Teachers.objects.all()
            queryset = self.filter_queryset(queryset)
            
            ordering_param = self.request.query_params.get('ordering', 'total_rating')
            total_count = queryset.count()
            if ordering_param == 'total_rating':
                serializer = SimpleTeacherSerializer(queryset, many=True)

                sorted_data = sorted(serializer.data, key=lambda x: x['total_rating'], reverse=True)
                response_data = {
                'total_count': total_count,
                'teachers': sorted_data
            }
                return Response(response_data)
            
            serializer = SimpleTeacherSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise PermissionDenied("You are not allowed to view subjects.")

    
    def create(self, request, *args, **kwargs):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            if self.request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise PermissionDenied("You are not allowed to create this object.")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request, *args, **kwargs):
        teacher = self.get_object()
        if request.user.role == "admin":
            teacher.delete()
            return Response({'response': 'Subject deleted successfully.'},status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You are not allowed to delete this object.")
        
    def update(self, request, *args, **kwargs):
        teacher = self.get_object()
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        
        if serializer.is_valid():
            if request.user.role == "admin":
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You are not allowed to update this object.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def retrieve(self, request, *args, **kwargs):
        teacher = self.get_object()
        if request.user.role in ["admin", "staff"]:
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("You are not allowed to view this object.")
