// File: main.cpp
// Description: Main flow for the Personality Test, parsing text files
// and interacting with the user via terminal.

#include <set>
#include <vector>
#include <map>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#include <stdexcept>
#include "driver.h"

using namespace std;

set<Question> readQuestions(const string& filename) {
    set<Question> questions;
    ifstream file(filename);
    if (!file.is_open()) throw runtime_error("Cannot open questions file!");

    string line;
    while (getline(file, line)) {
        if (line.empty()) continue;

        Question q;
        stringstream ss(line);
        string token;
        string qText = "";

        while (ss >> token) {
            if (token.find(':') != string::npos) {
                char trait = token[0];
                int val = stoi(token.substr(2));
                q.factors[trait] = val;
            } else {
                if (!qText.empty()) qText += " ";
                qText += token;
            }
        }
        q.questionText = qText;
        questions.insert(q);
    }
    return questions;
}

set<Person> readPeople(const string& filename) {
    set<Person> people;
    ifstream file(filename);
    if (!file.is_open()) throw runtime_error("Cannot open people file!");

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
        
        if (!pName.empty() && pName.back() == '.') {
            pName.pop_back();
        }
        p.name = pName;
        people.insert(p);
    }
    return people;
}

map<Question, int> administerTest(int numQuestions, set<Question>& questions) {
    map<Question, int> answers;
    for (int i = 0; i < numQuestions; ++i) {
        Question q = randomQuestionFrom(questions);
        cout << "\nHow much do you agree with this statement?\n";
        cout << "\"" << q.questionText << "\"\n\n";
        cout << "1. Strongly disagree\n2. Disagree\n3. Neutral\n4. Agree\n5. Strongly agree\n\n";
        cout << "Enter your answer here (1-5): ";
        
        int ans;
        cin >> ans;
        answers[q] = ans;
    }
    return answers;
}

int main() {
    cout << "Welcome to the Personality Quiz!\n\n";
    
    set<Question> allQuestions = readQuestions("questions.txt");
    int totalAvailable = (int)allQuestions.size();

    int numQuestions = 0;
    while (true) {
        cout << "How many questions would you like to answer? (min: 20, max: " << totalAvailable << "): ";
        
        if (!(cin >> numQuestions)) {
            cin.clear();             
            cin.ignore(10000, '\n'); 
            cout << "ERROR! Please input an integer.\n\n";
            continue;
        }

        if (numQuestions >= 20 && numQuestions <= totalAvailable) {
            break;
        } else {
            cout << "INVALID! Please input a number in range: [20 - " 
                << totalAvailable << "].\n\n";
        }
    }
    
    map<Question, int> answers = administerTest(numQuestions, allQuestions);
    map<char, int> scores = scoresFrom(answers);

    int choice;
    cout << "\n1. BabyAnimals\n2. Brooklyn99\n3. Disney\n4. Hogwarts\n5. MyersBriggs\n";
    cout << "6. SesameStreet\n7. StarWars\n8. Vegetables\n9. Brainrot\n10. Beatboxers\n\n";
    cout << "Choose test number (1-10): ";
    cin >> choice;

    vector<string> files = {"", "BabyAnimals.people", "Brooklyn99.people", "Disney.people", 
                            "Hogwarts.people", "MyersBriggs.people", "SesameStreet.people", 
                            "StarWars.people", "Vegetables.people", "Brainrot.people",
                            "Beatboxer.people"};
    
    set<Person> people = readPeople(files.at(choice));
    Person match = mostSimilarTo(scores, people);

    cout << "\nYou got " << match.name << "!\n";

    char bestTrait = ' ';
    int maxScore = -100;

    for (auto const& pair : match.scores) {
        if (pair.second > maxScore) {
            maxScore = pair.second;
            bestTrait = pair.first;
        }
    }

    cout << "Reason: You are a perfect match with " << match.name << " because you both ";

    switch (bestTrait) {
        case 'O': 
            cout << "have a highly open, creative mind and love exploring new ideas (Openness)!\n"; 
            break;
        case 'C': 
            cout << "are very disciplined, dedicated, and always strive for perfection (Conscientiousness)!\n"; 
            break;
        case 'E': 
            cout << "are full of energy, outgoing, and love to shine in a crowd (Extraversion)!\n"; 
            break;
        case 'A': 
            cout << "are very agreeable, friendly, and always bring positive vibes to others (Agreeableness)!\n"; 
            break;
        case 'N': 
            cout << "have a complex inner world, deep sensitivity, and intense emotions (Neuroticism)!\n"; 
            break;
        default:  
            cout << "share a strange, inexplicable soul connection!\n"; 
            break;
    }

    return 0;
}