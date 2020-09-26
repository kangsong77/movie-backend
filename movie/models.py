from django.db import models


class NowMovie(models.Model):
    tm_id = models.CharField(max_length=6)
    title = models.CharField(max_length=50)
    backdrop_path = models.URLField(null=True, blank=True)
    rating = models.CharField(max_length=5, null=True, blank=True)
    release_date = models.CharField(max_length=10, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    create_date = models.IntegerField()

    def __str__(self):
        return self.tm_id + " > " + self.title


class IntroMovie(models.Model):
    tm_id = models.CharField(max_length=6)
    title = models.CharField(max_length=50)
    backdrop_path = models.URLField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    create_date = models.IntegerField()

    def __str__(self):
        return self.tm_id + " > " + self.title


class MovieDetail (models.Model):
    tm_id = models.CharField(max_length=6, primary_key=True)
    title = models.CharField(max_length=50)
    backdrop_path = models.URLField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    tagline = models.CharField(max_length=100, null=True, blank=True)
    release_date = models.CharField(max_length=10, null=True, blank=True)
    runtime = models.CharField(max_length=10, null=True, blank=True)
    rating = models.CharField(max_length=5, null=True, blank=True)
    genre = models.CharField(max_length=50, null=True, blank=True)
    poster = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.tm_id + " > " + self.title


class MovieGallery (models.Model):
    tmdb_id = models.ForeignKey(MovieDetail, on_delete=models.CASCADE)
    backdrop_path = models.CharField(max_length=200)

    def __str__(self):
        return self.backdrop_path


class MovieCast (models.Model):
    tmdb_id = models.ForeignKey(MovieDetail, on_delete=models.CASCADE)
    cast_name = models.CharField(max_length=50)
    cast_role = models.CharField(max_length=100)
    cast_image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.cast_name + " : " + self.role


class SimulaMovie (models.Model):
    simula_id = models.CharField(max_length=6)
    title = models.CharField(max_length=50)
    backdrop_path = models.URLField(blank=True)
    tmdb_id = models.ForeignKey(MovieDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
