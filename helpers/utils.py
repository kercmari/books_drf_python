from bson import ObjectId
from datetime import datetime, date, time


def serializar_documento_mongo(doc):
    """Función auxiliar para serializar documentos de MongoDB"""
    if isinstance(doc, dict):
        return {k: serializar_documento_mongo(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serializar_documento_mongo(item) for item in item]
    elif isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, (datetime, date)):
        return doc.isoformat()
    return doc
