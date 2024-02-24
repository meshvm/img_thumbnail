# img_thumbnail
img thumbnail
Coding Exercise

You are developing the service layer of an application like Instagram. You are working
on a module which is responsible for supporting image upload, thumbnail generation,
and storage in the Cloud. Multiple users are going to use this service at the same
time. For this reason, the service should be scalable.
Create an API to upload images to the Cloud by using the API Gateway and Lambda
Function. Once an image is uploaded to the S3 Bucket a request should be added to a
queue to generate a thumbnail of the uploaded image. Build a Lambda function to
generate thumbnail of the images as soon as the request arrives. The function should
store the generated thumbnail in the same S3 Bucket. Create APIs to download the
image and to download the related thumbnail.
Language: Python3.7+
1. Create an API to upload image
2. Create an API to download/view uploaded image
3. Create an API to download/view thumbnail of the uploaded image
4. Write unit tests to cover all scenarios (optional)
5. Write a brief document providing API details and usage instructions (optional)