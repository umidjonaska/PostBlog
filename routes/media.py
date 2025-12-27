from fastapi import APIRouter, Depends

from services.media import MediaService
from schemas.media import Media, MediaPayload
from deps import media_service_dp
from utils.pagination import Page, PageParams, get_page_params

router = APIRouter()

@router.get("/media", summary="Barcha medialarni olish")
async def router_get_all(
    #current_user: User = Depends(get_current_sale_user),
    page_params: PageParams = Depends(get_page_params),
    _service: MediaService = Depends(media_service_dp)
) -> Page[Media]:

    return await _service.get_all(page_params)

@router.get("/media_one",summary="Media haqida to'liq ma'lumot olish")
async def router_get_one(
    id: str,
    #current_user: User = Depends(get_current_sale_user),
    _service: MediaService = Depends(media_service_dp)
):

    return await _service.get_one(id)

@router.post("/create_create", summary="Yangi media qo'shish", status_code=201)
async def router_create(
    payload: MediaPayload,
    #current_user: User = Depends(get_current_sale_user),
    _service: MediaService = Depends(media_service_dp)
):

    return await _service.create(payload)

@router.put("/media_update",summary="Media haqidagi ma'lumotni yangilash")
async def router_update(
    id: str,
    payload: MediaPayload,
    #current_user: User = Depends(get_current_sale_user),
    _service: MediaService = Depends(media_service_dp)
):

    return await _service.update(id, payload)

@router.delete("/media_delete",summary="Chiqim o'chirish")
async def router_delete(
    id: str,
    # current_user: User = Depends(get_current_sale_user),
    _service: MediaService = Depends(media_service_dp)
):
    return await _service.delete(id)