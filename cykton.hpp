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
    // class Node {
        
    //     bool canDerive(non_terminal S, string w) {
    //         return canDerive1(S, w, 0, w.size());
    //     }

    //     bool canDerive1(non_terminal S, string w, int start, int end) {
    //         /* Basis */
    //         if (end == start + 1) {
    //             return        
    //         }
    //         /* Rekurens */
    //         for (each production S -> AB) {
    //             for (int mid = start + 1; mid < end; mid++) {
    //                 if (canDerive1(A, w, start, mid) && canDerive1(B, w, mid, end)) {
    //                     return true;
    //                 }
    //             }
    //         }
    //         return false;
    //     }

    // }

    class grammar 
    {
        public:
        // Baca grammar dari file
        grammar(istream &is) 
        {
            string line;
            while (getline(is, line)) {
                line.erase(line.find_last_not_of("\r\n") + 1);
                if (line.size()) {
                    rule::ptr r = rule::create(line);
                    if (*r) {
                        rules_.push_back(r);
                    }
                }
            }

            // Get the terminals
            set<string> nonterminals;
            set<string> symbols;
            for (rule::const_ptr r : rules_) {
                nonterminals.insert(r -> left());
                for (const vector<string> &alternative : r -> right()) {
                    for (const string &symbol : alternative) {
                        symbols.insert(symbol);
                    }
                }
            }
            for (const std::string& symbol : symbols) {
                if (nonterminals.find(symbol) == nonterminals.end()) {
                    terminals_.push_back(symbol);
                }
            }
        }
    }




}



#endif // CYK_HPP