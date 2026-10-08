from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from api.schema.trip import TripRequest, TripResponse
from database.dependencies import get_db
from service.trip_service import trip_service

# from ingest import get_chunks, get_vector_db

load_dotenv()

#
# def main():
#     groq_api_key = os.getenv("GROQ_API_KEY")
#     model_name = os.getenv("GROQ_MODEL")
#
#     if not groq_api_key or not model_name:
#         raise ValueError(
#             "Missing GROQ_API_KEY or GROQ_MODEL"
#         )
#
#     model = ChatGroq(
#         api_key=groq_api_key,
#         model=model_name,
#         temperature=0.5
#     )
#
#     vector_db = get_vector_db()
#
#     user_input = "What temples can I visit in Tokyo?"
#
#     structure_meta_data = model.with_structured_output(
#         MetaDataFiltering,
#         method="json_schema"
#     )
#     result_meta_data = structure_meta_data.invoke(user_input)
#     city = result_meta_data.city
#     category = result_meta_data.category
#
#     chunks = get_chunks()
#     keywords = KeywordSearch(chunks)
#     keyword_results = keywords.search(
#         user_input,
#         k=10,
#         city=city,
#         category=category
#     )
#
#     results = vector_db.similarity_search_with_score(
#         user_input,
#         k=10,
#         filter={
#             "$and": [
#                 {"city": city},
#                 {"category": category}
#             ]
#         }
#     )
#
#     vector_documents = [document for document, _ in results]
#
#     hybrid_results = reciprocal_rank_fusion(
#         vector_documents,
#         keyword_results
#     )
#
#     reranker = Reranker()
#
#     reranked_results = reranker.rerank(
#         user_input,
#         hybrid_results[:10]
#     )
#
#     for document in reranked_results:
#         print("\n---")
#         print(document.page_content)
#
#     if not reranked_results:
#         print("I don't have enough information in my knowledge base.")
#         return
#
#     context = "\n\n".join(
#         document.page_content
#         for document in reranked_results
#     )
#
#     print(context)
#
#     prompt = ChatPromptTemplate.from_messages([
#         (
#             "system",
#             """You are a travel assistant.
#
#         Answer the user's question using only the provided context.
#
#         If the answer cannot be found in the context, say:
#         "I don't have enough information in my knowledge base."
#
#         Context:
#         {context}"""),
#         ("human", "{question}"),
#     ])
#
#     chain = prompt | model
#
#     response = chain.invoke({
#         "context": context,
#         "question": user_input
#     })
#
#     print(response.content)


app = FastAPI(title="TripMind AI")


@app.post(
    "/api/v1/trips",
    response_model=TripResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def create_trip(
        request: TripRequest,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
):
    return trip_service.create_trip(
        db=db,
        request=request,
        background_tasks=background_tasks,
    )


@app.get(
    "/api/v1/trips/{trip_id}",
    response_model=TripResponse,
)
def get_trip(
        trip_id: int,
        db: Session = Depends(get_db),
):
    trip = trip_service.get_trip(db=db, trip_id=trip_id)
    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip with id {trip_id} not found",
        )
    return trip


@app.get("/health")
def health():
    return {"message": "ok"}
