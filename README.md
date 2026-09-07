# \# AI Resume Analyzer



An AI-powered resume screening application that helps recruiters analyze, compare, and rank multiple candidates against a given job description.



The application extracts text from PDF resumes, evaluates candidate-job fit using an AI model, identifies strengths and skill gaps, provides a recommendation, and automatically ranks candidates based on their fit scores.



\---



### \## Project Overview



Recruiters often have to manually review a large number of resumes for a single job opening. This process can be time-consuming and may lead to inconsistent initial screening.



The \*\*AI Resume Analyzer\*\* automates the first stage of resume screening by comparing candidate resumes with a provided job description.



It provides recruiters with:



\* An overall candidate fit score

\* Key candidate strengths

\* Missing or weak skills

\* Hiring recommendation

\* Automatic candidate ranking

\* Exportable shortlist results



The project was developed as an \*\*AI/ML internship project for SafeX Solutions\*\*.



\---



### \## Objectives



The main objectives of this project are to:



1\. Automate initial resume screening.

2\. Compare resumes against job requirements using AI.

3\. Generate a candidate fit score from 0–100.

4\. Identify candidate strengths and skill gaps.

5\. Provide a clear hiring recommendation.

6\. Process multiple resumes at once.

7\. Automatically rank candidates.

8\. Export screening results for recruiter use.



\---



### \## Features



#### \### Core Features



\* PDF resume text extraction

\* Job description input

\* AI-powered resume analysis

\* Candidate fit score from 0–100

\* Strength identification

\* Skill gap detection

\* Hiring recommendation

\* Interactive screening dashboard



#### \### Advanced Features



\* Batch processing of multiple resumes

\* Automatic candidate ranking

\* Export ranked shortlist as CSV

\* Error handling for unreadable resumes and failed analysis



\---



### \## Technologies Used



&#x20;Technology     Purpose                             

&#x20;-------------  ----------------------------------- 

&#x20;Python         Application development             

&#x20;Streamlit      Web application interface           

&#x20;Hugging Face   AI model inference                  

&#x20;DeepSeek-V3    Resume/JD analysis                  

&#x20;pdfplumber     PDF text extraction                 

&#x20;pandas         Data processing and ranking         

&#x20;python-dotenv  Environment variable management     

&#x20;Git/GitHub     Version control and project sharing 



\---

### 

### \## AI Analysis Methodology



The application compares each resume with the provided job description using an AI-powered analysis prompt.



The candidate's final fit score is calculated using the following evaluation criteria:



| Evaluation Criteria              |   Weight |

| -------------------------------- | -------: |

| Required Skills                  |      30% |

| Relevant Experience and Projects |      25% |

| Job Responsibilities             |      20% |

| Education and Coursework         |      15% |

| Additional Relevant Skills       |      10% |

| \*\*Total\*\*                        | \*\*100%\*\* |



The AI also provides:



\* Candidate strengths

\* Skill gaps

\* Overall recommendation



#### \### Recommendation Categories



The system classifies candidates into one of four categories:



\*  \*\*Strong Match\*\*

\*  \*\*Good Match\*\*

\*  \*\*Consider with Reservations\*\*

\*  \*\*Weak Match\*\*





### \## Project Structure



```text

AI\_Resume\_Analyzer/

│

├── app.py

├── resume\_parser.py

├── ai\_analyzer.py

├── scoring.py

├── .env

├── .gitignore

├── README.md

│

├── resumes/

│

└── outputs/

```



#### \### File Descriptions



**#### `app.py`**



Main Streamlit application.



Responsible for:



\* User interface

\* Resume uploading

\* Job description input

\* Batch processing

\* Progress tracking

\* Results dashboard

\* Candidate ranking

\* Candidate selection

\* CSV export



**#### `resume\_parser.py`**



Extracts readable text from uploaded PDF resumes using `pdfplumber`.



**#### `ai\_analyzer.py`**



Handles AI-powered resume analysis.



Responsible for:



\* Sending resume and job description to the AI model

\* Applying the evaluation criteria

\* Generating fit scores

\* Identifying strengths

\* Identifying skill gaps

\* Generating recommendations

\* Parsing the AI response



**#### `scoring.py`**



Reserved for scoring-related functionality and future scoring improvements.



**#### `.env`**



Stores the Hugging Face API token securely.



This file should \*\*never be uploaded to GitHub\*\*.



**#### `.gitignore`**



Prevents sensitive files and unnecessary generated files from being committed to GitHub.



**#### `resumes/`**



Folder for storing sample or test resumes locally.



**#### `outputs/`**



Folder for generated output files.



\---



### \## Installation



**### 1. Clone the repository**



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

```



Then navigate into the project folder:



```bash

cd AI\_Resume\_Analyzer

```



\---



**### 2. Create a Conda environment**



```bash

conda create -n resume-analyzer python=3.13

```



Activate it:



```bash

conda activate resume-analyzer

```



\---



**### 3. Install dependencies**



```bash

pip install streamlit openai python-dotenv pandas pdfplumber huggingface\_hub

```



\---



### \## Environment Configuration



Create a `.env` file in the project root directory.



Add your Hugging Face API token:



```text

HF\_TOKEN=your\_huggingface\_token\_here

```



Replace the placeholder with your own token.



\*\*Never commit your `.env` file to GitHub.\*\*



The project already includes `.env` in `.gitignore`.



\---

### 

### \## Running the Application



Activate the Conda environment:



```bash

conda activate resume-analyzer

```



Run the Streamlit application:



```bash

streamlit run app.py

```



The application will open in your browser at:



```text

http://localhost:8501

```



\---



### \## Testing



The application was tested using multiple sample resumes and an AI/ML Engineer job description.



Example test results:



| Candidate       | Fit Score | Recommendation             |

| --------------- | --------: | -------------------------- |

| Sample Resume 2 |        85 | Good Match                 |

| Sample Resume 3 |        65 | Consider with Reservations |

| Sample Resume 1 |         5 | Weak Match                 |



The results demonstrated that candidates with stronger alignment to the job requirements received higher fit scores.



The application was also tested with multiple resumes simultaneously to verify:



\* Batch processing

\* Candidate ranking

\* Fit score generation

\* Strength identification

\* Skill gap identification

\* Recommendation generation

\* CSV export

\* Error handling



\---



### \## Error Handling



The application handles several possible errors, including:



\* No resume uploaded

\* No job description provided

\* PDF containing no readable text

\* AI analysis returning no result

\* Invalid AI-generated fit score

\* Individual resume processing failures



If one resume fails during batch processing, the application continues analyzing the remaining resumes and displays the processing error separately.



\---



### \## Example Output



For each candidate, the application displays:



```text

Candidate: sample\_resume2.pdf



Fit Score: 85/100



Recommendation:

Good Match



Strengths:

✓ Python

✓ Machine Learning

✓ Scikit-learn

✓ NLP

✓ ML Projects



Skill Gaps:

• Limited SQL experience

• Limited production deployment experience

```



Candidates are then automatically ranked from the highest fit score to the lowest.



\---



### \## Recruiter Use Case



A recruiter can use the application by:



1\. Uploading multiple candidate resumes.

2\. Pasting the job description.

3\. Clicking \*\*Analyze Candidates\*\*.

4\. Reviewing the ranked candidate list.

5\. Selecting individual candidates for detailed analysis.

6\. Reviewing strengths and skill gaps.

7\. Downloading the ranked shortlist as a CSV file.



This reduces the time required for manual first-pass resume screening.



\---



### \## Future Improvements



Possible future improvements include:



\* Support for DOCX resumes

\* Resume section detection

\* More advanced semantic matching

\* Keyword and skill visualization

\* Recruiter authentication

\* Database integration

\* Job description keyword extraction

\* Candidate comparison charts

\* PDF report generation

\* ATS-style keyword matching

\* Improved scoring calibration

\* Deployment to a cloud platform

\* Support for multiple job descriptions



\---



### \## Limitations



The current version is intended as an AI-assisted screening tool rather than a final hiring decision system.



The generated fit score depends on:



\* Quality of the resume text

\* Quality of the job description

\* AI model interpretation

\* Information available in the candidate's resume



Recruiters should use the results as a screening aid and review candidates before making final hiring decisions.



\---



### \## Project Information



\*\*Project:\*\* AI Resume Analyzer



\*\*Category:\*\* AI/ML



\*\*Difficulty:\*\* Advanced



\*\*Developed for:\*\* SafeX Solutions Internship



\*\*Primary Technologies:\*\* Python, Streamlit, Hugging Face, DeepSeek-V3



\---



### \## Conclusion



The AI Resume Analyzer provides an automated and interactive approach to first-pass candidate screening.



By combining PDF text extraction, AI-powered resume analysis, weighted candidate evaluation, batch processing, automatic ranking, and CSV export, the application provides a practical MVP that can assist recruiters in identifying relevant candidates more efficiently.



