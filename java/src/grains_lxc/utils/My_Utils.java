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
import org.opencv.imgproc.Imgproc;

public class My_Utils {

	public My_Utils() {
	}

	public double[] get_Hue(Mat input_img, Mat input_img_bin) {
		int total_valid_pixels = 0;
		int sum_H=0;
		int height = input_img_bin.rows();
		int width = input_img_bin.cols();
		
		Mat img_hsv=new Mat();
		Imgproc.cvtColor(input_img, img_hsv, Imgproc.COLOR_BGR2HSV);

		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				if (input_img_bin.get(y, x)[0] > 0) {
					total_valid_pixels += 1;
					double[] this_px = img_hsv.get(y, x);
					sum_H += new Double(this_px[0]).intValue();
				}
			}
		}

		double sum_H_avg=(new Double(sum_H).doubleValue())/total_valid_pixels;
		// 周期化映射
		double sum_H_avg_periodically=Math.PI * sum_H_avg / 90;
		
		return (new double[] {(1+Math.cos(sum_H_avg_periodically))/2,(1+Math.sin(sum_H_avg_periodically))/2 });
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
