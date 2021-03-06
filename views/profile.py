from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from openshift.models import SkillEntry, InterestEntry

@login_required
def profile(request): 
    skills = SkillEntry.objects.filter(user = request.user.id).order_by('proficiency')
    interests = InterestEntry.objects.filter(user = request.user.id).order_by('level')
    for interest in interests:
        interest.label_class = 'default'
        if interest.level == InterestEntry.NOT_MUCH_INTERESTED:
            interest.level_text = 'Not much Interested'
            interest.label_class = 'info'
        elif interest.level == InterestEntry.INTERESTED:
            interest.level_text = 'Interested'
            interest.label_class = 'success'
        elif interest.level == InterestEntry.VERY_INTERESTED:
            interest.level_text = 'Very Interested'
            interest.label_class = 'important'
            
    for skill in skills:
        skill.label_class = 'default'
        if skill.proficiency == SkillEntry.STUDENT:
            skill.proficiency_text = 'Student'
            skill.label_class = 'info'
        elif skill.proficiency == SkillEntry.BEGINNER:
            skill.proficiency_text = 'Beginner'
            skill.label_class = 'success'
        elif skill.proficiency == SkillEntry.INTERMEDIATE:
            skill.proficiency_text = 'Intermediate'
            skill.label_class = 'warning'
        elif skill.proficiency == SkillEntry.ADVANCED:
            skill.proficiency_text = 'Advanced'
            skill.label_class = 'important'
    return render(request, 'profile.html', { 'skills': skills, 'interests': interests } )
    
@csrf_exempt
@login_required
def add_skill(request):
    skill_name =  str(request.POST['skill_name']).lower()
    proficiency = int(request.POST['proficiency'])
    
    success = False
    if len(SkillEntry.objects.filter(skill_name = skill_name, user = request.user)) == 0:
        se = SkillEntry(skill_name = skill_name, proficiency = proficiency, user = request.user)
        se.save()
        success = True
    return render(request, 'profile_add_skill.html', { 'success': success } )
    
@csrf_exempt
@login_required
def remove_skill(request):
    skill_name = str(request.POST['skill_name']).lower()
    
    skill = get_object_or_404(SkillEntry.objects.filter(skill_name = skill_name, user = request.user))
    skill.delete()
    
    return render(request, 'profile_add_skill.html', { 'success': True } )
    
@csrf_exempt
@login_required
def add_interest(request):
    interest_name =  str(request.POST['interest_name']).lower()
    level = int(request.POST['level'])
    
    success = False
    if len(InterestEntry.objects.filter(interest_name = interest_name, user = request.user)) == 0:
        se = InterestEntry(interest_name = interest_name, level = level, user = request.user)
        se.save()
        success = True
    return render(request, 'profile_add_skill.html', { 'success': success } )
    
@csrf_exempt
@login_required
def remove_interest(request):
    interest_name = str(request.POST['interest_name']).lower()
    
    interest = get_object_or_404(InterestEntry.objects.filter(interest_name = interest_name, user = request.user))
    interest.delete()
    
    return render(request, 'profile_add_skill.html', { 'success': True } )
