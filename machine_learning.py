import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from xgboost import XGBClassifier, plot_importance
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from autogluon.tabular import TabularPredictor
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score, roc_auc_score
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler

X = y = X_train = X_test = y_train = y_test = None

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1
    )

xgb = XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='logloss'
    )

lgb = LGBMClassifier(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_samples=10,
    min_gain_to_split=0.0,
    random_state=42,
    verbosity=-1
    )

cat = CatBoostClassifier(
    iterations=300,
    learning_rate=0.1,
    depth=6,
    verbose=0
    )

et = ExtraTreesClassifier(
    n_estimators=300,
    max_depth=6,
    random_state=42
    )

lr = LogisticRegression(
    class_weight='balanced',
    max_iter=1000
    )


def set_df(df):
    global X, y, X_train, X_test, y_train, y_test
    X = df.drop(["is_phishing", "link","clean_domain","top_level_domain",'full_domain'], axis=1)
    y = df["is_phishing"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
def run_randomforestclassifier():
    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)
    y_proba = rf_model.predict_proba(X_test)[:, 1]

    print("\nClassification Report RandomForestClassifie:\n", classification_report(y_test, y_pred))

def run_xgboost():

    xgb.fit(X_train, y_train)

    y_pred = xgb.predict(X_test)

    print("\nClassification Report xgboost:\n", classification_report(y_test, y_pred))
    
    importance = xgb.get_booster().get_score(importance_type='gain')
    importance_df = pd.DataFrame({
        'Feature': list(importance.keys()),
        'Importance': list(importance.values())
    }).sort_values(by='Importance', ascending=False)
    
    print("\nFeature Importance (per gain):")
    print(importance_df)

def run_lightGBM():
    lgb.fit(X_train, y_train)

    y_pred = lgb.predict(X_test)

    print("\nClassification Report lightGBM:\n", classification_report(y_test, y_pred))

def run_catboost():
    cat.fit(X_train, y_train)

    y_pred = cat.predict(X_test)

    print("\nClassification Report catboost:\n", classification_report(y_test, y_pred))

def run_extraTrees():
    et.fit(X_train, y_train)

    y_pred = et.predict(X_test)

    print("\nClassification Report extraTrees:\n", classification_report(y_test, y_pred))

def run_LogReg():
    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_test)

    print("\nClassification Report LogisticRegression:\n", classification_report(y_test, y_pred))

def run_autoGluon(df):

    train_data, test_data = train_test_split(df, test_size=0.3, random_state=42)

    predictor = TabularPredictor(label="is_phishing",problem_type="binary",eval_metric="f1").fit(train_data=train_data,presets="best",time_limit=600,verbosity=0)

    y_pred = predictor.predict(test_data)
    print("\nClassification Report autoGluon:\n", classification_report(y_test, y_pred))
    fi = predictor.feature_importance(test_data)
    print("\nFeature Importance:\n", fi)

def predict_dominio(custom_df) :
    new_custom_df = custom_df.drop(columns=['link',"clean_domain","top_level_domain",'full_domain'])
    xgb.fit(X_train, y_train)

    y_pred_proba = xgb.predict_proba(new_custom_df)
    prob_phish = y_pred_proba[0][1]

    # Stampa risultati leggibili
    print(f"Probabilità che il dominio sia phishing: {prob_phish * 100:.2f}%")
    if prob_phish >= 0.80:
        print("Il dominio è classificato come Phishing ad alta confidenza.")
    elif prob_phish >= 0.60:
        print("Il dominio presenta un numero significativo di indicatori di phishing.")
    elif prob_phish >= 0.40:
        print("Il dominio mostra alcune caratteristiche ambigue o sospette")
    elif prob_phish >= 0.20:
        print("La classificazione indica una bassa probabilità di phishing.")
    else:
        print("Il rischio di phishing rilevato è minimo.")