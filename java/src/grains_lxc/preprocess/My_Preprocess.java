/*
 * Date: 2016年11月30日
 * Author: li
 */
package grains_lxc.preprocess;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.highgui.Highgui;
import org.opencv.imgproc.Imgproc;

public class My_Preprocess {

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}

	private Mat img = null;
	private Mat img_gray = null;
	private Mat img_bin = null;

	public My_Preprocess(String img_filename) {
		this(img_filename, 150.0, 150.0);
	}

	public My_Preprocess(String img_filename, double resize_width, double resize_height) {
		Mat mat = Highgui.imread(img_filename);
		this.img = new Mat();

		Size s = new Size(resize_width, resize_height);
		Imgproc.resize(mat, this.img, s, 0, 0, Imgproc.INTER_CUBIC);

		this.filter();
		this.rgb2gray();
		this.gray2binary();
		this.morphology(3.0);
		this.patch_img_bin_edge();
	}

	private void rgb2gray() {
		img_gray = new Mat();
		Imgproc.cvtColor(this.img, this.img_gray, Imgproc.COLOR_RGB2GRAY);
	}

	private void filter() {
		Mat mat = new Mat();
		Imgproc.medianBlur(img, mat, 1);
		Imgproc.bilateralFilter(mat, this.img, -1, 20.0, 20.0);
	}

	private void gray2binary() {
		img_bin = new Mat();
		Imgproc.threshold(this.img_gray, this.img_bin, 127.0, 255.0, Imgproc.THRESH_BINARY_INV + Imgproc.THRESH_OTSU);

	}

	private void morphology(double radius) {
		Size s = new Size(radius, radius);
		Mat kernel = Imgproc.getStructuringElement(Imgproc.MORPH_ELLIPSE, s);
		Mat mat = new Mat();
		Imgproc.morphologyEx(this.img_bin, mat, Imgproc.MORPH_CLOSE, kernel);
		img_bin = mat;
	}

	private void patch_img_bin_edge() {
		int width = img_bin.cols();
		int height = img_bin.rows();
		for (int i = 0; i < width; i++) {
			img_bin.put(0, i, (double) 0.0);
			img_bin.put(height - 1, i, (double) 0.0);
		}
		for (int i = 0; i < height; i++) {
			img_bin.put(i, 0, (double) 0.0);
			img_bin.put(i, width - 1, (double) 0.0);
		}
	}

	public Mat get_img() {
		return img;
	}

	public Mat get_img_gray() {
		return img_gray;
	}

	public Mat get_img_binary() {
		return img_bin;
	}
}
