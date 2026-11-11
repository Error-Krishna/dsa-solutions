class Solution {
    public boolean isAnagram(String s, String t) {
        int sizeS = s.length();
        int sizeT = t.length();
        HashMap <Character, Integer> hm1 = new HashMap<>();
        HashMap <Character, Integer> hm2 = new HashMap<>();
        
        if(sizeS != sizeT){
            return false;
        }

        for(int i = 0; i<sizeS; i++){
            hm1.put(s.charAt(i), hm1.getOrDefault(s.charAt(i),0)+1);
        
            hm2.put(t.charAt(i), hm2.getOrDefault(t.charAt(i),0)+1);
        }

        if(hm1.equals(hm2)){
            return true;
        }
        return false;
    }
}