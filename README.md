# open-analytics-antibiotic-cost

Plotly charts visualizing:
1. The total cost in £ of the antibiotics Amoxicillin, Doxycycline Hyclate, and Cefalexin per month for Clinical commissioning groups (CCGs).
2. The Total cost in £ of Amoxicillin, Doxycycline Hyclate, and Cefalexin per 1000 GP registered patients for the current year.

Data sources: NHS Digital, OpenPrescribing.net

## Install

Ensure that you have Jupyter installed:

```bash
pip install -r requirements.txt
brew install jq # if on mac
apt-get update && apt-get install jq  # if on linux

# start the development notebook
jupyter notebook
```
