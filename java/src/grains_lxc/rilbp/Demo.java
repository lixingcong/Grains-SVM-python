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

import org.opencv.core.Core;

public class Demo {
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	
	public static void main(String[] args) {
		My_RILBP my_rilbp=new My_RILBP(3.0,10);
		My_RILBP my_rilbp1=new My_RILBP(4.0,10);
	

	}
}
