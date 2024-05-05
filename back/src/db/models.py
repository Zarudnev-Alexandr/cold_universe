from sqlalchemy import Column, Integer, BigInteger, String, Float, Date, ForeignKey, Boolean, DateTime, TIMESTAMP
import datetime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email_code = Column(Integer, nullable=False)
    is_confirmed_email = Column(Boolean, nullable=False, default=False)
    nickname = Column(String, nullable=False)
    tag = Column(String, nullable=False, unique=True)
    level = Column(Integer, nullable=False, default=1)
    exp = Column(Integer, nullable=False, default=0)
    gem = Column(Integer, nullable=False, default=200)
    date_of_create = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now())
    access_id = Column(Integer, ForeignKey("access.id"), nullable=True)

    access = relationship("Access", back_populates="users", lazy="joined")


class Access(Base):
    __tablename__ = "access"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="access")
#
#
# class Card(Base):
#     __tablename__ = "card"
#
#     id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     name = Column(String, unique=True, nullable=False)
#     lore_description = Column(String, nullable=False)
#     image_url = Column(String, unique=True, nullable=True)
#     price_shop = Column(Integer, unique=False, nullable=False)
#     price_mana = Column(Integer, unique=False, nullable=False)
#     attack = Column(Integer, unique=False, nullable=False, default=1)
#     defense = Column(Integer, unique=False, nullable=False, default=1)
#     rarity = Column(Integer, unique=False, nullable=False, default=1)
#     classOfCard = Column(String, unique=False, nullable=False, default="attack")
#     coef_value = Column(Float, unique=False, nullable=False, default=1.2)
#
#
# class BoughtCard(Base):
#     __tablename__ = "bought_card"
#
#     id = Column(Integer, primary_key=True, unique=True, nullable=False)
#
#     user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
#     card_id = Column(Integer, ForeignKey("card.id"), nullable=False)
#     level = Column(Integer, unique=False, nullable=False, default=1)
#
#
# class BoughtCardInDeck(Base):
#     __tablename__ = "bought_card_in_user_deck"
#
#     id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     user_deck_id = Column(Integer, ForeignKey("user_deck.id"), nullable=False)
#     bought_card_id = Column(Integer, ForeignKey("bought_card.id"), nullable=False)
#
#
# class UserDeck(Base):
#     __tablename__ = "user_deck"
#
#     id = Column(Integer, primary_key=True, unique=True, nullable=False)
#
#     name = Column(String, unique=False, nullable=False, default="Default deck")
#
#     user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
#
#
# class PassiveEffects(Base):
#     __tablename__ = "passive_effect"
#
#     id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     visible_name = Column(String, unique=True, nullable=False)
#     value = Column(Float, unique=False, nullable=False)
#
#     card_id = Column(Integer, ForeignKey("card.id"), nullable=False)
#     effect_id = Column(Integer, ForeignKey("effect.id"), nullable=False)
#
#     # card = relationship("Card", back_populates="passive_effects", lazy="joined")
#     # effect = relationship("Effects", back_populates="passive_effects", lazy="joined")
#
#
# class Effects(Base):
#     __tablename__ = "effect"
#
#     id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     name = Column(String, unique=True, nullable=False)
#
#     # passive_effects = relationship("PassiveEffects", back_populates="effect", lazy="joined")
#
#
# class BoughtCardPassiveEffect(Base):
#     __tablename__ = "bought_card_passive_effect"
#
#     id = Column(Integer, primary_key=True, unique=True, nullable=False)
#     value = Column(Float, unique=False, nullable=False)
#
#     bought_card_id = Column(Integer, ForeignKey("bought_card.id"), nullable=False)
#     passive_effect_id = Column(Integer, ForeignKey("passive_effect.id"), nullable=False)
#
#     # bought_card = relationship("BoughtCard", back_populates="passive_effects", lazy="joined")
#     # passive_effect = relationship("PassiveEffects", back_populates="bought_cards", lazy="joined")
