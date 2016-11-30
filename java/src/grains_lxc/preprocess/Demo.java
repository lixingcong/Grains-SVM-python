/*
 * Date: 2016年11月30日
 * Author: li
 */
package grains_lxc.preprocess;

import org.opencv.core.Core;
import org.opencv.core.Mat;

import grains_lxc.imshow.Imshow;

public class Demo {
	
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	public static void main(String[] args) {
		My_Preprocess preprocess=new My_Preprocess("../data/yundou-1.png");
		
		Mat mat1=preprocess.get_img();
		Mat mat2=preprocess.get_img_gray();
		
		Imshow ims1 = new Imshow("input");
		ims1.showImage(mat1);
		
		Imshow ims2 = new Imshow("output");
		ims2.showImage(mat2);
	}
}
