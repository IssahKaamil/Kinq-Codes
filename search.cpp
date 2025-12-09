#include <iostream>

using namespace std;

// Function to search for an element in an array
int search(int arr[], int size, int key) {
    for (int i = 0; i < size; ++i) {
        if (arr[i] == key) {
            return i;
        }
    }
    return -1; // Element not found
}

int main() {
    const int MAX_SIZE = 100;
    int arr[MAX_SIZE] = {1, 3, 5, 7, 9};
    int size = 5;
    int key = 5;

    // Test search
    int index = search(arr, size, key);
    if (index != -1) {
        cout << key << " found at position " << index << endl;
    } else {
        cout << key << " not found in the array." << endl;
    }

    return 0;
}
