import boto3
import time
import os
import sys

from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv('configs/.env')

# boto3のSQSクライアントを作成
sqs = boto3.client('sqs')


# SQSに1回キューを追加
def send_message(type, queue_url):
    if type == 'standard':
        response = sqs.send_message(QueueUrl=queue_url, MessageBody='{"hoge": {"soiya": "a"}}')
        print("send standard message")
    elif type == 'fifo':
        response = sqs.send_message(QueueUrl=queue_url, MessageBody='{"hoge": {"soiya": "b"}}',MessageDeduplicationId=str(time.time_ns()), MessageGroupId='Group2')
        print("send fifo message")

# キューに入っている情報を確認し内容を標準出力
def receive_message(queue_url):
    messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)

    if 'Messages' in messages:  # キューが空でない場合
        for message in messages['Messages']:
            print(f"message: {message['Body']}")

# mメッセージの削除
def delete_message(queue_url):
    messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)

    if 'Messages' in messages:  # キューが空でない場合
        for message in messages['Messages']:
            print(f"message: {message['Body']}")
            # メッセージを削除
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

# SQS内の処理されていないキューの数を確認し標準出力
def get_approximate_number_of_messages(queue_url):
    attributes = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])
    print(f"未処理キュー数: {attributes['Attributes']['ApproximateNumberOfMessages']}")

# SQS内の処理されてないキューのうち最も時間が長いキューが何秒経っているか確認し標準出力
def get_oldest_message_age(queue_url):
    attributes = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['OldestMessageAge'])
    print(f"最長未処理時間: {str(int(int(attributes['Attributes']['OldestMessageAge'])/1000/60))}分 {str(int(int(attributes['Attributes']['OldestMessageAge'])/1000%60))}秒")

def get_count_and_old(queue_url):
    count_attributes = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])
    print(f"未処理キュー数: {count_attributes['Attributes']['ApproximateNumberOfMessages']}")
    old_attributes = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['OldestMessageAge'])
    print(f"最長未処理時間: {str(int(int(old_attributes['Attributes']['OldestMessageAge'])/1000/60))}分 {str(int(int(old_attributes['Attributes']['OldestMessageAge'])/1000%60))}秒")

def test(queue_url):
    count_attributes1 = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])
    old_attributes1 = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['OldestMessageAge'])
    count_attributes2 = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])
    old_attributes2 = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['OldestMessageAge'])
    count_attributes3 = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])
    old_attributes3 = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['OldestMessageAge'])

    messages1 = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)


    count_attributes4 = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])
    old_attributes4 = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['OldestMessageAge'])

    messages2 = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)

    count_attributes5 = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])
    old_attributes5 = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['OldestMessageAge'])

    print(f"c-1. 未処理キュー数: {count_attributes1['Attributes']['ApproximateNumberOfMessages']}, 最長未処理時間: {str(int(int(old_attributes1['Attributes']['OldestMessageAge'])/1000/60))}:{str(int(int(old_attributes1['Attributes']['OldestMessageAge'])/1000%60))}")
    print(f"c-2. 未処理キュー数: {count_attributes2['Attributes']['ApproximateNumberOfMessages']}, 最長未処理時間: {str(int(int(old_attributes2['Attributes']['OldestMessageAge'])/1000/60))}:{str(int(int(old_attributes2['Attributes']['OldestMessageAge'])/1000%60))}")
    print(f"c-3. 未処理キュー数: {count_attributes3['Attributes']['ApproximateNumberOfMessages']}, 最長未処理時間: {str(int(int(old_attributes3['Attributes']['OldestMessageAge'])/1000/60))}:{str(int(int(old_attributes3['Attributes']['OldestMessageAge'])/1000%60))}")
    if 'Messages' in messages1:  # キューが空でない場合
        for message in messages1['Messages']:
            print(f"m-1. message: {message['Body']}")
    else:
        print("m-1.no message")
    print(f"c-4. 未処理キュー数: {count_attributes4['Attributes']['ApproximateNumberOfMessages']}, 最長未処理時間: {str(int(int(old_attributes4['Attributes']['OldestMessageAge'])/1000/60))}:{str(int(int(old_attributes4['Attributes']['OldestMessageAge'])/1000%60))}")
    if 'Messages' in messages2:  # キューが空でない場合
        for message in messages2['Messages']:
            print(f"m-2. message: {message['Body']}")
    else:
        print("m-2. no message")
    print(f"c-5. 未処理キュー数: {count_attributes5['Attributes']['ApproximateNumberOfMessages']}, 最長未処理時間: {str(int(int(old_attributes5['Attributes']['OldestMessageAge'])/1000/60))}:{str(int(int(old_attributes5['Attributes']['OldestMessageAge'])/1000%60))}")

def main():
    type = sys.argv[1]
    operation = sys.argv[2]

    # キューのURL (ここを適切なURLに置き換えてください)

    if type == 'standard':
        queue_url = os.getenv("QUEUE_URL_STANDARD")
    elif type == 'fifo':
        queue_url = os.getenv("QUEUE_URL_FIFO")
    else:
        print(f'Unkown type: {type}')
        sys.exit

    if operation == 'send':
        send_message(type, queue_url)
    elif operation == 'receive':
        receive_message(queue_url)
    elif operation == 'delete':
        delete_message(queue_url)
    elif operation == 'get_count':
        get_approximate_number_of_messages(queue_url)
    elif operation == 'get_old':
        get_oldest_message_age(queue_url)
    elif operation == 'get_count_and_old':
        get_count_and_old(queue_url)
    elif operation == 'test':
        test(queue_url)
    else:
        print(f'Unknown operation: {operation}')


if __name__ == '__main__':
    main()