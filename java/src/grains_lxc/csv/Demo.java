/*
 * Date: 2016年11月29日
 * Author: li
 */
package grains_lxc.csv;

import java.util.List;

public class Demo {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		My_CSV csv=new My_CSV("/tmp/1.csv");
		
		List<String> content_read=null;
		content_read=csv.read();
		
		for(String line:content_read){
			System.out.println(line);
		}
	}

}
