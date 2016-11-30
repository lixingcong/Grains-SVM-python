/*
 * Date: 2016年11月30日
 * Author: li
 */
package grains_lxc.utils;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.highgui.Highgui;

public class Demo {
	
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	public static void main(String[] args) {
		Mat mat1 = Highgui.imread("/tmp/1.jpg");
		Mat mat2 = new Mat(mat1.rows(),mat1.cols(),CvType.CV_8UC1); 
		My_Utils ut=new My_Utils();
		
		double[] rgb=(ut.get_rgb_normolized(mat1, mat2));
		
		for(double i:rgb)
			System.out.print(i);
		
	}
}
