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

## Test scenario structure
Test scenario follows the structure of test written by using unittest framework.

    setup_class:
    
    setup:
    
    steps:
    
    teardown:
    
    teardown_class:

## Creating of test suites
The only possible option for creating test suites is by marking test scenario with a tag in scenario metadata and specifying tags we want to run in the global configuration. 

Tags can be specified as a list of `String` values in object `tags:`, both in scenario and in global configuration. 

    tags: ["regression", "acceptance"]
    
The object `tags:` is not mandatory and can contain `None` value. The effect would be the same as with empty array `[]`. 
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

- `close_driver:`

- `page_object:`



## Test data specification
There are several ways of specifying test data. These can be divided into two groups which are as following:
1. Direct specification of method parameters
2. Using of data for DDT

We can combine these tho approaches, but direct specification of method parameters takes priority over second approach. 
It means that we can run multiple tests with DDT functionality and in the same time to specify direct parameters for some method in one or more steps of the scenario. 
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
There are again to possible ways for specification data using DDT approach.
1. Inline specification in scenario with yaml format
2. Load of data from file

#### Inline specification
We can specify data for DDT directly in scenario using object `data:`. We can specify here array of data objects which will be parse into methods in the same way how would do it in external file.
But the format has to follow yaml format. The example below would generate two tests.

    data:
      - search_text: "text1"
      - search_text: "text2"
      
#### Data from file
For using data from file we have to only specify the name of the file, including file format, or its relative path from data folder which was specified in global configuration.
It's possible to use data in `json` of `yaml` format.

    data: "data.json"

