#ifndef CYK_HPP
#define CYK_HPP

#include <string>

namespace CYK 
{
    class Node {
        
        bool canDerive(non_terminal S, string w) {
            return canDerive1(S, w, 0, w.size());
        }

        bool canDerive1(non_terminal S, string w, int start, int end) {
            /* Basis */
            if (end == start + 1) {
                return        
            }
            /* Rekurens */
            for (each production S -> AB) {
                for (int mid = start + 1; mid < end; mid++) {
                    if (canDerive1(A, w, start, mid) && canDerive1(B, w, mid, end)) {
                        return true;
                    }
                }
            }
            return false;
        }

    }
}



#endif // CYK_HPP