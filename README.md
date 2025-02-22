# DreamDev-Hackathon

## Overview
This app processes transaction data from text files and computes key sales metrics. 

## Features
- **Highest Sales Volume in a Day** 
- **Highest Sales Value in a Day**
- **Most Sold Product ID by Volume**
- **Highest Sales Staff ID for Each Month**
- **Highest Hour of the Day by Average Transaction Volume**

## Implementation Details
### Technologies Used
- **Python**: Core programming language.
- **Flask**: Backend API:
- **HTML, CSS, Tailwind**: Frontend Display
- **AWS**

## Usage
- clone the repo
- create a virtual environment, activate and install all dependencies
```py
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```
- Run the code
```py
flask --app main --debug run

```
- Navigate to `http//:localhost:5000`


##> [!IMPORTANT]
> All code logic sales analytics are in `analytics.py`
