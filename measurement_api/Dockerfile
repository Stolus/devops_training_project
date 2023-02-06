FROM python:3.8-alpine

WORKDIR /app

# Ważne jest żeby zawsze najpierw kopiować requirementsy i je instalować
# A dopiero potem kopiować pliki
# Bo w przeciwnym razie przy każdej zmianie kodu trzeba by instalować wszystkie zależności od nowa
# W sumie w measurements_publisher i measurements_subscriber już tak masz

COPY . .

RUN pip install --no-cache-dir -r requirements.txt # do requirements.txt wrzuciłbym Flaska z odpowiednią wersją
# a już w ogóle na tip-top to by było skorzystać z mechanizmu pip install -r requirements.txt -c constraints.txt,
# gdzie constraints.txt zawierałby wersje podzależności
# Mi się raz zdarzyło że mimo że wersjonowałem zależności w requirements.txt to jednak coś się zepsuło
# bo najprawdopodobniej jedna moja zależność miała liberalną podzależność
# i w pewien dzień podbiła się wersja tej podzależności która miała buga
# i nagle mój kod przestał działać
# A jak się używa constraints.txt to takie rzeczy się nie dzieją, bo instalujemy ścisłe wersje również podzależności
# Ale może tutaj to nie jest takie ważne, bo w tym przypadku nie ma zbyt wielu zależności, tak po prostu dla info

EXPOSE 5000
# nie ma EXPOSED, jest EXPOSE ;D
# btw. EXPOSE to tylko dokumentacja
# The EXPOSE instruction does not actually publish the port.
# It functions as a type of documentation between the person who builds the image and the person who runs the container,
# about which ports are intended to be published.
# ~ https://docs.docker.com/engine/reference/builder/#expose

CMD ["python", "api.py"]
