# Q9
@app.get("/books", response_model=list[BookResponse])
async def get_books_by_published_year_and_rating(
    db: DB_DEPENDENCY,
    published_after: int | None = Query(gt=0),
    min_rating: int | None = Query(gt=0, lt=6),
):
    books = (
        db.query(models.Books)
        .filter_by(
            Book.published_year > published_after,
            Book.rating >= min_rating,
        )
        .all
    )
    return books
