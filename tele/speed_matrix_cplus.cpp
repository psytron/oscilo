
#include <iostream>
#include <chrono>
#include <vector>

std::vector<std::vector<int>> matrixMultiplication(std::vector<std::vector<int>>& a, std::vector<std::vector<int>>& b) {
    int n = a.size();
    std::vector<std::vector<int>> result(n, std::vector<int>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            result[i][j] = 0;
            for (int k = 0; k < n; k++) {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    return result;
}

int main() {
    using namespace std::chrono;
    auto start_time = high_resolution_clock::now();
    long long iterations = 0;

    while (true) {
        iterations++;
       // Create 2 2X2 matrices
        std::vector<std::vector<int>> a = {{rand() % 100, rand() % 100}, {rand() % 100, rand() % 100}};
        std::vector<std::vector<int>> b = {{rand() % 100, rand() % 100}, {rand() % 100, rand() % 100}};
        std::vector<std::vector<int>> res = matrixMultiplication(a, b);

        auto end_time = high_resolution_clock::now();
        duration<double> elapsed = end_time - start_time;

        if (elapsed.count() >= 1.0) {  // If more than a second has passed
            std::cout << "\n\n";
            std::cout << "C++\n";
            std::cout << "Hz       : " << iterations << "\n";
            std::cout << "Hz in KHz: " << iterations / 1000.0 << "\n";
            std::cout << "Hz in MHz: " << iterations / 1000000.0 << "\n";
            std::cout << "Hz in GHz: " << iterations / 1000000000.0 << "\n";
            std::cout << "   Result: ";
            for (const auto &row : res) {
                for (const auto &elem : row) {
                    std::cout << elem << " ";
                }
                std::cout << " ";
            }
            std::cout.flush();  // Flush the output buffer
            iterations = 0;
            start_time = high_resolution_clock::now();
        }
    }
    return 0;
}