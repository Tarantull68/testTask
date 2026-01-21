from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Chat, Message

def chat_list(request):
    chats = Chat.objects.all().order_by('-created_at')  # все чаты (новые сверху)
    return render(request, 'chat_list.html', {'chats': chats})

def create_chat(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Chat.objects.create(title=title)
            return redirect('chat_list')  # перенаправляем на список чатов
    # Если метод GET или ошибка — показываем форму снова
    return render(request, 'create_chat.html')

chats = Chat.objects.all()  # Должен возвращать все записи


def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # Получаем параметр count из GET-запроса (например, ?count=30)
    count = request.GET.get('count', 20)  # По умолчанию 20 сообщений

    # Преобразуем в число и ограничиваем максимум 100
    try:
        count = int(count)
        if count > 100:
            count = 100  # Максимум 100 сообщений
        elif count < 1:
            count = 1  # Минимум 1 сообщение
    except ValueError:
        count = 20  # Если count не число — устанавливаем 20

    # Получаем последние N сообщений, отсортированные по времени (новые сверху)
    messages = chat.messages.order_by('-created_at')[:count]

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(chat=chat, text=text)
            # Пересчитываем URL с текущим count для редиректа
            redirect_url = f'/chat/{chat_id}/?count={count}'
            return redirect(redirect_url)

    return render(request, 'chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'count': count  # Передаём count в шаблон для отображения
    })


def chat_delete(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == 'POST':
        chat.delete()  # Удаляет чат и все связанные сообщения (благодаря on_delete=models.CASCADE)
        messages.success(request, 'Чат и все сообщения удалены!')
        return redirect('chat_list')  # замените на ваш URL списка чатов

    return render(request, 'chat_delete_confirm.html', {'chat': chat})
