/*
 * Date: 2016年11月29日
 * Author: li
 */
package grains_lxc.features;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import grains_lxc.csv.My_CSV;

/*
 * CSV: splited by common
 * 
 * saved features csv file columns
 * ----------------------------------------------------------
 * | Chinese | category | color:R | color:G | Hu(1) | riLBP |
 * ----------------------------------------------------------
 * 
 * itemlist csv file columns, when category or Chinese are both 0, it means unknown item
 * -------------------------------------------
 * | Chinese | category | filename | is_good |
 * -------------------------------------------
 */

public class My_Features {

	String csv_features_save;
	String csv_split_char = ",";

	List<List<Double>> x = new ArrayList<List<Double>>();
	List<Double> y = new ArrayList<Double>();
	Map<String, String> dict_category_to_chinese = new HashMap<String, String>();
	List<String> features = null;

	public My_Features(String csv_features_save) {
		this.csv_features_save = csv_features_save;
	}

	public void load_saved_features() {
		My_CSV my_csv = new My_CSV(csv_features_save);
		features = my_csv.read();
		for (String line : features) {
			String[] line_splited = line.split(csv_split_char);
			dict_category_to_chinese.put(line_splited[1], line_splited[0]);
		}
		load_y_x_from_features();
	}

	private void load_y_x_from_features() {
		for (String line : features) {
			List<String> line_splited = Arrays.asList(line.split(csv_split_char));
			List<String> line_splited_x = line_splited.subList(2, line_splited.size());

			List<Double> this_x = new ArrayList<Double>();
			for (String _x : line_splited_x) {
				this_x.add(new Double(_x));
			}

			x.add(this_x);
			y.add(new Double(line_splited.get(1)));
		}
	}

	public String get_chinese_from_category(int c) {
		return dict_category_to_chinese.get(Integer.toString(c));
	}

	public List<Double> get_features_y() {
		return y;
	}

	public List<List<Double>> get_features_x() {
		return x;
	}

	public static void main(String[] args) {
		My_Features f = new My_Features("../data/test_features.csv");
		f.load_saved_features();
		// System.out.println(f.get_chinese_from_category(1));

		List<List<Double>> res_x = f.get_features_x();
		List<Double> res_y = f.get_features_y();

		for (int i = 0; i < res_y.size(); i++) {
			System.out.print(res_y.get(i));
			System.out.print(": ");
			System.out.println(res_x.get(i));
		}

	}
}
