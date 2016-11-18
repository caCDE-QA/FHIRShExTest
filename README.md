# FHIRShExTest
Test script for running ShEx validation against FHIR Example instances

## Requirements

* [python 3](https://www.python.org/) -- this has been tested with python 3.5.0
* [node.js](https://nodejs.org) -- JavaScript engine for shex.js
* [shex.js](https://github.com/caCDE-QA/shex.js) -- ShEx validation REST server

## Running FHIRShExTest
    
1. Download the [FHIR STU3 Distribution](http://hl7.org/fhir/2016Sep/index.html):

    There are a number of ways to accomplish this including:

    * Use the hcls-fhir-rdf 
    [download_fhir_spec](https://github.com/w3c/hcls-fhir-rdf/blob/gh-pages/scripts/download_fhir_spec)
    utility -- `> download_fhir_spec -u http://hl7.org/fhir/2016Sep/`
    * Download and unzip the [FHIR specification](http://hl7.org/fhir/2016Sep/fhir-spec.zip)
    * Build a local image using the [FHIR Build Process](http://wiki.hl7.org/index.php?title=FHIR_Build_Process).  Once the `publish.sh` or `publish.bat`
    script has been run, the final specification will be in the "publish" directory
    

2. Start the shex.js server as a separate thread:
    ```bash
    > git clone https://github.com/caCDE-QA/shex.js
    > cd shex.js
    > npm update -g shex-test
    > node --no-deprecation ./bin/validate -S http://localhost:4290/validate --regex-module nfax-val-1err --duplicate-shape ignore
      Visit http://localhost:4290/ in browser.

      Test with a supplied schema and data:
        curl -i http://localhost:4290/validate -F "schema=@test/cli/1dotOr2dot.shex" -F "shape=http://a.example/S1" -F "data=@test/cli/p2p3.ttl" -F "node=x"
      or preload the schema and just supply the data:
        bin/validate -x test/cli/1dotOr2dot.shex -s http://a.example/S1 -S  http://localhost:4290/validate
      and pass only the data parameters:
        curl -i http://localhost:4290/validate -F "data=@test/cli/p2p3.ttl" -F "node=x"
      Note that shape and node can be relative or prefixed URLs.
    
      Press CTRL+C to stop...
    ```
    
    The latest version of `node` issues a deprecation warning about calling an asynchronous function without a callback.  This is the reason for the
    `--no-deprecation` tag in the invocation above.
    
3. Set up a python3 virtual environment:

    ```bash
    > virtualenv FHIRShExTest -p python3
    > . FHIRShExTest/bin/activate
    (FHIRShExTest) >
    ```
    
4. Clone or download FHIRShExTest:
    ```bash
    (FHIRShExTest) > https://github.com/caCDE-QA/FHIRShExTest.git
    (FHIRShExTest) > cd FHIRShExTest
    (FHIRShExTest) > python setup.py
    ```
    
5. Copy the local changes to the ShEx specifications to the publish directory
    ```bash
    (FHIRShExTest) > cp changes/* <FHIR specification directory>
    ```
    
5. Run the FHIRShExTest script:
    ```bash
    (FHIRShExTest) > python src/FHIRShExTest -id <FHIR specification directory>  -od ../data --nosuccesslog
    /Users/mrf7578/Development/fhirstu3/stu3-ballot/publish/claim-example-vision-glasses.ttl	/Users/mrf7578/Development/fhirstu3/stu3-ballot/publish/claim.shex	MissingProperty	http://www.w3.org/1999/02/22-rdf-syntax-ns#type	JsonObj(property='http://www.w3.org/1999/02/22-rdf-syntax-ns#type', type='MissingProperty', valueExpr=JsonObj(type='NodeConstraint', values=['http://hl7.org/fhir/MedicationOrder']))
    /Users/mrf7578/Development/fhirstu3/stu3-ballot/publish/claimresponse-example.ttl	/Users/mrf7578/Development/fhirstu3/stu3-ballot/publish/claimresponse.shex	MissingProperty	http://www.w3.org/1999/02/22-rdf-syntax-ns#type	JsonObj(property='http://www.w3.org/1999/02/22-rdf-syntax-ns#type', type='MissingProperty', valueExpr=JsonObj(type='NodeConstraint', values=['http://hl7.org/fhir/Claim']))
        ...
    /Users/mrf7578/Development/fhirstu3/stu3-ballot/publish/rim.ttl		Not a FHIR resource instance
    Total=499 Successful=480
    Not a FHIR resource: 57
        Missing ShEx file: 0
        On skip list: 0
        Failed validation: 19
        Invalid RDF: 12
    ```
    
 ## Notes
 The Invalid RDF counts above are due to an [rdflib error](https://github.com/RDFLib/rdflib/issues/646).  We are awaiting an alternative resolution from the
 rdflib authors -- the solution is targeted for the rdflib 4.2.2 milestone.
