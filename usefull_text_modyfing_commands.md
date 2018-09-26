## *Usefull Text Modifying Commands*


**initial_file** to lower, remove multiple spaces and not alphanumeric characters
> cat **initial_file** | tr [:upper:] [:lower:] | tr -s [:space:] ' ' | tr -dc ' '[:alnum:] > **result_file**


take lines 20-30 from **initial_file**
> cat **initial_file** | head -n 30 | tail -n 10 > **result_file**
