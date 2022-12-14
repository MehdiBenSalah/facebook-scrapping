from fastapi import APIRouter, Request, Response, HTTPException, status, Query
try:
    from app.scraper import scrape_facebook_page
except:
    from scraper import scrape_facebook_page

router = APIRouter()



@router.post("/", response_description="Scrape a new facebook page and store it to database", status_code=status.HTTP_201_CREATED)
def scrape_and_store(
    request: Request,
    url : str = Query(default=None,regex='^(?:https?:\/\/)?(?:www\.)?(facebook|fb)\.(com|me)\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)'),
    max_number_of_facebook_posts_to_scrape : int = None
):
    if url :
        try :
            scrapped_data = scrape_facebook_page(url, max_number_of_facebook_posts_to_scrape)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error from source code : \n {e}")
        new_scrapped_data = request.app.database["facebook_pages"].insert_one(scrapped_data)
        created_data = request.app.database["facebook_pages"].find_one(
            {"_id": new_scrapped_data.inserted_id}
        )
        return created_data
    return {'message':'error'}

@router.get("/", response_description="List of scrapped facebook pages")
def list_of_scrapped_data(request: Request):
    pages = list(request.app.database["facebook_pages"].find(limit=100))
    return pages


@router.get("/{page_title}", response_description="Get all pages by their page title from database")
def find_facebook_page_by_page_title(request: Request,
        page_title : str
):
    
    if (facebook_page := request.app.database["facebook_pages"].find_one({"page title": page_title})) is not None:
        return facebook_page
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"facebook page with page title {page_title} not found")




@router.delete("/{id}", response_description="Delete a facebook page from database")
def delete_facebook_page_from_database(id: str, request: Request, response: Response):
    delete_result = request.app.database["facebook_pages"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Facebook page with ID {id} not found")
