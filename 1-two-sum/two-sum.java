class Solution {
    public int[] twoSum(int[] nums, int target) {
        for(int i = 0; i<nums.length; i++){
            for(int j = 0; j<nums.length; j++){
                if(i!=j){
                    int num = nums[i] + nums[j];
                    if (num == target){
                        return new int[]{i,j};
                    }
                }
            }
        }
        return new int[]{};
    }
}

/* 
unique elements only (no indice repeated)
unique solution


*/



