/*
 * Date: 2016年11月30日
 * Author: li
 */
package grains_lxc.imshow;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.highgui.Highgui;
import org.opencv.imgproc.Imgproc;

public class Demo {

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}

	public static void main(String[] args) {
		Mat mat1 = Highgui.imread("../data/grains/candou/1.jpg");
		Mat mat2 = new Mat(mat1.rows(),mat1.cols(),CvType.CV_8UC1); 
		// gray
		Imgproc.cvtColor(mat1, mat2, Imgproc.COLOR_RGB2GRAY);
		// resize window
		Imshow ims1 = new Imshow("input",400,300);
		ims1.showImage(mat1);
		
		Imshow ims2 = new Imshow("output");
		ims2.showImage(mat2);
	}

}
