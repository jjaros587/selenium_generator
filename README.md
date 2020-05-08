# Selenium generator
Features:
- Automated generation of Tests based on Scenarios in yaml format
- Data Driven Testing (DDT)
- Page Factory design pattern
- Creating of Test suites
- WebDriver manager
- Test report generating
- Taking screenshots on failure


## Global configuration
Global configuration holds everything what is needed for running the tests. Bellow are given its objects.

    scenarios: ""
    pages: ""
    data: ""
    report:
    tags: []
    drivers:
    
### Setting of paths
There are three objects for specification of paths to directories. 
All of them accept string values of relative paths to directories with `__main__` as starting point. 

**Scenarios** defines path to the folder with test scenarios. This value is mandatory. 
Scenarios inside the folder can be divided into more complex directory structure of multiple levels.
Framework loads scenarios from all folders recursively.

**Pages** defines path to the folder with  created Page Objects. This value is mandatory. 
Scenarios inside the folder can be divided into more complex directory structure of multiple levels in case of proper 
configuration of imports in `__init__` files. In the other words, it must be possible to load all classes from root folder.

**Data** defines path to test data which are loaded from test scenario during the execution. This field is not mandatory, 
unless you are using data from external files for scenarios. Otherwise `UnspecifiedDataFolder` exception would be raised and the test would fail.
              
### Test report configuration
Report object is used for overriding of a default configuration for a test report. 
All if its child objects are not mandatory, only these you want to override may be specified.

**Screenshots** object defines if you want to take screenshots on failure and to attache them in the test report. By default is set on `true`.

**Clean** object defines if you want to clear the folder where report and screenshots are being saved before the next text execution. By default is set on `true`.

**Params** object is used for a specification of parameters of the report itself.

- **output** defines the directory for generating of the report and saving of the screenshots. By default it's `/report` in the root directory of the project.
- **combine_reports** defines whether test classes should be combined into one report or divided into several reports. By default is set on `true`.
- **report_name** defines custom report name (name of the generated report). By default it is `"TestReport"`.
- **report_title** defines custom report title (header of the generated report). By default it is `"Test results"`.
- **template** is used for using custom template instead of the default one. The value is path to the custom template.
   
   
    report:
        screenshots: [true/false]
        clean: [true/false]
        params:
            output: "[folder for storing test report]"
            combine_reports: [true/false]
            report_name: "[test report file name]"
            report_title: "[test report title]"
            template: "[path to template]"
            

### Test suite specification

### Drivers configuration



    drivers:
        chrome:
            version: "80.0.3987.106"

        firefox:
            options:
                - "--width=150"
                - "--height=100"
#### Local WebDriver

#### Remote WebDriver

## Test scenario structure
Test scenario follows the structure of test written by using unittest framework.

    name:
    
    data:
    
    tags: 
    
    before_all:
    
    before_each:
    
    steps:
    
    after_each:
    
    after_all:

## Creating of test suites
The only possible option for creating test suites is by marking test scenario with a tag in scenario metadata and specifying tags we want to run in the global configuration. 

Tags can be specified as a list of `String` values in object `tags:`, both in scenario and in global configuration. 

    tags: ["regression", "acceptance"]
    
The object `tags:` is not mandatory. The effect would be the same as with an empty array `[]`. The array cannot contain empty `Strings`.
This behaviour is applied to both scenario and configuration. 

If no tag in configuration is specified, all scenarios will be run.  
If array contains at least one tag, the behaviour is as following:
1. List of tags in scenario contains at least one of the tags from global configuration &rarr; test will be run
2. List of tags in scenario doesn't contain any of the tags from global configuration
    1. List of tags in scenario contains String `"*"` &rarr; test will be run
    2. List of tags in scenario doesn't contain String `"*"` &rarr; test won't be run
    
As you can see, there is an option to specify string with character `*`. It simply means a scenario will be run all the times, no matter what tag was specified in global configuration.

## Keywords
- `run_driver:`

- `maximize:`

- `close_driver:`

- `page_object:`



## Test data specification
There are several ways for test data specification. These can be divided in two groups which are as following:
1. Direct specification of method's parameters
2. Using of data for DDT

We can combine these two approaches, but the direct specification of method's parameters takes priority over second approach. 
It means that we can run multiple tests with DDT functionality and in the same time to specify direct parameters for any step in a scenario. 
But... these direct parameters would be the same for all of the tests which were run with DDT. 

Before the data are parsed into class method which is being called, first of all, method's arguments are loaded. 
After that the specific data, from params object of data from DDT, are being searched. Only if data with specific key was found, the data would be parsed into method. 
A benefit of this approach is that the option of adding default `kwargs` into method, in the `Python` way, when the specific value wasn't specified is retained.

### Direct specification
For direct specification, object `params:` is used. This object has key-value pairs which represent kwargs arguments of the method which is being called. 
Once the object is specified, it is impossible to use data from the second approach.

See the example:

    steps:
      - page_object:
          class: "GoogleSearchPage"
          method: "search"
          params:
            search_text: "searched value"

### DDT
There are again to possible ways for data specification using DDT approach.
1. Inline specification in scenario with yaml format
2. Load of data from file

#### Inline specification
We can specify data for DDT directly in scenario using object `data:`. 
We can specify here array of data objects which will be parse into methods in the same way how would be done with external file.
But the format has to follow yaml format. The example below would generate two tests.

    data:
      - search_text: "text1"
      - search_text: "text2"
      
#### Data from file
For using data from file only file path specification, including file format, is needed. 
The file path should be relative path from data folder which was specified in global configuration.
It's possible to use data in `json` or `yaml` format.

    data: "data.json"

