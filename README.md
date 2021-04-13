# PredictIt
PredictIt - A Disease Predictor Website which uses ML to detect the disease and show precautions and predicted disease accordingly.

## Built using:
1. Flask
2. Python Scikit Learn Libraries
3. HTML, CSS, JS


## **Steps to run this site on your localhost:**

1. Install all the requirements by running the following code in terminal/cmd/ps:
```
pip install -r requirements.txt
```

2. Open the entire folder in your ide (VS Code preferably), then open the app.py  and run the commands below (This is for user database):
```
py -m venv env
```


.\env\Scripts\activate
```
flask db init
flask db migrate -m "Initial migrate"
flask db upgrade
```
3.Run the app.py and it should work properly.
