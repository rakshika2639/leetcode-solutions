class Solution(object):
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        ans=0
        for i in range(len(nums)):
            for j in range(i+1,len(nums)):
                ans=max(ans,(nums[i]-1)*(nums[j]-1))
        return ans
        
