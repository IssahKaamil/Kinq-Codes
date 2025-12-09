#include <iostream>
#include <algorithm>

using namespace std;

// Function to sort an array
void sort(int arr[], int size) {
    sort(arr, arr + size);
}

int main() {
    const int MAX_SIZE = 100;
    int arr[MAX_SIZE] = {9, 5, 1, 7, 3};
    int size = 5;

    // Test sort
    sort(arr, size);

    // Display array after sorting
    cout << "Array after sorting: ";
    for (int i = 0; i < size; ++i) {
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}
