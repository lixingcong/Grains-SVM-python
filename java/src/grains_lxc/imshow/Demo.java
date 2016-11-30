/*
 * Date: 2016年11月30日
 * Author: li
 */
package grains_lxc.imshow;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.highgui.Highgui;

public class Demo {

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}

	public static void main(String[] args) {
		Mat mat = Highgui.imread("../data/grains/candou/1.jpg");
		Imshow ims = new Imshow("Title");
		ims.showImage(mat);
	}

}
