#include <iostream>
#include <fstream>
#include <vector>

int main(int argc, char **argv) {
    if(argc < 3) {
        std::cout << "Please provide a path to a source file and an output file\n";
        std::cout << "E.g. use as ./txt2bin {path to source file} {path to output file}\n";
        return 1;
    }

    std::ifstream source_file{argv[1], std::ios::in};
    if(!source_file.good()) {
        std::cout << "Error in opening the source file " << argv[1] << "\n";
        return 1;
    }

    constexpr uint32_t max_power = 64;  // highest power of 2 s.t. <= highest possible lottery number
    uint32_t random_number;
    std::vector<uint32_t> numbers;
    while(source_file >> random_number) {
        if(random_number > max_power) continue;

        numbers.push_back(random_number - 1);
    }
    std::cout << "Loaded " << numbers.size() << " numbers from source file " << argv[1] << ".\n";

    source_file.close();

    std::ofstream output_file{argv[2], std::ios::out | std::ios::binary | std::ios::app};
    if(!output_file.good()) {
        std::cout << "Error in opening the output file " << argv[2] << "\n";
        return 1;
    }

    int valid_bits = 0;
    uint32_t buffer = 0;
    for(uint8_t number : numbers) {
        buffer |= number << valid_bits;
        valid_bits += 6;

        if(valid_bits >= 8) {
            uint8_t byte = buffer & 0xFF;
            output_file << byte;
            buffer = buffer >> 8;
            valid_bits -= 8;
        }        
    }

    output_file.close();
    
    return 0;
}
