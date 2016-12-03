/*
 * Date: 2016年11月29日
 * Author: li
 */
package grains_lxc.svm;

import grains_lxc.stat_model.StatModel;

import java.util.ArrayList;
import java.util.List;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.ml.CvSVM;
import org.opencv.ml.CvSVMParams;

public class My_SVM extends StatModel {

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}

	private CvSVM model_svm = null;
	final private String trained_model_filename = "../data/cv2_svm_model.xml";

	private CvSVMParams my_svm_params = new CvSVMParams();

	public My_SVM(double svm_param_C, double svm_param_gamma) {
		System.out.println("C, gamma= "+svm_param_C+", "+svm_param_gamma);
		this.model_svm = new CvSVM();
		this.my_svm_params.set_svm_type(CvSVM.C_SVC);
		this.my_svm_params.set_kernel_type(CvSVM.RBF);
		this.my_svm_params.set_C(svm_param_C);
		this.my_svm_params.set_gamma(svm_param_gamma);
	}

	public void train(List<List<Double>> train_x, List<Double> train_y) {
		int item_features_qty = train_x.get(0).size();
		int item_qty = train_y.size();

		Mat mat_train_x = new Mat(item_qty, item_features_qty, CvType.CV_32FC1);
		Mat mat_train_y = new Mat(item_qty, 1, CvType.CV_32FC1);

		// 填充数据到Mat类型中，将Double转成float型
		for (int i = 0; i < item_qty; i++) {
			mat_train_y.put(i, 0, train_y.get(i).floatValue());

			for (int j = 0; j < item_features_qty; j++) {
				mat_train_x.put(i, j, train_x.get(i).get(j).floatValue());
			}
		}

		model_svm.train(mat_train_x, mat_train_y, new Mat(), new Mat(), my_svm_params);
	}

	public List<Double> predict(List<List<Double>> test_x) {
		int item_features_qty = test_x.get(0).size();
		int item_qty = test_x.size();

		Mat mat_test_x = new Mat(item_qty, item_features_qty, CvType.CV_32FC1);
		Mat mat_test_y = new Mat(item_qty, 1, CvType.CV_32FC1);

		// 填充数据到Mat类型中，将Double转成float型
		for (int i = 0; i < item_qty; i++) {
			for (int j = 0; j < item_features_qty; j++)
				mat_test_x.put(i, j, test_x.get(i).get(j).floatValue());
		}

		model_svm.predict_all(mat_test_x, mat_test_y);

		List<Double> result = new ArrayList<Double>();
		for (int i = 0; i < mat_test_y.rows(); i++) {
			result.add(mat_test_y.get(i, 0)[0]);
		}

		return result;
	}

	public void load() {
		this.load(trained_model_filename);
	}
	
	@Override
	public void load(String filename) {
		model_svm.load(filename);
	}

	public void save() {
		this.save(trained_model_filename);
	}
	
	@Override
	public void save(String filename) {
		model_svm.save(filename);
	}
}
