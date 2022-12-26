import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from numpy.linalg import norm


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


class KNN:
    def __init__(self, k=3):
        self.k = k
        self.vectors_train = []
        self.labels_train = []

    def train(self, vectors,
              labels):  # buduje bazę przypadków uczących (przyjmuje przynajmniej wektory i prawidłowe odpowiedzi)

        for vector in vectors:
            self.vectors_train.append(list(vector))

        for label in labels:
            self.labels_train.append(label)

    def predict(self, vectors, method=euclidean_distance):  # =euclidean_distance):  # przyjmuje wektor (opcjonalnie: większą liczbę wektorów
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
        print(distances)

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
    vector_train = np.array([[2, 6], [3, 7], [4, 6], [7, 3], [8, 2], [9, 3]])
    label_train = np.array(["red", "red", "red", "blue", "blue", "blue"])
    x = vector_train[:, 0]
    y = vector_train[:, 1]

    #plt.figure()
    #plt.scatter(x, y, c=label_train)
    #plt.show()

    sample = np.array([[8, 4], [3, 5], [6, 4]])

    knn_eucl = KNN(k=3)
    knn_eucl.train(vector_train, label_train)
    print(knn_eucl.predict(sample,method=euclidean_distance))


