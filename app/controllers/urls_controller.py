from typing import Annotated, List
from fastapi import APIRouter, Depends,status
from sqlmodel import Session
from app.core.crud import get_url_with_users, get_urls, shorten
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.urls import Urls
from app.schemas.urls import Urls_response
from app.models.user import User

router = APIRouter(
    prefix="/url",
    tags=["url"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def shorten_url(url: Urls, db: Annotated[Session, Depends(get_session)],  user: Annotated[User, Depends(get_current_user)]):
    return await shorten(url, db, user)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Urls_response])
async def get_all_urls(db: Annotated[Session, Depends(get_session)]):
    return  await get_urls(db)

@router.get("/{url_id}", status_code=status.HTTP_200_OK, response_model=Urls_response)
async def get_user(url_id: int, db: Annotated[Session, Depends(get_session)]):
    return  await get_url_with_users(url_id, db)



# @router.put("/{project_id}", status_code=status.HTTP_200_OK, response_model=Urls_response)
# async def update_project(project_id: int, project: Urls, db: Annotated[Session, Depends(get_session)], user: Annotated[User, Depends(get_current_user)]):
#     project_query = db.get(Projects, project_id)
#     check_product = db.exec(select(Urls).where(Projects.project_header == project.project_header)).first()
#     if not project_query:
#         raise HTTPException(status.HTTP_403_FORBIDDEN, f"project with the id {project_id} does not exists")
#     if check_product:
#         raise HTTPException(status.HTTP_403_FORBIDDEN, f"project with the header {project.project_header} already exists")
#     for field, value in project.model_dump().items():
#         setattr(project_query, field, value)
#     db.commit()
#     db.refresh(project_query)
#     return project_query

# @router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_project(project_id: int, db: Annotated[Session, Depends(get_session)], user: Annotated[User, Depends(get_current_user)]):
#     project_query = db.get(Urls, project_id)
#     if not project_query:
#         raise HTTPException(status.HTTP_403_FORBIDDEN, f"project with the id {project_id} does not exists")
#     db.delete(project_query)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @router.get("/", status_code=status.HTTP_200_OK, response_model=List[Urls_response])
# async def get_projects( db: Annotated[Session, Depends(get_session)], user: Annotated[User, Depends(get_current_user)], limit: int = 4, skip: int = 0):
#     product_query = db.exec(select(Urls).limit(limit).offset(skip)).all()
#     return product_query
