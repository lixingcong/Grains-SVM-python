/*
 * Date: 2016年12月1日
 * Author: li
 */
package grains_lxc.features;

import java.util.List;

public class Demo {
	public static void main(String[] args) {
		My_Features f = new My_Features("../data/test_list.csv","../data/test_features.csv");
		f.load_saved_features();
//		f.load_itemlist();
//		f.save_features("/tmp/1.csv");

		My_Features img_f=new My_Features("../data/yundou-1.png");
		List<List<Double>> x=img_f.get_features_x();
		for(Double i:x.get(0)){
			System.out.println(i);
		}
	}
}
