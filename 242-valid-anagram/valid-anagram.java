class Solution {
    public boolean isAnagram(String s, String t) {
        int sizeS = s.length();
        int sizeT = t.length();
        int [] arr = new int[28];
        Arrays.fill(arr, 0);

        if(sizeS!=sizeT){
            return false;
        }
        for(int i = 0; i<sizeS; i++){
            arr[s.charAt(i)-'a']++;
        }
        for(int i = 0; i<sizeT; i++){
            arr[t.charAt(i)-'a']--;
        }
        for(int n: arr){
            if(n!=0){
                return false;
            }
        }

        return true;
    }
}