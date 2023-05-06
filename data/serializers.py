from rest_framework import  serializers
from .models import *

import logging
logger = logging.getLogger(__name__)


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'
















