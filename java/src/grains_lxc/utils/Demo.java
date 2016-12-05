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
		My_Preprocess mypreprocess=new My_Preprocess("../data/grains_6p/yundou/1.jpg");
		My_Utils ut=new My_Utils();
		
		double hue=(ut.get_Hue(mypreprocess.get_img(),mypreprocess.get_img_binary()));
		
		System.out.print(hue+"\n");
	}
}
