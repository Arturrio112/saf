# saf
SAF md, autors - Artūrs Palamarčuks
# Palaišanas instrukcija
1. Izveidojiet direktoriju, kurā vēlaties saglabāt kodu:
```
   mkdir projekta_nosaukums
   cd projekta_nosaukums
```
2. Nolādējiet kodu no repozitorija:
```
   git clone <repozitorija_URL>
   cd <repozitorija_nosaukums>
```
3. Kad projekts ir nolādēts lokāli, atveriet termināli šajā direktorijā un ierakstiet:
```
   docker-compose up --build
```
4. Ja nepieciešams pārtraukt konteinerus, varat izmantot:
   docker-compose down
5. Pārlūkā ierakstīt "localhost", lai atvērtu projektu

# Palaišanas instrukcija, ja Docker nestrādā

1. Pirmais un otrais punkts vienāds ar iepriekšējo palaišanas instrukciju

2. Atveriet termināli un ierakstiet:
    ```
    cd backend
    pip install --no-cache-dir -r requirements.txt
    python manage.py runserver
    ```

3. Atveriet citu termināli un ierakstiet:
```
    cd frontend
    npm i
    npm run dev
```
4. Pārlūkā ierakstiet "localhost:5173", lai atvērtu projektu
