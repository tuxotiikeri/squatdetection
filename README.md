# Työkalu polven frontaalitason nivelkulmalaskentaan 

## Yleiskuvaus

Tämä Python-skripti analysoi videoita, joissa kuvataan alaraajojen liikettä. Ohjelma hyödyntää MediaPipe Pose -algoritmia lonkan, polven ja nilkan nivelpisteiden tunnistamiseen videon jokaisesta kuvasta (frame). MediaPipe tunnistaa kuvasta nivelpisteiden koordinaatit (x, y), ja OpenCV piirtää kuvan päälle nivelpisteet sekä niiden väliset linjat. Koordinaatti- ja kulmatiedot tallentuvatat jokaisesta kuvasta.

Scriptin tarkoitus on auttaa tekemään objektiivinen arvio polven frontaalitason kulmasta, mutta se ei ole välttämättä luotettava referenssi muiden laitteiden validointiin. 

## Ohjelman toiminta
1. Videoanalyysi: Ohjelma lukee syöte-videon ja analysoi sen ruutu kerrallaan. 
2. MediaPipe-tunnistus: MediaPipe Pose tunnistaa lonkan, polven ja nilkan nivelpisteet ja tuottaa näiden koordinaatit (x, y).
3. Graafinen esitys: OpenCV piirtää nivelpisteet ja niitä yhdistävät segmentit videoon.
4. Signaalin suodatus: Ohjelma tallentaa nivelpisteiden koordinaatit Pandas DataFrameen ja suodattaa ne alipäästösuodattimella vähentäen nivelpisteiden tunnistuksessa esiintyvää jitteriä. Tämä tekee liikeradoista tasaisempia.
5. Kulman laskenta: Skripti laskee polven kulman suodatettujen koordinaattien perusteella kaavalla:
6. Tallennus: Lopuksi ohjelma tallentaa suodatetut koordinaatit ja lasketut kulmat CSV-tiedostoon.

## Riippuvuudet
Varmista, että seuraavat kirjastot on asennettu Python 3.9 -versiossa tai uudemmassa.

1. Python 3.9 tai uudempi: Tämä skripti on testattu Python 3.9 -versiolla.
2. MediaPipe: Nivelpisteiden tunnistamiseen.
3. OpenCV: Kuvankäsittelyyn ja nivelpisteiden piirtämiseen.
4. Pandas: Tietojen tallennukseen ja käsittelyyn.
5. NumPy: Matemaattisiin operaatioihin.
6. SciPy: Signaalin suodattamiseen.

## Käyttöohjeet
Lataa ja asenna tarvittavat kirjastot komennolla:
pip install numpy pandas opencv-python-headless mediapipe scipy

Käyttäjän muokattavat asetukset: Koodin alussa on osio, jossa voit muuttaa seuraavia asetuksia:

======= KÄYTTÄJÄN MUOKATTAVAT ASETUKSET =======
side = "right"  # Valitse "left" tai "right" analysoitavan jalan mukaan 
video_path = 'vids/insta/kyykky01_rotated.avi'  # Syötevideon polku
''' video_path = 0 # live-kuvaus läppärin omalla kameralla'''
save_path = 'results/'  # Tallennuskansio nivelpisteille ja nivelkulmille 
output_filename = f'{save_path}{side}_landmarks_and_angles.csv'  # Tallennustiedoston nimi 

## Ohjelman suorittaminen: Aja koodi komennolla:

python nivelkulma_laskenta.py

Ohjelma avaa videon ja näyttää analysoidun videon OpenCV-ikkunassa. Paina q sulkeaksesi ikkunan ja tallentaaksesi tulokset.

