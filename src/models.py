import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('faction_id', Integer, ForeignKey('SHIPS.ship_id')),
    Column('ship_id', Integer, ForeignKey('FACTIONS.faction_id'))
)



class User(Base):
    __tablename__ = 'USERS'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(250), nullable=False)
    
    user_favourites = relationship('Favourite', back_populates='fav_user')

class Favourite(Base):
    __tablename__ = 'FAVOURITES'
    fav_id = Column(Integer, primary_key=True)
    fav_user_id = Column(Integer, ForeignKey('USERS.user_id'), nullable=False)
    fav_chara_id = Column(Integer, ForeignKey('CHARACTERS.chara_id'), nullable=False)
    fav_planet_id = Column(Integer, ForeignKey('PLANETS.planet_id'), nullable=False)
    fav_ship_id = Column(Integer, ForeignKey('SHIPS.ship_id'), nullable=False)

    fav_user = relationship('User', back_populates='user_favourites')
    fav_character = relationship('Character', back_populates='chara_favourites')
    fav_planet = relationship('Planet', back_populates='planet_favourites')
    fav_ship = relationship('Ship', back_populates='ship_favourites')



class Character(Base):
    __tablename__ = 'CHARACTERS'
    chara_id = Column(Integer, primary_key=True)
    chara_name = Column(String(100), nullable=False)
    chara_from = Column(String, ForeignKey('PLANETS.planet_name'), nullable=False)
    chara_faction = Column(String, ForeignKey('FACTIONS.faction_name'), nullable=False)
    
    chara_favourites = relationship('Favourite', back_populates='fav_character')
    chara_fromPlanet = relationship('Planet', uselist=False, back_populates='planet_character')
    chara_team = relationship('Faction', uselist=False, back_populates='faction_chara')



class Planet(Base):
    __tablename__ = 'PLANETS'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String(100), nullable=False)
    planet_faction = Column(String, ForeignKey('FACTIONS.faction_id'), nullable=False)
    
    planet_favourites = relationship('Favourite', back_populates='fav_planet')
    planet_character = relationship('Character', back_populates='chara_fromPlanet')
    planet_from = relationship('Faction', back_populates='faction_planet')



class Ship(Base):
    __tablename__ = 'SHIPS'
    ship_id = Column(Integer, primary_key=True)
    ship_name = Column(String(100), nullable=False)
    # ship_team = Column(String, ForeignKey('FACTIONS.faction_name'), nullable=False)

    ship_favourites = relationship('Favourite', uselist=False, back_populates='fav_ship')
    ship_faction = relationship('Faction', secondary=association_table, back_populates='faction_ship')


class Faction(Base):
    __tablename__ = 'FACTIONS'
    faction_id = Column(Integer, primary_key=True)
    faction_name = Column(String(250), nullable=False, unique=True)
    
    faction_planet = relationship('Planet', back_populates='planet_from')
    faction_chara = relationship('Character', back_populates='chara_team')
    faction_ship = relationship('Ship', secondary=association_table, back_populates='ship_faction')





render_er(Base, 'diagram.png')
