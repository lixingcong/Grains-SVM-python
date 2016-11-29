/*
 * Date: 2016年11月29日
 * Author: li
 */
package grains_lxc.svm;

import java.util.ArrayList;
import java.util.List;
import grains_lxc.features.My_Features;

public class Demo {

	public static void main(String[] args) {
		My_SVM my_svm=new My_SVM(1.0,0.1);
		My_Features features=new My_Features("/tmp/1.csv");
		
		features.load_saved_features();
		
		List<List<Float>> res_x=features.get_features_x();
		List<Float> res_y=features.get_features_y();
		
//		System.out.print(res_x);
		my_svm.train(res_x, res_y);
		System.out.print(my_svm.predict(res_x));
	}

}
