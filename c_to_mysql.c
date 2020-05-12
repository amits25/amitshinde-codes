/*#####################################################################
	Author: Amit Shinde.
	Desc  : Simple C program that connects to MySQL Database server
         - This code will perform 1. Create Table 
                                  2. Insert into table
                                  3. Update  table 
                                  4. Delete Row from table
                                  5. Drop Table
         - Note: Every function is Generic. (no any restriction on table structure)
	Date  : 20 April 2020
      commands to run code:
      prerequsit command:(linux 16.04 LTS)
         note :- install mysql and create schema.
         1. sudo apt-get install libmysqlclient-dev
         2. mysql_config --libs
         3. mysql_config --cflags
      command to run:- 
         1. gcc -o output-file $(mysql_config --cflags) c_to_mysql.c $(mysql_config --libs)
         2. ./output-file
#######################################################################*/

#include <mysql/mysql.h>
#include <stdio.h>
#include <string.h>
#include<stdlib.h> 
//#include <mysql/my_global.h>

/* Global decleration*/
   MYSQL *conn;
   MYSQL_RES *res;
   MYSQL_ROW row;
   MYSQL_ROW row1;
   int result=0;
   char *table_update;
   int column_count=0;
   char *output_select_query[100];
  
 /* ########################## CONNECTION()###############################
 Connect to database */
int Connect_To_Mysql(char *ser, char *usr, char *pass)
{
   // printf("\n @ inside  Connect_To_Mysql Function\n");
   char *server = ser;
   char *user = usr;
   char *password = pass; 

   conn = mysql_init(NULL);
    if (!mysql_real_connect(conn, server,
         user, password, NULL, 0, NULL, 0)) {
         fprintf(stderr, "%s\n", mysql_error(conn));
         return 1;
      }
   return 0;
} 

 /* ############################# SELECT-*-TABLE()########################
 GENERIC - Execute Select query */
 void execute_Select_Query()
{  
    //printf("\n @ inside  execute_Select_Query Function\n");
   char *query="select * from  ";
   char *input;
   input = (char*) malloc(256);
   table_update=(char *) malloc(1 + strlen(input) );
   printf("\nEnter Table Name ::");
   scanf("%255s", input);
   strcpy(table_update, input);
   char * Final_query = (char *) malloc(1 + strlen(query)+ strlen(input) );
   strcpy(Final_query, query);
   strcat(Final_query, input);  //select query with user provided table name

   /*find columns from table  */ 
    char *columns="SELECT count(*) FROM information_schema.columns WHERE table_name = "; // Or int num_fields = mysql_num_fields(result);
    char *first="'" ;
    char *second="'";
    char * Final = (char *) malloc(1 + strlen(columns)+ strlen(input)+ strlen(first)+ strlen(second) );
    strcpy(Final,columns);
    strcat(Final,first);
    strcat(Final,input);
    strcat(Final,second);
    mysql_query(conn, Final);  // Query to find column no. for user provided table 
    res = mysql_use_result(conn);
    row1 = mysql_fetch_row(res);
    int size = atoi(row1[0]);  // column no in int format.
    column_count=size;
    //printf("colums size %d::\n", size);
    mysql_free_result(res); 
    
   // Initilization of output array
   for (int i=0; i < 100; i++)
   {
      output_select_query[i]= (char*) malloc(256);
      
   }


    /*  execte select query*/
    if (mysql_query(conn, Final_query)) {
        fprintf(stderr, "%s\n", mysql_error(conn));
      
   }
   res = mysql_use_result(conn);   

   /* table output */
   printf("MySQL Tables contains from table:: %s\n", input);
   while ((row = mysql_fetch_row(res)) != NULL){  
      printf("* ") ;
      for(int c=0; c<size;c++)        // for loop to print table rows and column Dyanamicall 
     { 
       printf("%s ", row[c]);
       strcpy(output_select_query[c],row[c]);
      // printf("\n %s  $$$ \n", output_select_query[c]);
       printf("|");
     }
     printf("\n");
   }
   
  /* for (int c1=0; c1 < size; c1++)
   {
      printf("\n %d ", c1);
      printf("\n%s", output_select_query[c1]);
      
   }*/

  // free(Final_query);
  // free(Final);

}

 /* ########################## SHOW-ALL SCHEMAS() #######################################
 show all DB's  */
void Show_All_Schemas(){
   //printf("\n @ inside Show_All_Schemas Function\n");
    if (mysql_query(conn, "show databases ")) {
      fprintf(stderr, "%s\n", mysql_error(conn));
      
   }

   res = mysql_use_result(conn);

   /* table output  */
   printf("MySQL  database:\n");
   while ((row = mysql_fetch_row(res)) != NULL)
      printf(" # %s  \n", row[0]);

}

 /* ####################### SELECT-SCHEMA() ##########################################
select DB */
void Select_DB(){
   // printf("\n @ inside Select_DB Function\n");
   char *input;
   input = (char*) malloc(256);
   //Show_All_Schemas();
   printf("Ebter schema name::");
   scanf("%255s", input);
   char *fix="use ";
   char * query = (char *) malloc(1 + strlen(input)+ strlen(fix) );
   strcpy(query, fix);
   strcat(query, input);
   //printf("schema selected::%s\n", input);

/* accept schema name from user then execeute query*/
 if (mysql_query(conn,query)) {
      fprintf(stderr, "%s\n", mysql_error(conn));
      
   }
   // Execute show tables query for user selected schema
   mysql_query(conn,"show tables") ;
     
   res = mysql_use_result(conn);

   /* table output*/
   printf("MySQL  database tables::\n");
   while ((row = mysql_fetch_row(res)) != NULL)
      printf(" # %s  \n", row[0]);
   
   free(query);
}
/* ########################################## UPDATE-TABLE()##############################################
  Execute Update Query*/
void Execut_Update_Query(){
    printf("\n @ inside Execut_Update_Query Function\n");
   char *update="UPDATE ";
   char *Set=" SET ";
   char *cloumn;
   cloumn = malloc(256); 
   char *To_value;
   To_value = malloc(256);
   char *Eqyuals=" ='";
   char *second="'";
   char *where=" WHERE ";
   char *value;
   value = malloc(256);
    char *Row_Unic;
   Row_Unic = malloc(256);
   char *Update_Query= (char *) malloc(1 + strlen(update)+ strlen(table_update)+ strlen(Set)+ strlen(cloumn)+ strlen(Eqyuals)+ strlen(second)+ strlen(where)+ strlen(value)+ strlen(Eqyuals)+ strlen(second)+ strlen(To_value)+ strlen(Row_Unic) );
   /*Show_All_Schemas();
   Select_DB();
   execute_Select_Query();*/
   printf("Enter colume name which you want to update::\n");
   scanf("%255s", cloumn);
   printf("Updated Value::\n");
   scanf("%255s", To_value);
   printf("Enter uniq row column name::\n");
   scanf("%255s", Row_Unic);
   printf("print Unic row Value::\n");
   scanf("%255s", value);
   strcpy(Update_Query,update);
   strcat(Update_Query, table_update);
   strcat(Update_Query, Set);
   strcat(Update_Query,cloumn);
   strcat(Update_Query,Eqyuals);
   strcat(Update_Query,To_value);
   strcat(Update_Query,second);
   strcat(Update_Query,where);
   strcat(Update_Query, Row_Unic);
   strcat(Update_Query,Eqyuals);
   strcat(Update_Query,value);
   strcat(Update_Query,second);
   printf("\n%s\n", Update_Query );

   if (mysql_query(conn,Update_Query)) {
      fprintf(stderr, "%s\n", mysql_error(conn));
      
   }
   execute_Select_Query();
   
   free(Update_Query);


}
/* ################################## GENERIC-Update() ######################################## 
  Execte update row query
*/
void Execute_Generic_Update_Query(){
   //Preparing Query
   char *update="UPDATE ";
   char *Set=" SET ";
   char *Eqyuals=" ='";
   char *second="'";
   char *where=" WHERE ";
   char *coma=",";
   char *value;
   value = malloc(256);
   char *Row_Unic;
   Row_Unic = malloc(256);

   //column count;
    char *columns="SELECT count(*) FROM information_schema.columns WHERE table_name = "; // Or int num_fields = mysql_num_fields(result);
    char *first="'" ;
    //char *second="'";
    char * Final = (char *) malloc(1 + strlen(columns)+ strlen(table_update)+ strlen(first)+ strlen(second) );
    strcpy(Final,columns);
    strcat(Final,first);
    strcat(Final,table_update);
    strcat(Final,second);
    mysql_query(conn, Final);  // Query to find column no. for user provided table 
    res = mysql_use_result(conn);
    row1 = mysql_fetch_row(res);
    int size = atoi(row1[0]);
    column_count=size;
    printf("\n num_field ::%d", size);
    mysql_free_result(res);

   
    //column names
   char *get_all_columns_name="SHOW COLUMNS FROM ";
   char *get_all_columns_name_query= (char*) malloc(1 + strlen(get_all_columns_name)+ strlen(table_update));
   strcpy(get_all_columns_name_query, get_all_columns_name);
   strcat(get_all_columns_name_query, table_update);
   printf("\n %s", get_all_columns_name_query);
   //execute query
    if (mysql_query(conn,get_all_columns_name_query)) {
      fprintf(stderr, "%s\n", mysql_error(conn));
    }
   res = mysql_use_result(conn);
   char *keyword[size];
   char *insert_values[size];
   for (int c=0; c < size; c++)
   {
      keyword[c]= (char*) malloc(256);
      insert_values[c]= (char*) malloc(256);
   }

   /* insert data into arrays */
   int c1=0;
   printf("\nMySQL %s table colums name and type and present values::\n", table_update);
   while ((row = mysql_fetch_row(res)) != NULL){
      
       printf("%d", c1);
       printf(" # %s :: %s :: %s \n", row[0], row[1], output_select_query[c1]);
       //strcpy(keyword[c1], row[0]);
       c1++;
       printf("\n");

   }

   //user Interface for upodtaed values
   int number=0;
   printf("\n How much column do you want to uodate out of %d::", size);
   scanf("%d", &number);
    for(int r=0; r< number; r++){
       printf("\n Enter column name::");
       scanf("%255s", keyword[r]);
       printf("\nEnter values for column::");
       scanf("%255s", insert_values[r]);

    }
    
   printf("print Unic column::\n");
   scanf("%255s", Row_Unic);
   printf("\n Enter uniqe value for unique::");
   scanf("%255s", value);
   
   // Conciatation for update Query
   char *GENERIC_Uodate_query=(char*) malloc(2048);
   strcpy(GENERIC_Uodate_query,update);
   strcat(GENERIC_Uodate_query,table_update);
   strcat(GENERIC_Uodate_query,Set);
   for (int e=0; e< number; e++){
      strcat(GENERIC_Uodate_query,keyword[e]);
      strcat(GENERIC_Uodate_query,Eqyuals);
      strcat(GENERIC_Uodate_query,insert_values[e]);
      strcat(GENERIC_Uodate_query,second);
      if( e < number-1){
         strcat(GENERIC_Uodate_query,coma);}
   }

   strcat(GENERIC_Uodate_query, where);
   strcat(GENERIC_Uodate_query,Row_Unic);
   strcat(GENERIC_Uodate_query,Eqyuals);
   strcat(GENERIC_Uodate_query,value);
   strcat(GENERIC_Uodate_query,second);

   printf("\n Execute Query= %s ", GENERIC_Uodate_query);   // Generic Update Query

   // Execute Update Query
    if (mysql_query(conn,GENERIC_Uodate_query)) {
      fprintf(stderr, "%s\n", mysql_error(conn));
     
   }
    execute_Select_Query();
   
   /* Free Memory
     free(GENERIC_Uodate_query);
     free(keyword);
     free(insert_values);
     free(Final);
     free(get_all_columns_name);
     free(output_select_query);
     free(output_select_query); */
   
   // UPDATE MyGuests SET firstname = 'AMIT', lastname ='SHINDE' WHERE id = 1;
}

/* ############################################# INSERT-INTO-TABLE() #########################################
  GENERIC - execute Insert Query For any Table*/
void Execute_Insert_query()
{
   // printf("\n @ inside Execute_Insert_query Function\n");

      /*find columns count from table  */ 
    char *columns="SELECT count(*) FROM information_schema.columns WHERE table_name = "; // Or int num_fields = mysql_num_fields(result);
    char *first="'" ;
    char *second="'";
    char * Final = (char *) malloc(1 + strlen(columns)+ strlen(table_update)+ strlen(first)+ strlen(second) );
    strcpy(Final,columns);
    strcat(Final,first);
    strcat(Final,table_update);
    strcat(Final,second);
    mysql_query(conn, Final);  // Query to find column no. for user provided table 
    res = mysql_use_result(conn);
    row1 = mysql_fetch_row(res);
    int size = atoi(row1[0]);
    printf("\n num_field ::%d", size);
    mysql_free_result(res);
  
   //get all colums name and type from database
   char *get_all_columns_name="SHOW COLUMNS FROM ";
   char *get_all_columns_name_query= (char*) malloc(1 + strlen(get_all_columns_name)+ strlen(table_update));
   strcpy(get_all_columns_name_query, get_all_columns_name);
   strcat(get_all_columns_name_query, table_update);
   printf("\n %s", get_all_columns_name_query);
   //execute query
    if (mysql_query(conn,get_all_columns_name_query)) {
      fprintf(stderr, "%s\n", mysql_error(conn));
    }
   res = mysql_use_result(conn);
   char *keyword[size];
   char *insert_values[size];
   for (int c=0; c < size; c++)
   {
      keyword[c]= (char*) malloc(256);
      insert_values[c]= (char*) malloc(256);
   }

   /* insert data into arrays */
   int c1=0;
   printf("\nMySQL %s table colums name and type::\n", table_update);
   while ((row = mysql_fetch_row(res)) != NULL){
      
       printf("%d", c1);
       printf(" # %s :: %s \n", row[0], row[1]);
       strcpy(keyword[c1], row[0]);
       c1++;
       printf("\n");

   }
   //accept values from user to insert
   for (int c=0; c< size;c++)
   {
      printf (" for %s::\n", keyword[c]);
       printf("\nEnter value to be insert into cloumn::");
       scanf("%255s", insert_values[c]);
   }
 /*  
   //to print output of arrays
  for (int c=0; c < size; c++)
   {
      printf("%d  ", c);
      printf("%s ", keyword[c]);
      printf("%s\n",insert_values[c]);
   }*/
   
   //preparing for Insert Query
   char *insert="insert into ";
   char *open_brac=" ( ";
   char *close_brac=" )";
   char *coma=", ";
   char *values="values( ";
   char *double_quote="'";
   char *Insert_quer=(char *) malloc(1024+ strlen(insert)+ strlen(open_brac) + strlen(close_brac)+ strlen(table_update)+ strlen(values));
   
   //concatation process
   strcpy(Insert_quer,insert);
   strcat(Insert_quer,table_update);
   strcat(Insert_quer,open_brac);
   for (int c=0; c<size; c++)
   {
      strcat(Insert_quer,keyword[c]);
      if (c < size-1){
      strcat(Insert_quer,coma);
      }
   }
   strcat(Insert_quer,close_brac);
   strcat(Insert_quer,values);
   for (int c=0; c<size; c++)
   {
      strcat(Insert_quer,double_quote);
      strcat(Insert_quer,insert_values[c]);
       strcat(Insert_quer,double_quote);
       if (c < size-1){
      strcat(Insert_quer,coma);
       }
   }
   strcat(Insert_quer,close_brac);
   printf("\n &&& %s\n", Insert_quer);   //Insert Query

   //Execution of query
    if (mysql_query(conn,Insert_quer)) {
      fprintf(stderr, "%s\n", mysql_error(conn));
     
   }
   execute_Select_Query();
    free(Insert_quer);
    free(Final);

// insert into example (id , data) values("1", "BMW S4");
}

/* ################################# Create-Table() ##################################################################
 GRNERIC - Execute Create Table Query */
void Execute_create_table_query(){
   //Preparation of query
   char *Create="create table ";
   char *Table_name;
   int column_no;
   Table_name= (char*) malloc(256);
   printf("\n Enter Tbale Name::\n");
   scanf("%255s", Table_name);
   printf("\n Enter Column Count::\n");
   scanf("%d", &column_no);
   char *open_brace=" ( ";
   char *coma=" , ";
   char *close_brac=" )";
   char *space=" ";
   char *Column_nmae[column_no];
   char *Column_type[column_no];
   for (int c=0; c < column_no; c++)
   {
      Column_nmae[c]=(char*) malloc(256);
      Column_type[c]= (char*) malloc(256);
   }

   //accept column name and column type from user
   int  show_no=1;
    for (int c=0; c < column_no; c++)
   {
      printf("\n Enter %d column name::",show_no);
      scanf("%255s", Column_nmae[c]);
      printf("\n Enter Type for Column %s ::",Column_nmae[c]);
      scanf("%255s", Column_type[c]);
      show_no++;
   }

//conciation for Query
   char *Cretae_table_query;
   Cretae_table_query= (char *) malloc(1024 + strlen(Create)+ strlen(Table_name)+ strlen(open_brace)+ strlen(close_brac)+ strlen(Column_nmae)+ strlen(Column_type));
   strcpy(Cretae_table_query,Create);
   strcat(Cretae_table_query,Table_name);
   strcat(Cretae_table_query,open_brace);
   for (int c=0; c < column_no; c++)
   {
      strcat(Cretae_table_query, Column_nmae[c]);
      strcat(Cretae_table_query,space);
      strcat(Cretae_table_query,Column_type[c]);
      if (c < column_no-1){
      strcat(Cretae_table_query,coma);
       }

   }
   strcat(Cretae_table_query, close_brac);
   printf("%s ", Cretae_table_query);
   
   /*
    //to see output of arrays
  for (int c=0; c < column_no; c++)
   {
      printf("%d  ", c);
      printf("%s ", Column_nmae[c]);
      printf("%s\n",Column_type[c]);
   }
    */
  
   // Execute Create-Table_Query
    if (mysql_query(conn,Cretae_table_query)) {
      fprintf(stderr, "%s\n", mysql_error(conn));
      
   }
   
   // Execute DESCRIBE-TABLE Query
   char *desc= "desc ";
   char *desc_table_query;
   desc_table_query=(char*) malloc(1 + strlen(desc) + strlen(Table_name));
   strcpy(desc_table_query,desc);
   strcat(desc_table_query,Table_name);
   mysql_query(conn, desc_table_query) ;    
   res = mysql_use_result(conn);
   printf("\nDESCRIBE table %s ::\n",Table_name);
   while ((row = mysql_fetch_row(res)) != NULL)
      printf(" * %s | %s | %s | %s | %s | %s | \n", row[0],row[1], row[2], row[3], row[4],row[5]);

   // Free Memory
   free(desc_table_query);
   free(Cretae_table_query);

  // create table login ( id int, name varchar(100), location varchar(100));

}

/* ############################### DElete-Row-From-table()##############################
   Execute Delete row from table on basis on uniqe colume*/
void Delete_From_table_query(){
   // Preparing Query
   char *delete="delete from ";
   char *where=" where ";
   char *uniq_cloumn;
   uniq_cloumn=(char*) malloc(256);
   printf("\n enter column NAME on basis you want to delete row::");
   scanf("%255s", uniq_cloumn);
   char *value=(char*) malloc(256);
   printf("\n enter column VALUE on basis you want to delete row::");
   scanf("%255s", value);
   char *equels="='";
   char *close_cloute="'";
   char *Delete_rwo_query= (char*) malloc(10+ strlen(delete)+ strlen(where)+ strlen(uniq_cloumn)+ strlen(equels)+ strlen(close_cloute)+ strlen(table_update) );
   strcpy(Delete_rwo_query,delete);
   strcat(Delete_rwo_query,table_update);
   strcat(Delete_rwo_query,where);
   strcat(Delete_rwo_query,uniq_cloumn);
   strcat(Delete_rwo_query,equels);
   strcat(Delete_rwo_query,value);
   strcat(Delete_rwo_query,close_cloute);
   printf("\n %s", Delete_rwo_query);  // Delete Query

   // Execute Delete Query
     if (mysql_query(conn,Delete_rwo_query)) {
      fprintf(stderr, "%s\n", mysql_error(conn)); 
   }
    execute_Select_Query(); 
    //Free Memory
    free(Delete_rwo_query);


// delete from example where id='1';

}
 
/* #################################### Drop-Table()##################################################S 
Execute Drop Table Query*/
void Drop_table_query(){
   // Preparing drop table query
   char *drop="drop table ";
   char *table_name=(char*) malloc(256);
   printf("\n Enter table Name to Delete::");
   scanf("%255s", table_name);
   char *Drop_table_query=(char*) malloc(1+ strlen(drop)+ strlen(table_name));
   strcpy(Drop_table_query,drop);
   strcat(Drop_table_query,table_name);

   //drop table Query
   printf("\n %s", Drop_table_query);   

   //Execution of Drop table query 
     if (mysql_query(conn,Drop_table_query)) {
      fprintf(stderr, "%s\n", mysql_error(conn)); 
   }
   else
   {
      printf("\n Table %s deleted", table_name);
   }
   
   // Free Memory
   free(Drop_table_query);
  

// drop table TIME; 
}

// ########################### SET-UP() ###############################################################
void Set_up_Function(){
  // printf("\n @ inside Set_up_Function Function\n");
   result= Connect_To_Mysql("localhost", "root", "kpit123"); //dont mention Schema name
   printf("MySQL client version: %s\n", mysql_get_client_info());
   Show_All_Schemas();
   Select_DB(); 
   execute_Select_Query();

}


//Menu Driven Function

int User_Choice(){
   int choice=0;
   printf("\n##################################################\n");
   printf("Enter Your Choice::\n");
   printf(" *1. To Select Schema\n");
   printf(" *2. To Execute Select Query\n");
   printf(" *3. TO Execute Update Query\n");
   printf(" *4. TO Execute Insert Query\n");
   printf(" *5. TO Execute Create-Table Query\n");
   printf(" *6. TO Execute Delete from Table Query\n");
   printf(" *7. TO Execute drop-Table Query\n");
   printf(" *0. To Exit\n");
   scanf("%d", &choice);
   return choice;
}
void Switch_case(){
   while (1)
   {
   switch (User_Choice())
   {
   case 1:
         result= Connect_To_Mysql("localhost", "root", "kpit123"); //dont mention Schema name
         Show_All_Schemas();
         Select_DB(); 
      break;
   case 2:
          result= Connect_To_Mysql("localhost", "root", "kpit123"); //dont mention Schema name
          printf("MySQL client version: %s\n", mysql_get_client_info());
          Show_All_Schemas();
          Select_DB(); 
         execute_Select_Query();
         break;
   case 0:
         exit(0);
         break;
   case 3:
         Set_up_Function();
         Execute_Generic_Update_Query();
         break;
   case 4:
         Set_up_Function();
         Execute_Insert_query();
         break;
   case 5:
         //Set_up_Function();
         result= Connect_To_Mysql("localhost", "root", "kpit123");
         printf("MySQL client version: %s\n", mysql_get_client_info());
         Show_All_Schemas();
         Select_DB();
         Execute_create_table_query();
          break;
   case 6:
         result= Connect_To_Mysql("localhost", "root", "kpit123");
         printf("MySQL client version: %s\n", mysql_get_client_info());
         Show_All_Schemas();
         Select_DB();
         execute_Select_Query();
         Delete_From_table_query();
         break;
   case 7:
         result= Connect_To_Mysql("localhost", "root", "kpit123");
         printf("MySQL client version: %s\n", mysql_get_client_info());
         Show_All_Schemas();
         Select_DB();
         Drop_table_query();
         break;
   default: 
         printf("\n please enter valid option::");
         break;
   }
}
}

// Program Flow
int main() {
 
   Switch_case();

   // close connection 
   free(output_select_query);
   mysql_free_result(res);
   mysql_close(conn);
   return 0;

}
