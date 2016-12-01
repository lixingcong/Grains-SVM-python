/*
 * Date: 2016年12月1日
 * Author: li
 */
package grains_lxc.crop;

import java.util.ArrayList;
import java.util.List;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.Rect;

public class My_Crop {

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}

	int pixels_split_horizontal, pixels_split_vertical;
	int blocks_split_horizontal, blocks_split_vertical;
	boolean is_pixel_mode;

	List<Mat> imgs = null;
	Mat img = null;

	public My_Crop(int split_horizontal, int split_vertical, boolean is_pixel_mode) {
		this.is_pixel_mode = is_pixel_mode;
		if (is_pixel_mode) {
			this.pixels_split_horizontal = split_horizontal;
			this.pixels_split_vertical = split_vertical;
		} else {
			this.blocks_split_horizontal = split_horizontal;
			this.blocks_split_vertical = split_vertical;
		}
	}

	private void assert_shape() throws Exception {
		int remains_1, remains_2;
		if (is_pixel_mode) {
			remains_1 = img.rows() % pixels_split_vertical;
			remains_2 = img.cols() % pixels_split_horizontal;
		} else {
			remains_1 = img.rows() % blocks_split_vertical;
			remains_2 = img.cols() % blocks_split_horizontal;
		}
		if (remains_1 != 0 || remains_2 != 0) {
			throw new Exception("image width or height should be devided by split_pixel or split_blks");
		}
	}

	public List<Mat> get_cropped_images(Mat input_img) {
		img = input_img;
		try {
			assert_shape();
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(1);
		}

		if (is_pixel_mode) {
			blocks_split_vertical = img.rows() / pixels_split_vertical;
			blocks_split_horizontal = img.cols() / pixels_split_horizontal;
		} else {
			pixels_split_vertical = img.rows() / blocks_split_vertical;
			pixels_split_horizontal = img.cols() / blocks_split_horizontal;
		}

		imgs = new ArrayList<Mat>();
		for (int block_num_vertical = 0; block_num_vertical < blocks_split_vertical; block_num_vertical++) {
			int y1 = pixels_split_vertical * block_num_vertical;

			for (int block_num_horizontal = 0; block_num_horizontal < blocks_split_horizontal; block_num_horizontal++) {
				int x1 = pixels_split_horizontal * block_num_horizontal;
				Rect roi = new Rect(x1, y1, this.pixels_split_horizontal, this.pixels_split_vertical);
				Mat img_this_block = new Mat(this.img, roi);
				imgs.add(img_this_block);
			}
		}

		return imgs;
	}
}
