#include <iostream>

using namespace std;

// Function to traverse an array
void traverse(int arr[], int size) {
    cout << "Array elements: ";
    for (int i = 0; i < size; ++i) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main() {
    const int MAX_SIZE = 100;
    int arr[MAX_SIZE] = {1, 3, 5, 7, 9};
    int size = 5;

    // Test traverse
    traverse(arr, size);

    return 0;
}
