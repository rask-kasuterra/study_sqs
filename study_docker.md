Dockerを使用する際に頻繁に使用される基本的なコマンドは以下のとおりです：

- `docker run`：新しいコンテナを作成して実行します。
    - 例：`docker run -it ubuntu bash`
- `docker ps`：現在稼働しているコンテナの一覧を表示します。
- `docker ps -a`：すべてのコンテナの一覧を表示します（稼働中、停止中含む）。
- `docker images`：ローカルに存在するDockerイメージの一覧を表示します。
- `docker pull`：Dockerイメージをレポジトリから取得します。
    - 例：`docker pull ubuntu`
- `docker build`：Dockerfileを元に新しいDockerイメージをビルドします。
    - 例：`docker build -t my_image .`
- `docker rm`：コンテナを削除します。
    - 例：`docker rm my_container`
- `docker rmi`：イメージを削除します。
    - 例：`docker rmi my_image`
- `docker stop`：稼働しているコンテナを停止します。
    - 例：`docker stop my_container`
- `docker start`：停止しているコンテナを再開します。
    - 例：`docker start my_container`
- `docker exec`：稼働中のコンテナ内でコマンドを実行します。
    - 例：`docker exec -it my_container bash`
- `docker logs`：コンテナのログを表示します。
    - 例：`docker logs my_container`

# 疑問
- [] Dockerfile には何書く？
- [] 新しいコンテナを作成だけして、実行しないことはできる？
- [] docker のコンテナ & イメージは作成後になにかファイルとして出力される？
- [] コンテナのログとは？コンテナでの標準出力やエラー出力全て？

# python3 で SQS 操作ができる docker image の作成

## Dockerfile を元にイメージをビルド
docker build -t sqs-study .

## 引数に AWS Cli の情報を渡しつつ python 環境を立ち上げる
docker run --name sqs-study -it -e AWS_ACCESS_KEY_ID=$(grep -A2 default ~/.aws/credentials | grep aws_access_key_id | cut -f3 -d' ') -e AWS_SECRET_ACCESS_KEY=$(grep -A2 default ~/.aws/credentials | grep aws_secret_access_key | cut -f3 -d' ') -e AWS_DEFAULT_REGION=$(grep -A2 default ~/.aws/config | grep region | cut -f3 -d' ') sqs-study bash 

