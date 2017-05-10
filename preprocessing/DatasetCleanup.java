import java.io.*;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;

public class DatasetCleanup {
	private static Scanner data;
	private static Scanner in = new Scanner(System.in);
	private static String[] labels;
	private static int groupSize;
	private static String[][] featureSpace;
	private static int[] survival;
	private static Number[][] featuresForJson;
		
	public static void main(String[] args) {
		readFile("train.csv");
		createFeatureSpace();
		fillMissingValues();
		createFamilySizeFeature();
		createAgeIntervalFeature();
		createDeckFeature();
		fillMissingValues();
		passengerInfo();
		//prepForJson();
		//toJson();
	}
	private static void readFile(String fileName) {
		try {
			data = new Scanner(new File(fileName));
		}
		catch (FileNotFoundException e) {
			System.out.println("File " + fileName + " not found");
			System.exit(0);
		}
	}
	private static void createFeatureSpace() {
		String line;
		Queue<String[]> featureGroup = new LinkedList<String[]>();
		while(data.hasNext()) {
			line = data.nextLine();
			String[] features = line.split(",");
			//for(int i = 0; i < features.length; i++)
				//System.out.println(features[i]);
			featureGroup.add(features);
		}
		String[] headers = featureGroup.poll();
		labels = new String[headers.length - 1];
		groupSize = featureGroup.size();
		survival = new int[groupSize];
		int j = 0;
		for(int i = 0; i < headers.length - 1; i++) {
			if(i == 1)
				j = 1;
			labels[i] = headers[i + j];
			//System.out.println(labels[i]);
		}
		featureSpace = new String[groupSize][12];
		//System.out.println(groupSize);
		addNewLabel("Title");
		for(int i = 0; i < groupSize; i++) {
			String[] features = featureGroup.poll();
			String name = (features[3] + "," + features[4]);
			name = name.substring(1, name.length() - 1);
			//System.out.println(name);
			featureSpace[i][0] = features[0];
			survival[i] = Integer.parseInt(features[1]);
			featureSpace[i][1] = features[2];
			featureSpace[i][2] = name;
			featureSpace[i][3] = features[5];
			featureSpace[i][4] = features[6];
			featureSpace[i][5] = features[7];
			featureSpace[i][6] = features[8];
			featureSpace[i][7] = features[9];
			featureSpace[i][8] = features[10];
			if(features[11].startsWith("F "))
				features[11] = features[11].substring(2);
			featureSpace[i][9] = features[11];
			featureSpace[i][10] = features[12];
			featureSpace[i][11] = createTitleFeature(i, features[4].trim());
			//System.out.println(featureSpace[i][0] + ": " + featureSpace[i][11]);
		}
	}
	private static String createTitleFeature(int index, String firstName) {
		String[] name = firstName.split(" ");
		if(name[0].equalsIgnoreCase("the")) {
			//System.out.println("*" + featureSpace[index][0] + ": " + name[0] + " " + name[1]);
			name[0] = name[1];
		}
		if(name[0].equalsIgnoreCase("Jonkheer.")
				|| name[0].equalsIgnoreCase("Don.")
				|| name[0].equalsIgnoreCase("Sir.")) {
			//System.out.println("*" + featureSpace[index][0] + ": " + name[0]);
			name[0] = "Mr.";
		}
		if(name[0].equalsIgnoreCase("Ms.")
				|| name[0].equalsIgnoreCase("Mme.")
				|| name[0].equalsIgnoreCase("Lady.")
				|| name[0].equalsIgnoreCase("Countess.")) {
			//System.out.println("*" + featureSpace[index][0] + ": " + name[0]);
			name[0] = "Mrs.";
		}
		if(name[0].equalsIgnoreCase("Mlle.")) {
			//System.out.println("*" + featureSpace[index][0] + ": " + name[0]);
			name[0] = "Miss.";
		}
		if(name[0].equalsIgnoreCase("Col.")
				|| name[0].equalsIgnoreCase("Major.")) {
			//System.out.println("*" + featureSpace[index][0] + ": " + name[0]);
			name[0] = "Offcr.";
		}
		/*
		if(!name[0].equals("Mr.")
				&& !name[0].equals("Mrs.")
				&& !name[0].equals("Miss.")
				&& !name[0].equals("Master.")
				&& !name[0].equals("Dr.")
				&& !name[0].equals("Rev.")) {
			System.out.println(name[0] + "\t" + featureSpace[index][0]);
		}
		*/
		return name[0];
	}
	private static void createFamilySizeFeature() {
		int numFeatures = addNewLabel("FamilySize");
		String[][] newFeatures = addBlankFeature(numFeatures);
		for(int i = 0; i < groupSize; i++) {
			int sibsp = Integer.parseInt(featureSpace[i][5]);
			int parch = Integer.parseInt(featureSpace[i][6]);
			newFeatures[i][numFeatures] = String.valueOf(sibsp + parch + 1);
		}
		//System.out.println(featureSpace[3][numFeatures - 1]);
		featureSpace = newFeatures;
		//System.out.println(featureSpace[3][numFeatures]);
	}
	private static void createAgeIntervalFeature() {
		int numFeatures = addNewLabel("AgeInterval");
		String[][] newFeatures = addBlankFeature(numFeatures);
		for(int i = 0; i < groupSize; i++) {
			String ageString = featureSpace[i][4];
			if(!featureSpace[i][4].equals("")) {
				double age = Double.parseDouble(ageString);
				if(age <= 10)
					newFeatures[i][numFeatures] = String.valueOf(0);
				else if(age > 60)
					newFeatures[i][numFeatures] = String.valueOf(2);
				else
					newFeatures[i][numFeatures] = String.valueOf(1);
			}
			//System.out.println(featureSpace[i][0] + ": "
							//+ ageString + ": "
							//+ newFeatures[i][numFeatures]);
		}
		featureSpace = newFeatures;
	}
	private static void createDeckFeature() {
		int numFeatures = addNewLabel("Deck");
		String[][] newFeatures = addBlankFeature(numFeatures);
		for(int i = 0; i < groupSize; i++) {
			if(!featureSpace[i][9].equals(null)
									&& !featureSpace[i][9].equals("")
									&& !featureSpace[i][9].equals("-1")) {
				int deckChar = 0;
				if(featureSpace[i][9].startsWith("F "))
					deckChar = 2;
				char deck = featureSpace[i][9].charAt(deckChar);
				newFeatures[i][numFeatures] = String.valueOf(deck);
			}
			else
				newFeatures[i][numFeatures] = String.valueOf(-1);
			//System.out.println(featureSpace[i][0] + ": " + newFeatures[i][numFeatures]);
		}
		featureSpace = newFeatures;
	}
	private static int addNewLabel(String newLabel) {
		int numFeatures = labels.length;
		String[] newLabels = new String[numFeatures + 1];
		for(int i = 0; i < labels.length; i++)
			newLabels[i] = labels[i];
		newLabels[numFeatures] = newLabel;
		labels = newLabels;
		return numFeatures;
	}
	private static String[][] addBlankFeature(int numFeatures) {
		String[][] newFeatures = new String[groupSize][numFeatures + 1];
		for(int i = 0; i < groupSize; i++)
			for(int j = 0; j < numFeatures; j++)
				newFeatures[i][j] = featureSpace[i][j];
		return newFeatures;
	}
	private static void fillMissingValues() {
		for(int i = 0; i < groupSize; i++) {
			for(int j = 0; j < labels.length; j++) {
				if(featureSpace[i][j].equals(null) || featureSpace[i][j].equals(""))
					featureSpace[i][j] = String.valueOf(-1);
			}
		}
	}
	private static void passengerInfo() {
		System.out.println("Please type in a Passenger ID Number. Enter a blank to quit.");
		String passID;
		int pID;
		do {
			System.out.print(">>> ");
			passID = in.nextLine();
			if(passID.equals(""))
				return;
			pID = Integer.parseInt(passID);
			while(pID > groupSize || pID < 1) {
				System.out.println("Invalid ID. Please Enter a new ID.");
				System.out.print(">>> ");
				passID = in.nextLine();
				if(passID.equals(""))
					return;
				pID = Integer.parseInt(passID);
			}
			System.out.println("---------------------------------------------------------");
			for(int i = 0; i < labels.length; i++) {
				System.out.println(String.format("%1$-13s", labels[i] + ":") + featureSpace[pID - 1][i]);
			}
			System.out.println(String.format("%1$-13s", "Survived:") + survival[pID - 1]);
			System.out.println("---------------------------------------------------------");
		} while(!passID.equals(""));
	}
	private static void prepForJson() {
		ArrayList<String> sexes = new ArrayList<String>(); //index 3
		ArrayList<String> embarks = new ArrayList<String>(); //index 10
		ArrayList<String> titles = new ArrayList<String>(); //index 11
		ArrayList<String> decks = new ArrayList<String>(); //index 14
		for(int i = 0; i < groupSize; i++) {
			if(!sexes.contains(featureSpace[i][3]))
				sexes.add(featureSpace[i][3]);
			if(!embarks.contains(featureSpace[i][10]))
				embarks.add(featureSpace[i][10]);
			if(!titles.contains(featureSpace[i][11]))
				titles.add(featureSpace[i][11]);
			if(!decks.contains(featureSpace[i][14]))
				decks.add(featureSpace[i][14]);
		}
		
		System.out.println("Sexes: " + sexes.size() + "\t" + sexes);
		System.out.println("Embarks: " + embarks.size() + "\t" + embarks);
		System.out.println("Titles: " + titles.size() + "\t" + titles);
		System.out.println("Decks: " + decks.size() + "\t" + decks);
		
		/*
		Feature			Index	JSON Index
		PID				0		0
		Pclass			1		1
		Sex				3		2
		Age				4		3
		Sibsp			5		4
		Parch			6		5
		Embarked		10		6
		Title			11		7
		FamilySize		12		8
		AgeInterval		13		9
		Deck			14		10
		*/
		featuresForJson = new Number[groupSize][11];
		for(int i = 0; i < groupSize; i++) {
			featuresForJson[i][0] = Integer.parseInt(featureSpace[i][0]);
			featuresForJson[i][1] = Integer.parseInt(featureSpace[i][1]);
			switch(featureSpace[i][3]) {
			case "male": featuresForJson[i][2] = 0;
				break;
			case "female": featuresForJson[i][2] = 1;
				break;
			}
			featuresForJson[i][3] = Double.parseDouble(featureSpace[i][4]);
			featuresForJson[i][4] = Integer.parseInt(featureSpace[i][5]);
			featuresForJson[i][5] = Integer.parseInt(featureSpace[i][6]);
			switch(featureSpace[i][10]) {
			case "S": featuresForJson[i][6] = 0;
				break;
			case "C": featuresForJson[i][6] = 1;
				break;
			case "Q": featuresForJson[i][6] = 2;
				break;
			}
			switch(featureSpace[i][11]) {
			case "Mr.": featuresForJson[i][7] = 0;
				break;
			case "Mrs.": featuresForJson[i][7] = 1;
				break;
			case "Miss.": featuresForJson[i][7] = 2;
				break;
			case "Master.": featuresForJson[i][7] = 3;
				break;
			case "Rev.": featuresForJson[i][7] = 4;
				break;
			case "Dr.": featuresForJson[i][7] = 5;
				break;
			case "Offcr.": featuresForJson[i][7] = 6;
				break;
			case "Capt.": featuresForJson[i][7] = 7;
				break;
			}
			featuresForJson[i][8] = Integer.parseInt(featureSpace[i][12]);
			featuresForJson[i][9] = Integer.parseInt(featureSpace[i][13]);
			switch(featureSpace[i][14]) {
			case "-1": featuresForJson[i][10] = -1;
				break;
			case "A": featuresForJson[i][10] = 0;
				break;
			case "B": featuresForJson[i][10] = 1;
				break;
			case "C": featuresForJson[i][10] = 2;
				break;
			case "D": featuresForJson[i][10] = 3;
				break;
			case "E": featuresForJson[i][10] = 4;
				break;
			case "F": featuresForJson[i][10] = 5;
				break;
			case "G": featuresForJson[i][10] = 6;
				break;
			case "T": featuresForJson[i][10] = 7;
				break;
			}
			System.out.print("[");
			for(int j = 0; j < 10; j++) {
				System.out.print(featuresForJson[i][j] + ", ");
			}
			System.out.println(featuresForJson[i][10] + "]");
		}
	}
	private static void toJson() {
		PrintStream features = null;
		PrintStream survived = null;
		try {
			features = new PrintStream(new File("features.json"));
			survived = new PrintStream(new File("survived.json"));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		features.print("[");
		for(int i = 0; i < groupSize - 1; i++) {
			features.print("[");
			for(int j = 0; j < 10; j++)
				features.print(featuresForJson[i][j] + ",");
			features.print(featuresForJson[i][10] + "],");
		}
		features.print("[");
		for(int i = 0; i < 10; i++)
			features.print(featuresForJson[groupSize - 1][i] + ",");
		features.print(featuresForJson[groupSize - 1][10] + "]]");
		survived.print("[");
		for(int i = 0; i < groupSize - 1; i++) {
			survived.print(survival[i] + ",");
		}
		survived.print(survival[groupSize - 1] + "]");
	}
}
