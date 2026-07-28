class Solution(object):
    def checkGoodInteger(self, n):
        """
        :type n: int
        :rtype: bool
        """
        d=0
        s=0
        for i in list(str(n)):
            d+=int(i)
            s+=int(i)**2
        if s-d>=50:
            return True
        else:
            return False

        
