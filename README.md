# Belief Revision Engine

This is a project made for the course **02180 Introduction to Artificial Intelligence** on DTU 

Made by:
- Stig Bødtker Petersen - s186333
- Emil Nymark Trangeled - s195478
- Hans Christian Let-Nissen - s205435
- Kasper Falch Skov - s205429

### Prerequsites

Before starting the python script you will have to install the required librarises using the following command:
        $ pip install -r requirements.txt


### Using the program

To start the program you will have to run the command:
        $ python cli.py

To use the different logical operators look in the table below:
|  Text | CLI symbol  |
| :---:  | :---:  |
| Not  | ~  |
| And  | &  |
| Or  | &#124;  |
| Implication  | >> or << |

When the script has been run you will be greeted with a menu with a set of options.
To enter a new belief you can us the command <code>r</code> then the formula. ex. <code>a | b</code> and the order of belief <code>0.5</code>
This can be seen in the example below:

        ####################################    
            Belief Revision Agent - Group 45    
        ####################################    

        ----------------menu----------------    

                available commands:

            r:  Belief revison
            e:  Empty belief base
            p:  Print belief base
            h:  Print help dialog
            q:  Quit

        ------------------------------------    

        Select command: **r**
        Revision

        Please enter formula: **a | b**
        Formula to CNF:  a | b 

        Please enter order (real number from 0 to 1): **0.5**