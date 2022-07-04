#No terminal GCP

git clone https://github.com/flavio185/mlops.git

cd mlops/Flask/gcpVM/

#Cria VM

./01-createvm.sh

#Acessar vm via ssh

#Configurar VM.

git clone https://github.com/flavio185/mlops.git

cd mlops/Flask/gcpVM/

./02-setupvm.sh

#Copiar modelo

cd ~/mlops/Flask/app

gsutil cp gs://treinamento_modelo_trabalho_final/classifier_emprestimo_20220627_234054/model.joblib .

#Buildando imagem.

cd ~/mlops/Flask

sudo docker build -t flask_prediction .

#Rodando a imagem

sudo docker run  -p 8080:80 -d -v $PWD/app:/app flask_prediction

