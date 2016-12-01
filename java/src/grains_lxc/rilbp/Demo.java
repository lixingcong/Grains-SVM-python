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

import grains_lxc.preprocess.My_Preprocess;

public class Demo {
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	public static void main(String[] args) {
		My_RILBP my_rilbp=new My_RILBP();
		My_Preprocess mypreprocess=new My_Preprocess("../data/yundou-1.png");
		List<Double> histogram=my_rilbp.get_lbp_histogram(mypreprocess.get_img_gray());
		for(int i=0;i<histogram.size();i++){
			System.out.println(i+": "+histogram.get(i));
		}
	}
}
