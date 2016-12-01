/*
 * Date: 2016年12月1日
 * Author: li
 */
package grains_lxc.rilbp;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.opencv.core.Core;

public class Demo {
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	public static void main(String[] args) {
		My_RILBP my_rilbp=new My_RILBP();
		List<Integer> input_bin=new ArrayList<Integer>(Arrays.asList(1,1,1,1,0,0,0,1));
		System.out.println(My_RILBP.get_sum_from_bin(input_bin));
	}
}
