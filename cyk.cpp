#include <fstream>
#include <iostream>
#include <bits/stdc++.h>

#include "grammar.hpp"
#include "cyk.hpp"
 
using namespace std;
int main()
{
    string filename = "cyk.dat";
    string inputfile;
    cin >> inputfile;
    ifstream ifs(filename);
    ifstream ifs2(inputfile);
    if (ifs && ifs2) {
        MB::grammar grammar(ifs);
        string bacafile;
        getline(ifs2, bacafile, '\0');
        string sentence[bacafile.length()];
        for (int i = 0; i < bacafile.length(); i++) {
            sentence[i] = bacafile[i];
        }
        //cout << bacafile << endl;
        const size_t len = sizeof(sentence) / sizeof(sentence[0]);
        bool success = MB::cyk_parser(grammar).parse(sentence, sentence + len, cout);
        cout << "Success: " << boolalpha << success << '\n';
    }
    else {
        cerr << "Couldn't open " << filename << " for reading\n";
    }
}