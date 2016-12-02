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

import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;

import grains_lxc.crop.My_Crop;
import grains_lxc.csv.My_CSV;
import grains_lxc.preprocess.My_Preprocess;
import grains_lxc.rilbp.My_RILBP;
import grains_lxc.shape.My_Shape;
import grains_lxc.utils.My_Utils;

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
	String csv_itemlist;
	String csv_split_char = ",";

	private List<List<Double>> x = new ArrayList<List<Double>>();
	private List<Double> y = new ArrayList<Double>();
	private Map<String, String> dict_category_to_chinese = new HashMap<String, String>();
	private List<String> features = null;
	private List<String> itemlist=null;
	
	private My_RILBP myrilbp=null;
	private My_Crop mycrop=null;
	private My_Utils myutils=null;

	public My_Features(String csv_itemlist, String csv_features_save) {
		this.csv_features_save = csv_features_save;
		this.csv_itemlist=csv_itemlist;
		this.mycrop=new My_Crop(3,3,false);
		this.myrilbp=new My_RILBP();
		this.myutils=new My_Utils();
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
	
	public void save_features(){
		this.save_features(csv_features_save);
	}
	
	public void save_features(String csv_filename){
		My_CSV my_csv = new My_CSV(csv_filename);
		my_csv.write(features);
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
	
	private void generate_features_from_y_x(){
		features=new ArrayList<String>();
		for(int i=0;i<y.size();i++){
			Integer this_y=new Integer(new Double(y.get(i)).intValue());
			int category_int=this_y.intValue();
			String category_str=this_y.toString();
			String this_line="";
			this_line+=get_chinese_from_category(category_int)+",";
			this_line+=category_str+",";
			for(Double this_feature:x.get(i)){
				this_line+=this_feature.toString()+",";
			}
			features.add(this_line);
		}
	}

	public String get_chinese_from_category(int c) {
		return dict_category_to_chinese.get(Integer.toString(c));
	}
	
	public void load_itemlist(){
		My_CSV my_csv = new My_CSV(this.csv_itemlist);
		itemlist=my_csv.read();
		int item_qty=itemlist.size();
		int index=1;
		for(String line:itemlist){
			String[] this_line_spilted=line.split(this.csv_split_char);
			dict_category_to_chinese.put(this_line_spilted[1], this_line_spilted[0]);
		}
		for(int i=0;i<itemlist.size();i++){
			System.out.println(index+"/"+item_qty);
			calc_a_features_from_itemlist(i);
			index+=1;
		}
		
		// normalize
		normalize_x();
		
		// convert y x to feature string
		generate_features_from_y_x();
	}
	
	private void calc_a_features_from_itemlist(int index){
		String this_line=itemlist.get(index);
		String[] this_line_spilted=this_line.split(this.csv_split_char);
		
		// skip item which has an abnormal flag
		if(this_line_spilted[3]=="0")
			return;
		
		String filename=this_line_spilted[2];
		calc_feature_from_filename(filename,Double.parseDouble(this_line_spilted[1]));
	}
	
	private void calc_feature_from_filename(String filename,double this_y){
		List<Double> this_feature=new ArrayList<Double>();
		
		My_Preprocess mypreprocess=new My_Preprocess(filename);
		
		// RGB features
		double[] RGB=myutils.get_rgb_normolized(mypreprocess.get_img(), mypreprocess.get_img_binary());
		this_feature.add(RGB[0]);
		this_feature.add(RGB[1]);
		
		// Hu(1)
		My_Shape myshape=new My_Shape(mypreprocess.get_img_gray());
		double Hu_1=myshape.get_humoments();
		this_feature.add(Hu_1);
		
		// LBP
		Mat img_foreground=myshape.get_foreground();
		Mat img_resized=new Mat();		
		Size s = new Size(48.0,48.0);
		Imgproc.resize(img_foreground, img_resized, s, 0, 0, Imgproc.INTER_CUBIC);
		List<Mat> img_splited=mycrop.get_cropped_images(img_resized);
		
		for(Mat img_:img_splited){
			List<Double> lbp_histogram=myrilbp.get_lbp_histogram(img_);
			this_feature.addAll(lbp_histogram);
		}
		
		// add to y and x
		x.add(this_feature);
		y.add(this_y);
	}
	
	private void normalize_x(){
		x=myutils.normalize_from_list(x);
	}

	public List<Double> get_features_y() {
		return y;
	}

	public List<List<Double>> get_features_x() {
		return x;
	}


}
