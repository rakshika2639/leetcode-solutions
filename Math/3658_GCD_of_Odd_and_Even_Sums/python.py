class Solution(object):
    def gcdOfOddEvenSums(self, n):
        """
        :type n: int
        :rtype: int
        """
        o=n**2
        e=n*(n+1)
        while e:
            o,e=e,o%e
        return abs(o)
        
        
