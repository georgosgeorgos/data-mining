package sbnhw1;
/**
 *
 * @author georgos
 */
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
import java.io.BufferedReader;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.*;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.store.FSDirectory;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
/**
 *
 * @author georgos
 */
public class Lucene {
    
    //public static File file;
    public static File[] listOfFiles;
    public static String indexPath;

    public static Analyzer analyzer;
    public static Directory directory;
    //public static final Version luceneVersion = Version.LUCENE_43;
    public Lucene() throws IOException 
    {    
        indexPath = "index";
        //file = new File("src/lucene_tutorial/data.csv");
        File folder = new File("src/sbnhw1/data");
        listOfFiles = folder.listFiles();
        
        analyzer = new StandardAnalyzer();
        directory = FSDirectory.open(Paths.get(indexPath));
    }
    
    public static void createIndex() throws IOException
    {    
        IndexWriterConfig config;
        config = new IndexWriterConfig(analyzer);
        
        IndexWriter writer;
        writer = new IndexWriter(directory, config);
        
        for (int i=0; i<(listOfFiles.length); i++)
        {
            Document document = new Document();
            
            File file = listOfFiles[i];
            //System.out.println(file);
            FileInputStream fstream = new FileInputStream(file);
            InputStreamReader reader = new InputStreamReader(fstream);

            try (BufferedReader br = new BufferedReader(reader)) 
            {
                String line;
                String[] s;
                //Read File Line By Line
                Field name = null;
                Field age = null;
                Field description = null;
                Field diet = null;
                
                while ((line = br.readLine()) != null) 
                {
                    // Print the content on the console
                    s = line.split(";");
                    
                    Long f = Long.valueOf(s[1]);

                    name = new TextField("name", s[0], Field.Store.YES);
                    age = new NumericDocValuesField("age", f);
                    description = new TextField("description", s[2], Field.Store.YES);
                    diet = new TextField("diet", s[3], Field.Store.YES);
                }
                document.add(name);
                document.add(age);
                document.add(description);
                document.add(diet);
                //Close the input stream
            }
        //String text = "This is text to be indexed";
        writer.addDocument(document);
        }
        //br.close();
        writer.commit();
        writer.close();
    }
    
    public static void searchIndex(String string) throws IOException, ParseException
    {    
        DirectoryReader reader;
        reader = DirectoryReader.open(directory);
        
        IndexSearcher searcher;
        searcher = new IndexSearcher(reader);
        
        // query
        //Query q = new TermQuery( new Term("name", string));
        
        QueryParser parser;
        parser = new QueryParser("name", analyzer);
        
//        try
//        {
//            Long f = Long.valueOf(string);
//            String q = "name:" + f + " OR " + "diet:" + f + " OR " + "description:" + f;
//        }
//        catch(NumberFormatException e){}
        
        String q = "name:" + string + " OR " + "diet:" + string + " OR " + "description:" + string;
        
        Query query = parser.parse(q);
        TopDocs top = searcher.search(query, 10); // perform a query and limit results number
        ScoreDoc[] hits = top.scoreDocs;
        
        System.out.println("result:");
        if (hits.length > 0) {
            for (ScoreDoc hit : hits) 
            {
                Document hitDoc = searcher.doc(hit.doc);
                System.out.println(hit);
                System.out.println("doc number: " + hit.doc);
                System.out.println("doc score: " + hit.score);
                System.out.println("doc name field: " + hitDoc.get("name"));
                System.out.println("doc diet field: " + hitDoc.get("diet"));
                System.out.println("doc description field: " + hitDoc.get("description"));
                System.out.println("--------------------------------");
                System.out.println();
            }
        }
        else {
            System.out.println("no hits");
        }
            
        reader.close();
        directory.close();
    }
}
