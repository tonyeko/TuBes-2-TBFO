#ifndef CYK_HPP
#define CYK_HPP

#include <string>

#include <string>
#include <vector>
#include <fstream>
#include <iterator>
#include <list>
#include <sstream>
#include <set>
#include <algorithm>
#include <utility>
#include <memory>

using namespace std;
namespace CYK 
{
    // class grammar 
    // {
    //     public:
    //     // Baca grammar dari file
    //     grammar(istream &is) 
    //     {
    //         string line;
    //         while (getline(is, line)) {
    //             line.erase(line.find_last_not_of("\r\n") + 1);
    //             if (line.size()) {
    //                 rule::ptr r = rule::create(line);
    //                 if (*r) {
    //                     rules_.push_back(r);
    //                 }
    //             }
    //         }

    //         // Get the terminals
    //         set<string> nonterminals;
    //         set<string> symbols;
    //         for (rule::const_ptr r : rules_) {
    //             nonterminals.insert(r -> left());
    //             for (const vector<string> &alternative : r -> right()) {
    //                 for (const string &symbol : alternative) {
    //                     symbols.insert(symbol);
    //                 }
    //             }
    //         }
    //         for (const std::string& symbol : symbols) {
    //             if (nonterminals.find(symbol) == nonterminals.end()) {
    //                 terminals_.push_back(symbol);
    //             }
    //         }
    //     }

    //     const vector<rule::ptr> &rules() const {
    //         return rules_;
    //     }
    
    //     // Get all of the rules where symbol is the subject
    //     template <class OutputIt>
    //     OutputIt get_rules_for_symbols(InputIt begin, InputIt end, OutputIt it) const {
    //         for (InputIt init = begin; init != end; ++init) {
    //             for (rule::const_ptr r : rules_) {
    //                 for (const std::vector<std::string>& alternative : r->right()) {
    //                     if (alternative.size() == 2
    //                             && alternative[0] == init->first
    //                             && alternative[1] == init->second) {
    //                         *it++ = r;
    //                     }
    //                 }
    //             }
    //         }
    //         return it;
    //     }

    //     private:
    //     std::vector<rule::ptr> rules_;
    //     std::vector<rule::ptr> start_rules_;
    //     std::vector<std::string> terminals_;

    
    // };


    class CYK_PARSER {
        
    }

}



#endif // CYK_HPP