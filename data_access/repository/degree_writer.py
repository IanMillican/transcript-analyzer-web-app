import json
from pathlib import Path
from exceptions.degree_writer_error import DegreeWriterException

def write_degree(degree: dict, allow_overwrite: bool = False) -> None:
    if not allow_overwrite:
        if "program" not in degree or degree["program"] in (None, ""):
            raise DegreeWriterException("Program must have a name")
        if "sections" not in degree or not isinstance(degree["sections"], list) or len(degree["sections"]) == 0:
            raise DegreeWriterException("Program must have a section")
        
        filename = degree['program'].lower().replace(' ', '_') + '.json'
        file_path = f"data_access/config/requirements/{filename}"

        if Path(f"data_access/config/requirements/{degree['program']}.json").exists():
            raise DegreeWriterException("Degree already exists")
        
        with open(file_path, "w") as f:
            json.dump(degree, f, indent=4)
    else:
        pass
