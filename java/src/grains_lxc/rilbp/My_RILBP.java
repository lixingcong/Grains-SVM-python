/*
 * Date: 2016年12月1日
 * Author: li
 */
package grains_lxc.rilbp;

import java.util.List;
import java.util.Map;

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
	}
	
	static private void gen_dict_sum_to_rilbp(){
		
	}
	
	static public int get_sum_from_bin(List<Integer> input_list){
		int res=0;
		int len=input_list.size();
		for(int i=0;i<len;i++){
			res+=(input_list.get(i).intValue() << (i));
		}
		return res;
	}
}
