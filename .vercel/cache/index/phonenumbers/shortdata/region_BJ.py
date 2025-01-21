"""Auto-generated file, do not edit by hand. BJ metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BJ = PhoneMetadata(id='BJ', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='[17]\\d{2,3}', possible_length=(3, 4)),
    toll_free=PhoneNumberDesc(national_number_pattern='1(?:1[246-8]|3[68]|6[06])|7[3-5]\\d\\d', example_number='112', possible_length=(3, 4)),
    emergency=PhoneNumberDesc(national_number_pattern='11[246-8]', example_number='112', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='1(?:05|1[24-8]|2[02-5]|3[126-8]|5[05]|6[06]|89)|7[0-5]\\d\\d', example_number='105', possible_length=(3, 4)),
    carrier_specific=PhoneNumberDesc(national_number_pattern='12[02-5]', example_number='120', possible_length=(3,)),
    short_data=True)
