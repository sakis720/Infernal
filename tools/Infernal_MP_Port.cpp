#include <fstream>
#include <iostream>

int main()
{
    std::fstream binaryFile("test.tex", std::ios::in | std::ios::out | std::ios::binary);
    if (!binaryFile.is_open()) {
        std::cerr << "Unable to open file\n";
        return -1;
    }

    if (!binaryFile.seekg(0x18/*offsetToRead*/)) {
        std::cerr << "Unable to seek file for reading\n";
        return -1;
    }

    char value;
    if (!binaryFile.get(value)) {
        std::cerr << "Unable to read from file\n";
        return -1;
    }

    if (value == 0x34) {
        value = 0x32/*ValueToReplace*/;
    } 
    else if (value == 0x2C) {
        value = 0x2B/*ValueToReplace*/;
    }
    else {
        std::cout << "Value not updated!\n";
        return 0;
    }

    if (!binaryFile.seekp(0x18/*offsetToWrite*/)) {
        std::cerr << "Unable to seek file for writing\n";
        return -1;
    }

    if (!binaryFile.put(value)) {
        std::cerr << "Unable to write to file\n";
        return -1;
    }

    std::cout << "Value updated!\n";

    return 0;
}