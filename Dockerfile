# 基本となるイメージの指定
FROM python:3.10-slim-buster

# Install tzdata package
RUN apt-get update && apt-get install -y tzdata

# Set the timezone to JST
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
# ここでは、AWS CLIとBoto3（Python用AWS SDK）をインストールしています
RUN pip install --no-cache-dir awscli boto3
RUN pip install --no-cache-dir python-dotenv

# ソースコードのコピー
# （ローカルの./srcディレクトリにある全ての.pyファイルを/appにコピーする）
#COPY ./src/*.py ./
#COPY ./configs/.env /app/configs/

# コンテナ起動時に実行されるコマンド(今回は起動時に実行ではなく、起動後にコンテナ内部に入り、プログラム実行をする)
# CMD ["python", "./your_main_script.py"]
