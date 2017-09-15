class sulu(object):
    def sum(self, nums, target):
        i = 0;
        arr = {}
        for i in range(len(nums)):
            if (target - nums[i]) in arr:
                return [arr[target - nums[i]], i]
            arr[nums[i]] = i

lis = [3, 2, 4]
tar = 6

print sulu().sum(lis, tar)