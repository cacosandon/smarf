from scaf.smart_call import smart_call


def get_country_data(city: str):
    country = smart_call(city)

    return {
        "country_name": country["name"],
        "country_code": country["code"],
        "country_flag_emoji": country["emoji"],
    }


if __name__ == "__main__":
    print(get_country_data(city="Paris"))
