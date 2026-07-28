class Solution(object):
    def restoreString(self, s, indices):
        """
        :type s: str
        :type indices: List[int]
        :rtype: str
        """
        n=len(s)
        ans=""
        for i in range(n):
            x=indices.index(i)
            ans+=s[x]
        return ans
        
