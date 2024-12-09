from django.db import models
from enumeration.mixins import EnumeratedModelMixin


class Document(EnumeratedModelMixin):
    date = models.DateField()

    def get_enumeration_context(self):
        return {"date": self.date}
