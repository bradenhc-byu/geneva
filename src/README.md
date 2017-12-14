# Gene Variant Analyzer (GeneVA)

Many diseases can be traced to mutations in the genes of the infected individual. While mutations can be easily identified through whole-genome sequencing, identifying which are deleterious remains a challenge. Many popular algorithms exist for this purpose, including many based on machine learning, but their accuracy remains relatively low. We attempt to address this issue by developing Gene Variant Analyzer (GeneVA), an automated pipeline for compiling mutation data and features and training machine learning algorithms using Weka 3. GeneVA allows for convenient identification of the features and algorithms most effective in predicting the clinical impact of a mutation on patients' lives.

### How to use GeneVA

- Make sure that Python 2.7 is installed on the host machine
- Decompress the geneva-{version}.tar.gz into the desired folder
- Run the following command from inside the geneva-{version} folder:

`python geneva.py`

### Software Design and Details
To build upon the work completed in this field, we created our own program to predict the accuracy of various algorithms: the Gene Variant Analyzer (GeneVA). GeneVA gathers any combination of selected features from its repertoire, runs them through various machine learning models, and outputs the model accuracy on a test data set, effectively serving as a way to analyze combinations of features and machine learning algorithms in predicting deleterious mutations.

#### ClinVar Dataset
To test GeneVA, we used variants taken from the ClinVar database, a publicly available resource containing data on human mutations along with interpretations of their clinical significance. We ignored mutations classified as "likely pathogenic," "risk factor," and "uncertain" significance, leaving only those classified as "benign" or pathogenic." We also stripped the data of duplicate entries and conflicting classifications, leaving our final ClinVar dataset with 55,886 mutations.

#### Weka
GeneVA interfaces with Weka, a machine learning workbench capable of pre-processing and filtering various datasets and putting them through different machine learning classifiers. By utilizing pre-existing machine learning, we were able to focus on automating the process of acquiring and pre-processing data, enabling facile implementation of new datasets and features and putting the focus more on finding significant features for classifying mutations.

#### Program Design Overview
In the attitude of simplicity, GeneVA is built around two major data types: the WekaData object and the Mutation object. An instance of the WekaData object is created every time the 'run' command is invoked from the program user interface, which functions much like a command line interpreter. The WekaData instance is then populated with a list of Mutation objects created from information in a file describing several mutations (the ClinVar database). Once initialized, additional features are added to the WekaData object to provide more information to the machine learning algorithms inside of Weka. The fully populated WekaData object is then written to a file in ARFF format and passed off to Weka to be analyzed using Weka's internal machine learning algorithms.

#### Initialization
Once GeneVA is run, a new WekaData object is initialized with a file containing variants. Relevant data is stored: the gene in which the mutation occurred, the index of the mutation, and the amino acids that were changed.  Each instance is represented as a Mutation object and added to the WekaData object during initialization.

Once all the mutations have been created, GeneVA loads several amino acid properties of each mutation into the WekaData object. We created a parser to parse the 94 amino acid properties found in the files aaindex2 and aaindex3. This allowed us to extract the property delta values across any two amino acids for each property. These delta values are critical in finding disease-causing mutations. If an amino acid change is larger, the numeric value for the properties will be higher, and the chance of the new amino acid acting differently will be higher--heightening the probability of a disease-causing mutation.

Unfortunately, not all of the mutations from our dataset were included in these amino acid property indices. Some mutations lack a property that others have, but have a property that others do not. These variations in amino acid property availability are handled by a Weka filter before the training data is passed into Weka. Once the WekaData object has been fully initialized, it is passed to the Wrangler to pick up more features.

#### Data Wrangling and Additional Features
The Wrangler object is responsible for gathering more feature information about mutations and updating the WekaData object with the additional data. To test different combinations of features, we are able to select which additional features we want the Wrangler to include before the program is run from the terminal user interface to the program. In order to reduce run-time, our program caches the data downloaded for each feature. Besides amino acid properties, we focused our efforts primarily on three different kinds of additional features: gene family, allele frequency, and phastCons score of the mutation. 

#### Weka Preparation
Weka uses attribute-relation file formatted (ARFF) files to train its algorithms. Once the WekaData object is fully populated, all the data is written to an ARFF file, with each mutation feature as an attribute. This ARFF file then undergoes a process that converts and filters the file to improve the training accuracy and efficiency. Once the file has been processed, Weka uses it in a series of algorithms that determine the accuracy of classifying the mutations as pathogenic or benign given different combinations of mutation features. 

#### Programming Tools
All code was written in Python 2.7. Collaboration and storage of code was done using GitHub, and our public repository can be found here.