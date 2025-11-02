import chromadb
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

client = chromadb.PersistentClient(path="./data/chroma_db")
collection = client.get_collection(name="amazon_products")

@tool
def search_product(
    query: str,
    price: float | None = None,
    brand: str | None = None,
    rating: float | None = None
) -> dict:
    """
    Search for products in the vector store using semantic similarity and optional filters.

    This tool performs a hybrid search:
    - **Semantic search** via the input `query` (embedded and matched against product titles/descriptions).
    - **Metadata filtering** on price, brand, and minimum rating.

    Results are printed to console for debugging and returned as a raw query result dict
    (compatible with Chroma/Weaviate-style vector DB output).

    Args:
        query (str): The search query (e.g., "wireless noise-cancelling headphones").
        price (float | None, optional): Maximum price to include. Filters products where
            ``price <= price``. Defaults to None (no price cap).
        brand (str | None, optional): Exact brand name to filter by (case-sensitive).
            Defaults to None (no brand filter).
        rating (float | None, optional): Minimum average rating (0.0 to 5.0). Filters products
            where ``rating >= rating``. Defaults to None (no rating filter).

    Returns:
        dict: The full query result from the vector store, with keys:
            - ``ids``: List of matching document IDs
            - ``documents``: List of raw text content
            - ``metadatas``: List of metadata dicts (brand, title, price, rating, etc.)
            - ``distances``: Semantic similarity scores (lower = more similar)

    Example:
        >>> result = search_product("laptop", price=1500, rating=4.5)
        Top Matches:
        1. Dell - XPS 13 | $1299.0 | Rating: 4.7 | Distance: 0.1234
        2. HP - Spectre x360 | $1399.0 | Rating: 4.6 | Distance: 0.1891
        >>> print(result["metadatas"][0][0]["title"])
        XPS 13

    Note:
        - Requires a pre-initialized `collection` (e.g., Chroma collection) in scope.
        - Filters use MongoDB-style query syntax (``$lte``, ``$gte``, ``$and``).
        - Prints top matches to stdout for immediate feedback.
    """
    filters = []
    
    if price is not None:
        filters.append({"price": {"$lte": price}})
    if rating is not None:
        filters.append({"rating": {"$gte": rating}})
    if brand is not None:
        filters.append({"brand": brand})
    
    where_clause = {"$and": filters} if filters else None

    results = collection.query(
        query_texts=[query],
        n_results=10,
        where=where_clause,
        include=["metadatas", "distances", "documents"]
    )
    
    print("\nTop Matches:")
    if results["ids"][0]:
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]
            dist = results["distances"][0][i]
            print(
                f"{i+1}. {meta['brand']} - {meta['title']} | "
                f"${meta['price']} | Rating: {meta['rating']} | "
                f"Distance: {dist:.4f}"
            )
    else:
        print("No matches found.")

    return results