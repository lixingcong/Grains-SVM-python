/*
 * Date: 2016年12月1日
 * Author: li
 */
package grains_lxc.rilbp;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;

public class My_RILBP {

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}

	static double lbp_radius;
	static int lbp_neighbors;

	static Map<Integer, Integer> dict_sum_to_rilbp = null;
	static Map<Integer, Integer> dict_rilbp_to_histogram_x = null;

	static int histogram_x_width = 0;

	int[] histogram_result = null;

	Mat img = null;

	public My_RILBP() {
		this(1.0, 8);
	}

	public My_RILBP(double radius, int neighbors) {
		if (My_RILBP.dict_sum_to_rilbp == null) {
			// System.out.println("generating...");
			My_RILBP.lbp_radius = radius;
			My_RILBP.lbp_neighbors = neighbors;
			My_RILBP.gen_dict_sum_to_rilbp();
			My_RILBP.gen_dict_rilbp_to_histogram_x();
		}
	}

	static private void gen_dict_sum_to_rilbp() {
		int max_val = 1 << lbp_neighbors;
		dict_sum_to_rilbp = new HashMap<Integer, Integer>();

		for (int i = 0; i < max_val; i++) {
			List<Integer> bits = new ArrayList<Integer>();

			for (int bit = 0; bit < lbp_neighbors; bit++) {
				bits.add(new Integer(i & (1 << bit)) >> bit);
			}

			int sum_ = get_rilbp_from_bin(bits);
			dict_sum_to_rilbp.put(i, sum_);
		}
	}

	// 计算一个二进制列表的对应十进制值
	static private int get_sum_from_bin(List<Integer> input_list) {
		int res = 0;
		int len = input_list.size();
		for (int i = 0; i < len; i++) {
			res += (input_list.get(i).intValue() << (i));
		}
		return res;
	}

	// 循环不变LBP的最小值
	static private int get_rilbp_from_bin(List<Integer> input_list) {
		int len = input_list.size();
		int min_lbp = get_sum_from_bin(input_list);
		int this_sum;
		for (int i = 1; i < len; i++) {
			Integer first_element = input_list.remove(0);
			input_list.add(first_element);
			this_sum = get_sum_from_bin(input_list);
			if (this_sum < min_lbp)
				min_lbp = this_sum;
		}

		return min_lbp;
	}

	static private void gen_dict_rilbp_to_histogram_x() {
		TreeSet<Integer> set_rilbp = new TreeSet<Integer>();
		dict_rilbp_to_histogram_x = new HashMap<Integer, Integer>();

		for (Map.Entry<Integer, Integer> entry : dict_sum_to_rilbp.entrySet()) {
			set_rilbp.add(entry.getValue());
		}

		Integer index = new Integer(0);
		for (Integer i : set_rilbp) {
			dict_rilbp_to_histogram_x.put(i, index);
			index += 1;
		}

		histogram_x_width = index;
	}

	// 灰度
	private double get_pixel_else_0(double idx, double idy) {
		int x = new Double(idx).intValue();
		int y = new Double(idy).intValue();
		if (x < img.cols() && y < img.rows())
			return img.get(y, x)[0];
		else
			return 0.0;
	}

	private double bilinear_interpolation(double x, double y) {
		double x1 = new Double(x).intValue();
		double y1 = new Double(y).intValue();
		double x2 = Math.ceil(x);
		double y2 = Math.ceil(y);

		double r1 = (x2 - x) / (x2 - x1) * get_pixel_else_0(x1, y1) + (x - x1) / (x2 - x1) * get_pixel_else_0(x2, y1);
		double r2 = (x2 - x) / (x2 - x1) * get_pixel_else_0(x1, y2) + (x - x1) / (x2 - x1) * get_pixel_else_0(x2, y2);

		return (y2 - y) / (y2 - y1) * r1 + (y - y1) / (y2 - y1) * r2;
	}

	private boolean is_int_equal_double(double num) {
		// 这里是个坑，刻度应为无穷小，这里取1E-17.
		if (Math.abs(num - (new Double(num).intValue())) <= 1E-17)
			return true;
		else
			return false;
	}

	static public Object get_d() {
		return dict_rilbp_to_histogram_x;
	}

	public List<Double> get_lbp_histogram(Mat input_img) {
		if (input_img.channels() != 1) {
			img = new Mat();
			Imgproc.cvtColor(input_img, img, Imgproc.COLOR_RGB2GRAY);
		} else {
			img = input_img;
		}

		histogram_result = new int[My_RILBP.histogram_x_width];
		Arrays.fill(histogram_result, 0);

		double r1, r2, c1, c2, w1, w2, res;
		int rilbp_sum, rilbp_min, histogram_x;

		for (int x = 0; x < img.cols(); x++) {
			for (int y = 0; y < img.rows(); y++) {
				double center = get_pixel_else_0(x, y);
				List<Double> pixels = new ArrayList<Double>();

				for (int point = 1; point <= My_RILBP.lbp_neighbors; point++) {
					double r = x + My_RILBP.lbp_radius * Math.cos(2 * Math.PI * point / My_RILBP.lbp_neighbors);
					double c = y - My_RILBP.lbp_radius * Math.sin(2 * Math.PI * point / My_RILBP.lbp_neighbors);

					if (r < 0.0 || c < 0.0) {
						pixels.add(0.0);
						continue;
					}

					if (is_int_equal_double(r)) {
						if (is_int_equal_double(c) == false) {
							c1 = new Double(c).intValue();
							c2 = Math.ceil(c);
							w1 = (c2 - c) / (c2 - c1);
							w2 = (c - c1) / (c2 - c1);

							res = w1 * get_pixel_else_0(r, c) + w2 * get_pixel_else_0(r, Math.ceil(c));
							res = res / (w1 + w2);

							pixels.add(new Double(res));
						} else {
							pixels.add(get_pixel_else_0(r, c));
						}
					} else if (is_int_equal_double(c)) {
						r1 = new Double(r).intValue();
						r2 = Math.ceil(r);
						w1 = (r2 - r) / (r2 - r1);
						w2 = (r - r1) / (r2 - r1);

						res = w1 * get_pixel_else_0(r, c) + w2 * get_pixel_else_0(Math.ceil(r), c);
						res = res / (w1 + w2);

						pixels.add(new Double(res));
					} else {
						// 双线性插值
						pixels.add(bilinear_interpolation(r, c));
					}

				}

				List<Integer> value_bits = thresholded(center, pixels);
				rilbp_sum = get_sum_from_bin(value_bits);
				rilbp_min = dict_sum_to_rilbp.get(rilbp_sum);
				histogram_x = dict_rilbp_to_histogram_x.get(rilbp_min);
				histogram_result[histogram_x] += 1;
			}
		}

		// 归一化
		double histogram_y_sum = 0;
		for (int i : histogram_result) {
			histogram_y_sum += i;
		}

		List<Double> histogram_y_normalized = new ArrayList<Double>();
		for (int i : histogram_result)
			histogram_y_normalized.add(new Double(i / histogram_y_sum));

		return histogram_y_normalized;
	}

	private List<Integer> thresholded(double center, List<Double> pixels) {
		List<Integer> out = new ArrayList<Integer>();
		for (Double i : pixels) {
			if (i.doubleValue() >= center)
				out.add(1);
			else
				out.add(0);
		}
		return out;
	}
}
