#include "driver.h"
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>

using namespace std;

// Hàm đọc file nhân vật (Copy từ main.cpp sang để file này chạy độc lập)
set<Person> readPeopleAPI(const string& filename) {
    set<Person> people;
    ifstream file(filename);
    if (!file.is_open()) return people;

    string line;
    while (getline(file, line)) {
        if (line.empty()) continue;
        Person p;
        stringstream ss(line);
        string token;
        string pName = "";
        while (ss >> token) {
            if (token.find(':') != string::npos) {
                char trait = token[0];
                int val = stoi(token.substr(2));
                p.scores[trait] = val;
            } else {
                if (!pName.empty()) pName += " ";
                pName += token;
            }
        }
        if (!pName.empty() && pName.back() == '.') pName.pop_back();
        p.name = pName;
        people.insert(p);
    }
    return people;
}

// KHU VỰC GIAO TIẾP VỚI PYTHON
extern "C" {
    // Thêm macro để tương thích xuất file DLL trên Windows
    #ifdef _WIN32
        #define EXPORT __declspec(dllexport)
    #else
        #define EXPORT
    #endif

    // Hàm nhận 5 điểm OCEAN và đường dẫn file, trả về tên nhân vật
    EXPORT const char* get_best_match_api(int o, int c, int e, int a, int n, const char* filepath) {
        // 1. Đóng gói điểm từ Python vào map của C++
        map<char, int> scores;
        if (o != 0) scores['O'] = o;
        if (c != 0) scores['C'] = c;
        if (e != 0) scores['E'] = e;
        if (a != 0) scores['A'] = a;
        if (n != 0) scores['N'] = n;

        // 2. Đọc file nhân vật
        set<Person> people = readPeopleAPI(filepath);
        if (people.empty()) return "Error: Cannot read file";

        // 3. Gọi hàm toán học Cosine Similarity từ driver.h
        Person match = mostSimilarTo(scores, people);

        // 4. Ép kiểu String của C++ về mảng Char tĩnh (để Python đọc được an toàn)
        static char resultName[256];
        strncpy(resultName, match.name.c_str(), sizeof(resultName));
        resultName[sizeof(resultName) - 1] = '\0'; // Đảm bảo kết thúc chuỗi an toàn

        return resultName;
    }
}