# Peloton-Data
Peloton Dataset - Everything Peloton

### About
This dataset is a compilation of the Peloton data ecosystem.

### Versioning
1.0 - All public-facing data
2.0 - All Workout Data

### Usage
Main datasets are instructors.csv and workouts.csv. Any '_id' in instructors or workouts data references data in the metadata folder.

    workouts.csv
    class_type_ids: ['bf6639f2e50a4f0395cb1479542ed4bd']
    
    metadata/class_types-metadata.csv
    bf6639f2e50a4f0395cb1479542ed4bd,Climb,Climb,cycling,True,107
    
### Updated
Datasets will update weekly at 00:00 UTC on Sunday morning.

### Sources
https://github.com/geudrik/peloton-client-library/blob/master/API_DOCS.md

https://api.onepeloton.com/api/