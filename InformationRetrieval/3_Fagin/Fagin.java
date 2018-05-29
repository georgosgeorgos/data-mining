import java.util.*;
import java.io.*;

public class Fagin {
	public static void main(String arg[]) throws Exception{
		// java Fagin C:\Users\cecin\Desktop\DataScience\DMT\hw01\output\output_cranESS_bm25_title.tsv C:\Users\cecin\Desktop\DataScience\DMT\hw01\output\output_cranESS_bm25_text.tsv C:\Users\cecin\Desktop\DataScience\DMT\hw01\output\output_Fagin2.tsv k
		if(arg.length != 4) {
			System.out.println("\nWrong number of arguments: given "+arg.length
					+" arguments, the correct number is 4.\n");
			System.out.println("Correct use:\n");
			System.out.println("java fagin output_title_file.tsv output_text_file.tsv"
					+ " output_fagin_file.tsv k");
			return;
		}
		String titlef = arg[0];
		String textf = arg[1];
		String outputf = arg[2];
		int k = Integer.valueOf(arg[3]);
		Fagin pr = new Fagin();
		/*
		String path = "C:\\Users\\cecin\\Desktop\\DataScience\\DMT\\hw01\\output\\";
		String titlef = path+"output_cranESS_bm25_title.tsv";
		String textf = path+"output_cranESS_bm25_text.tsv";
		String outputf = path+"output_Fagin2.tsv";
		*/
		Map<String, String> cran_title,cran_text;
		cran_title = pr.createQueryDic(titlef);
		cran_text = pr.createQueryDic(textf);
		pr.printFaginResults(cran_title,cran_text,k,outputf);
	}
	private Map<String, String> createQueryDic(String cranFile) throws Exception {
		Map<String, String> cranDic = new HashMap<String, String>();
		String row, Query_ID = "", Doc_ID, Score, key, Docs= "";
   		FileReader fr = new FileReader(cranFile);
   		BufferedReader br = new BufferedReader(fr);
   		row = br.readLine();
   		int n = 0;
   		String[] app;
   		while((row = br.readLine())!=null) {
   			app = row.split("\\t");
   			if(app.length>1) {
   				if(Query_ID.length()>0 && Integer.parseInt(Query_ID)==Integer.parseInt(app[0])){
   					Docs += app[1]+" ";
   					n++;
   				}
   				else{
   					if(n>0){
   						cranDic.put("Q"+Query_ID+"_rank", Docs);
   					}
   					n = 0;
   					Docs = app[1]+" ";
   				}
   				Query_ID = app[0];
   				Doc_ID = app[1];
   				Score = app[3];
   				key = 'Q'+Query_ID+'_'+Doc_ID;
   				cranDic.put(key, Score);
   			}
   		}
		cranDic.put("Q"+Query_ID+"_rank", Docs);
		cranDic.put("nQueries", Query_ID);
   		br.close();
   		return(cranDic);
	}
	
	private Map<Float,ArrayList<String>>  fagin(Map<String, String> cran_title, Map<String, String> cran_text, int q, int k) {
		Set<String> cdocs = new HashSet<String>();
		Map<Float,ArrayList<String>> fdocs = new TreeMap<Float,ArrayList<String>>(Collections.reverseOrder());
		String doc;
		int count = 0, row = 0;
		String[] title_docs;
		String[] text_docs;
		if(cran_title.get("Q"+q+"_rank")!=null) {
			title_docs = cran_title.get("Q"+q+"_rank").split(" ");
		}
		else {
			title_docs = new String[0];
		}
		if(cran_text.get("Q"+q+"_rank")!=null) {
			text_docs = cran_text.get("Q"+q+"_rank").split(" ");
			
		}
		else {
			text_docs = new String[0];
		}
		while(count<k && row<title_docs.length && row<text_docs.length) {
			doc = title_docs[row];
			if(cdocs.contains(doc)==false) {
				cdocs.add(doc);
			}
			else {
				count ++;
			}
			doc = text_docs[row];
			if(cdocs.contains(doc)==false) {
				cdocs.add(doc);
			}
			else {
				count ++;
			}
			row ++;
		}
		
		if(count<k) {
			if(row<title_docs.length) {
				while(row<title_docs.length) {
					doc = title_docs[row];
					cdocs.add(doc);
					row ++;
				}
			}
			else {
				while(row<text_docs.length) {
					doc = text_docs[row];
					cdocs.add(doc);
					row ++;
				}
			}
		}
		
		for (String key: cdocs) {
			float Score = 0;
			String s;
			s = cran_title.get("Q"+q+"_"+key);
			if(s!=null) {
				Score = Float.valueOf(s)*2; 
			}
			s = cran_text.get("Q"+q+"_"+key);
			if(s!=null) {
				Score += Float.valueOf(s);
			}
        	ArrayList<String> d = new ArrayList<String>();
        	if (fdocs.containsKey(Score)==false) {
        		d.add(key);
        		fdocs.put(Score, d);
        	}
        	else {
        		d = fdocs.get(Score);
        		d.add(key);
        		fdocs.put(Score, d);
        	}
		}
		return(fdocs);
	}

	private void printFaginResults(Map<String, String> cran_title, Map<String, String> cran_text, int k, String outputFile) {
		try {
			FileOutputStream tsv_writer = new FileOutputStream(outputFile);
			PrintStream writerow = new PrintStream(tsv_writer);
			writerow.println("Query_ID\tDoc_ID\tRank\tScore");
			for(int q=1; q<Integer.valueOf(cran_title.get("nQueries"))+1; q++) {
				Map<Float,ArrayList<String>> result = fagin(cran_title,cran_text,q,k);
				int r = 1;
				for(Float score: result.keySet()) {
					for(String doc: result.get(score)) {
						if(r<k+1) {
							writerow.print(String.valueOf(q)+"\t"+doc+"\t");
							writerow.print(String.valueOf(r)+"\t"+String.valueOf(score));
							writerow.println();
							r += 1;
						}
					}
				}
			}
			writerow.close();
		}
		catch (IOException e) {
			System.out.println("Error: " + e);
		    System.exit(1);
		}
		
	}
}
