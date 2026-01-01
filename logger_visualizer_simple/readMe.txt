current architecture : 

      collector + logger     // collects data from 'top' and 
                             // logs it in csv.logger
             |  
             |
             V
        
          syslog.csv         // data is logged here.

             ^
             |
             |

         visualizer/terminal_ui    // read data from logger and                                                      // generates a graph or display in terminal

 
