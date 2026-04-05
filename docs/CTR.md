## Что такое ctr??\
# ctr - клиент командной строки, который идет в составе проекта containerd. (Если установлен containerd, то ctr установлен по умолчанию) \
Клиент ctr похож на одноименный интерфейс командной строки Docker, но команды и флаги часто отличаются от своих (как правило, более удобных для пользователя) docker аналогов. /
Однако ctr может стать отличным инструментом для изучения для более широкой аудитории — он работает поверх API containerd, и, изучив доступные команды, вы сможете составить представление о том, что может и чего не может делать containerd.\
\
## Основные комагды ctr\
## Для извлечения образов с помощью ctr всегда требуется полная ссылка — другими словами, нельзя опускать домен или тег (хотя дайджест указывать необязательно).\
Например:\
sudo ctr image pull quay.io/quay/busybox:latest\
## Получение изображения из другого реестра — в данном случае из Quay:\
sudo ctr image pull quay.io/quay/busybox:latest
## Список локальных изображений:
sudo ctr image ls
\
Однако, несмотря на то, что containerd часто используется инструментами более высокого уровня для создания образов контейнеров, он не предоставляет готовых функций для создания образов, поэтому в нем нет команды ctr image build .\
Как загрузить существующие образы в containerd с помощью ctr image import. В какой-то степени это компенсирует отсутствие команды build. Вот как можно создать образ с помощью традиционной команды docker build, а затем импортировать его:\
docker build -t example.com/iximiuz/test:latest --sbom=false --provenance=false - <<EOF \
FROM busybox:latest\
CMD ["echo", "just a test"]\
EOF\
docker save -o iximiuz-test.tar example.com/iximiuz/test:latest \
sudo ctr image import iximiuz-test.tar \
## Как и в Docker, вы можете помечать локальные образы тегами ctr image tag. Например:\
sudo ctr image tag example.com/iximiuz/test:latest \
  registry.iximiuz.com/test:latest \
  
