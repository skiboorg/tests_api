from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from rest_framework import generics, viewsets, status

import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from scipy.cluster.hierarchy import dendrogram, linkage
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from scipy.cluster import hierarchy
from scipy.spatial.distance import pdist
from sklearn.preprocessing import LabelEncoder
class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    lookup_field = 'session_id'



class CalcTestResult(APIView):
    def get(self, request):
        total_results = TestResult.objects.all().count()
        test1_55_65 = TestResult.objects.filter(test1__gte=55, test1__lte=65).count()
        test1_65_80 = TestResult.objects.filter(test1__gte=65, test1__lte=80).count()
        test1_80_95 = TestResult.objects.filter(test1__gte=80, test1__lte=95).count()
        test1_95_500 = TestResult.objects.filter(test1__gte=95).count()

        test_2_0_24 = TestResult.objects.filter(test2__gte=0, test2__lte=24).count()
        test_2_24_500 = TestResult.objects.filter(test2__gte=24).count()

        test_3_0_3 = TestResult.objects.filter(test3__gte=0, test3__lte=3).count()
        test_3_4_7 = TestResult.objects.filter(test3__gte=4, test3__lte=7).count()
        test_3_8_11 = TestResult.objects.filter(test3__gte=8, test3__lte=11).count()
        test_3_12_15 = TestResult.objects.filter(test3__gte=12, test3__lte=15).count()

        test1_1 = (test1_55_65 / total_results) * 100
        test1_2 = (test1_65_80 / total_results) * 100
        test1_3 = (test1_80_95 / total_results) * 100
        test1_4 = (test1_95_500 / total_results) * 100

        test2_1 = (test_2_0_24 / total_results) * 100
        test2_2 = (test_2_24_500 / total_results) * 100

        test3_1 = (test_3_0_3 / total_results) * 100
        test3_2 = (test_3_4_7 / total_results) * 100
        test3_3 = (test_3_8_11 / total_results) * 100
        test3_4 = (test_3_12_15 / total_results) * 100

        return Response({
            "test1_1": test1_1,
            "test1_2": test1_2,
            "test1_3": test1_3,
            "test1_4": test1_4,
            "test2_1": test2_1,
            "test2_2": test2_2,
            "test3_1": test3_1,
            "test3_2": test3_2,
            "test3_3": test3_3,
            "test3_4": test3_4,
        }, status=200)

def create_dend(data):
    Z = linkage(data, method='ward')
    plt.figure(figsize=(10, 10))
    plt.title('Дендрограмма')
    plt.xlabel('Объекты')
    plt.ylabel('Расстояние')
    dendrogram(Z, leaf_rotation=90., leaf_font_size=8.)
    plt.savefig('media/3/dend.png')

class CalcTest(APIView):
    def get(self,request):
        from scipy.cluster.hierarchy import dendrogram
        data = TestResult.objects.values('age', 'gender', 'speciality', 'city', 'test1')
        df = pd.DataFrame.from_records(data)

        # Предварительная обработка данных
        # Кодируем категориальные признаки в числовые
        label_encoder = LabelEncoder()
        df['gender'] = label_encoder.fit_transform(df['gender'])
        df['speciality'] = label_encoder.fit_transform(df['speciality'])
        df['city'] = label_encoder.fit_transform(df['city'])

        # Масштабирование данных
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df)

        # Применение алгоритма KMeans для кластеризации
        kmeans = KMeans(n_clusters=3)  # Замените 3 на желаемое количество кластеров
        kmeans.fit(scaled_data)

        # Построение графика каменистой осыпи
        distortions = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i, random_state=0)
            kmeans.fit(scaled_data)
            distortions.append(kmeans.inertia_)

        plt.plot(range(1, 11), distortions, marker='o')
        plt.xlabel('Количество кластеров')
        plt.ylabel('Искажение')
        plt.title('График каменистой осыпи')
        plt.savefig('media/1/stone.png')

        # Построение паутинообразной диаграммы
        cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
        feature_labels = ['возраст', 'пол', 'Специальность', 'Город', 'Результаты_теста']

        fig, ax = plt.subplots(figsize=(8, 8))
        for i, cluster_center in enumerate(cluster_centers):
            angles = [n / float(len(feature_labels)) * 2 * 3.1415 for n in range(len(feature_labels))]
            angles += angles[:1]
            values = list(cluster_center)
            values += values[:1]
            ax.plot(angles, values, marker='o', linestyle='-', linewidth=2, label=f'Кластер {i + 1}')

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(feature_labels)
        ax.yaxis.grid(True)
        ax.legend()
        plt.title('Паутинообразная диаграмма')
        plt.savefig('media/spider.png')

        create_dend(scaled_data)


        return Response(status=200)