#include <iostream>

using namespace std;

// Function to insert an element into an array
void insert(int arr[], int& size, int element, int position) {
    if (position < 0 || position > size) {
        cout << "Invalid position for insertion." << endl;
        return;
    }
    for (int i = size - 1; i >= position; --i) {
        arr[i + 1] = arr[i];
    }
    arr[position] = element;
    size++;
}

int main() {
    const int MAX_SIZE = 100;
    int arr[MAX_SIZE] = {1, 3, 5, 7, 9};
    int size = 5;

    // Test insert
    int element = 4;
    int position = 2;
    insert(arr, size, element, position);

    // Display array after insertion
    cout << "Array after insertion: ";
    for (int i = 0; i < size; ++i) {
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}
