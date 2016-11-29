/*
 * Date: 2016年11月29日
 * Author: li
 */
package grains_lxc.svm;
import grains_lxc.stat_model.StatModel;
import org.opencv.ml.CvSVM;

public class My_SVM extends StatModel{

	CvSVM model_svm=null;
	
	public My_SVM(){
		model_svm=new CvSVM();
	}
	
	@Override
	public void load(String filename) {
	}

	@Override
	public void save(String filename) {

	}
	
	// http://stackoverflow.com/questions/23776610/svm-prediction-of-images-opencv
	public void sss() {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);

		Mat classes = new Mat();
		Mat trainingData = new Mat();
		Mat trainingImages = new Mat();
		Mat trainingLabels = new Mat();
		CvSVM clasificador;
		String path = "C:\\java workspace\\ora\\images\\Color_Happy_jpg";
		for (File file : new File(path).listFiles()) {
			Mat img = new Mat();
			Mat con = Highgui.imread(path + "\\" + file.getName(), Highgui.CV_LOAD_IMAGE_GRAYSCALE);
			con.convertTo(img, CvType.CV_32FC1, 1.0 / 255.0);

			img.reshape(1, 1);
			trainingImages.push_back(img);
			trainingLabels.push_back(Mat.ones(new Size(1, 75), CvType.CV_32FC1));

		}
		System.out.println("divide");
		path = "C:\\java workspace\\ora\\images\\Color_Sad_jpg";
		for (File file : new File(path).listFiles()) {
			Mat img = new Mat();
			Mat m = new Mat(new Size(640, 480), CvType.CV_32FC1);
			Mat con = Highgui.imread(file.getAbsolutePath(), Highgui.CV_LOAD_IMAGE_GRAYSCALE);

			con.convertTo(img, CvType.CV_32FC1, 1.0 / 255.0);
			img.reshape(1, 1);
			trainingImages.push_back(img);

			trainingLabels.push_back(Mat.zeros(new Size(1, 75), CvType.CV_32FC1));

		}

		trainingLabels.copyTo(classes);
		CvSVMParams params = new CvSVMParams();
		params.set_kernel_type(CvSVM.LINEAR);
		CvType.typeToString(trainingImages.type());
		CvSVM svm = new CvSVM();

		clasificador = new CvSVM(trainingImages, classes, new Mat(), new Mat(), params);

		clasificador.save("C:\\java workspace\\ora\\images\\svm.xml");
		Mat out = new Mat();

		clasificador.load("C:\\java workspace\\ora\\images\\svm.xml");
		Mat sample = Highgui.imread("C:\\java workspace\\ora\\images\\Color_Sad_jpg\\EMBfemale20-2happy.jpg",
				Highgui.CV_LOAD_IMAGE_GRAYSCALE);

		sample.convertTo(out, CvType.CV_32FC1, 1.0 / 255.0);
		out.reshape(1, 75);
		System.out.println(clasificador.predict(out));
	}
	
}
