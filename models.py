import sqlalchemy as sql
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

"""
Creating a database tables in accordance with a flowchart
"""

# Connecting a db
Base = declarative_base()

# an Engine, which the Session will use for connection
engine = sql.create_engine("postgresql://postgres:4Fabregas15@localhost:5432/vKinder_bot_db")

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()
connection = engine.connect()


class BotUser(Base):
    """
    Class BotUser creates a table "bot_user" in database "vKinder_bot_db"
    """
    __tablename__ = "bot_user"
    id_bot_user = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    bot_user_vk_id = sql.Column(sql.Integer, unique=True, nullable=False)

    def __repr__(self):
        return f'{self.id_bot_user} {self.bot_user_vk_id}'


class FavoriteUser(Base):
    """
    Class FavoriteUser creates a table "favorites_list" in database "vKinder_bot_db"
    """
    __tablename__ = 'favorites_list'
    id_favorites = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    vk_user_id = sql.Column(sql.Integer, unique=True, nullable=False)
    vk_user_first_name = sql.Column(sql.String)
    vk_user_last_name = sql.Column(sql.String)
    vk_user_url = sql.Column(sql.String)
    # vk_user_city = sql.Column(sql.String)
    # vk_user_bdate = sql.Column(sql.String)
    # vk_user_sex = sql.Column(sql.String)
    bot_user_vk_id = sql.Column(sql.Integer, sql.ForeignKey('bot_user.bot_user_vk_id', ondelete='CASCADE'))

    def __repr__(self):
        return f'{self.vk_user_first_name} {self.vk_user_last_name} {self.vk_user_url}'


class BlackList(Base):
    """
    Class Blacklist creates a table "black_list" in database "vKinder_bot_db"
    """
    __tablename__ = 'black_list'
    id_black_list = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    vk_user_id = sql.Column(sql.Integer, unique=True, nullable=False)
    vk_user_first_name = sql.Column(sql.String)
    vk_user_last_name = sql.Column(sql.String)
    vk_user_url = sql.Column(sql.String)
    # vk_user_city = sql.Column(sql.String)
    # vk_user_bdate = sql.Column(sql.String)
    # vk_user_sex = sql.Column(sql.String)
    bot_user_vk_id = sql.Column(sql.Integer, sql.ForeignKey('bot_user.bot_user_vk_id', ondelete='CASCADE'))

    def __repr__(self):
        return f'{self.vk_user_first_name} {self.vk_user_last_name} {self.vk_user_url}'


class VkUserPhoto(Base):
    """
    Class VkUserPhoto creates a table "vk_user_photo" in database "vKinder_bot_db"
    """
    __tablename__ = 'vk_user_photo'
    id_photo = sql.Column(sql.Integer, primary_key=True, autoincrement=True, nullable=False)
    photo_name = sql.Column(sql.String, unique=True, nullable=False)
    # vk_user_id = sql.Column(sql.Integer, sql.ForeignKey('favorites_list.vk_user_id', ondelete='CASCADE'))
    vk_user_id = sql.Column(sql.Integer, nullable=True)

    def __repr__(self):
        return f'{self.id_photo} {self.photo_name} {self.vk_user_id}'


"""
Functions to work with database
"""


def add_bot_user(id_vk):
    """
    Adds new bot user to database 'vKinder_bot_db'
    :param id_vk: int
    :return: Boolean
    """
    new_entry = BotUser(
        bot_user_vk_id=id_vk
    )
    session.add(new_entry)
    session.commit()
    return True


def check_if_bot_user_exists(id_vk):
    """
    Checks if bot user already exists in database 'vKinder_bot_db'
    :param id_vk: int
    """
    new_entry = session.query(BotUser).filter_by(bot_user_vk_id=id_vk).first()
    return new_entry


def add_new_match_to_favorites(vk_user_id, bot_user_vk_id, first_name, last_name, vk_user_url):
    """
    Adds new match to favorites list in accordance with user's request
    :param vk_user_id: int
    :param first_name: str
    :param last_name: str
    :param vk_user_url: str
    :param city: str
    :param bdate: str
    :param sex: str
    :param bot_user_vk_id: int
    :return: Boolean
    """
    if check_if_match_exists(vk_user_id)[0] is not None:
        return False
    new_entry = FavoriteUser(
        vk_user_id=vk_user_id,
        vk_user_first_name=first_name,
        vk_user_last_name=last_name,
        vk_user_url=vk_user_url,
        # vk_user_city=city,
        # vk_user_bdate=bdate,
        # vk_user_sex=sex,
        bot_user_vk_id=bot_user_vk_id
    )
    session.add(new_entry)
    session.commit()
    return True


def add_new_match_to_black_list(vk_user_id, bot_user_vk_id, first_name, last_name, vk_user_url):
    """
    Adds new match to black list in accordance with user's request
    :param vk_user_id: int
    :param first_name: str
    :param last_name: str
    :param vk_user_url: str
    :param city: str
    :param bdate: str
    :param sex: str
    :param bot_user_vk_id: int
    :return: Boolean
    """
    if check_if_match_exists(vk_user_id)[1] is not None:
        return False
    new_entry = BlackList(
        vk_user_id=vk_user_id,
        vk_user_first_name=first_name,
        vk_user_last_name=last_name,
        vk_user_url=vk_user_url,
        # vk_user_city=city,
        # vk_user_bdate=bdate,
        # vk_user_sex=sex,
        bot_user_vk_id=bot_user_vk_id
    )
    session.add(new_entry)
    session.commit()
    return True


def delete_match_from_black_list(vk_id):
    """
    Deletes match from black list
    :param vk_id: int
    """
    new_entry = session.query(BlackList).filter_by(vk_user_id=vk_id).first()
    session.delete(new_entry)
    session.commit()


def delete_match_from_favorites_list(vk_id):
    """
    Deletes match from favorites list
    :param vk_id: int
    """
    new_entry = session.query(FavoriteUser).filter_by(vk_user_id=vk_id).first()
    session.delete(new_entry)
    session.commit()


def check_if_match_exists(id_vk):
    """
    Checks if match already present in database (both black and favorites list)
    :param id_vk: int
    :return: Tuple
    """
    favorite_list = session.query(FavoriteUser.vk_user_id).filter_by(vk_user_id=id_vk).first()
    black_list = session.query(BlackList.vk_user_id).filter_by(vk_user_id=id_vk).first()
    return favorite_list, black_list

def add_photo_of_the_match(photo_name, vk_user_id):
    """
    Adds photo of matching user to a database photo-table
    :param photo_likes_count: int
    :param photo_url: str
    :param vk_user_id: str
    :return: Boolean
    """
    new_entry = VkUserPhoto(
        photo_name=photo_name,
        vk_user_id=vk_user_id,
    )
    session.add(new_entry)
    session.commit()
    return True


def show_all_favorites(vk_user_id):
    """
    Shows all favorite users of current bot user
    :param id_: int
    :return: list of favorite users
    """
    all_favorites = session.query(FavoriteUser.vk_user_first_name,
                                  FavoriteUser.vk_user_last_name,
                                  FavoriteUser.vk_user_url,
                                  VkUserPhoto.photo_name
                                  ).join(VkUserPhoto,
                                         VkUserPhoto.vk_user_id == FavoriteUser.vk_user_id).filter(
        vk_user_id == FavoriteUser.bot_user_vk_id).all()
    return all_favorites


def show_all_blacklisted(vk_user_id):
    """
    Shows all blacklisted users of current bot user
    :param id_: int
    :return: list of blacklisted users
    """
    all_blacklisted = session.query(BlackList.vk_user_first_name,
                                    BlackList.vk_user_last_name,
                                    BlackList.vk_user_url,
                                    VkUserPhoto.photo_name
                                    ).join(VkUserPhoto,
                                           VkUserPhoto.vk_user_id == BlackList.vk_user_id).filter(
        BlackList.bot_user_vk_id == vk_user_id).all()
    return all_blacklisted


if __name__ == '__main__':
    Base.metadata.create_all(engine)
