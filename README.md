# Cafe-Manager

> [!IMPORTANT]
>DECLARATION OF USE OF AI: Anthropic: Claude version Opus 5.5 was used help with creating Dockerfile and compose.yaml and debugging code 

Skeleton web app for managing a cafe’s menu, staff and customers. Each data set (menu, staff and customers) has its own database and front end to view the data from each database.

## Video
https://github.com/user-attachments/assets/36961717-25ed-4213-9b4b-767a0dba0e11

| Database | Technology | Stored |
| -------- | ---------- | ------ |
|   Menu   | SQLite     | data/menu.db |
|   Saff   | SQLite     | data/staff.db |
|   Customers   | MongoDB     | database "cafe", collection "customers" |


These database technologies were chosen because I was already familiar with them and how they work and how well they work with python. This level of app could have been accomplished with just using different SQLite databases because of the small amount of dummy data and the data saved in the database was not very complex. It felt little boring and I decided to mix things up and use MongoDB too. I’m quite new to Flask and have used it few times and decided to challenge my self. **BIG** mistake. Most of my time went into getting everything to work together (and poor time management did not help :D ). Alas, here we are with minimum viable product.

## Docker
If you have Docker installed:
```
git clone <repository-url>
cd cafe_manager
cp .env.example .env
docker compose up --build
```

Open http://localhost:5000

### TO DO LIST

- [x] Create a pr.ogram that has at least three databases
- [x] Create a front end for your program that allows you to access the different databases
- [x] The user should be able to select which database they are accessing
- [x] The user should be able to read and modify the data
- [x] Prepare some dummy data for your database that can be used
- [x] Short video showing how everything works.


### Future work

- Adding error handling. Right now, this does not exists
- Improve the appearance of the web app. Now the app has almost none existing styling and it shows. 
- No “join” clauses. Everything is separate for reason. In the future there could be an addition of needing data from multiple databases at once like which staff member is working on which customers drink, and tracking sales data
- Finishing the database views and adding filtering for what is shown. Now not all gathered data is displayed for example the favourite drinks are not displayed at all. 
