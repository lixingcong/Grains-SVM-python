/*
 * Date: 2016年12月1日
 * Author: li
 */
package grains_lxc.crop;

import java.util.List;

import org.opencv.core.Core;
import org.opencv.core.Mat;

import grains_lxc.imshow.Imshow;
import grains_lxc.preprocess.My_Preprocess;

public class Demo {

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	public static void main(String[] args) {
		My_Preprocess mypreprocess=new My_Preprocess("../data/grains/candou/1.jpg");
		My_Crop mycrop=new My_Crop(2,2,false);
		List<Mat> img_cropped=mycrop.get_cropped_images(mypreprocess.get_img_gray());
		
		for(int i=0;i<img_cropped.size();i++){
			Imshow ims = new Imshow("c"+i);
			ims.showImage(img_cropped.get(i));
		}
	}

}
