import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from numpy.linalg import norm
import pandas as pd


def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


def taxicab_distance(x1, x2):  # manhatten/city block distance
    return np.sum(np.abs(x1 - x2))


def maximum_distance(x1, x2):
    return np.max(np.abs(x1 - x2))


def cosine_distance(x1, x2):
    cosine_similarity = np.dot(x1, x2) / (norm(x1) * norm(x2))
    return 1 - cosine_similarity  # the cosine similarity is greatest when the angle is the same: cos(0º) = 1,
    # so the neighbours with the greatest cosine similarity are the closest ones


def accuracy(predicted_classification, actual_classification):
    try:
        if len(predicted_classification) != len(actual_classification):
            raise IndexError

        truefalse_arr = np.equal(predicted_classification, actual_classification)
        accuracy = np.sum(truefalse_arr) / len(truefalse_arr)

    except IndexError:
        print("Podane macierze muszą być równe")

    return accuracy


class KNN:
    def __init__(self, k=3):
        self.k = k
        self.vectors_train = []
        self.labels_train = []

    def train(self, vectors,
              labels):  # buduje bazę przypadków uczących (przyjmuje przynajmniej wektory i prawidłowe odpowiedzi)

        try:
            for vector in vectors:
                self.vectors_train.append(list(vector))

            for label in labels:
                self.labels_train.append(label)

            if len(self.labels_train) != len(self.vectors_train):
                raise IndexError

        except IndexError:
            print("Dla przypadków uczących do każdego wektora musi zostać przypisana klasyfikacja i odwrotnie")
            print("Sprawdź wymiary macierzy")
            exit(1)

    def predict(self, vectors,
                method=euclidean_distance):  # =euclidean_distance):  # przyjmuje wektor (opcjonalnie: większą liczbę wektorów
        # naraz) i zwraca odpowiedź klasyfikatora

        # dla wektora 1D (pojedynczy wektor) zmiana na 2D:
        if np.ndim(vectors) == 1:
            vectors = np.array([vectors])

        # obiczanie odleglosci od punktow z train dla kazdego wektora
        distances = []

        for vector in vectors:
            distances_vector = []  # dla pojedynczego wektora
            for v_train in self.vectors_train:
                distances_vector.append(method(vector, v_train))
            distances.append(distances_vector)

        distances = np.array(distances)

        # szukanie klasyfikacji dla k najblizszych sasiadow

        k_nearest_indexes = np.argsort(distances)[:, :self.k]  # indeksy k najkrotszych odleglosci (dla
        # przyporzadkowania klasyfikacji)

        k_nearest_labels = []
        for _ in k_nearest_indexes:
            k_nearest_labels.append([self.labels_train[i] for i in _])

        # wybor najczesciej wystepujacej klasy
        most_common = []
        for _ in k_nearest_labels:
            most_common.append(Counter(_).most_common(1)[0][0])

        return np.array(most_common)  # zwracam array z przyporzadkowanymi klasyfikacjami


if __name__ == '__main__':
    # PRZYKLAD DZIALANIA NA WAGACH Z ZAJEC

    df = pd.read_csv('weight.csv')
    arr = df.to_numpy()

    # 20 przypadkow uczacych

    vector_train_weights = arr[0:20, :2]
    label_train_weights = arr[0:20, 2]

    # 10 przypadkow testowych

    vector_predict_weights = arr[20:, :2]
    label_predict_weights = arr[20:, 2]

    # sprawdzam accuracy dla kazdej metody

    knn_weights = KNN(k=6)
    knn_weights.train(vector_train_weights, label_train_weights)

    prediction_euclidean = knn_weights.predict(vector_predict_weights, method=euclidean_distance)
    prediction_taxicab = knn_weights.predict(vector_predict_weights, method=taxicab_distance)
    prediction_maximum = knn_weights.predict(vector_predict_weights, method=maximum_distance)
    prediction_cosine = knn_weights.predict(vector_predict_weights, method=cosine_distance)

    print("Accuracy, euklidean: ", accuracy(prediction_euclidean, label_predict_weights))
    print("Accuracy, taxicab: ", accuracy(prediction_taxicab, label_predict_weights))
    print("Accuracy, maximum: ", accuracy(prediction_maximum, label_predict_weights))
    print("Accuracy, cosine: ", accuracy(prediction_cosine, label_predict_weights))
