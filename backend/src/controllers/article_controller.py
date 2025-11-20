from src import models
from slugify import slugify
from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def create_article(db: AsyncSession, author_id: int, title: str, description: Optional[str], body: Optional[str], tag_list: Optional[List[str]]):
    slug = slugify(title)
    article = models.article.Article(
        slug=slug,
        title=title,
        description=description or "",
        body=body or "",
        tag_list=tag_list or [],
        author_id=author_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article


async def get_article(db: AsyncSession, slug: str):
    db.expire_all()
    result = await db.execute(
        select(models.article.Article)
        .filter(models.article.Article.slug == slug)
    )
    return result.scalar_one_or_none()


async def get_all_articles(db: AsyncSession, skip: int = 0, limit: int = 100):
    db.expire_all()
    result = await db.execute(
        select(models.article.Article)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_article(db: AsyncSession, article: models.article.Article, title: str = None, description: str = None, body: str = None):
    if title is not None:
        article.title = title
        article.slug = slugify(title)
    if description is not None:
        article.description = description
    if body is not None:
        article.body = body
    article.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(article)
    return article


async def delete_article(db: AsyncSession, article: models.article.Article):
    await db.delete(article)
    await db.commit()


async def add_comment(db: AsyncSession, article: models.article.Article, author_id: int, body: str):
    comment = models.comment.Comment(
        body=body,
        article_id=article.id,
        author_id=author_id,
        created_at=datetime.utcnow()
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def get_comments(db: AsyncSession, article: models.article.Article):
    result = await db.execute(select(models.comment.Comment).filter(models.comment.Comment.article_id == article.id))
    return result.scalars().all()


async def delete_comment(db: AsyncSession, comment: models.comment.Comment):
    await db.delete(comment)
    await db.commit()
