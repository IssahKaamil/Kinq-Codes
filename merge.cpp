#include <iostream>

using namespace std;

// Function to merge two sorted arrays into one
void merge(int arr1[], int size1, int arr2[], int size2, int result[]) {
    int i = 0, j = 0, k = 0;
    while (i < size1 && j < size2) {
        if (arr1[i] < arr2[j]) {
            result[k++] = arr1[i++];
        } else {
            result[k++] = arr2[j++];
        }
    }
    while (i < size1) {
        result[k++] = arr1[i++];
    }
    while (j < size2) {
        result[k++] = arr2[j++];
    }
}

int main() {
    const int MAX_SIZE = 100;
    int arr1[MAX_SIZE] = {1, 3, 5, 7, 9};
    int size1 = 5;
    int arr2[MAX_SIZE] = {2, 4, 6, 8};
    int size2 = 4;
    int result[MAX_SIZE + MAX_SIZE];

    // Test merge
    merge(arr1, size1, arr2, size2, result);

    // Display merged array
    cout << "Merged array: ";
    for (int i = 0; i < size1 + size2; ++i) {
        cout << result[i] << " ";
    }
    cout << endl;

    return 0;
}
