# Authentication
TBNB_ID = "343676d7-e677-4164-a5c0-16809229bafd"
BEARER_TOKEN = ("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9"
                ".eyJhdWQiOiIxIiwianRpIjoiNDQ1YWVmMWUxNGZkMTBjZDQ0MDhiZmVmODE3Zjk3OGRkZWM2Y2M5MGU5ZjM3YT"
                "gwM2E1MGIyZWNmZDc2MzljMWMzZGEzZjEzMmU0YzRmZTgiLCJpYXQiOjE3MjM3MzA5NTcuMDg3ODY2LCJuYmYiO"
                "jE3MjM3MzA5NTcuMDg3ODY4LCJleHAiOjQ4NDc3ODIxNTcuMDgyODY4LCJzdWIiOiIyOTciLCJzY29wZXMiOltd"
                "fQ.cQCi3XKeKL3B1D4Adcm_qKbiSROnU0CIyZYt6EfdvHWIKgMUYUUsMCvXl_kqRVxDq2QdR_agl490jqZLQ_Rq"
                "wmzxPqmoqrM-vZfnZCFo9s3ZTg77oz6NOd34mlsZ2uI2v8i4zSGdA2hpEn5QqAZtLkhgdJ8Cd8QoAo1Ttryagsl"
                "4gKmDG6ne0lJBPQRth0pEZwolKpECbQ7ZFjYCOjf3ypJblZE4EK2pNsUwoRaBpg63gG3mZXqDnTB33KzQKCiPAD"
                "jBX4mZHlS1vn-I7WQGtLfZXnW6UzsghRVmTzo9oB1i7aQJZaR_5POJHRB0p2XIflvjnWf_SbfKqcRuCiqugM17t"
                "rdqeEMQTysxTUPXfyufmjWZ-6QspGsYekLbASh9RHyHhCh3H6IwL370Pj0JqBV0wznTGXebo2xuIKoFMxDMbfB3"
                "EyufDvuMv61RC-wztrTPwkCBx1HVfFbo7yhjyLTZBpYW4r3wbcB5_goRhdRtxxrk1SvN89Vfx4xRaK3jFDarQR-"
                "MYiMrcCBdm6yRGA82P8gJX0ax6X1ymeVhy6rplptk4ij5ClXg8q_JB9i4vdOhdgX54ZvbxJuK35S_dSzytU8P3Q"
                "6OJva5Jj0KrXmip9pV5_yfX5pPm42qmLyG8xipmskE6cJ2qK_dSXE8y4efM7L46vinDo7Y4zMrfko")
# Messages
SCHEDULE_WASHBAR = ("\n\nWashBar : Le WashBar se situe au au : 39 Rue Ausone, 33000, Bordeaux. Attention : Le WashBar "
                    "est fermé le samedi, ainsi que le dimanche jusqu'à 15h.")
MESSAGE_PUT_TAKE_BEFORE_SATURDAY = (", vous devez aller déposer le linge après votre ménage, à la laverie partenaire "
                                    "WashBar. N'oubliez pas d'aller récupérer le linge avant samedi prochain. "
                                    + SCHEDULE_WASHBAR)
MESSAGE_TAKE_LINGE_FRIDAY = (", vous devez aller chercher le linge propre au plus tard vendredi, à la "
                             "laverie partenaire WashBar." + SCHEDULE_WASHBAR)
MESSAGE_PUT_LINGE_SUNDAY = (", vous devez aller déposer le linge sale dimanche, à partir de 15h et le récupérer au "
                            "plus tard vendredi, à la laverie partenaire WashBar." + SCHEDULE_WASHBAR)
MESSAGE_PUT_MONDAY = (", vous devez aller déposer le linge sale lundi, à la laverie partenaire WashBar."
                      + SCHEDULE_WASHBAR)
MESSAGE_PUT_TUESDAY = (", vous devez aller déposer le linge sale mardi, à la laverie partenaire WashBar."
                       + SCHEDULE_WASHBAR)
MESSAGE_PUT_WEDNESDAY = (", vous devez aller déposer le linge sale mercredi, à la laverie partenaire WashBar."
                         + SCHEDULE_WASHBAR)
MESSAGE_PUT_MONDAY_TAKE_FRIDAY = (", vous devez aller déposer le linge sale lundi, à la laverie partenaire WashBar."
                                  "Vous devez également aller le récupérer vendredi car une réservation à lieu le même "
                                  "jour." + SCHEDULE_WASHBAR)
MESSAGE_PUT_TUESDAY_TAKE_FRIDAY = (", vous devez aller déposer le linge sale mardi, à la laverie partenaire WashBar. "
                                   "Vous devez également aller le récupérer vendredi car une réservation à lieu le même"
                                   " jour." + SCHEDULE_WASHBAR)
MESSAGE_PUT_WEDNESDAY_TAKE_FRIDAY = (", vous devez aller déposer le linge sale mercredi, à la laverie partenaire "
                                     "WashBar. Vous devez également aller le récupérer vendredi car une réservation à "
                                     "lieu le même jour." + SCHEDULE_WASHBAR)
MESSAGE_PUT_THURSDAY_TAKE_FRIDAY = (", vous devez aller déposer le linge sale aujourd'hui, à la laverie partenaire "
                                    "WashBar. Vous devez également aller le récupérer vendredi car une réservation à "
                                    "lieu le même jour." + SCHEDULE_WASHBAR)
MESSAGE_PUT_THURSDAY_TAKE_FRIDAY_SATURDAY = (", vous devez aller déposer le linge sale aujourd'hui, à la laverie "
                                             "partenaire WashBar. Vous devez également aller le récupérer vendredi "
                                             "car une réservation à lieu le samedi et que la laverie sera fermée."
                                             + SCHEDULE_WASHBAR)
MESSAGE_CHECK_FORM = ", n'oubliez pas de remplir le formulaire pour le linge sale."
