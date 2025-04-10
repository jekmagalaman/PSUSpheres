from django.forms import ModelForm
from django import forms
from .models import Organization, OrgMember, Student, College, Program

#Organization
class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"

#Organization Members
class OrganizationMembersForm(ModelForm):
    class Meta:
        model = OrgMember
        fields = "__all__"

#Students
class StudentsForm(ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

#College
class CollegeForm(ModelForm):
    class Meta:
        model = College
        fields = "__all__"

#Program
class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = "__all__"