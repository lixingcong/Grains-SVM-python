/*
 * Date: 2016年12月1日
 * Author: li
 */
package grains_lxc.rilbp;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.opencv.core.Core;

public class Demo {
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	public static void main(String[] args) {
		My_RILBP my_rilbp=new My_RILBP();
		
		Map<Integer, Integer> dict_sum_to_rilbp=(Map<Integer, Integer>)my_rilbp.get_d();
		
		for(int i=0;i<256;i++){
			System.out.print(i+": ");
			System.out.println(dict_sum_to_rilbp.get(new Integer(i)));
		}
	}
}
