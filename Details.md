Conversion status
==============
The [August FHIR STU3](http://hl7.org/fhir/2016Sep/index.html) release contains 568 RDF Turtle files in the `publish` directory.  Applying the validation process to these files yields the following results:

* 57 files are not FHIR resources. A RDF dataset is considered a FHIR resource if there is at least one subject s such that:

        s?  fhir:nodeRole fhir:treeRoot 
        s?  fhir:rdf:type fhir:*
        
* ?? files representing three resources, [Claim](http://hl7.org/fhir/2016Sep/claim.html), [ExplanationOfBenefit](http://hl7.org/fhir/2016Sep/explanationofbenefit.html), and [PlanDefinition](http://hl7.org/fhir/2016Sep/plandefinition.html) had one or more examples with *required* `Coded` value sets.  The ShEx tooling in STU3 assumes (incorrectly) that all *required* value sets are of type `code`.  The definitions in causing the errors were manually corrected and the results can be found in the [changes](changes) directory.  Details of the changes are described below.
* ?? file representing four resources, [DocumentReference](http://hl7.org/fhir/2016Sep/documentreference.html), [ImagingManifest](http://hl7.org/fhir/2016Sep/imagingmanifest.html), [Patient](http://hl7.org/fhir/2016Sep/patient.html), and [Procedure](http://hl7.org/fhir/2016Sep/procedure.html) had one or examples with *required* `CodedEntry` value sets.  The definitions were manually corrected, which addressed all but *one* of the errors. The exception, [patient-example-f201-roel.html](http://hl7.org/fhir/2016Sep/patient-example-f201-roel.html), had two entries for the required value set, `marital-status`





Representing *required* `Coding` value sets in ShEx
-------
Four of the STU3 examples ([plandefinition-exclusive-breastfeeding-intervention-01](http://hl7.org/fhor/2016Sep/plandefinition-exclusive-breastfeeding-intervention-01.html) through [plandefinition-exclusive-breastfeeding-intervention-04](http://hl7.org/fhor/2016Sep/plandefinition-exclusive-breastfeeding-intervention-04.html)) supplied only the `code` part of `PlanActionType` - a  *Required* `Coding`   A [question](https://chat.fhir.org/#narrow/stream/terminology/topic/Required.20Coding.20value.20sets) was posted on the FHIR chat about whether this was legal.  The answer was a guarded "yes", stating that the result was only "partially computable".  Following this, we propose the rule for Required Coding types be that, *if* the `system` is present, it must match that in the value set.  The `code` must always be in the code enumeration

```turtle
fhir:<predicate> @<Coding> AND @fhirvs:<valueset><cardinality>; 
     ...
fhirvs:<valueset> {
    fhir:Coding.system {fhir:value ["<code system url>"]}?;
    fhir:Coding.code { fhir:value ["<code1>" "<code2>" ... "<codeN>"]}
}
```

As an example, the [STU3 FHIR PlanDefinition](http://hl7.org/fhir/2016Sep/plandefinition.html) resource defines an optional `action-type` value set that is represented as

```turtle
fhir:PlanDefinition.actionDefinition.type @<Coding> AND @fhirvs:action-type?;
...
fhirvs:action-type {
    fhir:Coding.system {fhir:value ["http://hl7.org/fhir/ValueSet/action-type"]}?;
    fhir:Coding.code { fhir:value ["create" "update" "remove" "fire-event"]}
}
```
Note that this pattern will need to be extended to support codes that derive from different systems.

Representing *required* `CodeableConcept` value sets in ShEx
-----
*Required* `CodeableConcepts` represent a more difficult problem, as the required value set must be represented in at least(?) (exactly?) one of the `coding` entries.  To represent this, we use the following pattern:

```turtle
    fhir:<predicate> @<CodeableConcept> AND
        @fhirvs:<valueset><cardinality>;
        ...    
 fhirvs:<valueset> EXTRA fhir:CodeableConcept.coding {
 	fhir:CodeableConcept.coding {
		fhir:Coding.system {fhir:value [<code system>]};
    	      fhir:Coding.code {fhir:value ["<code1>" "<code2>" ... "<codeN>"]}
    	 }
}
```
Note that this rule assumes that the system must be supplied.  While it is technically possible that the `Coding` rule described above may appear here as well, we are assuming that it would never actually be the case and, as such, should be flagged as an error.

As an example, the STU3 FHIR Patient resource defines an optional marital-status value set that is represented as:

```turtle
     fhir:Patient.maritalStatus @<CodeableConcept> AND @fhirvs:marital-status?;  # Marital (civil) status of a patient   
         ...
fhirvs:marital-status  EXTRA fhir:CodeableConcept.coding {
     fhir:CodeableConcept.coding {
        fhir:Coding.system {fhir:value ["http://hl7.org/fhir/v3/MaritalStatus"]};
        fhir:Coding.code {fhir:value ["A" "D" "I" "L" "M" "P" "S" "T" "U" "W" "UNK"]} } }
}
```
This pattern will also need to be extended to support multiple code systems.
