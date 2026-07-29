class Solution(object):
    def sumDivisibleByK(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        ans=0
        for i in list(set(nums)):
            if (nums.count(i))%k==0:
                ans+=i*nums.count(i)
        return ans
        
