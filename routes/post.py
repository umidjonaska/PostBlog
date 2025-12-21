from fastapi import APIRouter, Depends

from utils.pagination import Page, PageParams, get_page_params
from deps import user_service_dp

from services.user import UserService
from schemas.user import PostResponse, PostCreate