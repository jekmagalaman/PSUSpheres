from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrganizationMembersForm, StudentsForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q

from django.db import connection
from django.http import JsonResponse
from django.db.models.functions import ExtractMonth

from django.db.models import Count
from datetime import datetime

from django.shortcuts import render


@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

#Dashboard
class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass

def PieCountbySeverity(request):
    data = OrgMember.objects.values('organization__name').annotate(count=Count('organization')).order_by()
    response_data = [{'name': entry['organization__name'], 'count': entry['count']} for entry in data]
    return JsonResponse(response_data, safe=False)


#Org List
class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs): 
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs) 
        if self.request.GET.get("q") != None: 
            query = self.request.GET.get('q') 
            qs = qs.filter(Q(name__icontains=query) | 
                            Q(description__icontains=query)) 
        return qs
#Create
class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')
#Update
class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')
#Delete
class OrganizationDeleteView(DeleteView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

#
#
#
#Org Member
class OrganizationMembers(ListView):
    model = OrgMember
    context_object_name = 'org_members'
    template_name = 'org_members.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs): 
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query: 
            qs = qs.filter(
                Q(organization__name__icontains=query) | 
                Q(organization__description__icontains=query)
            )
        return qs
#Create
class OrganizationMembersCreateView(CreateView):
    model = OrgMember
    form_class = OrganizationMembersForm
    template_name = 'org_member_add.html'
    success_url = reverse_lazy('organization-members')
#Update
class OrganizationMembersUpdateView(UpdateView):
    model = OrgMember
    form_class = OrganizationMembersForm
    template_name = 'org_member_edit.html'
    success_url = reverse_lazy('organization-members')
#Delete
class OrganizationMembersDeleteView(DeleteView):
    model = OrgMember
    form_class = OrganizationMembersForm
    template_name = 'org_member_delete.html'
    success_url = reverse_lazy('organization-members')

#
#
#
#Students
class StudentList(ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'stud_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(lastname__icontains=query) |
                Q(middlename__icontains=query) |
                Q(firstname__icontains=query) |
                Q(student_id__icontains=query)
            )
        return qs
#Create
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentsForm
    template_name = 'stud_add.html'
    success_url = reverse_lazy('student-list')
#Update
class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentsForm
    template_name = 'stud_edit.html'
    success_url = reverse_lazy('student-list')
#Delete
class StudentDeleteView(DeleteView):
    model = Student
    form_class = StudentsForm
    template_name = 'stud_delete.html'
    success_url = reverse_lazy('student-list')

#
#
#
#College
class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = 'college_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(college_name__icontains=query)
            )
        return qs
#Create
class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')
#Update
class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')
#Delete
class CollegeDeleteView(DeleteView):
    model = College
    form_class = CollegeForm
    template_name = 'college_delete.html'
    success_url = reverse_lazy('college-list')

#
#
#
#Program
class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'prog_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(prog_name__icontains=query)
            )
        return qs
#Create
class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'prog_add.html'
    success_url = reverse_lazy('program-list')
#Update
class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'prog_edit.html'
    success_url = reverse_lazy('program-list')
#Delete
class ProgramDeleteView(DeleteView):
    model = Program
    form_class = ProgramForm
    template_name = 'prog_delete.html'
    success_url = reverse_lazy('program-list')