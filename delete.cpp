#include <iostream>

using namespace std;

// Function to delete an element from an array
void remove(int arr[], int& size, int position) {
    if (position < 0 || position >= size) {
        cout << "Invalid position for deletion." << endl;
        return;
    }
    for (int i = position; i < size - 1; ++i) {
        arr[i] = arr[i + 1];
    }
    size--;
}

int main() {
    const int MAX_SIZE = 100;
    int arr[MAX_SIZE] = {1, 3, 5, 7, 9};
    int size = 5;

    // Test delete
    int position = 2;
    remove(arr, size, position);

    // Display array after deletion
    cout << "Array after deletion: ";
    for (int i = 0; i < size; ++i) {
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}
