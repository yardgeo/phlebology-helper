echo "Start all"
cd backend
docker-compose up -d --build

echo "Backend started"

cd ../vue-phlebology-helper
docker-compose up -d --build

cd ..
echo "Web started"