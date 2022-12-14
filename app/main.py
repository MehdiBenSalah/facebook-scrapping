from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient
from urllib.parse import quote_plus
try :
    from app.routes import router
except :
    from routes import router

app = FastAPI()
password = quote_plus('mehdi1234/')

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(f"mongodb+srv://root:{password}@elyadatatest.grio5jv.mongodb.net/test")
    app.database = app.mongodb_client["scraping_facebook"]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()



app.include_router(router)




if __name__ == "__main__":
    uvicorn.run(app)