from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Chat, Message
import logging

logger = logging.getLogger(__name__)

def chat_list(request):
    logger.info("Выполняется запрос на получение списка чатов")
    chats = Chat.objects.all().order_by('-created_at') # все чаты (новые сверху)
    logger.debug(f"Найдено чатов: {len(chats)}")
    return render(request, 'chat_list.html', {'chats': chats})

def create_chat(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            chat = Chat.objects.create(title=title)
            logger.info(f"Создан чат с заголовком: {title}, ID: {chat.id}")
            return redirect('chat_list')
    return render(request, 'create_chat.html')


chats = Chat.objects.all()

def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    logger.info(f"Загружен чат ID: {chat_id}, заголовок: {chat.title}")

    count = request.GET.get('count', 20)
    try:
        count = int(count)
        if count > 100:
            count = 100
        elif count < 1:
            count = 1
    except ValueError:
        count = 20

    messages = chat.messages.order_by('-created_at')[:count]
    logger.debug(f"Выведено {len(messages)} сообщений для чата ID: {chat_id}")

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(chat=chat, text=text)
            logger.info(f"Добавлено сообщение в чат ID: {chat_id}, текст: {text[:50]}...")
            redirect_url = f'/chat/{chat_id}/?count={count}'
            return redirect(redirect_url)

    return render(request, 'chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'count': count
    })



'''def chat_delete(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == 'POST':
        chat.delete()  # Удаляет чат и все связанные сообщения
        messages.success(request, 'Чат и все сообщения удалены!')
        return redirect('chat_list')

    return render(request, 'chat_delete_confirm.html', {'chat': chat})'''

def chat_delete(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    logger.info(f"Попытка удаления чата ID: {chat_id}, заголовок: {chat.title}")

    if request.method == 'POST':
        chat.delete()
        logger.info(f"Чат ID: {chat_id} удалён успешно")
        messages.success(request, 'Чат и все сообщения удалены!')
        return redirect('chat_list')

    return render(request, 'chat_delete_confirm.html', {'chat': chat})

