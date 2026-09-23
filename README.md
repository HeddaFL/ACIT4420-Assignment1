# Smart Fitness Session Analyzer

## Course: ACIT4420 - Python Programming Assignment 1
## Option A: Smart Fitness Session Analyzer 
## Student name: Hedda Fløtre Laupstad
## Student number: helau2698 

## Description
A fitness centre receives simulated measurements from wearable devices used during training sessions. This program organizes participants and their traning sessions. It validates the measurement window and compares measuremensts against the baseline of each participant. It will also classify session intensity, detect recovery and provide a readable report for each session.


## Class Designs 

THis program contain 4 meaningful classes. These are: Participant, SensorReading (abstract), Observation and Session. 

Class Participant: 
- Stores one participants identifier and personal baseline values (heart rate, skin response, temperature).
- The classmethod "from_profile" builds a Participant a profile dictionary. 

Class SensorReading: 
- This class is an abstract base class using ABC. 
- It shores a timestamp, tracks validation errors and exposes an "is_valid" property. 
- It also declears an abstract "validate()" method that subclasses must implement. 

Class Observation: 
- is a subclass of SensorReading.
- represents one measurement window (heart rate, skin response, temperature, activity level, signal quality).
- implements the method "validate()" to check each field against a range. 
- adds a "is_usable" property. 
- "from_dict" builds an Observation from a dictionary. 

Class Session: 
- represents one traning session for one Participant and many Observation objects. 
- Backbone for logic in maintaining the observation list private.
- Exposes usable/rejected observations and counts.
- "from_observations" builds a Session from a list of observation dictionaries. 

The functions for calculations, validation and presentation is represented in the Analysis.py file. This is seperated from the above classes. The file Analysis.py contains the functions: 
- summarize_values
- compare_baseline
- detect_recovery
- classify_intensity
- generate_session_summary
- build_console_report. 


## Composition, Encapsulation, Inheritance and Overriding
Composition:
- The class Session contains one Participant and multiple Observation objects. An important note here, is that a Session cannot exist without a Participant, but a Participant can exist without a Session. The relationship is defined by a "has-a". Composition is therefore a natural choice for the class. 

Encapsulation: 
- Both of the classes Participant and Session use private attributes (__ prefix) and properties (@property). This ensures that a participants Id and baseline values cannot be changed or reassigned by accident. 
- Another encapsulation is that Session returns a copy of its observation list. This ensures that the real observation list cannot be changed. The way to add data is through "add_observation()".

Inheritance: 
- The class Observation inherits from the abstract class SensorReading. This means that the parent (SensorReading) defines what each and every sensor reading needs, while the child class (Observation) defines what a fitness observation should measure and how to valide it. This relationship ensures that the parent class gives a minimum level of values while a child class can be more specific.

Overriding: 
- The class Observation implements the abstract validate() method, which is defined by the class SensorReading. It is not instantiated in SensorReading, which means that every subclass of SensorReading need to define and valide its own rules insted of inheriting. 

## Assumptions and classification rules:
Validity: 
The validation of an observation is only true if every one of the fields in the validate() function id within the range for heart_rate, skin_response, temperature, activity_level and signal_quality.

Usability: 
Additionally, a valid observation is only usable if the signal_quality is >= 0.5. This can mean that a previous valid reading can be excluded from analysis. This is to ensure that a valid observation also has signal_quality. 

Recovery detection: 
There is also a "detect_recovery" in the file Analysis.py that indicates that every usable observation also needs to have 4 usable observations. The usable observations is also divided into two by timestamp. This divide is also constrained that the second heart_rate is more than 3 bpm lower than the first half, and that the second-falf of activity_level is more that 0.05 lower in the first half. The reason for the numbers 3 bpm and 0.05 was to ensure that small measurement noise was elimiated.

Classify: 
I used the classification of "resting", "moderate activity" and "high activity". This classification is conditioned (can be seen in Analysis.py for specific numbers). The heart rate is always compared to the participants own baseline rather than a fixed number. This is due to heart rates being different accross participants. 

Additionaly is also "recovering" and "insufficient data" part of the classification. The recovering is checked and will override everything else. Insufficient data is checked first and also overrides if there is not enough usable observations.

## Exact installation and running intructions

git clone https://github.com/HeddaFL/ACIT4420-Assignment1.git

cd ACIT4420-Assignment1

python main.py

## Testing adn running
The file tests.py uses Python's built-in unittest. The reason of tests.py is to verify that the program is behaving appropriatly and as expected. The tests.py checks multiple things, such as:
- only valid observations are used.
- missing values are rejected.
- impossible values are rejected. 
- an observation iwth low signal_quality is excluded from analysis. 
These tests are created specifically without generated data to ensure i could test my program with specific invalid situations. 

The test has five scenarioes (same as before) and the "generate_session_summary()" to return a dictionary. Now this is using data generated by data_generator.py. This is to ensure that the program works correctly.  

To test the automated tests, use the following command: 
python -m unittest tests.py -v

## Example output
The following output is copypasted from the terminal after i used the command "python main.py". 

```
Scenario: resting 
============================================================
Session report: P001-resting (participant P001)
============================================================
Observations used: 12/12 (0 rejected as missing/impossible/low-quality)
Classification: RESTING
Recovery detected: no - no significant decline in heart rate and activity toward the end of the session
------------------------------------------------------------
Heart rate (bpm)  : avg=80, min=76, max=85 (n=12)
Skin response     : avg=1.19, min=0.97, max=1.32 (n=12)
Temperature (C)   : avg=32.78, min=32.68, max=32.94 (n=12)
Activity level    : avg=0.11, min=0.04, max=0.18 (n=12)
Avg heart rate vs. baseline: +2.00 bpm

Scenario: moderate_activity 
============================================================
Session report: P001-moderate_activity (participant P001)
============================================================
Observations used: 12/12 (0 rejected as missing/impossible/low-quality)
Classification: MODERATE ACTIVITY
Recovery detected: no - no significant decline in heart rate and activity toward the end of the session
------------------------------------------------------------
Heart rate (bpm)  : avg=105.75, min=97, max=116 (n=12)
Skin response     : avg=1.51, min=1.17, max=1.71 (n=12)
Temperature (C)   : avg=33.03, min=32.92, max=33.24 (n=12)
Activity level    : avg=0.51, min=0.39, max=0.62 (n=12)
Avg heart rate vs. baseline: +27.75 bpm

Scenario: high_activity 
============================================================
Session report: P001-high_activity (participant P001)
============================================================
Observations used: 12/12 (0 rejected as missing/impossible/low-quality)
Classification: HIGH ACTIVITY
Recovery detected: no - no significant decline in heart rate and activity toward the end of the session
------------------------------------------------------------
Heart rate (bpm)  : avg=135.67, min=123, max=150 (n=12)
Skin response     : avg=1.8, min=1.3, max=2.1 (n=12)
Temperature (C)   : avg=33.34, min=33.17, max=33.65 (n=12)
Activity level    : avg=0.8, min=0.69, max=0.91 (n=12)
Avg heart rate vs. baseline: +57.67 bpm

Scenario: recovery 
============================================================
Session report: P001-recovery (participant P001)
============================================================
Observations used: 12/12 (0 rejected as missing/impossible/low-quality)
Classification: RECOVERING
Recovery detected: yes - Heart rate fell from 126.8 to 98.8 bpm and activity fell from 0.70 to 0.26 over the second half of the session
------------------------------------------------------------
Heart rate (bpm)  : avg=112.83, min=86, max=141 (n=12)
Skin response     : avg=1.57, min=1.22, max=1.93 (n=12)
Temperature (C)   : avg=33.05, min=32.81, max=33.34 (n=12)
Activity level    : avg=0.48, min=0.1, max=0.88 (n=12)
Avg heart rate vs. baseline: +34.83 bpm

Scenario: poor_quality 
============================================================
Session report: P001-poor_quality (participant P001)
============================================================
Observations used: 0/12 (12 rejected as missing/impossible/low-quality)
Classification: INSUFFICIENT DATA
Recovery detected: no - not enough usable observations to evaluate recovery
------------------------------------------------------------
Heart rate (bpm)  : no usable data
Skin response     : no usable data
Temperature (C)   : no usable data
Activity level    : no usable data
```

## Known limitations
The choice to using 3 bpm and 0.05 in recovery as a threshold is due to my own inspection of the generated data provided. A different threshold might shift some sessions into different classifications. 

The "poor_quality" scenario is rejected in every observation. This is due to a invalid problem. This can either be the heart_rate is missing/impossible, that the activity_level is negative or that skin_response is missing. This means that for every single observation, there is one rotating problem. This means that all 12 observations are always rejected, because they are not usable. 

Another limitation is that i  divided the recovery detection so it only compares the first and second half. Meaning that a session with a short dip in the middle could be misclassified. 

When running the proram, the report in the console is not saved into a file. This means that the results only exist in the console. 

The program only supports five scenarios. It has not been tested against scenarios outside of what "data_generator.py" produces. 