/*
 * Date: 2016年11月30日
 * Author: li
 */
package grains_lxc.shape;

import org.opencv.core.Core;
import org.opencv.core.Mat;

import grains_lxc.imshow.Imshow;
import grains_lxc.preprocess.My_Preprocess;

public class Demo {

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	public static void main(String[] args) {
		My_Preprocess preprocess=new My_Preprocess("../data/grains/candou/1.jpg");
		My_Shape myshape=new My_Shape(preprocess.get_img_gray());
		myshape.draw_contours_largest();
		
		myshape.get_humoments();
		
		Mat foreground=myshape.get_foreground();
		Imshow ims1 = new Imshow("fore");
		ims1.showImage(foreground);
	}

}
