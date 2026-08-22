## Что такое ctr?
# ctr - клиент командной строки, который идет в составе проекта containerd. (Если установлен containerd, то ctr установлен по умолчанию) 
Клиент ctr похож на одноименный интерфейс командной строки Docker, но команды и флаги часто отличаются от своих (как правило, более удобных для пользователя) docker аналогов.\
Однако ctr может стать отличным инструментом для изучения для более широкой аудитории — он работает поверх API containerd, и, изучив доступные команды, вы сможете составить представление о том, что может и чего не может делать containerd.\
\
## Основные комагды ctr\
## Для извлечения образов с помощью ctr всегда требуется полная ссылка — другими словами, нельзя опускать домен или тег (хотя дайджест указывать необязательно).
Например:\
sudo ctr image pull quay.io/quay/busybox:latest
## Получение изображения из другого реестра — в данном случае из Quay:
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
sudo ctr image import iximiuz-test.tar 
## Как и в Docker, вы можете помечать локальные образы тегами ctr image tag. Например:
sudo ctr image tag example.com/iximiuz/test:latest \
  registry.iximiuz.com/test:latest 

Что бы отправить контейнер во временный реестр, дрступный по адресу registry.iximiuz.com достаточно выполнить команду:
sudo ctr image push --user {username}:{password} {image}:{tag}

Чтобы удалить локальный image :
sudo ctr image remove {image}:{tag}

Иногда может возникнуть необходимость просмотреть содержимое образа. С помощью ctr это можно сделать с помощью команды ctr image export, которая сохраняет содержимое образа в архив:

sudo ctr image export /tmp/nginx.tar docker.io/library/nginx:latest
Копировать в буфер обмена


Запустите игровую площадку, чтобы активировать эту проверку
Теперь вы можете изучить содержимое файла /tmp/nginx.tar . Экспортированный архив будет содержать данные образа nginx, сохраненные в формате OCI Image Layout.

Вы можете распаковать архив в временную папку и изучить его содержимое:

mkdir /tmp/nginx_image
tar -xf /tmp/nginx.tar -C /tmp/nginx_image/
ls -lah /tmp/nginx_image/
Копировать в буфер обмена
Результат должен выглядеть следующим образом:

total 24K
drwxr-xr-x  3 root root 4.0K Jun  3 11:23 .
drwxrwxrwt 11 root root 4.0K Jun  3 11:23 ..
drwxr-xr-x  3 root root 4.0K Jan  1  1970 blobs
-rw-r--r--  1 root root  323 Jan  1  1970 index.json
-rw-r--r--  1 root root  611 Jan  1  1970 manifest.json
-r--r--r--  1 root root   30 Jan  1  1970 oci-layout
Копировать в буфер обмена
Если работа с необработанными слоями изображений нежелательна, вы можете смонтировать изображение во временную папку на хосте и исследовать ее корневую файловую систему как обычный каталог:

sudo ctr image mount docker.io/library/nginx:latest
Копировать в буфер обмена
sha256:b97c52357821ac794246c890299695624c55b94551032ab74b9de33af039834d
/run/containerd/io.containerd.mount-manager.v1.bolt/t/1/1
Копировать в буфер обмена


Start playground to activate this check
Now you can explore the rootfs of the Nginx image. The file and directories of the Nginx image should be available at the path returned by the ctr image mount command. Try:

sudo ls -l /run/containerd/io.containerd.mount-manager.v1.bolt/t/1/1
Copy to clipboard
Результат будет выглядеть как обычная файловая система Linux, и это неудивительно, поскольку образ Nginx основан на дистрибутиве Debian Linux:

total 84
drwxr-xr-x 2 root root 4096 May  2 00:00 bin
drwxr-xr-x 2 root root 4096 Apr  2 11:55 boot
drwxr-xr-x 2 root root 4096 May  2 00:00 dev
drwxr-xr-x 1 root root 4096 May  3 19:51 docker-entrypoint.d
-rwxrwxr-x 1 root root 1616 May  3 19:50 docker-entrypoint.sh
drwxr-xr-x 1 root root 4096 May  3 19:51 etc

Не забудьте отмонтировать образ, когда закончите с ним работать

sudo ctr image unmount /run/containerd/io.containerd.mount-manager.v1.bolt/t/1/1
