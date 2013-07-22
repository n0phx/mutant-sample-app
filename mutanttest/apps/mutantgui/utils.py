# -*- coding: utf-8 -*-
from mutant.models import FieldDefinitionBase


MUTANT_TYPES = FieldDefinitionBase._field_definitions
FIELD_MAP = dict((v.get_content_type().pk, k) for k, v in MUTANT_TYPES.items())
FIELD_TYPES = tuple((key, value.__name__) for key, value in FIELD_MAP.items())
FIELD_TYPES = sorted(FIELD_TYPES, key=lambda x: x[1])

get_mutant_type = lambda field_type_pk: MUTANT_TYPES[FIELD_MAP[field_type_pk]]
