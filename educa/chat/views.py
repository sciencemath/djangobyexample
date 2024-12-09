from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from courses.models import Course

@login_required
def course_chat_room(request, course_id):
  try:
    course = request.user.courses_joined.get(id=course_id)
  except Course.DoesNotExist:
    return HttpResponseForbidden()
  # select_related() saves us a SQL query
  latest_messages = course.chat_messages.select_related(
    'user'
  ).order_by('-id')[:5] # this would be for all time, maybe we should do last hour only as well
  # Django doesn't support negative indexing, we must use reversed()
  latest_messages = reversed(latest_messages)
  return render(
    request,
    'chat/room.html',
    {
      'course': course,
      'latest_messages': latest_messages
    }
  )