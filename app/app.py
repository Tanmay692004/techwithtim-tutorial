from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from app.schemas import PostCreate, PostResponse, UserCreate, UserRead, UserUpdate
from app.db import Post, create_db_and_tables, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile
import asyncio
import typing
from app.users import auth_backend, fastapi_users, current_active_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])


@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(""),
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )

        if upload_result.response_metadata.http_status_code == 200:
            post = Post(
                user_id=user.id,
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    result = await session.execute(select(Post).order_by(Post.createdate.desc()))
    posts = [row[0] for row in result.all()]
    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id: u.email for u in users}
    
    
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "user_id": str(post.user_id),
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "createdate": post.createdate.isoformat(),
                "is_owner": post.user_id == user.id,
                "email": user_dict.get(post.user_id, "Unknown")
            }
        )
    return {"posts": posts_data}

@app.delete("/posts/{post_id}")
async def delete_post( post_id: str, session: AsyncSession = Depends(get_async_session)):
    try: 
        post_uuid = uuid.UUID(post_id)
        
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail="your ass is not authorized for this action")
        await session.delete(post)
        await session.commit()
        return {"detail": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

"""
                HARDCODE
textpost = {1: {"title": "First Post", "content": "This is the content of the first post."},
            2: {"title": "Second Post", "content": "This is the content of the second post."},
            3: {"title": "Third Post", "content": "This is the content of the third post."}}

@app.get("/posts")
async def getallposts(limit: int = None):
    if limit:
        return list(textpost.values())[:limit]
    return textpost

@app.get("/posts/{id}")
async def getpostbyid(id: int) -> PostResponse:
    if id not in textpost:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return textpost.get(id)

@app.post("/posts")
async def create_post(post: PostCreate) -> PostResponse:
    newPost = {"title" : post.title , "content": post.content}
    textpost[max(textpost) + 1] = newPost
    return newPost"""