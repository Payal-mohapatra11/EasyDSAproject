from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Topic,Progress


# Show all topics
def topic_list(request):
    topics = Topic.objects.all()
    return render(request, "learning/topic_list.html", {
        "topics": topics
    })


@login_required
def handle_progress(request, topic_name):
    topic = get_object_or_404(Topic, name=topic_name)

    progress, created = Progress.objects.get_or_create(
        user=request.user,
        topic=topic
    )

    if request.method == "POST":
        if request.POST.get("complete_topic"):
            progress.is_completed = True
            progress.completed_at = timezone.now()
        else:
            progress.is_completed = False
            progress.completed_at = None

        progress.save()
         # Redirect after saving
        return redirect("progress_profile")

    return topic, progress


@login_required
def array_visualizer(request):
    result = handle_progress(request, "Array")

    # If redirect happened
    if isinstance(result, HttpResponse):
        return result

    topic, progress = result

    return render(request, "arrayvisualizers.html", {
        "topic": topic,
        "progress": progress
    })

@login_required
def linkedlist_visualizer(request):
    result = handle_progress(request,"Linkedlist")
    if isinstance(result,HttpResponse):
        return result
    topic,progress = result
    return render(request,"linkedlistvisualizer.html",{
        "topic":topic,
        "progress":progress
    })

@login_required
def stack_visualizer(request):
    result = handle_progress(request,"Stack")
    if isinstance(result,HttpResponse):
        return result
    topic,progress = result
       
    return render(request, "stackvisualizer.html", {
        "topic": topic,
        "progress": progress
    })


@login_required
def queue_visualizer(request):
    result = handle_progress(request,"Queue")
    if isinstance(result,HttpResponse):
        return result
    topic,progress = result

    return render(request, "queuevisualizer.html", {
        "topic": topic,
        "progress": progress
    })
    
@login_required
def tree_visualizer(request):
    result = handle_progress(request,"Tree")
    if isinstance(result,HttpResponse):
        return result
    topic,progress = result

    return render(request, "treevisualizer.html", {
        "topic": topic,
        "progress": progress
    })
    
@login_required
def graph_visualizer(request):
    result = handle_progress(request,"Graph")
    if isinstance(result,HttpResponse):
        return result
    topic,progress = result

    return render(request, "graphvisualizer.html", {
        "topic": topic,
        "progress": progress
    })
    
@login_required
def sorting_visualizer(request):
    result = handle_progress(request,"Sorting")
    if isinstance(result,HttpResponse):
        return result
    topic,progress = result
    return render(request,"sort.html",{
        "topic":topic,
        "progress":progress
    })
    
@login_required
def searching_visualizer(request):
    result = handle_progress(request,"Searching")
    if isinstance(result,HttpResponse):
        return result
    topic,progress = result
    return render(request,"searching.html",{
        "topic":topic,
        "progress":progress
    })


@login_required
def progress_profile(request):
    total_topics=Topic.objects.count()
    completed_progress = Progress.objects.filter(user=request.user,is_completed=True)
    completed_count=completed_progress.count()
    
    percentage = 0
    if total_topics>0:
        percentage = int((completed_count/total_topics)*100)
        
    
    pending_topics=Topic.objects.exclude(id__in=completed_progress.values_list("topic_id", flat=True))
   
    context={
       "total_topics":total_topics,
       "completed_count":completed_count,
       "percentage":percentage,
     
        "completed_progress": completed_progress,
       "pending_topics":pending_topics,
    }  
    return render(request, "learning/progress_profile.html", context)

@login_required
def continue_learning(request):
    user = request.user
    in_progress=Progress.objects.filter(user=user,is_completed=False).first()
    if in_progress:
        topic_name=in_progress.topic.name
        return redirect_topic(topic_name)
    completed_topics=Progress.objects.filter(user=user,is_completed=True).values_list("topic_id",flat=True)
    next_topic=Topic.objects.exclude(id__in=completed_topics).first()
    if next_topic:
        return redirect_topic(next_topic.name)
    last_topic=Topic.objects.last()
    if last_topic:
        return redirect_topic(last_topic.name)
    return redirect("topic_list")

def redirect_topic(topic_name):
    mapping={
        "Array":"array_visualizer",
        "Linkedlist":"linkedlist_visualizer",
        "Stack":"stack_visualizer",
        "Queue":"queue_visualizer",
        "Tree":"tree_visualizer",
        "Sorting":"sorting_visualizer",
        "Searching":"searching_visualizer",
    }
    return redirect(mapping.get(topic_name,"topic_list"))