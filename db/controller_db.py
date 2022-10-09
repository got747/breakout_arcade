import os.path
from typing import Dict

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    ForeignKey,
    Table,
    create_engine,
    insert,
    select,
    update,
)
from config import DB_NAME, DB_PATH

engine = create_engine("sqlite:///" + DB_NAME)

metadata = MetaData()

game_saves = Table(
    "game_saves",
    metadata,
    Column("save_id", Integer(), primary_key=True),
    Column("save_name", String(200), unique=True, nullable=False),
)

balls_info = Table(
    "balls_info",
    metadata,
    Column("ball_id", ForeignKey("game_saves.save_id"), primary_key=True),
    Column("x", Integer(), nullable=False),
    Column("y", Integer(), nullable=False),
    Column("change_x", Integer(), nullable=False),
    Column("change_y", Integer(), nullable=False),
)

bats_info = Table(
    "bats_info",
    metadata,
    Column("bat_id", ForeignKey("game_saves.save_id"), primary_key=True),
    Column("x", Integer(), nullable=False),
    Column("y", Integer(), nullable=False),
    Column("change_x", Integer(), nullable=False),
)

if not os.path.isfile(DB_PATH + DB_NAME):  # тут проблемы с путями
    metadata.create_all(engine)


def save_game(save_name: String, game_data: Dict):
    connection_db = engine.connect()
    get_save_record = select([game_saves]).where(game_saves.c.save_name == save_name)
    result_get_save_record = connection_db.execute(get_save_record).first()
    if result_get_save_record is None:
        request_insert_in_geme_save = insert(game_saves).values(
            save_name=save_name,
        )
        id_game_save = connection_db.execute(
            request_insert_in_geme_save
        ).inserted_primary_key[0]

        connection_db.execute(
            insert(balls_info), [{"ball_id": id_game_save} | game_data["balls_info"]]
        )
        connection_db.execute(
            insert(bats_info), [{"bat_id": id_game_save} | game_data["bats_info"]]
        )
    else:
        update_ball = (
            update(balls_info)
            .where(balls_info.c.ball_id == result_get_save_record[0])
            .values(
                game_data["balls_info"],
            )
        )

        connection_db.execute(update_ball)

        update_bat = (
            update(bats_info)
            .where(bats_info.c.bat_id == result_get_save_record[0])
            .values(
                game_data["bats_info"],
            )
        )

        connection_db.execute(update_bat)


def loud_game(save_name):
    connection_db = engine.connect()
    get_save_record = select([game_saves]).where(game_saves.c.save_name == save_name)
    result_get_save_record = connection_db.execute(get_save_record).first()
    if result_get_save_record is None:
        return {}
    else:
        request_game_data = (
            select(
                [
                    game_saves,
                    bats_info,
                    balls_info,
                ]
            )
            .select_from(game_saves.join(bats_info).join(balls_info))
            .where(
                game_saves.c.save_id == result_get_save_record[0],
            )
        )

        request_game_data = connection_db.execute(request_game_data)
        return {
            key: value
            for key, value in zip(request_game_data.keys(), request_game_data.first())
            if "id" not in key
        }
