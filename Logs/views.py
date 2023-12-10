from django.shortcuts import redirect, render
from .models import Topic
from .forms import TopicForm
from .forms import TopicForm, EntryForm
from .models import Topic, Entry

def index(request):
    """Домашняя страница приложения Logs"""
    return render(request, 'Logs/index.html')

def topics(request):
    """Выводит список тем."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'Logs/topics.html', context)

def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'Logs/topic.html', context)

def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Logs:topics')
    context = {'form': form}
    return render(request, 'Logs/new_topic.html', context)

def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('Logs:topic', topic_id=topic_id)
    # Вывести пустую или недействительную форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'Logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'Logs/edit_entry.html', context)