//  TODO:  Write file header comment here.

#include <math.h>
#include <limits>
#include <string>
#include <map>
#include <set>
#include "myrandom.h"
#include <stdexcept> // new

using namespace std;

constexpr double lowest_double = std::numeric_limits<double>::lowest();

/* Type: Question
 *
 * Type representing a personality quiz question.
 */
struct Question {
    string questionText;  // Text of the question
    map<char, int> factors;   // Map from factors to +1 or -1
    friend bool operator< (const Question& lhs, const Question& rhs) {
        return lhs.questionText < rhs.questionText;
    }
    friend bool operator== (const Question& lhs, const Question& rhs) {
        return lhs.questionText == rhs.questionText;
    }
    friend bool operator!= (const Question& lhs, const Question& rhs) {
        return lhs.questionText != rhs.questionText;
    }
};

/* Type: Person
 *
 * Type representing a person, used to represent people when determining
 * who's the closest match to the user.
 */
struct Person {
    string name;      // Name of the person
    map<char, int> scores;  // Map from factors to +1 or -1
    friend bool operator< (const Person& lhs,   const Person& rhs) {
        return lhs.name < rhs.name;
    }
    friend bool operator== (const Person& lhs, const Person& rhs) {
        return lhs.name == rhs.name;
    }
    friend bool operator!= (const Person& lhs, const Person& rhs) {
        return lhs.name != rhs.name;
    }
};

/* randomElement
 *
 * This function selects, at random, a Question from the inputted questions set
 * and returns the question.  Note, this function does not remove the randomly
 * selected question from the set.
*/
Question randomElement(set<Question>& questions) {
    int ind = randomInteger(0, (int)questions.size()-1);
    int i = 0;
    for (auto e : questions) {
        if (i == ind) {
            return e;
        }
        i++;
    }
    return {};
}

// TODO: Write this function header comment.
Question randomQuestionFrom(set<Question>& questions) {
    if(questions.empty()) {
        throw std::runtime_error("Lỗi: Tập câu hỏi đang rỗng!");
    }
    
    Question selectedQuestion = randomElement(questions);
    
    questions.erase(selectedQuestion);
    
    return selectedQuestion;
}

// TODO: Write this function header comment.
map<char, int> scoresFrom(map<Question, int>& answers) {
    map<char, int> ocean_scores;

    for (const auto& pair : answers) {
        const Question& q = pair.first;
        int answer_val = pair.second;
        
        int weight = answer_val - 3;    

        for (const auto& factor_pair : q.factors) {
            char trait = factor_pair.first;
            int factor_val = factor_pair.second;
            
            ocean_scores[trait] += (weight * factor_val);
        }
    }

    for (auto it = ocean_scores.begin(); it != ocean_scores.end(); ) {
        if (it->second == 0) {
            it = ocean_scores.erase(it);
        } else {
            ++it;
        }
    }

    return ocean_scores;
}

// TODO: Write this function header comment.
map<char, double> normalize(map<char, int>& scores) {
    map<char, double> normalized_scores;
    
    if (scores.empty()) {
        return normalized_scores;
    }

    double sum_of_squares = 0.0;
    for (const auto& pair : scores) {
        sum_of_squares += pow(pair.second, 2);
    }

    double length = sqrt(sum_of_squares);

    if (length == 0.0) {
        return normalized_scores; 
    }

    for (const auto& pair : scores) {
        normalized_scores[pair.first] = pair.second / length;
    }

    return normalized_scores;
}

// TODO: Write this function header comment.
double cosineSimilarityOf(const map<char, double>& lhs,
                          const map<char, double>& rhs) {
    double similarity = 0.0;

    for (const auto& pair : lhs) {
        char trait = pair.first;
        double lhs_val = pair.second;

        if (rhs.count(trait) > 0) {
            double rhs_val = rhs.at(trait);
            similarity += (lhs_val * rhs_val);
        }
    }

    return similarity;
}

// TODO: Write this function header comment.
Person mostSimilarTo(map<char, int>& scores, set<Person>& people) {
    if (people.empty()) {
        throw std::runtime_error("Tập dữ liệu nhân vật đang rỗng!");
    }

    map<char, double> user_normalized = normalize(scores);

    double highest_sim = lowest_double;
    Person best_match;

    for (const Person& p : people) {
        map<char, int> person_scores = p.scores;
        
        map<char, double> person_normalized = normalize(person_scores);
        
        double current_sim = cosineSimilarityOf(user_normalized, person_normalized);
        
        if (current_sim > highest_sim) {
            highest_sim = current_sim;
            best_match = p;
        }
    }

    return best_match;
}
