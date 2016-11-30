/*
 * Date: 2016年11月30日
 * Author: li
 */
package grains_lxc.preprocess;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.highgui.Highgui;
import org.opencv.imgproc.Imgproc;

public class My_Preprocess {
	
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	Mat img=null;
	Mat img_gray=null;
	
	public My_Preprocess(String img_filename){
		this(img_filename, 72.0, 72.0);
	}
	
	public My_Preprocess(String img_filename,double resize_width,double resize_height){
		Mat mat=Highgui.imread(img_filename);
		this.img=new Mat();
		this.img_gray=new Mat();
		
		Size s=new Size(resize_width,resize_height);
		Imgproc.resize(mat,this.img,s);

		this.filter();
		this.rgb2gray();
	}
	
	private void rgb2gray(){
		Imgproc.cvtColor(this.img, this.img_gray, Imgproc.COLOR_RGB2GRAY);
	}
	
	private void filter(){
		Mat mat=new Mat();
		Imgproc.medianBlur(img, mat, 1);
		Imgproc.bilateralFilter(mat, this.img, -1, 20.0, 20.0);
	}

	public Mat get_img(){
		return img;
	}
	
	public Mat get_img_gray(){
		return img_gray;
	}
}
