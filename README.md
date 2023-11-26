# Contexto
Nesse repositório se encontra o código necessário para a execução da parte relacionada à API no trabalho prático 2 da disciplina de Computação em Nuvem

# Comandos
A seguir segue uma lista de comandos a serem utilizados para configuração do Docker, Kubernetes e ArgoCD. É necessário que eles sejam executados na pasta onde o repositório foi clonado para garantir seu funcionamento.

Também e necesário executar os comandos listados no repositório do gerador de modelo, https://github.com/pdrgbr/model_generator, para garantir o funcionamento do projeto como um todo.

## Montar imagem no Docker
docker image build -t flask_api_pedro .

## Executar imagem no Docker
docker run -p 32210:32210 -d flask_api_pedro

## Buildar imagem a ser publicada no DockerHub
docker build -t pdrgbr/flask-api:0.X .

## Publicar imagem no DockerHub
docker push pdrgbr/flask-api:0.X

## Aplicar configurações do Kubernetes
kubectl -n pedroribeiro apply -f deployment.yaml

kubectl -n pedroribeiro apply -f service.yaml

## Alterar número de réplicas do Deployment
kubectl scale deployment pedroribeiro-playlist-recommender-deployment --replicas=X -n pedroribeiro

## Obter detalhes do Deployment
kubectl describe deployment pedroribeiro-playlist-recommender-deployment -n pedroribeiro   

## Deletar Deployment
kubectl -n pedroribeiro delete deployment pedroribeiro-playlist-recommender-deployment

## Obter status do Kubernetes
kubectl -n pedroribeiro get service 

kubectl -n pedroribeiro get deployment 

## Criar aplicação no ArgoCD
argocd app create pedroribeiro-api \
  --repo https://github.com/pdrgbr/flask_api \
  --path . \
  --project pedroribeiro-project \
  --dest-namespace pedroribeiro \
  --dest-server https://kubernetes.default.svc \
  --sync-policy automated \
  --self-heal \
  --auto-prune

## Obter status da aplicação no ArgoCD
argocd app get pedroribeiro-api 

# Teste do sistema

Para garantir que tudo está funcionando execute o comando:

wget --server-response \
	   --output-document response.out \
	   --header='Content-Type: application/json' \
	   --post-data '{"songs": ["Crash And Burn"]}' \
	   http://$CLUSTER-IP:32210/api/recommender

É esperado que seja criado um arquivo response.out contendo uma lista de nomes de músicas sugeridas.

Para obter o $CLUSTER-IP execute o comando: 

kubectl -n pedroribeiro get service 
