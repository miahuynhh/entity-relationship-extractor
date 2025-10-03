Project: Entity Relationship Visualizer W/ KG
Overview
(NOTE: Use of AI is strongly recommended for this assignment 🙂)

Build an interactive web application w/ Python backend that allows users to explore entities and relationships in free-form text. The interface should have two main components:
Left panel: a text box where the user can enter arbitrary free-form text.


Right panel: a dynamic visualization area that displays the entities and their relationships.
Please read carefully the Evaluation Instructions below as that is how your project will be graded.
Some Necessary Background
Example: “Alan Turing is from the United Kingdom, and Mr. Turing works on Computer Science.”
Entity Mentions: Text spans that refer to entities, e.g., “Alan Turing” and “Mr. Turing”.


Entities: The real-world objects behind mentions; here, both mentions point to the same entity, Alan Turing.


Relationships: Links between entities, expressed as subject–predicate–object (S–P–O) triplets. For instance, “Alan Turing is from England” → (Alan Turing, country of citizenship, United Kingdom).
These triplets are directed: the subject points to the object via the predicate. Direction matters because reversing it changes or breaks the meaning (e.g., (United Kingdom, country of citizenship, Alan Turing) does not make any sense).
Core Functionality
(Hint: Start with implementing core functionality step by step, and then build upon it for additional functionality)
Entity Extraction
Parse the input text to automatically identify named entities.
Use python lib `spacy` and load `en_core_web_sm`.
Note: It is CASE-SENSITIVE to the input text. But we will not take this into account when testing., you can directly apply the lib over input text.
Knowledge Graph Integration (What is a Knowledge Graph?)
Query the Wikidata Knowledge Graph API to retrieve the entities labels.
And then based on the retrieved entities, retrieve relationships labels between the identified entities. (e.g., https://www.wikidata.org/wiki/Q194057 -> label is `Mount Rainier`, and its relationship of Peter Rainier is labeled as `named_after` [https://www.wikidata.org/wiki/Property:P138])
Note: use `requests` lib, ask LLM to generate functions for retrieving entities and relationships between them if it exists. If there are multiple relationship labels, take the one with the shortest string length.
Graph Visualization
Display the entities labels as nodes in a graph, with edges representing relationships labels discovered in Wikidata.
Note: Each node and edge should be labeled with its type, and edge should be directed.
Additional Functionality (Try your best if you can & have time, will not be graded.)
Additional Visualization
Adjust node sizes based on “popularity,” measured by the entity’s in-degree (i.e., how many incoming links it has within Wikidata) relative to other entities within the same input text.
E.g., (Node A has 2 incoming edges, and node B has 8 incoming edges, node A’s size should be 4 times smaller than that of node B.)

Submission Instructions 
Your submission must include the following files and directory structure:
a1/
├── src/            # all your source code files
│   └── ...         
├── input.txt       # example input file
├── output.txt      # example output file
└── generate.sh     # script to run as specified below

Place all your code inside the src/ directory.
input.txt should contain the test input for your program.
output.txt should contain the expected output produced by your program. (you MUST also have generated the output based on the this provided input file content [save the content into input.txt])
generate.sh must be an executable shell script that can reproduce the results (e.g., compile and run your program, then write the output to output.txt).

Then:
From the parent directory of a1/, run the following command to create your submission archive:
tar -czvf a1.tar.gz a1/
This should create a compressed file named a1.tar.gz that contains the entire a1/ directory with the required structure.
Submit a1.tar.gz  to Canvas.

Evaluation Instructions 
Write a shell script that is named install.sh, and it should install necessary environments for eval.
Write a shell script that is named generate.sh that leverages your current Python backend, and it takes a txt file as input like follows:
./generate.sh --input ./input.txt --output ./output.txt
For example, if I have the text “Alan Turing was a pioneering mathematician and computer scientist from the United Kingdom.”
It should generate an output file, each line in output.txt is a json formatted string (key, value are str format with single quote) looks like follows. 
{'subject': 'Alan Turing', 'subject_qid': 'Q7251', 'predicate': 'country of citizenship', 'predicate_pid': 'P27', 'object': 'United Kingdom', 'object_qid': 'Q145'}
and if you have implemented the additional visualization, add ‘subject_in_degree’ and ‘object_in_degree’keys in the json string for each triplets found.
Other Requirements
For structure and readability, work with the LLM to design the application in sub-modules, with each feature implemented as a separate, manageable component.
You should document and write package requirements if there is any.
