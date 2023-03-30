import datetime
import pytz

import os
import json
from ruamel import yaml
import ruamel
from collections import defaultdict
import re

import pandas as pd
import numpy as np

import great_expectations 
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.checkpoint.checkpoint import SimpleCheckpoint
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import (
    DataContextConfig,
    FilesystemStoreBackendDefaults,
)
from great_expectations.profile.user_configurable_profiler  import UserConfigurableProfiler
from great_expectations.core.batch import BatchRequest
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.profile.json_schema_profiler import JsonSchemaProfiler
import datetime
import IPython

from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import (
    DataContextConfig,
    FilesystemStoreBackendDefaults,
)
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler

import great_expectations as ge
import logging

class DataQuality():
    
    def __init__(self, root_directory, datasource_yaml, expectations_config):
        
        '''
        create great expectations context and default runtime datasource
        '''
        self.datasource_yaml = datasource_yaml
        datasource_dict = yaml.load(datasource_yaml, Loader=ruamel.yaml.Loader)
        self.root_directory = root_directory
        self.datasource_name = datasource_dict['execution_engine']['credentials']['database']
        self.data_asset_name = list(datasource_dict['data_connectors']['default_configured_data_connector_name']['assets'])[0]
        self.expectations_config =  expectations_config
        #self.expectation_suite_name = f"{self.datasource_name}.{self.data_asset_name}_expectation_suite"
        self.expectation_suite_name = f"{self.datasource_name}.{self.expectations_config['expectation_suite_name']}_expectation_suite"
        self.checkpoint_name = f"{self.datasource_name}.{self.data_asset_name}_checkpoint"
            
        # create data context
        data_context_config = DataContextConfig( store_backend_defaults=FilesystemStoreBackendDefaults(root_directory=root_directory) )
        context = BaseDataContext(project_config = data_context_config)
        yaml.load(datasource_yaml, Loader=ruamel.yaml.Loader)
                   
        
        context.test_yaml_config(datasource_yaml)
        context.add_datasource(**yaml.load(datasource_yaml, Loader=ruamel.yaml.Loader))
        
        self.context = context
    
    def get_context(self):
        
        '''
        retrieving data context in case you would like to manually extract / tweak the context by yourself
        '''
        
        return self.context
    
    def get_expectation_suit(self):
        
        '''
        retriving the current expectation suite
        '''
        
        return self.context.get_expectation_suite(self.expectation_suite_name)
    
    def create_batch_data(self):
        
        '''
        create runtime batch request from the input spark dataframe and partition date
        '''
        
        # Here is an example BatchRequest for all batches associated with the specified DataAsset
        batch_request = BatchRequest(
        datasource_name=self.datasource_name,
        data_connector_name="default_configured_data_connector_name",
        data_asset_name=self.data_asset_name,
        limit = 1000)

        
        return batch_request
    
    def create_expectation_suite_if_not_exist(self):
        
        '''
        create expectation suite if not exist
        '''
        
        try:
            # create expectation suite
            #logging.info(self.expectation_suite_name)
            
            self.suite = self.context.create_expectation_suite(
                expectation_suite_name = self.expectation_suite_name,
                overwrite_existing=True
            )
            
            
            for expectation in self.expectations_config['expectations']:
                expectation_configuration = ExpectationConfiguration(
                    expectation_type = expectation['expectation_type'],
                    kwargs= expectation['kwargs'],
                    meta = expectation['meta']
                )
                self.suite.add_expectation(expectation_configuration=expectation_configuration)
                self.context.save_expectation_suite(self.suite, self.expectation_suite_name)
                
                
            
            
            # expectation_configuration = ExpectationConfiguration(
            #     # Name of expectation type being added
            #     expectation_type="expect_column_distinct_values_to_be_in_set",
            #     # These are the arguments of the expectation
            #     # The keys allowed in the dictionary are Parameters and
            #     # Keyword Arguments of this Expectation Type
            #     kwargs={
            #         "column":"emp_no",
            #         "value_set" : [1,2,3]
            #     },
            #     # This is how you can optionally add a comment about this expectation.
            #     # It will be rendered in Data Docs.
            #     # See this guide for details:
            #     # `How to add comments to Expectations and display them in Data Docs`.
            #     meta={
            #         "notes": {
            #             "format": "markdown",
            #             "content": "Some clever comment about this expectation. **Markdown** `Supported`"
            #         }
            #     }
            # )
            # Add the Expectation to the suite
            
            # self.suite.add_expectation(expectation_configuration=expectation_configuration)
            # self.context.save_expectation_suite(self.suite, self.expectation_suite_name)
            

           
            
            
        except great_expectations.exceptions.DataContextError as e:
            print(e)
            
    def delete_expectation_suite(self):
        
        '''
        delete the expectation suite
        '''
        
        self.context.delete_expectation_suite(expectation_suite_name = self.expectation_suite_name)
    
    def get_validator(self, with_profiled=False):
        
        '''
        retreiving a validator object for a fine grain adjustment on the expectation suite.
        this creates initial expectations which you can edit with_profiled
        '''
        
        batch_request = self.create_batch_data()
        self.create_expectation_suite_if_not_exist()

        validator = self.context.get_validator(
            batch_request = batch_request,
            expectation_suite_name = self.expectation_suite_name
        )
        
        
        
        if with_profiled:

            # build expectation with profiler
            not_null_only = True
            table_expectations_only = False

            profiler = UserConfigurableProfiler(
                profile_dataset = validator,
                not_null_only = not_null_only,
                table_expectations_only = table_expectations_only
            )

            suite = profiler.build_suite()

            # save validation
            validator.save_expectation_suite(discard_failed_expectations=False)
        
        return validator
    
            
    
    
    def create_checkpoint_if_not_exist(self):
        
        '''
        create checkpoint if not exist.
        '''
        
        try:
            batch_request = self.create_batch_data()   
            
            checkpoint_config: dict = {
                 "name": self.checkpoint_name,
                 "config_version": 1.0,
                 "class_name": "SimpleCheckpoint",
                 "run_name_template": "%Y%m%d-%H%M%S",
                 "expectation_suite_name":self.expectation_suite_name,
                 "validations": [
                            {
                                "batch_request": batch_request
                            }
                        ]  
             }
           
            
            #self.context.test_yaml_config(yaml.dump(checkpoint_config))
            #self.context.add_checkpoint(**checkpoint_config)
            self.context.add_checkpoint(**checkpoint_config)
                    
            

        except Error as e:
            raise e
            
            
    def validate_data(self):
        
        '''
        validate dataset using the input dataset when initiated the class
        or user provided dataset when calling the method.
        '''
        
        batch_request = self.create_batch_data()            
        
        self.create_checkpoint_if_not_exist()
        
        # run expectation_suite against data
        print (self.expectation_suite_name)
        print ('@@@@@@\n\n\n\n\n\n')
        checkpoint_result = self.context.run_checkpoint(
            checkpoint_name = self.checkpoint_name,
        )
        
        for k,v in checkpoint_result['run_results'].items():
            self.render_file = v['actions_results']['update_data_docs']['local_site'].replace('file://', '')
    
        return checkpoint_result
    
    def render_report(self, to_render_file=None):
        
        '''
        render report from the validation result
        required user to trigger `validate_data` at least once.
        or render report from the `to_render_file` absolute path.
        '''
        
        try:
            if not to_render_file:
                to_render_file = self.render_file
        except AttributeError:
            raise ValueError("The render file doesn't exists, please call the `validate_data` method to get a render file")
        except Error as e:
            raise e
                
        with open(to_render_file, "r", encoding='utf-8') as f:
            text= f.read()

        IPython.display.HTML(filename = to_render_file)
        
    def render_expectation_report(self):
        
        '''
        retreiving the current expectation suite.
        '''
        
        expectation_path = f'{self.root_directory}/uncommitted/data_docs/local_site/expectations/{self.expectation_suite_name.replace(".", "/")}.html'
        
        with open(expectation_path, "r", encoding='utf-8') as f:
            text= f.read()

        IPython.display.HTML(filename = expectation_path)
        
    def backup_great_expectations_db(self, persisted_target_dir):
        
        '''
        back up great expectation database to azure blob storage.
        '''
        
        dbutils.fs.cp(self.root_directory, persisted_target_dir, recurse=True)