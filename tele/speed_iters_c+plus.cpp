


#include <iostream>
#include <chrono>

int main() {
    using namespace std::chrono;
    auto start_time = high_resolution_clock::now();
    long long iterations = 0;

    while (true) {
        iterations++;

        auto end_time = high_resolution_clock::now();
        duration<double> elapsed = end_time - start_time;

        if (elapsed.count() >= 1.0) {  // If more than a second has passed
            std::cout << "\n\n";
            std::cout << "Hz       : " << iterations << "\n";
            std::cout << "Hz in KHz: " << iterations / 1000.0 << "\n";
            std::cout << "Hz in MHz: " << iterations / 1000000.0 << "\n";
            std::cout << "Hz in GHz: " << iterations / 1000000000.0 << "\n";

            iterations = 0;
            start_time = high_resolution_clock::now();
        }
    }

    return 0;
}