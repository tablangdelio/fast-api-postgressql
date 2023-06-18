from database import Base
from sqlalchemy import String, Boolean, Integer, Float, Text, Column


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    on_offer = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Item name={self.name}  description={self.description} price={self.price} on_offer={self.on_offer}>"
