package yatra.generator;

import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

/**
 * @author Mitikaa
 *
 */
public class RdfGenerator {

	private static final String FILE_PATH = "/Users/Mitikaa/Desktop/Fall 2016/Semantic Web/Yatra/YatraCrawler/Output.csv";
	
	public static void main(String[] args){
		RdfGenerator rdfGenerator = new RdfGenerator();
		String rdfString = rdfGenerator.createRdfFromCSV();
		rdfGenerator.writeRdfFile(rdfString);
	}

	public String createRdfFromCSV() {
		StringBuilder rdfString = new StringBuilder();
		rdfString.append("<?xml version=\"1.0\"?>\n");
		rdfString.append("<!DOCTYPE rdf:RDF [\n");
		rdfString.append("	<!ENTITY xsd \"http://www.w3.org/2001/XMLSchema#\">\n");
		rdfString.append("	<!ENTITY rdfs \"http://www.w3.org/2000/01/rdf-schema#\">\n");
		rdfString.append("	<!ENTITY rdf \"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">\n");
		rdfString.append("	<!ENTITY yatra \"http://www.semanticweb.org/ontologies/2016/12/Yatra#\">\n");
		rdfString.append("]>\n");
		rdfString.append("<rdf:RDF\n");
		rdfString.append("	xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n");
		rdfString.append("	xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n");
		rdfString.append("	xmlns:yatra=\"http://www.semanticweb.org/ontologies/2016/12/Yatra#\">\n");
		rdfString.append(appendCSVData());
		rdfString.append("</rdf:RDF>");
		//System.out.println(rdfString.toString());
		return rdfString.toString();
	}
	
	private String appendCSVData(){
		ArrayList<ArrayList<String>> csvData = loadCSVData();
		StringBuilder rdfString = new StringBuilder();
		for (int i=1; i<csvData.size()-1; i++){
			ArrayList<String> row = csvData.get(i);
			rdfString.append("		<rdf:Description rdf:about=\"&yatra;automobile" + i +"\">\n");
			rdfString.append("		<yatra:hasVehicle rdf:datatype=\"&xsd;string\">" + row.get(0)  + "</yatra:hasVehicle>\n");
			rdfString.append("		<yatra:hasMilage rdf:datatype=\"&xsd;float\">" + row.get(5)  + "</yatra:hasMilage>\n");
			rdfString.append("		<yatra:hasFuelType rdf:datatype=\"&xsd;string\">" + row.get(3)  + "</yatra:hasFuelType>\n");
			rdfString.append("		<yatra:hasTransmissionType rdf:datatype=\"&xsd;string\">" + row.get(2)  + "</yatra:hasTransmissionType>\n");
			rdfString.append("		<yatra:hasImage rdf:datatype=\"&xsd;string\">" + row.get(4)  + "</yatra:hasImage>\n");
			rdfString.append("	</rdf:Description>\n");
		}
		System.out.println("Data appened!");
		return rdfString.toString();
	}
	
	@SuppressWarnings("deprecation")
	private ArrayList<ArrayList<String>> loadCSVData(){
		ArrayList<ArrayList<String>> csvData = null;
		ArrayList<String> row = null;
		String line;
		try {
			FileInputStream fileStream = new FileInputStream(FILE_PATH);
			DataInputStream dataStream = new DataInputStream(fileStream);
			csvData = new ArrayList<ArrayList<String>>();
			while((line = dataStream.readLine()) != null){
				row = new ArrayList<String>();
				String[] rowData = line.split(",");
				for(String data: rowData){
					row.add(data);
				}
				csvData.add(row);
			}
			fileStream.close();
			dataStream.close();
		} catch (FileNotFoundException e) {
			System.err.println("Error finding and loading CSV file");
			e.printStackTrace();
		} catch (IOException e){
			System.err.println("Error reading CSV file");
			e.printStackTrace();
		}
		System.out.println("File loaded!");
		return csvData;
	}
	
	private void writeRdfFile(String rdfString){
		PrintWriter out;
		try {
			out = new PrintWriter("/Users/Mitikaa/Desktop/Fall 2016/Semantic Web/Yatra/Yatra/Files/automobile.rdf");
			out.println(rdfString);
			out.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println("File written!");
	}
}
