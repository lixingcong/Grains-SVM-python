/*
 * Date: 2016年11月29日
 * Author: li
 * https://www.mkyong.com/java/how-to-read-and-parse-csv-file-in-java/
 */
package grains_lxc.csv;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class My_CSV {

	String csv_file;
	String line = "";
	BufferedReader br = null;
	List<String> content_read = null;

	public My_CSV(String csv_file) {
		this.csv_file = csv_file;
	}

	private void read_all() {
		if (content_read == null) {
			content_read = new ArrayList<String>();

			try (BufferedReader br = new BufferedReader(new FileReader(csv_file))) {
				while ((line = br.readLine()) != null) {
					content_read.add(line);
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	public void write(List<String> data) {
		StringBuilder builder = new StringBuilder();

		for (String line : data) {
			builder.append(line + '\n');
		}

		try {
			PrintWriter writer = new PrintWriter(csv_file, "UTF-8");
			writer.write(builder.toString());
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}

	}

	public List<String> read() {
		read_all();
		return content_read;
	}

	public int get_total_rows() {
		return content_read.size();
	}

	// 仅供测试
	public static void main(String[] args) {
		My_CSV csv1 = new My_CSV("/tmp/1.csv");
		My_CSV csv2 = new My_CSV("/tmp/2.csv");

		List<String> content_read = null;
		content_read = csv1.read();

		for (String line : content_read) {
			System.out.println(line);
		}

		System.out.println(csv1.get_total_rows());

		List<String> content_write = Arrays.asList("Line 1: hello world", "Line 2: Java is good");
		csv2.write(content_write);
	}
}
