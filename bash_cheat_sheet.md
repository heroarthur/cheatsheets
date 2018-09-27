## *Bash cheat sheet*


_**grabbing commands output**_   
> **home_directory**="/home/user"  
> **initial_file**="file_name"  
> **output**="$(cat **$home_directory/$initial_file** | tr [:upper:] [:lower:] | tr -s [:space:] ' ' | tr -dc ' '[:alnum:])"  
  
_**checking file existence and permissions**_  
> **file_directory**="/home/user"; 
> **file_name**="/file_name"; 
> **file**="\$file_directory\$file_name"; 
> **message**="echo msg";    
  
> if [ -d "\$file" ]; then  
>   echo "\$file directory not exists"  
> elif [ ! -f "\$file" ] || [ ! -w "\$file" ]; then  
>   echo "$file not exists or not writable"  	
> else  
>   echo $message > $file  
> fi   



