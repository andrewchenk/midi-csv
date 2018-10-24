# midi-csv
A tool written in Python for representing midi files as data. It converts from midi to a intuitive csv format based on musical notes and vice versa. Still a work in progress.

## Usage
To install requirements: 

```console
$ pip install -r requirements.txt
```

For an example of midi to csv: 
```console
$ python midi_to_csv.py example/test
Outputting csv files in to example/test-output-csvs
Processing Garrett_Generated1.mid in to Garrett_Generated1.csv
Done creating csvs!
```

For an example of csv to midi: 
```console
$ python csv_to_midi.py example/test-output-csvs
Outputting mid files in to example/test-output-csvs-output-midis
Processing Garrett_Generated1.csv in to Garrett_Generated1.mid
Done creating midis!
```

An example of the csv format (rendered in Github Flavored Markdown thanks to [this tool](https://csvtomd.com/#/)): 

|    | note_name | start_time | duration | velocity | tempo |
| -- | --------- | ---------- | -------- | -------- | ----- |
| 0  | E-4       | 0.292      | 1.0      | 90       | 120   |
| 1  | B-4       | 0.292      | 1.0      | 90       | 120   |
| 2  | C4        | 1.08       | 0.25     | 105      | 120   |
| 3  | G4        | 1.08       | 0.25     | 105      | 120   |
| 4  | A3        | 1.412      | 1.0      | 110      | 120   |
| 5  | F#4       | 1.412      | 1.0      | 110      | 120   |