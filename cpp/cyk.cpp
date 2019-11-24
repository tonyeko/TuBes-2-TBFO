#include <fstream>
#include <iostream>
#include <bits/stdc++.h>

#include "grammar.hpp"
#include "cyk.hpp"
 
using namespace std;
int main()
{
    string cnf_file = "chowsky";
    string pythonfile;
    cin >> pythonfile;
    ifstream cnf(cnf_file);
    ifstream program(pythonfile);
    if (cnf && program) {
        MB::grammar grammar(cnf);
        string bacafile;
        getline(program, bacafile, '\0');
        string sentence[bacafile.length()-count(bacafile.begin(), bacafile.end(), '\n')];
        int j = 0;
        for (int i = 0; i < bacafile.length(); i++) {
            if (bacafile[i] == ' ') {
                sentence[j] = '~'; 
            } else if (bacafile[i] == '\t'){
                sentence[j] = '$';
            } else if (bacafile[i] == '\r'){
                sentence[j] = ';';
            } else if (bacafile[i] == '\n'){
                j--;
            } else {
                sentence[j] = bacafile[i];
            }
            j++;
        }
        // cout << j << bacafile.length()-count(bacafile.begin(), bacafile.end(), '\n') << endl;
        const size_t len = sizeof(sentence) / sizeof(sentence[0]);
        bool success = MB::cyk_parser(grammar).parse(sentence, sentence + len, cout);
        cout << "Success: " << boolalpha << success << '\n';
    }
    else {
        cerr << "Couldn't open " << cnf_file << " for reading\n";
    }
}