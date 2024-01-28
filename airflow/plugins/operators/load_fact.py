from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """
        Loads dimension table in Redshift from data in staging table(s).

    :param redshift_conn_id: Redshift connection ID.
    :param table: Target table in Redshift to load.
    :param sql: SQL query for retrieving data to load into the target table.
    :param insert_only: Parameter is a boolean value. If set to True, it indicates that the table should be deleted before insertion.
                        If set to False, it means that the insertion should proceed directly without deleting the table.
                        
    """


    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 sql = "",
                 table = "",
                 insert_only = False,
                 *args, **kwargs):
                    
        super(LoadFactOperator, self).__init__(*args, **kwargs)
        
        self.redshift_conn_id = redshift_conn_id
        self.sql = sql
        self.table = table
        self.insert_only = insert_only

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if not self.insert_only:
            self.log.info("Delete {} fact table".format(self.table))
            redshift.run("DELETE FROM {}".format(self.table))  
            
        self.log.info("Transfer data from the staging table into the {} dimension table.".format(self.table))
        
        insertion = f"INSERT INTO {self.table} \n{self.sql}"
        self.log.info(f"Running SQL: \n{insertion}")
        redshift.run(insertion)
        self.log.info(f"The insertion into {self.table} was completed successfully.")
