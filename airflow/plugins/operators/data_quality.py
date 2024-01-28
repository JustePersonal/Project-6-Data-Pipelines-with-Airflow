from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
    This function executes a data quality check.
    
    :param redshift_conn_id: ID of the Redshift connection.
    :param tables: Tables on which the data quality check needs to be executed.
    
    """
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 tables = [],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        
        self.redshift_conn_id = redshift_conn_id
        self.tables =  tables

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        for table in self.tables:
            records = redshift.get_records("SELECT COUNT(*) FROM {}".format(table))
            
            if len(records) < 1 or len(records[0]) < 1:
                self.log.error("{} returned no results".format(table))
                raise ValueError("The data quality validation did not meet the requirements. {} did not produce any results".format(table))
                
            num_records = records[0][0]
            if num_records == 0:
                self.log.error("There are no records in the destination table {}".format(table))
                raise ValueError("There are no records available in the destination {}".format(table))
                
            self.log.info("Quality assessment of table {} indicates {} records passed the check.".format(table, num_records))
