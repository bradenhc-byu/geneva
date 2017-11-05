import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class parse_Variants {
	
	static String[] amnio_acids = {"Ala", "Arg", "Asn", "Asp", "Cys", "Gln", "Glu", "Gly", "His", "Ile", "Leu", "Lys", "Met", "Phe", "Pro", "Ser", "Thr", "Trp", "Tyr", "Val", "Ter"};
	static String acid_abbreviations = "ARNDCQEGHILKMFPSTWYV*";

	public static void main(String[] args) {
		List<String> lines = new ArrayList<String>();
	    
	    BufferedReader br;
	    FileInputStream fin;
	    try {
	    	fin = new FileInputStream("C:/cleaned_variants");
	        br = new BufferedReader(new InputStreamReader(fin));
	        
	        String line = br.readLine();
	        line = br.readLine();
	        while (line != null) {
	        	parse(line);
	        	line = br.readLine();
	        }
	        fin.close();
	        br.close();
	    } catch (FileNotFoundException e) {
	        System.out.println("Your Message");
	    } catch (IOException e) {
	        System.out.println("Your Message");
	    }
	}
	
	static String del = " ";
	public static void parse(String line) {
		//System.out.println(line);
		
		String[] items = line.split("\t");
		String GeneSymbol = items[1];
		
		//System.out.println(items[0]);
		
		// name = Gly1046Arg
		String name = items[0].substring(items[0].lastIndexOf("(")+3);
		name = name.substring(0, name.length()-1);
		
		//System.out.println(name);
		
		try {
			String location = ""+findNum(name);
			String to = name.substring(0,name.indexOf(location));
			String from = name.substring(name.indexOf(location)+location.length());
			
			to = convert(to);
			from = convert(from);
			
			//String location = name.substring(3,name.length()-3);
			
			System.out.println(GeneSymbol+del+location+del+to+del+from);
		} catch (Exception e) {
			
		}
	}
	
	public static String convert(String aminoAcid) {
		for (int i=0;i<amnio_acids.length;i++) {
			if (amnio_acids[i].toLowerCase().equals(aminoAcid.toLowerCase())) {
				return acid_abbreviations.substring(i, i+1);
			}
		}
		return "?";
	}
	
	public static int findNum(String str) {
		int res = new Scanner(str).useDelimiter("\\D+").nextInt();
		return res;
	}
}
