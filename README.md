# Transcript Analyzer

A local web application that automates the academic transcript audit process for university students. Upload a PDF transcript, and the app parses your completed courses, compares them against a degree program's requirements, and displays a visual progress dashboard showing what you've satisfied and what remains.

> Currently designed and tested for the **University of New Brunswick (UNB) Bachelor of Computer Science (BCS)** program, with the architecture in place to support additional undergraduate degrees.

---

## Features

- **PDF transcript parsing** — Extracts student info, terms, and course attempts from UNB unofficial transcript PDFs
- **Requirement evaluation** — Supports AND, OR, XOR, and constraint-based requirement trees with GPA-aware branch selection
- **Elective classification** — Automatically classifies electives against configurable subject/level constraints
- **Visual dashboard** — Results page with a two-column section layout and color-coded satisfied/unsatisfied rows
- **Degree program builder** — Client-side UI to define new degree programs as structured JSON, with a recursive requirement tree builder
- **Extensible degree format** — Degree requirements stored as JSON files; add new programs by dropping in a new file

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Flask |
| Frontend | HTML, CSS, Flask, vanilla JavaScript, Jinja2 |
| PDF Parsing | pypdf (PdfReader) |
| Degree Data | JSON |
| Storage | None (local filesystem only, no database yet) |

---

## Project Structure

```
transcript-analyzer/
├── app.py                          # Flask entry point
├── domain/
│   ├── model/
│   │   ├── course.py               # Base course class
│   │   ├── course_attempt.py       # Transcript entry with grade
│   │   ├── student.py              # Student info (name, ID, DOB)
│   │   ├── term.py                 # Academic term with course list
│   │   ├── transcript.py           # Full transcript: Student + Terms
│   │   ├── month_day.py            # Month/day dataclass (no year)
│   │   ├── degree_program/
│   │   │   ├── requirement.py      # Requirement tree node (AND/OR/XOR/COURSE/CONSTRAINT)
│   │   │   ├── section.py          # Degree section with name and priority
│   │   │   └── degree.py           # Full degree: program name, exclusions, sections
│   │   └── results/
│   │       ├── requirement_result.py
│   │       ├── section_result.py
│   │       └── comparison_result.py
│   └── service/
│       ├── transcript_service.py   # parse_transcript(path) -> Transcript
│       ├── degree_service.py       # get_degree(path) -> Degree
│       ├── evaluator.py            # Core evaluation logic
│       └── evaluator_service.py    # evaluate_transcript(...) -> ComparisonResult
├── data_access/
│   ├── parsers/
│   │   ├── course_parser.py
│   │   ├── term_parser.py
│   │   ├── transcript_parser.py
│   │   └── degree_parser.py
│   ├── repository/
│   │   └── degree_writer.py
│   └── config/
│       └── requirements/
│           └── computer_science.json   # BCS degree requirements
├── static/
│   ├── styles.css
│   ├── index.css
│   ├── transcript_preview.css
│   ├── create_section.css
│   ├── create_degree.css
│   └── js/
│       ├── create_section.js
│       └── create_degree.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── transcript_preview.html
│   ├── create_section.html
│   └── create_degree.html
├── utils/
│   └── constants.py
├── exceptions/
│   ├── parsing_exception.py
│   ├── invalid_argument.py
│   ├── invalid_grade.py
│   └── degree_writer_error.py
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- `pip`

### Installation

```bash
# Clone the repository
git clone https://github.com/IanMillican/transcript-analyzer-web-app
cd transcript-analyzer

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
python3 -m flask run
```

Then open your browser to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Usage

### Analyzing a Transcript

1. Navigate to the home page
2. Upload your UNB unofficial transcript PDF
3. The app parses your transcript and evaluates it against the BCS degree requirements
4. Results are displayed as a dashboard satisfied courses having a ✓ and unsatisfied courses having a ✗

> **Note:** The degree is currently hardcoded to `computer_science.json`. Degree selection on upload is planned.

### Creating a New Degree Program

1. Go to **Data Management → Create Degree** in the nav
2. Enter the program name and any excluded subjects or courses
3. Add sections and build each section's requirement tree using the interactive builder
4. Submit — the degree is saved as a JSON file in `data_access/config/requirements/`

---

## Degree JSON Format

Degree programs are defined as JSON files. The structure supports nested AND/OR/XOR logic for complex requirement trees, as well as constraint-based elective sections.

```json
{
    "program": "Computer Science",
    "excluded_subjects": [],
    "excluded_courses": [],
    "sections": [
        {
            "name": "CS Core",
            "priority": 1,
            "requirements": {
                "and": [
                    {"Subject": "CS", "Number": 1073, "Name": "Intro to CS I", "CreditHours": 4, "Coop": false},
                    {"xor": [
                        {"Subject": "CS", "Number": 1303, "Name": "Discrete Structures", "CreditHours": 3, "Coop": false},
                        {"Subject": "MATH", "Number": 2203, "Name": "Discrete Math", "CreditHours": 3, "Coop": false}
                    ]}
                ]
            }
        },
        {
            "name": "Technical Electives",
            "priority": 3,
            "requirements": {
                "constraint": {
                    "count": 7,
                    "min_credit_hours": 21,
                    "include_subject": ["CS", "SWE"],
                    "exclude_subject": [],
                    "min_level_2000": 0,
                    "min_level_3000": 3,
                    "min_level_4000": 1
                }
            }
        }
    ]
}
```

### Requirement Node Types

| Type | Behaviour |
|---|---|
| `and` | All children must be satisfied |
| `or` | At least one branch satisfied; highest-GPA branch wins; unused satisfied branches return courses to pool |
| `xor` | Exactly one branch; highest-GPA branch wins; unused satisfied branches keep courses removed from pool |
| `course` | Leaf node matching by course code; excludes invalid grades (W, WF, INC, NCR, N/A) |
| `constraint` | Greedy elective selection prioritizing level minimums, then filling count |

Sections are evaluated in **priority order** (lower number = evaluated first).

---

## Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | Upload page |
| POST | `/upload/` | Parse transcript PDF and render results |
| GET | `/create-degree/` | Degree creation page |
| POST | `/create-degree/` | Save new degree JSON to disk |
| GET | `/create-section/` | Requirement tree builder |

---

## Known Limitations

- Only tested against UNB unofficial transcript PDF format
- Degree program is hardcoded to BCS on upload (not yet user-selectable)
- No user authentication
- No persistent storage between sessions — each upload is stateless

---

## Planned Features

-  Editable degree programs
- User-selectable degree on upload
- Projection engine (estimated terms/years to graduation)
- W/P course tracking (writing-intensive, programming-intensive)
- Analytics and insights page
- Export student data
- Multiple transcript comparison
- Server-side persistent storage
- User authentication

---

## Dependencies

```
flask
pypdf
```

Standard library modules used: `json`, `re`, `os`, `copy`, `datetime`, `tempfile`, `pathlib`, `enum`, `dataclasses`

---

## License

*No license defined yet.*