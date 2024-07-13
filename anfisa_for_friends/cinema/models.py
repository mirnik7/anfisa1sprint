# cinema/models.py
from django.db import models


class OriginalTitle(models.Model):
    title = models.CharField(max_length=128)


class ProductType(models.Model):
    title = models.CharField(max_length=128)


class Director(models.Model):
    full_name = models.CharField(max_length=128)


class BaseModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к модели дату создания и последнего изменения.
    """
    # Параметр auto_now_add=True означает
    # "при СОЗДАНИИ записи автоматически записывать в это поле текущее время".
    created_at = models.DateTimeField(auto_now_add=True)
    # Параметр auto_now=True означает
    # "при ИЗМЕНЕНИИ записи автоматически записывать в это поле текущее время".
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    # С помощью необязательного внутреннего класса Meta можно добавить
    # к модели дополнительные настройки.
    class Meta:
        # Эта строка объявляет модель абстрактной:
        abstract = True


# Абстрактная модель, которая наследуется от другой абстрактной модели
class CommonInfoBaseModel(BaseModel):
    name = models.CharField(max_length=128)
    description = models.TextField()

    # Нужно указывать обязательно, чтобы модель читалась как абстрактная
    class Meta:
        abstract = True

# Наследуемся от абстрактной модели BaseModel,
# можно наследоваться от нескольких
class VideoProduct(BaseModel):
    title = models.CharField(max_length=128)

    # Связь "один-к-одному"
    original_title = models.OneToOneField(
        # На какую модель ссылаемся
        OriginalTitle,
        # Поведение при удалении:
        # если оригинальное имя будет удалено,
        # то и сам фильм будет удалён.
        on_delete=models.CASCADE,

        # При удалении объекта, на который ведёт ссылка, в ссылающихся записях
        # вместо ссылки на объект будет установлен null
        # on_delete=models.SET_NULL,
        # null=True

        # Указывает на то, что поле обязательное
        # True - если необязательное
        blank=False
    )
    # Связь "многие к одному"
    product_type = models.ForeignKey(
        ProductType,
        # обязательный аргумент
        on_delete=models.CASCADE
    )
    # Связь "многие к многим"
    # Параметр through указывает, какую модель надо назначить промежуточной:
    directors = models.ManyToManyField(Director, through='Partnership')


class Partnership(models.Model):
    # Поле, ссылающееся на модель Director:
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    # Поле, ссылающееся на модель VideoProduct:
    videoproduct = models.ForeignKey(VideoProduct, on_delete=models.CASCADE)
    # Дополнительные поля:
    # дата начала работы режиссёра над фильмом...
    date_joined = models.DateField()
    # ...и история о том, почему на фильм пригласили именно этого режиссёра.
    invite_reason = models.CharField(max_length=300)
