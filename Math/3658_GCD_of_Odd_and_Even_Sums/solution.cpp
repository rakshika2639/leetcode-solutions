class Solution {
public:
    int gcdOfOddEvenSums(int n) {
        int o=pow(n,2);
        int e=n*(n+1);
        while (e){
            int remainder = o % e;
            o = e;
            e = remainder;
            }
        return abs(o);
            


        
    }
};
