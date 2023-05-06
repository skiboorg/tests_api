from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import *
from rest_framework import generics, viewsets, status

import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    lookup_field = 'session_id'


def create_graph(user_data,categories, filename):
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    user_data[:, 1] = le.fit_transform(user_data[:, 1])
    user_data[:, 2] = le.fit_transform(user_data[:, 2])
    user_data[:, 3] = le.fit_transform(user_data[:, 3])

    kmeans = KMeans(n_clusters=3, random_state=0).fit(user_data)
    labels = kmeans.labels_
    cluster_centers = kmeans.cluster_centers_


    for i in range(len(cluster_centers)):
        values = cluster_centers[i]
        values = np.append(values, values[0])
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
        angles = np.append(angles, angles[0])
        plt.polar(angles, values, 'o-', linewidth=2)
        plt.fill(angles, values, alpha=0.25)
    # plt.legend(['Cluster 1', 'Cluster 2', 'Cluster 3'], loc='upper right', bbox_to_anchor=(1.5, 1))
    plt.xticks(angles[:-1], categories)
    plt.yticks(np.arange(0, 4, 0.5))

    print(cluster_centers)
    plt.savefig(f'media/{filename}.png')

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
class CalcTest(APIView):
    def get(self,request):



        user_data = np.array(TestResult.objects.values_list('age', 'gender', 'speciality', 'city', 'test1', 'test2', 'test3'))
        categories = ['Возраст', 'Пол', 'Специальность', 'Город', 'Результаты теста1', 'Результаты теста2',
                      'Результаты теста3']
        filename='total'
        create_graph(user_data,categories,filename)

        user_data = np.array(
            TestResult.objects.values_list('age', 'gender', 'speciality', 'city', 'test1',))
        categories = ['Возраст', 'Пол', 'Специальность', 'Город', 'Результаты теста1']
        filename = 'test1'
        create_graph(user_data, categories, filename)

        user_data = np.array(
            TestResult.objects.values_list('age', 'gender', 'speciality', 'city', 'test2', ))
        categories = ['Возраст', 'Пол', 'Специальность', 'Город', 'Результаты теста2']
        filename = 'test2'
        create_graph(user_data, categories, filename)

        user_data = np.array(
            TestResult.objects.values_list('age', 'gender', 'speciality', 'city', 'test3', ))
        categories = ['Возраст', 'Пол', 'Специальность', 'Город', 'Результаты теста3']
        filename = 'test3'
        create_graph(user_data, categories, filename)




        # print(user_data)
        #
        # X = list(user_data)
        # distortions = []
        # K = range(1, len(user_data))
        # for i in K:
        #     kmeans = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=300, random_state=0)
        #     kmeans.fit(X)
        #     distortions.append(kmeans.inertia_)
        #
        # # Определяем количество кластеров как точку перегиба на графике "Каменистой осыпи"
        # num_clusters = np.argmin(np.diff(distortions)) + 1
        #
        # print('num_clusters',num_clusters)
        #
        # # Отображение графика метода локтя
        # plt.figure(figsize=(16, 8))
        # plt.plot(K, distortions, 'bx-')
        # plt.xlabel('Кластеров')
        # plt.ylabel('Расхождение')
        #
        #
        #
        # plt.savefig('my_plot.png')
        #
        # # Кластеризуем данные с использованием метода k-средних
        # kmeans = KMeans(n_clusters=num_clusters, init='k-means++', n_init=10, max_iter=300, random_state=0)
        # kmeans.fit(X)
        #
        # # Определяем средние значения переменных в каждом кластере
        # cluster_centers = kmeans.cluster_centers_
        #
        # # Выводим средние значения переменных в каждом кластере
        # for i in range(num_clusters):
        #     print("Кластер ", i + 1, " средние значения:")
        #     print("Возраст: ", cluster_centers[i][0])
        #     print("Пол: ", cluster_centers[i][1])
        #     print("Test 1: ", cluster_centers[i][2])
        #     print("Test 2: ", cluster_centers[i][3])
        #     print("Test 3: ", cluster_centers[i][4])


        # # определение оптимального количества кластеров методом локтя
        # distortions = []
        # K = range(1, len(user_data))
        # for k in K:
        #     kmeanModel = KMeans(n_clusters=k)
        #     kmeanModel.fit(user_data)
        #     distortions.append(kmeanModel.inertia_)
        # print(distortions)
        # plt.figure(figsize=(16, 8))
        # plt.plot(K, distortions, 'bx-')
        # plt.xlabel('Кол-во кластеров')
        # plt.ylabel('Расхождение')

        # K = range(1, len(user_data))
        # distortions = []
        # # Вычисление и добавление искажений для каждого K
        # for k in K:
        #     kmeanModel = KMeans(n_clusters=k)
        #     kmeanModel.fit(user_data)
        #     distortions.append(kmeanModel.inertia_)
        #
        # # Отображение графика метода локтя
        # plt.figure(figsize=(16, 8))
        # plt.plot(K, distortions, 'bx-')
        # plt.xlabel('Кластеров')
        # plt.ylabel('Расхождение')
        #
        #
        #
        # plt.savefig('my_plot.png')
        # optimal_k = np.argmin(distortions) + 1
        # print(f'Оптимальное количество кластеров: {optimal_k}')



        return Response(status=200)