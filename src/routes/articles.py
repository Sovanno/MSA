from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import get_db, get_current_user
from src import models
from src.controllers.article_controller import create_article, get_all_articles, get_article, update_article, delete_article, add_comment, get_comments, delete_comment
from src import schemas

router = APIRouter(prefix="/api/articles")


@router.post("/", tags=["articles"])
async def create_article_route(payload: schemas.ArticleCreate, db: AsyncSession = Depends(get_db), current_user: models.user.User = Depends(get_current_user)):
    try:
        article = create_article(db, current_user, payload.title, payload.description, payload.body, payload.tagList)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return schemas.ArticleResponse(
        slug=article.slug,
        title=article.title,
        description=article.description,
        body=article.body,
        tagList=article.tag_list,
        author=current_user.username
    )


@router.get("/", tags=["articles"])
async def list_articles(db: AsyncSession = Depends(get_db)):
    articles = get_all_articles(db)
    return {"articles": [
        {"slug": a.slug, "title": a.title, "description": a.description, "body": a.body, "tagList": a.tag_list,
         "author": a.author.username if a.author else None}
        for a in articles
    ]}


@router.get("/{slug}", tags=["articles"])
async def get_article_route(slug:str, db: AsyncSession = Depends(get_db)):
    article = get_article(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return schemas.ArticleResponse(
        slug=article.slug,
        title=article.title,
        description=article.description,
        body=article.body,
        tagList=article.tag_list,
        author=article.author.username
    )


@router.put("/{slug}", tags=["articles"])
async def update_article_route(slug: str, payload: schemas.ArticleUpdate, db: AsyncSession = Depends(get_db), current_user: models.user.User = Depends(get_current_user)):
    article = get_article(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на изменение статьи")
    updated = update_article(db, article, title=payload.title, description=payload.description, body=payload.body)
    return schemas.ArticleResponse(
        slug=article.slug,
        title=article.title,
        description=article.description,
        body=article.body,
        tagList=article.tag_list,
        author=current_user.username
    )


@router.delete("/{slug}", tags=["articles"])
async def delete_article_route(slug: str, db: AsyncSession = Depends(get_db), current_user: models.user.User = Depends(get_current_user)):
    article = get_article(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление статьи")
    delete_article(db, article)
    return {"detail": "Статья удалена"}


@router.post("/{slug}/comments", tags=["comments"])
async def add_comment_route(slug: str, payload: schemas.CommentCreate, db: AsyncSession = Depends(get_db), current_user: models.user.User = Depends(get_current_user)):
    article = get_article(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    comment = add_comment(db, article, current_user, payload.body)
    return schemas.CommentResponse(id=comment.id, body=comment.body, author=current_user.username)


@router.get("/{slug}/comments", tags=["comments"])
async def list_comments_route(slug: str, db: AsyncSession = Depends(get_db)):
    article = get_article(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    comments = get_comments(db, article)
    return {"comments": [
        {"id": c.id, "body": c.body, "author": c.author.username}
        for c in comments
    ]}


@router.delete("/{slug}/comments/{comment_id}", tags=["comments"])
async def delete_comment_route(slug: str, comment_id: int, db: AsyncSession = Depends(get_db), current_user: models.user.User = Depends(get_current_user)):
    article = get_article(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    comment = db.query(models.comment.Comment).filter(models.comment.Comment.id == comment_id,
                                                      models.comment.Comment.article_id == article.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Нет прав на удаление этого комментария")
    delete_comment(db, comment)
    return {"detail": "Комментарий удален"}
