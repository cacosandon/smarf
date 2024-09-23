from smarf.smart_call import smart_call


def get_country_data(city: str):
    country_data = smart_call()

    return {
        "country_name": country_data["name"],
        "country_code": country_data["code"],
        "country_flag": country_data["flag_emoji"],
    }


if __name__ == "__main__":
    print(get_country_data(city="Paris"))
