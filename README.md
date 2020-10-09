# PredictIt
PredictIt - A Disease Predictor Model which uses ML to detect the disease and show precautions and predicted disease accordingly.


## **Steps to run this site on your localhost:**

1. Install all the requirements by running the following code in terminal/cmd/ps:
```
pip install -r requirements.txt
```

2. Open the entire folder in your ide (VS Code preferably), then open the app.py  and run the commands below (This is for user database):
```
flask db init
flask db migrate -m "Initial migrate"
flask db upgrade
```
3.Run the app.py and it should work properly.