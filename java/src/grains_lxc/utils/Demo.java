/*
 * Date: 2016年11月30日
 * Author: li
 */
package grains_lxc.utils;

import java.util.ArrayList;
import java.util.List;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.highgui.Highgui;

import grains_lxc.preprocess.My_Preprocess;

public class Demo {
	
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	public static void main(String[] args) {
		My_Preprocess mypreprocess=new My_Preprocess("../data/yundou-1.png");
		My_Utils ut=new My_Utils();
		
		double[] rgb=(ut.get_rgb_normolized(mypreprocess.get_img(),mypreprocess.get_img_binary()));
		
		List<List<Double>> rgb_list=new ArrayList<List<Double>>();
		List<Double> rgb_a_line=new ArrayList<Double>();
		for(double i:rgb){
			System.out.print(i+"\n");
			rgb_a_line.add(i);
		}
		rgb_list.add(rgb_a_line);
		
		List<List<Double>> normalized=ut.normalize_from_list(rgb_list);
		for(List<Double> i:normalized){
			for(Double j:i){
				System.out.println(j);
			}
		}
	}
}
