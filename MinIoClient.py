# _*_ coding:utf-8 _*_
'''"""
作者：cai
日期：2024年11月20日
minio的python方法实现
“”“'''
from minio import Minio
from minio.error import S3Error

class MinioClient:
    def __init__(self, endpoint= "172.16.100.247:9000", access_key= "minioadmin", secret_key= "minioadmin", secure=False):
        """
        初始化 MinIO 客户端。

        :param endpoint: MinIO 服务地址（如 "localhost:9000"）
        :param access_key: 访问密钥
        :param secret_key: 秘密密钥
        :param secure: 是否使用 HTTPS（默认 True）
        """
        self.client = Minio(endpoint, access_key, secret_key, secure=secure)

    def upload_file(self, bucket_name, object_name, file_path):
        """
        上传文件到指定的桶。

        :param bucket_name: 桶名称
        :param object_name: 对象名称（存储在 MinIO 中的文件名）
        :param file_path: 本地文件路径
        """
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
            self.client.fput_object(bucket_name, object_name, file_path)
            print(f"文件 '{file_path}' 已上传到桶 '{bucket_name}' 中，名称为 '{object_name}'。")
        except S3Error as e:
            print(f"上传文件时出错：{e}")

    def download_file(self, bucket_name, object_name, file_path):
        """
        从指定的桶下载文件。

        :param bucket_name: 桶名称
        :param object_name: 对象名称（存储在 MinIO 中的文件名）
        :param file_path: 下载到本地的文件路径
        """
        try:
            self.client.fget_object(bucket_name, object_name, file_path)
            print(f"文件 '{object_name}' 已从桶 '{bucket_name}' 下载到本地路径 '{file_path}'。")
        except S3Error as e:
            print(f"下载文件时出错：{e}")


if __name__ == '__main__':
    final_point = "172.16.100.247:9000"
    # endpoint = "127.0.0.1:9000"
    access_key = "minioadmin"
    secret_key = "minioadmin"
    minio_client = MinioClient(final_point,access_key=access_key,secret_key=secret_key)
    print(minio_client)
    #                          桶名称   在minio中的文件名称（自定义） 文件路径加名称
    # minio_client.upload_file("dev","test_VideoUrl.txt","test_VideoUrl.txt")

    #从minio中下载文件            桶名称   桶中的文件名称       路径加自定义的名字
    # minio_client.download_file("dev","task.split-mp3.notify/2024/11/20/27WZE3UPLYU31EAK5PROZSNQA.mp4","log/down_test.mp4")




