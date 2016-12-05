/*
 * Date: 2016年11月29日
 * Author: li
 */
package grains_lxc.svm;

import java.util.List;
import grains_lxc.features.My_Features;

public class Demo {

	public static void main(String[] args) {
		My_SVM my_svm=new My_SVM(8.0, 0.0078125);
		My_Features features_train=new My_Features("../data/grain_list.csv","../data/grain_features.csv");
		My_Features features_test=new My_Features("../data/test_list.csv","../data/test_features.csv");
		
		// 载入特征
//		features_train.load_saved_features();
		features_test.load_saved_features();
		
		// 如果不载入特征，可以重新计算特征
		features_train.load_itemlist();
		features_train.save_features();
//		features_test.load_itemlist();
//		features_test.save_features();
		
		List<List<Double>> train_x=features_train.get_features_x();
		List<Double> train_y=features_train.get_features_y();
		int train_number=train_y.size();
		
		List<List<Double>> test_x=features_test.get_features_x();
		List<Double> test_y=features_test.get_features_y();
		int test_number=test_x.size();

		// 训练，预测
		my_svm.train(train_x, train_y);
		List<Double> predict_y=my_svm.predict(test_x);
		
		// 统计结果
		int predict_error_counter = 0;
		for(int i=0;i<test_number;i++){
			double test_y_=test_y.get(i);
			double predict_val=predict_y.get(i);
			if(Math.abs(predict_val-test_y_)>0.01){
				System.out.format("[WRONG] predict=%f, test_y=%f\n",predict_val,test_y_);
				predict_error_counter+=1;
			}
		}
		
		// 正确率
		System.out.format("train_num=%d, test_num=%d, predict_correct_num=%d\n",train_number, test_number, test_number - predict_error_counter);
		System.out.format("predict accuracy=%.1f%%\n", (100 * (double)(test_number - predict_error_counter) / test_number));
		
		// 保存svm模型
		my_svm.save();
	}

}
