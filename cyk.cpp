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
        string sentence[bacafile.length()-count(bacafile.begin(), bacafile.end(), '\n')];
        int j = 0;
        for (int i = 0; i < bacafile.length(); i++) {
            if (bacafile[i] == ' ') {
                sentence[j] = '~'; 
            } else if (bacafile[i] == '\r'){
                sentence[j] = ';';
            } else if (bacafile[i] == '\n'){
                j--;
            } else {
                sentence[j] = bacafile[i];
            }
            j++;
        }
        //cout << j << bacafile.length()-count(bacafile.begin(), bacafile.end(), '\n') << endl;
        const size_t len = sizeof(sentence) / sizeof(sentence[0]);
        bool success = MB::cyk_parser(grammar).parse(sentence, sentence + len, cout);
        cout << "Success: " << boolalpha << success << '\n';
    }
    else {
        cerr << "Couldn't open " << filename << " for reading\n";
    }
}