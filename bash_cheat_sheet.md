## *Bash cheat sheet*


_**grabbing commands output**_   
> **home_directory**="/home/user"  
> **initial_file**="file_name"  
> **output**="$(**$home_directory/$initial_file** | tr [:upper:] [:lower:] | tr -s [:space:] ' ' | tr -dc ' '[:alnum:])"  
