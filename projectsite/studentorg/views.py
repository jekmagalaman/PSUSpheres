from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, Student, OrgMember, College, Program
from studentorg.forms import OrganizationForm, StudentForm, OrgMemberForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from  django.contrib.auth.decorators import login_required

from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q

from django.db import connection
from django.http import JsonResponse

@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    contextobject_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'organization/org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                        Q (description__icontains=query) |
                        Q (college__college_name__icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'organization/org_del.html'
    success_url = reverse_lazy('organization-list')


#student ---------------------------------------------------------------

class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student/stud_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(firstname__icontains=query) |
                        Q (lastname__icontains=query) | 
                        Q (middlename__icontains=query) |
                        Q (student_id__icontains=query)|
                        Q (program__prog_name__icontains=query))
        return qs

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/stud_add.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/stud_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student/stud_del.html'
    success_url = reverse_lazy('student-list')



#Organization Members ---------------------------------------------------------------

class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'org_member/orgmem_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(organization__name__icontains=query))
        return qs

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_member/orgmem_add.html'
    success_url = reverse_lazy('orgmem-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_member/orgmem_edit.html'
    success_url = reverse_lazy('orgmem-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'org_member/orgmem_del.html'
    success_url = reverse_lazy('orgmem-list')



#College ---------------------------------------------------------------

class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = 'college/college_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(college_name__icontains=query))
        return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college/college_add.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college/college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college/college_del.html'
    success_url = reverse_lazy('college-list')


#Program ---------------------------------------------------------------

class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'program/program_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(prog_name__icontains=query) |
                        Q (college__college_name__icontains=query))
        return qs

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program/program_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program/program_edit.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program/program_del.html'
    success_url = reverse_lazy('program-list')

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass

def DoughStudCountbyCollege(request):
    query = '''
    SELECT studentorg_college.college_name, COUNT(studentorg_student.id) AS total_students
    FROM studentorg_college
    JOIN studentorg_program ON studentorg_college.id = studentorg_program.college_id
    JOIN studentorg_student ON studentorg_program.id = studentorg_student.program_id
    GROUP BY studentorg_college.college_name;

    '''
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            data = {prog_name: count for prog_name, count in rows}
        else:
            data = {}

    return JsonResponse(data)

def PolarCountByProgram(request):
    query = '''
    SELECT TRIM(studentorg_program.prog_name) as program_name, COUNT(*) as count
    FROM studentorg_student
    JOIN studentorg_program ON studentorg_student.program_id = studentorg_program.id
    GROUP BY TRIM(studentorg_program.prog_name);
    '''
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            data = {prog_name: count for prog_name, count in rows}
        else:
            data = {}

    return JsonResponse(data)

def DoughnutCountByCollege(request):
    query = '''
    SELECT studentorg_college.college_name, COUNT(studentorg_organization.id) AS total_organizations
    FROM studentorg_college
    JOIN studentorg_organization ON studentorg_college.id = studentorg_organization.college_id
    GROUP BY studentorg_college.college_name;
    '''

    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            data = {row[0]: row[1] for row in rows}
        else:
            data = {}

    return JsonResponse(data)

def PolarCountOrgmem(request):
    query = '''
        SELECT studentorg_organization.name, COUNT(studentorg_orgmember.id) AS total_members
        FROM studentorg_organization
        JOIN studentorg_orgmember ON studentorg_organization.id = studentorg_orgmember.organization_id
        GROUP BY studentorg_organization.name;
        '''

    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            data = {row[0]: row[1] for row in rows}
        else:
            data = {}

    return JsonResponse(data)

def PolarCountstudYear(request):
    query = '''
        SELECT SUBSTR(student_id, 1, 4) AS enrollment_year, COUNT(id) AS total_students
        FROM studentorg_student
        GROUP BY enrollment_year;
        '''
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            data = {row[0]: row[1] for row in rows}
        else:
            data = {}

    return JsonResponse(data)