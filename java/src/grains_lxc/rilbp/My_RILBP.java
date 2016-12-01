/*
 * Date: 2016年12月1日
 * Author: li
 */
package grains_lxc.rilbp;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;

import org.opencv.core.Core;

public class My_RILBP {

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	static double lbp_radius;
	static int lbp_neighbors;
	
	static Map<Integer, Integer> dict_sum_to_rilbp=null;
	static Map<Integer, Integer> dict_rilbp_to_histogram_x=null;
	
	static int histogram_x_width=0;
	
	int[] histogram_result=null;
	
	public My_RILBP() {
		this(1.0, 8);
	}
	
	public My_RILBP(double radius,int neighbors) {
		My_RILBP.lbp_radius=radius;
		My_RILBP.lbp_neighbors=neighbors;
		
		if(My_RILBP.dict_sum_to_rilbp == null){
			//System.out.println("generating...");
			My_RILBP.gen_dict_sum_to_rilbp();
			My_RILBP.gen_dict_rilbp_to_histogram_x();	
		}
	}
	
	static private void gen_dict_sum_to_rilbp(){
		int max_val=1<<lbp_neighbors;
		dict_sum_to_rilbp=new HashMap<Integer, Integer>();
		
		for(int i=0;i<max_val;i++){
			List<Integer> bits=new ArrayList<Integer>();
			
			for(int bit=0;bit<lbp_neighbors;bit++){
				bits.add(new Integer(i & (1<<bit)) >> bit);
			}
			
			int sum_=get_rilbp_from_bin(bits);
			dict_sum_to_rilbp.put(i, sum_);
		}
	}
	
	// 计算一个二进制列表的对应十进制值
	static private int get_sum_from_bin(List<Integer> input_list){
		int res=0;
		int len=input_list.size();
		for(int i=0;i<len;i++){
			res+=(input_list.get(i).intValue() << (i));
		}
		return res;
	}
	
	// 循环不变LBP的最小值
	static private int get_rilbp_from_bin(List<Integer> input_list){
		int len=input_list.size();
		int min_lbp=get_sum_from_bin(input_list);
		int this_sum;
		for(int i=1;i<len;i++){
			Integer first_element=input_list.remove(0);
			input_list.add(first_element);
			this_sum=get_sum_from_bin(input_list);
			if(this_sum<min_lbp)
				min_lbp=this_sum;
		}
		
		return min_lbp;
	}
	
	static private void gen_dict_rilbp_to_histogram_x(){
		TreeSet<Integer> set_rilbp=new TreeSet<Integer>();
		dict_rilbp_to_histogram_x=new HashMap<Integer, Integer>();
		
		for(Map.Entry<Integer, Integer> entry:dict_sum_to_rilbp.entrySet()){
			set_rilbp.add(entry.getValue());
		}
		
		Integer index=new Integer(0);
		for(Integer i:set_rilbp){
			dict_rilbp_to_histogram_x.put(i, index);
			index+=1;
		}
		
		histogram_x_width=index;
	}
	
	static public Object get_d(){
		return dict_sum_to_rilbp;
	}
}
