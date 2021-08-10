echo "Stop all"
cd backend
docker-compose down

echo "Backend stopped"

cd ../vue-phlebology-helper
docker-compose down

cd ..
echo "Web stopped"