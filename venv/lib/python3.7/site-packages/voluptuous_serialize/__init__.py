"""Module to convert voluptuous schemas to dictionaries."""
from collections.abc import Mapping

import voluptuous as vol


TYPES_MAP = {
    int: 'integer',
    str: 'string',
    float: 'float',
    bool: 'boolean',
}


def convert(schema):
    """Convert a voluptuous schema to a dictionary."""
    # pylint: disable=too-many-return-statements,too-many-branches
    if isinstance(schema, vol.Schema):
        schema = schema.schema

    if isinstance(schema, Mapping):
        val = []

        for key, value in schema.items():
            description = None
            if isinstance(key, vol.Marker):
                pkey = key.schema
                description = key.description
            else:
                pkey = key

            pval = convert(value)
            pval['name'] = pkey
            if description is not None:
                pval['description'] = description

            if isinstance(key, (vol.Required, vol.Optional)):
                pval[key.__class__.__name__.lower()] = True

                if key.default is not vol.UNDEFINED:
                    pval['default'] = key.default()

            val.append(pval)

        return val

    if isinstance(schema, vol.All):
        val = {}
        for validator in schema.validators:
            val.update(convert(validator))
        return val

    if isinstance(schema, (vol.Clamp, vol.Range)):
        val = {}
        if schema.min is not None:
            val['valueMin'] = schema.min
        if schema.max is not None:
            val['valueMax'] = schema.max
        return val

    if isinstance(schema, vol.Length):
        val = {}
        if schema.min is not None:
            val['lengthMin'] = schema.min
        if schema.max is not None:
            val['lengthMax'] = schema.max
        return val

    if isinstance(schema, vol.Datetime):
        return {
            'type': 'datetime',
            'format': schema.format,
        }

    if isinstance(schema, vol.In):
        if isinstance(schema.container, Mapping):
            return {
                'type': 'select',
                'options': list(schema.container.items()),
            }
        return {
            'type': 'select',
            'options': [(item, item) for item in schema.container]
        }

    if schema in (vol.Lower, vol.Upper, vol.Capitalize, vol.Title, vol.Strip):
        return {
            schema.__name__.lower(): True,
        }

    if isinstance(schema, vol.Coerce):
        schema = schema.type

    if schema in TYPES_MAP:
        return {'type': TYPES_MAP[schema]}

    raise ValueError('Unable to convert schema: {}'.format(schema))
