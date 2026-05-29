Create an image
docker build -t flask-app .

Run the container
docker run -d -p 5000:5000 -w /app -v "${pwd}:/app" flask-app

-w - Current working directory of the container
-v - Linking the pwd(host) to the working directory of the container
