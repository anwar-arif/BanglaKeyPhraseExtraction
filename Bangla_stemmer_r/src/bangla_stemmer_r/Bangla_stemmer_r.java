package bangla_stemmer_r;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;

public class Bangla_stemmer_r {

    public static void main(String[] args) {
                
                String ruleFilePath = "G:\\semester\\semester 3-2\\project 300\\Bangla_stemmer_r rules in out\\rules.in" ;
                String inputFilePath = "G:\\semester\\semester 3-2\\project 300\\N-gram keyphrase\\FinalNgrams.txt" ;
                String outputFilePath = "G:\\semester\\semester 3-2\\project 300\\N-gram keyphrase\\StemmedNgrams.txt" ;
		
		RuleFileParser parser = new RuleFileParser(ruleFilePath);

		File file;
                file = new File(inputFilePath);
		
		try (BufferedReader inputFileReader = 
				new BufferedReader(new FileReader(file))) {
			String line;
                        FileWriter fw = new FileWriter(outputFilePath);
                        String newline = System.getProperty("line.separator") ;
                        BufferedWriter bw = new BufferedWriter(fw);
			while ((line = inputFileReader.readLine()) != null) {
				System.out.println(line);
                                int cnt = 0 ;
                                String str = "";
				for (String word : line.split("[\\s।%,ঃ]+")) {
					System.out.print(parser.stemOfWord(word) + " ");
//                                        bw.write(parser.stemOfWord(word) + " ") ;
                                        if( cnt == 1 ) str += " " ;
                                        cnt = 1 ;
                                        str += parser.stemOfWord(word) ;
				}
				System.out.println();
                                str += " # " ;
                                bw.write(str) ;
			}
                        bw.close() ;
                        fw.close() ;
		}
		catch (IOException exception) {
			exception.printStackTrace();
		}
	}
}
