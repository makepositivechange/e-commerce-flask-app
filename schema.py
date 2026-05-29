from marshmallow import Schema, fields  # pyright: ignore


class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    shop_id = fields.Str(required=True)


# this will be used for only incoming requests
class ProductUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    shop_id = fields.Str()


class ShopSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ShopUpdateSchema(Schema):
    name = fields.Str()
