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

    uint32_t random_number;
    std::vector<uint32_t> numbers;
    while(source_file >> random_number) {
        uint32_t sanitized = (random_number - 1) & 0b11111;
        numbers.push_back(sanitized);
    }

    source_file.close();

    std::ofstream output_file{argv[2], std::ios::out | std::ios::binary | std::ios::app};

    int valid_bits = 0;
    uint32_t buffer = 0;
    for(uint8_t number : numbers) {
        buffer |= number << valid_bits;
        valid_bits += 5;

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
