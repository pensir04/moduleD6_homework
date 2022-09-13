from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser.username}'

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.all().aggregate(commentRating=Sum('commentRating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.rating = cRat * 3 + cRat
        self.save()


class Category(models.Model):
    categories = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscriber', blank=True)

    def __str__(self):
        return f'{self.categories}'

class Subscriber(models.Model):
    subscriber_user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed_category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Post(models.Model):
    article = 'AR'
    news = 'NW'

    SELECTION = [
        (article, 'статья'),
        (news, 'новость')
    ]
# поле с выбором статья или новость
    selection = models.CharField(max_length=2, choices = SELECTION, default = news)
# автоматически добавляемое дата и время создания
    time = models.DateTimeField(auto_now_add=True)
# заголовок статьи
    header = models.CharField(max_length=255)
# текст статьи
    text = models.TextField()
# рейтинг статьи
    rating = models.IntegerField(default=0)
# связь многие ко многим с моделью Category через модель PostCategory
    postCategory = models.ManyToManyField(Category, through='PostCategory')
# связь один ко ногим с моделью Author
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.header}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с постом
        return f'/posts/{self.id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    postConnection = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryConnection = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentTime = models.DateTimeField(auto_now_add=True)
    commentRating = models.IntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()
