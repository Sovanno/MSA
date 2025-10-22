from sqlalchemy.orm import Session
from src import models
from slugify import slugify
from datetime import datetime

def create_article(db: Session, author: models.User, title: str, description: str, body: str, tag_list: list):
    slug = slugify(title)
    article = models.Article(
        slug=slug,
        title=title,
        description=description,
        body=body,
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
    return db.query(models.Article).filter(models.Article.slug == slug).first()

def get_all_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()

def update_article(db: Session, article: models.Article, title: str = None, description: str = None, body: ste = None):
    if title:
        article.title = title
        article.slug = slugify(title)
    if description:
        article.description = description
    if body:
        article.body = body
    article.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, article: models.Article):
    db.delete(article)
    db.commit()

def add_comment(db: Session, article: models.Article, author: models.User, body: str):
    comment = models.Comment(
        body=body,
        article_id=article.id,
        author_id=author.id,
        created_at=datetime.utcnow()
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_comments(db: Session, article: models.Article):
    return db.query(models.Comment).filter(models.Comment.article_id == article.id).all()

def delete_comment(db: Session, comment: models.Comment):
    db.delete(comment)
    db.commit()
