/*
 * Date: 2016年12月1日
 * Author: li
 */
package grains_lxc.features;

import java.util.List;

public class Demo {
	public static void main(String[] args) {
		My_Features f = new My_Features("../data/test_list.csv","../data/test_features.csv");
//		f.load_saved_features();
		f.load_itemlist();
		f.save_features("/tmp/1.csv");
		// System.out.println(f.get_chinese_from_category(1));

//		List<List<Double>> res_x = f.get_features_x();
//		List<Double> res_y = f.get_features_y();
//
//		for (int i = 0; i < res_y.size(); i++) {
//			System.out.print(res_y.get(i));
//			System.out.print(": ");
//			System.out.println(res_x.get(i));
//		}
	}
}
