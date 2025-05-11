from time import time

from app.models import get_db, Painting, User
from app.depenencies import verify_access_token, get_current_user
from app.repository import painting_repository, user_repository

from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import FileResponse

import requests
import os
import pandas as pd
import random


painting_router = APIRouter(
    prefix="/painting",
    tags=["Painting"],
)


API_KEY = "Jm5nsYYY"
ID = "SK-C-5"
DETAIL_URL = "https://www.rijksmuseum.nl/api/en/collection/{}?key={}"

COLOR_WEIGHT = 0.25
DESCRIPTION_WEIGHT = 0.25
STYLE_WEIGTH = 0.25
VISUAL_WEIGHT = 0.25

DESCRIPTION_DF = pd.read_csv("app/data/similarity_matrix_description.csv", index_col=0)
COLOR_DF = pd.read_csv("app/data/similarity_matrix_color.csv", index_col=0)
STYLE_DF = pd.read_csv("app/data/similarity_matrix_style.csv", index_col=0)
VISUAL_DF = pd.read_csv("app/data/similarity_matrix_visual.csv", index_col=0)

def get_datails_for_painting(painting_obj_id: str):
    url = DETAIL_URL.format(painting_obj_id, API_KEY)
    response = requests.get(url)

    if response.status_code == 200:
        json = response.json()
        print(json["artObject"])
        description = json["artObject"]["artObjectPage"]["plaqueDescription"]
        title = json["artObject"]["title"]
        maker = json["artObject"]["principalMaker"]
        date = json["artObject"]["dating"]["presentingDate"]
        return {
            "title": title,
            "description": description,
            "maker": maker,
            "date": date,
        }
    else:
        print("failed")
        return None


@painting_router.get("/details/{painting_id}/")
async def get_painting_details(painting_id: str, _=Depends(verify_access_token)):
    return get_datails_for_painting(painting_id)


@painting_router.get("/file/{painting_id}/")
async def get_painting_file(
    painting_id: str, _=Depends(verify_access_token), db: Session = Depends(get_db)
):
    file_path = "app/images/" + painting_id + ".jpg"

    if not os.path.exists(file_path):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "file not found")

    return FileResponse(file_path)


@painting_router.get("/{painting_id}/")
async def get_painting(
    painting_id: str, _=Depends(verify_access_token), db: Session = Depends(get_db)
):
    p = painting_repository.get_painting_by_object_number(db, painting_id)

    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "painting not found")

    return {
        "painting": p,
        "art_style": p.get_art_style
    }


@painting_router.get("/random/get/")
async def get_random_painting(
    _=Depends(verify_access_token), db: Session = Depends(get_db)
):
    p = painting_repository.get_random_painting(db)
    return {
        "painting": p,
        "art_style": p.get_art_style
    }


@painting_router.get("/recommendations/{painting_id}/")
async def register_paintings(
    painting_id: str,
    offset: int = 0,
    _=Depends(verify_access_token),
    db: Session = Depends(get_db),
):
    ids = []
    p = painting_repository.get_painting_by_object_number(db, painting_id)

    if not p:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "painting not found")

    random_index = random.randint(1,44)

    if p.color == None:
        painting_style = STYLE_DF[painting_id]
        style_sorted = painting_style.sort_values()
        other_style = style_sorted[style_sorted > 0]
        ids.extend(other_style.index[random_index + offset: random_index + 2 + offset])
    else:
        painting_style = STYLE_DF[painting_id]
        style_sorted = painting_style.sort_values()
        other_style = style_sorted[style_sorted > 0]
        ids.extend(other_style.index[random_index + offset: random_index + 1 + offset])

        painting_color = COLOR_DF[painting_id]
        color_sorted = painting_color.sort_values(ascending=False)
        ids.extend(color_sorted.index[220 + offset: 221 + offset])

    painting_description = DESCRIPTION_DF[painting_id]
    desc_sorted = painting_description.sort_values(ascending=False)
    ids.extend(desc_sorted.index[44 + offset: 45 + offset])

    painting_visual = VISUAL_DF[painting_id]
    visual_sorted = painting_visual.sort_values(ascending=False)
    ids.extend(visual_sorted.index[220 + offset: 221 + offset])

    paint_d = painting_description * DESCRIPTION_WEIGHT
    paint_s = painting_style * STYLE_WEIGTH
    paint_v = painting_visual * VISUAL_WEIGHT

    if p.color == None:
        similarity = pd.concat([paint_d, paint_s, paint_v], axis=1)
    else:
        paint_c = painting_color * COLOR_WEIGHT
        similarity = pd.concat([paint_d, paint_c, paint_s, paint_v], axis=1)

    sorted = similarity.sum(axis=1).sort_values(ascending=False)

    ids.extend(sorted.index[220 + offset:221 + offset])

    paintings = []

    for id in ids:
        paintings.append(painting_repository.get_painting_by_object_number(db, id))

    return paintings


@painting_router.get("/register/")
async def register_paintings(db: Session = Depends(get_db)):
    for _, _, files in os.walk("./app/images", topdown=False):
        for name in files:
            obj_id = name.split(".")[0]
            painting = Painting()
            painting.object_number = obj_id
            painting_repository.save(db, painting)


@painting_router.get("/details/fill")
async def get_painting_details(db=Depends(get_db)):
    file1 = open("/home/joran/Documents/uva/year4/dsp/Image_scrape/object_url.txt", "r")
    lines = file1.readlines()

    for line in lines:
        obj = line.split("\n")[0]
        obj = obj.split(" ")
        obj_num = obj[0]
        obj_url = obj[1]

        p = painting_repository.get_painting_by_object_number(db, obj_num)

        if p:
            continue

        details = get_datails_for_painting(obj_num)

        if not details:
            continue

        painting = Painting()
        painting.object_number = obj_num
        painting.url = obj_url
        painting.title = details["title"]
        painting.maker = details["maker"]
        painting.description = details["description"]
        painting.year = details["date"]
        painting_repository.save(db, painting)


@painting_router.get("/details/description/fill")
async def get_painting_details(db=Depends(get_db)):
    paintings = painting_repository.get_all_paintings(db)

    for idx, painting in enumerate(paintings):
        details = get_datails_for_painting(painting.object_number)


        if not details["details"]:
            print("no details")
            continue

        if idx == 10:
            break

        painting.description = details["description"]
        painting_repository.save(db, painting)


@painting_router.get("/details/url/fill")
async def get_painting_details(db=Depends(get_db)):
    file1 = open("/home/joran/Documents/uva/year4/dsp/Image_scrape/object_url.txt", "r")
    lines = file1.readlines()

    for line in lines:
        obj = line.split("\n")[0]
        obj = obj.split(" ")
        obj_num = obj[0]
        obj_url = obj[1]

        p = painting_repository.get_painting_by_object_number(db, obj_num)

        if not p:
            continue
        else:
            p.url = obj_url
            painting_repository.save(db, p)


@painting_router.get("/details/colors/fill")
async def get_painting_details(db=Depends(get_db)):
    file1 = open(
        "/home/joran/Documents/uva/year4/dsp/dsp_project/backend/colors.csv", "r"
    )
    lines = file1.readlines()

    for line in lines:
        line = line.split("\n")[0]
        obj = line.split(",")
        color = obj[1:]
        obj_id = obj[0]

        if color == [""]:
            print(obj_id)
            continue

        p = painting_repository.get_painting_by_object_number(db, obj_id)

        if not p:
            continue
        else:
            t = []

            for i in range(0, len(color) - 1, 2):
                t.append((color[i], color[i + 1]))

            highest_percentage = 0
            color = ""

            for (percentage, val) in t:
                if int(percentage) > highest_percentage:
                    color = val
                    highest_percentage = int(percentage)

            print(obj_id, color, highest_percentage)

            p.color = color.strip()
            painting_repository.save(db, p)

@painting_router.get("/details/styles/fill")
async def get_painting_details(db=Depends(get_db)):
    file1 = open(
        "/home/joran/Documents/uva/year4/dsp/style_classifier/output_final.csv", "r"
    )
    lines = file1.readlines()

    for line in lines:
        line = line.split("\n")[0]
        obj = line.split(",")
        style = obj[1]
        obj_id = obj[0]

        p = painting_repository.get_painting_by_object_number(db, obj_id)

        if not p:
            continue
        else:
            p.art_style = style
            painting_repository.save(db, p)
