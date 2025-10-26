from sqlalchemy.orm import Session
from src import models
from slugify import slugify
from datetime import datetime
from typing import List, Optional


def create_article(db: Session, author: models.user.User, title: str, description: Optional[str], body: Optional[str], tag_list: Optional[List[str]]):
    slug = slugify(title)
    article = models.article.Article(
        slug=slug,
        title=title,
        description=description or "",
        body=body or "",
        tag_list=tag_list or [],
        author_id=author.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def get_article(db: Session, slug: str):
    return db.query(models.article.Article).filter(models.article.Article.slug == slug).first()


def get_all_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.article.Article).offset(skip).limit(limit).all()


def update_article(db: Session, article: models.article.Article, title: str = None, description: str = None, body: str = None):
    if title is not None:
        article.title = title
        article.slug = slugify(title)
    if description is not None:
        article.description = description
    if body is not None:
        article.body = body
    article.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, article: models.article.Article):
    db.delete(article)
    db.commit()


def add_comment(db: Session, article: models.article.Article, author: models.user.User, body: str):
    comment = models.comment.Comment(
        body=body,
        article_id=article.id,
        author_id=author.id,
        created_at=datetime.utcnow()
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(db: Session, article: models.article.Article):
    return db.query(models.comment.Comment).filter(models.comment.Comment.article_id == article.id).all()


def delete_comment(db: Session, comment: models.comment.Comment):
    db.delete(comment)
    db.commit()
