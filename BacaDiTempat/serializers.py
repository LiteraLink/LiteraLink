from collections import OrderedDict
from typing import Any
from django.core.serializers.json import Serializer
from django.db.models.base import Model

from authentication.models import UserProfile

class BookVenueSerializer(Serializer):
    def end_object(self, obj: Any) -> None:
        user = self._current['user']
        if (user != None):
            username = UserProfile.objects.get(id=self._current['user']).user.username
            self._current['user'] = username

        return super().end_object(obj)