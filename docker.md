```bash
docker-compose build
docker-compose --env-file .env up -d
npx prisma db pull
npx prisma generate
```

```bash
docker save -o back.tar back:latest
scp back.tar dev@ras.navong.xyz:/home/pi/
docker load < /home/pi/back.tar
docker images
```


```bash
docker tag news-backend nolandev1/news-backend
docker push nolandev1/news-backend
```