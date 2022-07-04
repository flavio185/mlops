import datetime
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from google.cloud import storage

import ssl

BUCKET_NAME='treinamento_modelo_trabalho_final'

# Determine CSV, label, and key columns
CSV_COLUMNS = ["etnia", 
               "sexo", 
               "casapropria",
               "outrasrendas", 
               "estadocivil", 
               "escolaridade",
               "renda",
               "idade"]
LABEL_COLUMN = "default"

def importDataSet():
  ssl._create_default_https_context = ssl._create_unverified_context
  url = 'https://raw.githubusercontent.com/flavio185/mlops/main/BaseDefault01.csv'
  url2 = 'https://raw.githubusercontent.com/flavio185/mlops/main/BaseDefault02.csv'
  dataset1 = pd.read_csv(url)
  dataset2 = pd.read_csv(url2)
  dataset = pd.concat([dataset1, dataset2])
  return dataset

def prepareDataForTraining(dataset):
  # Remove the column we are trying to predict ('income-level') from our features list
  # Convert the Dataframe to a lists of lists
  train_features = dataset[CSV_COLUMNS].values.tolist()
  # Create our training labels list, convert the Dataframe to a lists of lists
  train_labels = (dataset[LABEL_COLUMN]).values.tolist()
  # [END define-and-load-data]
  #Split dataset into test and training
  X_train, X_test, y_train, y_test = train_test_split(train_features, train_labels, test_size=0.3, random_state=7)
  return X_train, X_test, y_train, y_test

def trainClassifierModel(classifier):                            
  model = classifier.fit(X_train, y_train)

  y_pred = model.predict(X_test)

  accuracy = model.score(X_test, y_test)

  report = classification_report(y_test,y_pred)
  
  writeModelInfoToFile("Classifier:"+str(classifier))
  writeModelInfoToFile("\nAccuracy:"+str(accuracy))
  writeModelInfoToFile("\nReport\n"+str(report))

  exportModel(model)


def exportModel(model):
  # Export the model to a file
  joblib.dump(model, 'model.joblib')

def uploadFilestoGCStorage(gcs_folder_name):
  # Upload the model to GCS
  bucket = storage.Client().bucket(BUCKET_NAME)
  blob = bucket.blob('{}/{}'.format(gcs_folder_name,'model.info'))
  blob.upload_from_filename('model.info')
  blob = bucket.blob('{}/{}'.format(gcs_folder_name,'model.joblib'))
  blob.upload_from_filename('model.joblib')

def writeModelInfoToFile(info):
  f = open("model.info", "a")
  f.write(info)
  f.close()

###
# Create the classifier
classifierRF = RandomForestClassifier(random_state = 1,
                                  n_estimators = 750,
                                  max_depth = 15, 
                                  min_samples_split = 5,  min_samples_leaf = 1) 


dataset = importDataSet()
X_train, X_test, y_train, y_test = prepareDataForTraining(dataset)
trainClassifierModel(classifierRF)

#
gcs_folder_name=datetime.datetime.now().strftime('classifier_emprestimo_%Y%m%d_%H%M%S')
uploadFilestoGCStorage(gcs_folder_name)

