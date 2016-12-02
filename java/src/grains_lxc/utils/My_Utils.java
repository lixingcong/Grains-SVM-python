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

public class My_Utils {

	public My_Utils() {
	}

	public double[] get_rgb_normolized(Mat input_img, Mat input_img_bin) {
		int total_valid_pixels = 0;
		int[] sum_BGR = new int[] { 0, 0, 0 }; // Blue Green Red
		int height = input_img_bin.rows();
		int width = input_img_bin.cols();

		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				if (input_img_bin.get(y, x)[0] > 0) {
					total_valid_pixels += 1;
					double[] this_px = input_img.get(y, x);
					sum_BGR[0] += new Double(this_px[0]).intValue();
					sum_BGR[1] += new Double(this_px[1]).intValue();
					sum_BGR[2] += new Double(this_px[2]).intValue();
				}
			}
		}

		// 归一化
		double[] sum_BGR_double = new double[3];
		for (int i = 0; i < 3; i++) {
			sum_BGR_double[i] = sum_BGR[i] / total_valid_pixels;
		}

		double R = sum_BGR_double[2];
		double G = sum_BGR_double[1];
		double B = sum_BGR_double[0];
		double RGB = R + G + B;

		// web配色预览
		// System.out.format("#%02x%02x%02x\n",
		// new Double(R).intValue(),
		// new Double(G).intValue(),
		// new Double(B).intValue());

		return (new double[] { R / RGB, G / RGB, B / RGB });
	}

	public List<List<Double>> normalize_from_list(List<List<Double>> input_list) {
		List<List<Double>> results = new ArrayList<List<Double>>();
		int item_features_qty = input_list.get(0).size();

		for (List<Double> line : input_list) {
			List<Double> result_this_line = new ArrayList<Double>();
			Mat mat1 = new Mat(1, item_features_qty, CvType.CV_64FC1);
			Mat mat2 = new Mat(1, item_features_qty, CvType.CV_64FC1);

			for (int i = 0; i < item_features_qty; i++) {
				mat1.put(0, i, line.get(i));
			}

			Core.normalize(mat1, mat2, -1.0, 1.0, Core.NORM_MINMAX);

			for (int i = 0; i < item_features_qty; i++) {
				result_this_line.add(mat2.get(0, i)[0]);
			}

			results.add(result_this_line);
		}
		return results;
	}

}
