def handle_uploaded_file(f, name):  # ручная загрузка файла
    path = 'static/img/products_photo/' + name  # указываем путь к картинке и добовляем имя файла
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():  # пользуемся методом который позволяет читать файл в бинарном режиме честями
            destination.write(chunk)  # записываем эти части на сервер
        return path
